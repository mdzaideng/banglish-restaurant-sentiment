# Banglish Restaurant Sentiment Code Release v1.0.0

> **This is a research-code release, not a reproducibility archive and not
> a public-results archive.** It ships preprocessing/VADER/RoBERTa/
> XLM-RoBERTa/TF-IDF+LogReg code, no row-level review data, no reviewer
> names, no review URLs, no model checkpoints, and no final figures or
> tables. See `results/README.md` for the full manuscript-item inventory
> (Figures 1-9, Tables 1-12, exact captions) and
> `docs/REPRODUCIBILITY_LIMITATIONS.md` for exactly what this release can
> and cannot independently verify against the manuscript's reported
> numbers.

## What this release covers

The study analyzes customer reviews across **five anonymized restaurant
brands** operating in Bangladesh, referred to throughout this repository
only as **Brand A, Brand B, Brand C, Brand D, and Brand E**. Restaurant
brand identities are not disclosed anywhere in this repository -- not in
prose, file names, folder names, code, comments, or configuration.

Two review populations are covered:

- **English reviews**, scored with VADER (lexicon-based) and RoBERTa
  (`cardiffnlp/twitter-roberta-base-sentiment-latest`), per brand.
- **Code-mixed Banglish reviews**, scored with a fine-tuned XLM-RoBERTa
  (`xlm-roberta-base`) model and a TF-IDF + Logistic Regression baseline,
  on a shared train/validation split.

## What is not included

- Raw or cleaned review data, in any language or processing stage.
- Reviewer names or any other personally identifying information.
- Per-review URLs.
- Final figures or tables -- no manuscript-reported number, chart, or
  table is shipped, copied, or recomputed here (see `results/README.md`).
- Trained model checkpoints (RoBERTa is used pretrained, as-is, from the
  Hugging Face Hub at runtime; the fine-tuned XLM-RoBERTa weights are
  excluded, with a future Zenodo deposit intended -- see
  `models/README.md`).
- Any file over 100 MB.

## Code changes made for this release

Every file under `src/` is byte-identical to its original except for six
files, which were corrected to repair file-naming and commented-out-output
defects that would otherwise make the per-brand pipeline silently fail to
chain together. `archive/original_scripts/` preserves the unmodified
original (defects included) for all 34 scripts. One further instance of
the same defect class was found and deliberately left unfixed, since
fixing it required an editorial choice rather than a one-line correction --
see `docs/CODE_CHANGES.md` for the full before/after table and reasoning.

`tests/test_preprocessing_output_contract.py` was added: a static fixture
test asserting every preprocessing script's output filename matches its
corresponding VADER/RoBERTa scorer's input filename, for all five brands.

## Package contents

**90 files, 280.0 KiB (286,749 bytes)** -- recomputed directly from disk.
No file is anywhere near GitHub's 100 MB limit; the entire package is
under 300 KB.

## Validation performed

| Check | Command | Result |
|---|---|---|
| Python syntax compilation, every `src/`+`tests/` script | `python -m py_compile <file>` for each of 36 `.py` files | **Pass -- genuinely executed.** All 36 compiled with exit code 0. |
| `tests/smoke_test.py` | `python tests/smoke_test.py` | **Pass -- genuinely executed.** All 4 sub-checks passed, exit code 0. |
| `tests/test_preprocessing_output_contract.py` | `python tests/test_preprocessing_output_contract.py` | **Pass -- genuinely executed.** All 10 preprocessing-output/scorer-input filename pairs (5 brands x VADER/RoBERTa) matched, exit code 0. |
| Requirements-import completeness | manual cross-check of every `import`/`from` in `src/**` against `requirements.txt` | **Pass.** `langdetect`, `deep_translator`, and all other third-party imports are covered; `openpyxl` is listed despite no direct import, needed by pandas' `.xlsx` engine. |
| Manifest SHA-256 verification | `Get-FileHash -Algorithm SHA256` against every shipped file, compared to `RELEASE_MANIFEST.csv` | **Pass.** Archive/src pairs for all 34 scripts hash-verified consistent. |
| Scan for the five restaurant brand names | case-insensitive search across every file's content and file/folder name | **Pass -- zero hits.** |
| Scan for secrets/credentials | pattern search for API-key/password/token/private-key patterns | **Pass** -- zero hits. |
| Scan for absolute local paths | pattern search for `[A-Za-z]:\\`, `/mnt/`, `/home/`, `/Users/` | **Pass** -- zero hits. |
| Scan for raw review text / reviewer names / URLs | pattern search across every remaining CSV/XLSX/JSON in the package | **Pass.** Only `data/example/synthetic_schema_example.csv` (three fabricated rows) contains review-shaped content. |
| Scan for model checkpoints / venv / build artifacts | search for `venv`, `*.safetensors`, `*.pt`, `*.bin`, `checkpoint-*`, `__pycache__`, `*.pyc` | **Pass** -- zero hits. |
| Scan for files over 100 MB | file-size scan | **Pass** -- zero hits. |

## How to read RELEASE_MANIFEST.csv

Every file is tracked with a `Decision` (`COPIED`, `EXCLUDED`,
`GENERATED`), its original path, release path, and archive path where
applicable, a SHA-256 hash for each shipped copy, and a `Reason` explaining
the decision.

## Judgment calls that should be reviewed by the authors

1. **Removing all results artifacts is a policy choice**, not a
   case-by-case judgment about which individual figures are "clean
   enough." See `results/README.md`, "Why nothing here is released."
2. **mBERT and a synthetic-data-only classical-ML comparison** were judged
   out-of-scope relative to the manuscript's reported methods -- an
   interpretive call the authors should confirm (see
   `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 7).
3. **The exact RoBERTa checkpoint revision and a pinned historical label
   mapping** are not recoverable from any retained file (see
   `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 5).

## Recommendation

Suitable for publication as a research code release, subject to author
completion of repository metadata (GitHub repository description, topics,
and the Zenodo deposit referenced in `models/README.md`); not a complete
results-reproduction archive.
