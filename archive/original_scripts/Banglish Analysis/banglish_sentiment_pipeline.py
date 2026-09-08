# banglish_sentiment_pipeline_v2.py
#
# Research-grade fixes applied on top of the original pipeline:
#   1. Smoothed (sqrt) class weights instead of fully "balanced" weights.
#      Fully-balanced weights gave the Positive class (majority, 466 rows)
#      the LOWEST loss weight (0.70) and Neutral the HIGHEST (1.76). That
#      makes "always predict Negative" a cheap way to minimize loss, which
#      is exactly the collapse seen in the original run (890/977 predicted
#      Negative, val loss stuck at ln(3)=1.0986 the whole time).
#   2. A mandatory overfit sanity check before real training: fine-tune on
#      a tiny 24-example slice for 40 steps and assert train accuracy goes
#      above 0.9. If this fails, something in the training loop itself is
#      broken (bad gradient flow, frozen params, wrong labels) and the
#      real run is aborted instead of silently producing junk numbers.
#   3. More epochs + patience (small, hard, code-mixed dataset needs more
#      than 4 epochs to move off the ln(3) plateau) and a slightly higher
#      classifier-head LR vs backbone LR (discriminative fine-tuning).
#   4. Two baselines saved alongside the transformer: majority-class and
#      TF-IDF + Logistic Regression. A "research grade" claim needs the
#      transformer to beat both, on the same split.
#   5. Stratified K-fold option (default k=5) so metrics on this small
#      (~976 row) dataset are reported as mean +/- std, not a single
#      lucky/unlucky split.
#   6. Per-class precision/recall/F1 saved in metrics json, not just
#      accuracy + macro-F1.
#
# You need a machine with internet access to huggingface.co (or a cached
# xlm-roberta-base) and ideally a GPU. This will NOT run in a sandboxed
# environment with no internet access to HF.

import json
import random
from pathlib import Path
from contextlib import nullcontext

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
import torch.nn as nn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.utils.class_weight import compute_class_weight
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    get_linear_schedule_with_warmup,
)

SEED = 42
MODEL_NAME = "xlm-roberta-base"
EPOCHS = 10                # was 4 -- too few steps to move off the ln(3) plateau
PATIENCE = 3                # was 2
TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 32
MAX_LENGTH = 128
BACKBONE_LR = 2e-5
HEAD_LR = 1e-3               # classifier head trains faster/separately from the encoder
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.1
TEST_SIZE = 0.2
DROPOUT = 0.2
CLASS_WEIGHT_POWER = 0.5     # sqrt-smoothed weights instead of fully "balanced" (power=1.0)
RUN_CROSS_VALIDATION = False  # set True for the final research-grade run (slow: trains k models)
N_FOLDS = 5

LABEL_NAMES = {0: "Negative", 1: "Neutral", 2: "Positive"}


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def stars_to_label(stars):
    if stars <= 2:
        return 0
    if stars == 3:
        return 1
    return 2


def detect_text_column(df):
    preferred = ["reviews", "review", "text", "comment", "comments"]
    lower_map = {c.lower(): c for c in df.columns}
    for c in preferred:
        if c in lower_map:
            return lower_map[c]
    obj_cols = [c for c in df.columns if df[c].dtype == object]
    if obj_cols:
        return obj_cols[0]
    raise ValueError("No text column found.")


def smoothed_class_weights(y, power=0.5):
    """Inverse-frequency weights raised to `power`, then renormalized to
    mean 1.0. power=1.0 reproduces sklearn's fully "balanced" weights
    (the ones that caused the collapse); power=0.5 (sqrt) softens the
    effect so the majority class isn't penalized into irrelevance."""
    classes = np.array(sorted(np.unique(y)))
    counts = np.array([np.sum(y == c) for c in classes], dtype=np.float64)
    raw = (counts.sum() / (len(classes) * counts)) ** power
    raw = raw / raw.mean()
    return raw


class TokenizedDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length, labels=None):
        self.encodings = tokenizer(texts, truncation=True, max_length=max_length)
        self.labels = labels

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx):
        item = {k: self.encodings[k][idx] for k in self.encodings}
        if self.labels is not None:
            item["labels"] = int(self.labels[idx])
        return item


def make_loader(texts, labels, tokenizer, batch_size, max_length, shuffle):
    ds = TokenizedDataset(texts=texts, tokenizer=tokenizer, max_length=max_length, labels=labels)
    collator = DataCollatorWithPadding(
        tokenizer=tokenizer,
        pad_to_multiple_of=8 if torch.cuda.is_available() else None,
    )
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, collate_fn=collator)


def softmax_np(x):
    z = x - np.max(x, axis=1, keepdims=True)
    exp = np.exp(z)
    return exp / np.sum(exp, axis=1, keepdims=True)


def build_optimizer(model, backbone_lr, head_lr, weight_decay):
    """Discriminative learning rates: the randomly-initialized
    classification head needs to move much faster than the pretrained
    encoder, especially with only ~4 real epochs worth of steps."""
    backbone_params, head_params = [], []
    for name, p in model.named_parameters():
        if "classifier" in name or "pooler" in name:
            head_params.append(p)
        else:
            backbone_params.append(p)
    return AdamW(
        [
            {"params": backbone_params, "lr": backbone_lr, "weight_decay": weight_decay},
            {"params": head_params, "lr": head_lr, "weight_decay": weight_decay},
        ]
    )


def sanity_check_overfit(model_name, config, tokenizer, texts, labels, device, n=24, steps=150):
    """Mandatory pre-flight check. Fine-tune a fresh copy of the model on
    a tiny slice and require it to memorize that slice. If it can't even
    overfit 24 examples, something in the training loop is broken
    (frozen weights, label mismatch, gradients not applied) -- exactly
    the failure mode that produced the original run's flat ln(3) loss
    curve. Catch it here instead of discovering it after a full run.

    Dropout is forced to 0 for this probe only (a copy of `config`; the
    real training config is untouched) -- with dropout on, a handful of
    steps mixes "can't memorize" with "eval-mode/train-mode mismatch
    from dropout" and gives a false alarm. Loss is printed periodically
    and the first-step gradient norm is printed so a genuine
    frozen-gradient bug is visible directly, not just inferred from the
    final accuracy number.
    """
    import copy
    print(f"[sanity check] Overfitting a fresh model on {n} examples for up to {steps} steps...")
    idx = np.random.RandomState(0).choice(len(texts), size=min(n, len(texts)), replace=False)
    sub_texts = [texts[i] for i in idx]
    sub_labels = [labels[i] for i in idx]

    probe_config = copy.deepcopy(config)
    probe_config.hidden_dropout_prob = 0.0
    probe_config.attention_probs_dropout_prob = 0.0

    probe = AutoModelForSequenceClassification.from_pretrained(
        model_name, config=probe_config, ignore_mismatched_sizes=True
    ).to(device)
    loader = make_loader(sub_texts, sub_labels, tokenizer, batch_size=n, max_length=MAX_LENGTH, shuffle=False)
    opt = AdamW(probe.parameters(), lr=5e-5)

    probe.train()
    acc = 0.0
    for step in range(1, steps + 1):
        for batch in loader:
            labels_t = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            opt.zero_grad(set_to_none=True)
            logits = probe(**batch).logits
            loss = nn.functional.cross_entropy(logits, labels_t)
            loss.backward()

            if step == 1:
                total_norm = sum(
                    p.grad.detach().norm(2).item() ** 2
                    for p in probe.parameters() if p.grad is not None
                ) ** 0.5
                n_with_grad = sum(1 for p in probe.parameters() if p.grad is not None)
                n_total = sum(1 for _ in probe.parameters())
                print(f"[sanity check] step 1: grad_norm={total_norm:.6f}, "
                      f"params_with_grad={n_with_grad}/{n_total}")
                if total_norm < 1e-6:
                    raise RuntimeError(
                        "Sanity check FAILED: gradient norm is ~0 on step 1. Gradients are "
                        "not flowing at all -- check optimizer.zero_grad placement, that "
                        "loss.backward() is called before optimizer.step(), and that no "
                        "torch.no_grad() context wraps the forward pass."
                    )

            opt.step()

            with torch.no_grad():
                preds = logits.argmax(dim=1)
                acc = (preds.cpu() == labels_t.cpu()).float().mean().item()

        if step % 20 == 0 or step == 1:
            print(f"[sanity check] step {step}: loss={loss.item():.4f}, train_acc={acc:.3f}")
        if acc >= 0.99:
            print(f"[sanity check] Reached {acc:.3f} accuracy at step {step}, stopping early.")
            break

    print(f"[sanity check] Final train accuracy on the {n}-example slice: {acc:.3f}")
    del probe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    if acc < 0.9:
        raise RuntimeError(
            f"Sanity check FAILED (train acc={acc:.3f} < 0.9 after {steps} steps with "
            "dropout disabled). Gradients ARE flowing (see grad_norm above), so this points "
            "to something softer: learning rate too low for this many steps, tokenizer "
            "truncating/mangling the Banglish text, or a label off-by-one. Do not trust a "
            "full run until this passes -- share the step-by-step loss printout to narrow it "
            "down further."
        )
    print("[sanity check] Passed.\n")


def evaluate(model, loader, loss_fn, device):
    model.eval()
    total_loss = 0.0
    all_logits, all_labels = [], []
    with torch.no_grad():
        for batch in loader:
            labels = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            logits = model(**batch).logits
            loss = loss_fn(logits, labels)
            total_loss += loss.item()
            all_logits.append(logits.detach().cpu().numpy())
            all_labels.append(labels.detach().cpu().numpy())
    logits_np = np.concatenate(all_logits, axis=0)
    labels_np = np.concatenate(all_labels, axis=0)
    return total_loss / max(1, len(loader)), logits_np, labels_np


def predict_logits(model, loader, device):
    model.eval()
    outs = []
    with torch.no_grad():
        for batch in loader:
            batch.pop("labels", None)
            batch = {k: v.to(device) for k, v in batch.items()}
            logits = model(**batch).logits
            outs.append(logits.detach().cpu().numpy())
    return np.concatenate(outs, axis=0)


def calibrate_temperature(logits_np, labels_np, device):
    logits = torch.tensor(logits_np, dtype=torch.float32, device=device)
    labels = torch.tensor(labels_np, dtype=torch.long, device=device)
    temperature = torch.ones(1, device=device, requires_grad=True)
    nll = nn.CrossEntropyLoss()
    optimizer = torch.optim.LBFGS([temperature], lr=0.01, max_iter=80)

    def closure():
        optimizer.zero_grad()
        t = torch.clamp(temperature, 0.5, 5.0)
        loss = nll(logits / t, labels)
        loss.backward()
        return loss

    try:
        optimizer.step(closure)
        return float(torch.clamp(temperature.detach(), 0.5, 5.0).item())
    except Exception:
        return 1.0


def train_one_split(train_df, val_df, text_col, tokenizer, device, tag=""):
    config = AutoConfig.from_pretrained(MODEL_NAME)
    config.num_labels = 3
    config.hidden_dropout_prob = DROPOUT
    config.attention_probs_dropout_prob = DROPOUT

    # Pre-flight sanity check on the actual training data.
    sanity_check_overfit(
        MODEL_NAME, config, tokenizer,
        train_df[text_col].tolist(), train_df["label"].tolist(), device,
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, config=config, ignore_mismatched_sizes=True
    ).to(device)

    train_loader = make_loader(train_df[text_col].tolist(), train_df["label"].tolist(),
                                tokenizer, TRAIN_BATCH_SIZE, MAX_LENGTH, shuffle=True)
    val_loader = make_loader(val_df[text_col].tolist(), val_df["label"].tolist(),
                              tokenizer, EVAL_BATCH_SIZE, MAX_LENGTH, shuffle=False)

    weights = smoothed_class_weights(train_df["label"].values, power=CLASS_WEIGHT_POWER)
    print(f"[{tag}] class weights (power={CLASS_WEIGHT_POWER}): "
          f"Neg={weights[0]:.3f} Neu={weights[1]:.3f} Pos={weights[2]:.3f}")
    loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float32, device=device))

    optimizer = build_optimizer(model, BACKBONE_LR, HEAD_LR, WEIGHT_DECAY)
    total_steps = len(train_loader) * EPOCHS
    warmup_steps = int(total_steps * WARMUP_RATIO)
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    use_amp = torch.cuda.is_available()
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    best_f1, best_state, no_improve = -1.0, None, 0
    history = {"epoch": [], "train_loss": [], "val_loss": [], "val_f1": []}

    for epoch in range(1, EPOCHS + 1):
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            labels = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad(set_to_none=True)
            amp_ctx = torch.cuda.amp.autocast(enabled=use_amp) if use_amp else nullcontext()
            with amp_ctx:
                logits = model(**batch).logits
                loss = loss_fn(logits, labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            running_loss += loss.item()

        train_loss = running_loss / max(1, len(train_loader))
        val_loss, val_logits, val_labels = evaluate(model, val_loader, loss_fn, device)
        val_preds = np.argmax(val_logits, axis=1)
        val_f1 = f1_score(val_labels, val_preds, average="macro")
        val_acc = accuracy_score(val_labels, val_preds)
        print(f"[{tag}] Epoch {epoch}/{EPOCHS} | train_loss={train_loss:.4f} | "
              f"val_loss={val_loss:.4f} | val_acc={val_acc:.4f} | val_f1={val_f1:.4f}")

        history["epoch"].append(epoch)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_f1"].append(val_f1)

        if val_f1 > best_f1 + 1e-6:
            best_f1 = val_f1
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= PATIENCE:
                print(f"[{tag}] Early stopping.")
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    _, val_logits, val_labels = evaluate(model, val_loader, loss_fn, device)
    val_preds = np.argmax(val_logits, axis=1)
    return model, tokenizer, history, val_logits, val_labels, val_preds


def baseline_majority(y_train, y_val):
    majority = np.bincount(y_train).argmax()
    preds = np.full_like(y_val, majority)
    return {
        "accuracy": float(accuracy_score(y_val, preds)),
        "f1_macro": float(f1_score(y_val, preds, average="macro", zero_division=0)),
    }


def baseline_tfidf_logreg(train_texts, y_train, val_texts, y_val):
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)
    Xtr = vec.fit_transform(train_texts)
    Xval = vec.transform(val_texts)
    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(Xtr, y_train)
    preds = clf.predict(Xval)
    return {
        "accuracy": float(accuracy_score(y_val, preds)),
        "f1_macro": float(f1_score(y_val, preds, average="macro", zero_division=0)),
    }


def save_confusion_matrix(y_true, y_pred, path, title="Confusion Matrix (Validation)"):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Negative", "Neutral", "Positive"],
                yticklabels=["Negative", "Neutral", "Positive"])
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_training_curve(history, path):
    plt.figure(figsize=(10, 5))
    plt.plot(history["epoch"], history["train_loss"], label="Train Loss")
    plt.plot(history["epoch"], history["val_loss"], label="Val Loss")
    plt.plot(history["epoch"], history["val_f1"], label="Val F1-macro")
    plt.axhline(np.log(3), color="gray", linestyle=":", label="Random chance (ln 3)")
    plt.title("Training Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    script_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    csv_path = script_dir / "banglish_dataset_final.csv"
    if not csv_path.exists():
        csv_path = Path.cwd() / "banglish_dataset_final.csv"
    if not csv_path.exists():
        raise FileNotFoundError("banglish_dataset_final.csv not found in this folder.")
    out_dir = csv_path.parent

    df = pd.read_csv(csv_path)
    text_col = detect_text_column(df)
    if "stars" not in df.columns:
        raise ValueError("CSV must contain 'stars' column.")

    df = df.dropna(subset=[text_col, "stars"]).copy()
    df[text_col] = df[text_col].astype(str).str.strip()
    df = df[df[text_col] != ""].copy()
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    df = df.dropna(subset=["stars"]).copy()
    df["label"] = df["stars"].apply(stars_to_label)
    df["sentiment"] = df["label"].map(LABEL_NAMES)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_df, val_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=SEED, stratify=df["label"]
    )

    # --- Baselines (mandatory for a research-grade claim) ---
    maj = baseline_majority(train_df["label"].values, val_df["label"].values)
    tfidf = baseline_tfidf_logreg(
        train_df[text_col].tolist(), train_df["label"].values,
        val_df[text_col].tolist(), val_df["label"].values,
    )
    print(f"Baseline (majority class): acc={maj['accuracy']:.4f}, f1_macro={maj['f1_macro']:.4f}")
    print(f"Baseline (TF-IDF + LogReg): acc={tfidf['accuracy']:.4f}, f1_macro={tfidf['f1_macro']:.4f}")

    # --- Main transformer run ---
    model, tokenizer, history, val_logits, val_labels, val_preds = train_one_split(
        train_df, val_df, text_col, tokenizer, device, tag="main"
    )

    print("\nValidation Report (transformer):")
    print(classification_report(val_labels, val_preds, target_names=["Negative", "Neutral", "Positive"],
                                 digits=4, zero_division=0))

    per_class = precision_recall_fscore_support(val_labels, val_preds, labels=[0, 1, 2], zero_division=0)

    temperature = calibrate_temperature(val_logits, val_labels, device)
    print(f"Temperature: {temperature:.4f}")

    full_loader = make_loader(df[text_col].tolist(), None, tokenizer, EVAL_BATCH_SIZE, MAX_LENGTH, shuffle=False)
    logits_all = predict_logits(model, full_loader, device)
    probs = softmax_np(logits_all / temperature)
    preds = np.argmax(probs, axis=1)

    scored_df = df.copy().reset_index(drop=True)
    scored_df["predicted_sentiment"] = [LABEL_NAMES[i] for i in preds]
    scored_df["score_negative"] = probs[:, 0].round(4)
    scored_df["score_neutral"] = probs[:, 1].round(4)
    scored_df["score_positive"] = probs[:, 2].round(4)
    scored_df["confidence"] = probs.max(axis=1).round(4)
    scored_df["sentiment_score"] = np.clip(probs[:, 2] - probs[:, 0], -1.0, 1.0).round(4)

    out_csv = out_dir / "banglish_sentiment_scored_v2.csv"
    pref = ["name", "stars", text_col, "sentiment", "predicted_sentiment", "sentiment_score",
            "score_negative", "score_neutral", "score_positive", "confidence"]
    cols = [c for c in pref if c in scored_df.columns] + [c for c in scored_df.columns if c not in pref]
    scored_df[cols].to_csv(out_csv, index=False, encoding="utf-8-sig")

    save_confusion_matrix(val_labels, val_preds, out_dir / "confusion_matrix_validation_v2.png")
    save_training_curve(history, out_dir / "training_curve_v2.png")

    # --- Optional: stratified k-fold for robust small-sample reporting ---
    cv_summary = None
    if RUN_CROSS_VALIDATION:
        skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
        fold_accs, fold_f1s = [], []
        for fold, (tr_idx, va_idx) in enumerate(skf.split(df[text_col], df["label"]), start=1):
            tr_fold, va_fold = df.iloc[tr_idx], df.iloc[va_idx]
            _, _, _, _, va_labels_f, va_preds_f = train_one_split(
                tr_fold, va_fold, text_col, tokenizer, device, tag=f"fold{fold}"
            )
            fold_accs.append(accuracy_score(va_labels_f, va_preds_f))
            fold_f1s.append(f1_score(va_labels_f, va_preds_f, average="macro"))
        cv_summary = {
            "accuracy_mean": float(np.mean(fold_accs)), "accuracy_std": float(np.std(fold_accs)),
            "f1_macro_mean": float(np.mean(fold_f1s)), "f1_macro_std": float(np.std(fold_f1s)),
            "n_folds": N_FOLDS,
        }
        print(f"\n{N_FOLDS}-fold CV: acc={cv_summary['accuracy_mean']:.4f}+/-{cv_summary['accuracy_std']:.4f}, "
              f"f1_macro={cv_summary['f1_macro_mean']:.4f}+/-{cv_summary['f1_macro_std']:.4f}")

    metrics = {
        "model_name": MODEL_NAME,
        "rows": int(len(df)),
        "train_rows": int(len(train_df)),
        "val_rows": int(len(val_df)),
        "val_accuracy": float(accuracy_score(val_labels, val_preds)),
        "val_f1_macro": float(f1_score(val_labels, val_preds, average="macro")),
        "per_class_precision": per_class[0].tolist(),
        "per_class_recall": per_class[1].tolist(),
        "per_class_f1": per_class[2].tolist(),
        "temperature": float(temperature),
        "baseline_majority": maj,
        "baseline_tfidf_logreg": tfidf,
        "cross_validation": cv_summary,
        "class_weight_power": CLASS_WEIGHT_POWER,
        "epochs_configured": EPOCHS,
    }
    with open(out_dir / "training_metrics_v2.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved: {out_csv}")
    print(f"All outputs saved in: {out_dir}")


if __name__ == "__main__":
    main()