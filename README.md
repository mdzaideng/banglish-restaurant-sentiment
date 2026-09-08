
<div align="center">

<h1>Banglish Restaurant Sentiment</h1>

<p><em>Rating-Derived Sentiment Classification of English and Code-Mixed Banglish Restaurant Reviews:<br>
A Descriptive Comparison of Lexicon, Linear, and Transformer Approaches</em></p>

<br>

[![DOI](https://zenodo.org/badge/1361147783.svg)](https://doi.org/10.5281/zenodo.22660963)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=flat-square&logo=python&logoColor=white)](requirements.txt)
[![Release Type](https://img.shields.io/badge/Release%20Type-Code%20Only-lightgrey?style=flat-square)](#what-this-repository-is)

<br>

---

</div>

> **Before running anything:** This repository ships **code only** — no row-level review data,
> no model weights, and no figures or tables. See [`data/README.md`](data/README.md) for the
> full explanation and the schema your own authorized data must match.

---

## Table of Contents

- [What This Repository Is](#what-this-repository-is)
- [Study Overview](#study-overview)
- [Methods Covered](#methods-covered)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Pipeline Execution Order](#pipeline-execution-order)
- [Label Definitions](#label-definitions)
- [Model Checkpoints](#model-checkpoints)
- [English Corpora Note](#two-independently-compiled-english-corpora)
- [Why No Results Are Shipped](#why-this-release-ships-no-results-at-all)
- [Reproducibility Limitations](#reproducibility-limitations)
- [Data and Privacy](#data-and-privacy)
- [License](#license)
- [Citation](#citation)
- [Authors](#authors)

---

## What This Repository Is

This is a **research-code release** — the preprocessing, VADER, RoBERTa, XLM-RoBERTa, and
TF-IDF + Logistic Regression baseline pipelines behind the manuscript listed above.

It is **not** a reproducibility archive and **not** a results archive. It ships:

| Included | Not Included |
|---|---|
| All modeling and preprocessing scripts | Row-level review data of any kind |
| Synthetic schema example and smoke / contract tests | Trained model checkpoints |
| Full documentation of reproducibility limitations | Manuscript figures or tables |
| MIT license and citation metadata | Reviewer names or personally identifying information |

> **Do not treat this repository as reproducing or verifying any manuscript-reported number.**
> The manuscript's agreement statistics and performance figures are its own reported results.
> This code release neither recomputes nor confirms them.

---

## Study Overview

The study analyzes customer reviews across **five anonymized restaurant brands** operating in
Bangladesh, referred to throughout this repository as **Brand A, Brand B, Brand C, Brand D,
and Brand E**. Two review populations are covered:

- **English reviews** — scored with both a lexicon-based method (VADER) and a transformer
  model (RoBERTa), per brand.
- **Code-mixed Banglish reviews** — scored with a fine-tuned transformer (XLM-RoBERTa) and a
  TF-IDF + Logistic Regression baseline, on a shared train / validation split.

Restaurant brand identities are not disclosed anywhere in this repository, its code, its file
names, or its documentation.

---

## Methods Covered

| Pipeline | Model | Target Language |
|---|---|---|
| Lexicon-based | VADER | English reviews (per brand) |
| Transformer | RoBERTa — `cardiffnlp/twitter-roberta-base-sentiment-latest` | English reviews (per brand) |
| Fine-tuned Transformer | XLM-RoBERTa — `xlm-roberta-base` | Code-mixed Banglish reviews |
| Baseline | TF-IDF + Logistic Regression | Banglish (same train / val split) |

An mBERT model and a separate synthetic-data classical-ML comparison exist in the original
project but are **not** manuscript-reported methods and are excluded here — see
[`docs/REPRODUCIBILITY_LIMITATIONS.md`](docs/REPRODUCIBILITY_LIMITATIONS.md), item 7.

---

## Repository Structure

```
banglish-restaurant-sentiment/
│
├── README.md                              ← this file
├── LICENSE                                ← MIT License
├── CITATION.cff                           ← citation metadata
├── requirements.txt                       ← reconstructed dependencies
├── RELEASE_MANIFEST.csv                   ← all files with SHA-256 hashes and rationale
├── RELEASE_NOTES.md                       ← validation results and release scope
├── .gitignore
│
├── config/
│   └── model_registry.yaml               ← exact checkpoints and hyperparameters
│
├── data/
│   ├── README.md                         ← schemas, privacy rationale, label mapping
│   ├── LICENSE_DATA.md                   ← data licensing statement
│   └── example/
│       └── synthetic_schema_example.csv  ← fabricated schema demo (not study data)
│
├── src/
│   ├── preprocessing/                    ← per-brand translation and cleaning scripts
│   ├── vader/                            ← per-brand VADER scoring scripts
│   ├── roberta/                          ← per-brand RoBERTa scoring scripts
│   ├── banglish/                         ← XLM-RoBERTa + TF-IDF/LogReg (Banglish)
│   ├── baseline/                         ← see baseline/README.md
│   ├── evaluation/                       ← see evaluation/README.md (aggregation gap)
│   └── utilities/                        ← CSV ↔ Excel helper scripts
│
├── archive/
│   └── original_scripts/                 ← byte-identical originals (defects preserved)
│
├── results/
│   └── README.md                         ← inventory of Tables 1–12 / Figures 1–9
│                                            with exact captions; no artifacts shipped
│
├── models/
│   └── README.md                         ← model weight availability (future Zenodo)
│
├── docs/
│   ├── REPRODUCIBILITY_LIMITATIONS.md    ← read this first
│   ├── CODE_CHANGES.md                   ← exact defects repaired, before/after
│   ├── ENVIRONMENT_NOTES.md
│   ├── DATA_PROVENANCE.md
│   └── PIPELINE.md
│
└── tests/
    ├── smoke_test.py                      ← synthetic-data-only smoke test
    └── test_preprocessing_output_contract.py
```

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**NLTK resource — required for VADER:**

```bash
python -m nltk.downloader vader_lexicon
```

See [`docs/ENVIRONMENT_NOTES.md`](docs/ENVIRONMENT_NOTES.md) for which dependency pins are
exact-evidence vs. best-effort bounded ranges.

---

## Pipeline Execution Order

```
preprocessing
    └── brand_a_clean_vader.py / brand_a_clean_roberta.py  (repeat per brand)
         │
         ├── src/vader/        VADER scoring    (English, independent per brand)
         ├── src/roberta/      RoBERTa scoring  (English, independent per brand)
         └── src/banglish/     XLM-RoBERTa + TF-IDF/LogReg baseline (Banglish)
```

Each script expects its input file(s) in its **current working directory**, unchanged from the
original project's convention. See [`docs/PIPELINE.md`](docs/PIPELINE.md) for the full
execution table and [`docs/CODE_CHANGES.md`](docs/CODE_CHANGES.md) for why no path-handling
changes were made.

> **Note:** Aggregation of per-brand outputs into the manuscript's final cross-brand tables is
> an unresolved manual step — no script for it exists, and none was invented here. See
> [`docs/REPRODUCIBILITY_LIMITATIONS.md`](docs/REPRODUCIBILITY_LIMITATIONS.md), item 2.

---

## Label Definitions

Star ratings are mapped to a 3-class proxy label, confirmed directly in
`src/banglish/banglish_sentiment_pipeline.py`:

| Stars | Sentiment Label |
|:---:|:---|
| 1 – 2 | Negative |
| 3 | Neutral |
| 4 – 5 | Positive |

This is a **proxy label derived from the star rating, not a human-expert-annotated gold
standard.** English-dataset accuracy and F1 figures are computed against this proxy. Only the
Banglish XLM-RoBERTa validation metrics are genuine held-out performance figures. See
[`docs/REPRODUCIBILITY_LIMITATIONS.md`](docs/REPRODUCIBILITY_LIMITATIONS.md), item 8.

---

## Model Checkpoints

| Model | Checkpoint | Confirmed in |
|---|---|---|
| RoBERTa (English) | `cardiffnlp/twitter-roberta-base-sentiment-latest` | All five `src/roberta/*.py` scripts |
| XLM-RoBERTa (Banglish) | `xlm-roberta-base` (fine-tuned) | `src/banglish/banglish_sentiment_pipeline.py` |

The exact Hugging Face Hub revision/commit is not pinned in either the code or the manuscript.
Fine-tuned XLM-RoBERTa weights are **not** included in this repository. A future Zenodo
deposit is planned — see [`models/README.md`](models/README.md).

---

## Two Independently Compiled English Corpora

The manuscript reports two independently compiled English corpora **by design**: a
VADER-scored corpus and a separately compiled, non-row-identical RoBERTa-scored corpus
(Table 1). This is not a data-integrity conflict. Neither corpus is included here — all files
carry real reviewer names and unredacted text. See
[`docs/REPRODUCIBILITY_LIMITATIONS.md`](docs/REPRODUCIBILITY_LIMITATIONS.md), item 1.

---

## Why This Release Ships No Results at All

This is a **policy choice**, made independently of whatever the manuscript's numbers turn out
to be. This repository draws a hard line at "code only" because:

1. None of the underlying review corpora are shipped (see [`data/README.md`](data/README.md)),
   so even fully-traceable computations cannot be regenerated from this repository alone.
2. Shipping a subset of result figures or tables — even ones that appear internally consistent
   — would invite readers to treat this repository as a source of verified results, which it
   is not intended to be.

---

## Reproducibility Limitations

Full detail in [`docs/REPRODUCIBILITY_LIMITATIONS.md`](docs/REPRODUCIBILITY_LIMITATIONS.md).

<details>
<summary>Click to expand the full list</summary>

1. **English corpus totals unverified** — the manuscript reports 11,235 VADER-scored and
   11,783 RoBERTa-scored reviews and a 9,892-row matched subset. No raw data or aggregation
   script is included; this release cannot independently reproduce or verify these figures.
2. **No cross-brand aggregation script** — the per-brand to cross-brand table step was
   undocumented in the original project and was not reconstructed here.
3. **Year-wise data excluded** — Table 3 / Figure 2 timestamped source data and generation
   procedure are not included in this release.
4. **Three non-final figures excluded** — existed only in a scratch folder in the original
   project; treated as non-final.
5. **RoBERTa checkpoint revision unpinned** — the checkpoint name is confirmed in code and
   manuscript; the exact Hugging Face Hub revision/commit and historical label mapping are not
   recorded in either.
6. **Fine-tuned XLM-RoBERTa weights excluded** — future Zenodo deposit; see
   [`models/README.md`](models/README.md).
7. **mBERT and synthetic classical-ML excluded** — judged out of scope relative to the
   manuscript's reported methods (authors should confirm).
8. **No full pipeline execution** — only static compilation and synthetic smoke/contract tests
   were run. No manuscript-reported number was reproduced.
9. **No results artifacts shipped** — see [`results/README.md`](results/README.md) for the
   manuscript-verbatim inventory of Figures 1–9 and Tables 1–12.
10. **Raw English input file not established** — which retained raw compilation underlies the
    manuscript's two corpora is not determinable from retained files.
11. **Banglish denominator discrepancy (975 vs. 976)** — the manuscript states 975 valid
    reviews but the training run recorded 780 + 196 = 976. Both this release's inspection of
    `training_metrics_v2.json` and the manuscript's own Abstract / Sections 3.2/3.5/6.2
    report this as unresolved.
12. **Authoritative manuscript numbering** — the manuscript contains exactly Figures 1–9 and
    Tables 1–12, reproduced verbatim in `results/README.md`. Earlier project drafts used
    different numbering and are not used anywhere in this repository.

</details>

---

## Data and Privacy

No row-level review data — raw, cleaned, translated, or scored; English or Banglish — is
included. Every file inspected in the original project carried real reviewer display names and
unredacted review text scraped from Google Maps.

Restaurant brand identities are likewise not disclosed. All five brands are referred to only
as **Brand A** through **Brand E** throughout this repository, including in file names, folder
names, code comments, and configuration.

See [`data/README.md`](data/README.md) for the full classification table and instructions for
supplying your own authorized data.

---

## License

This project's code is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for the
full text. Data is separately governed — see [`data/LICENSE_DATA.md`](data/LICENSE_DATA.md).
No license is granted for the underlying third-party review data, because none is shipped.

---

## Citation

If you use this code, please cite it using the metadata in [`CITATION.cff`](CITATION.cff).

**Zenodo DOI:** [10.5281/zenodo.22660964](https://doi.org/10.5281/zenodo.22660964)

```bibtex
@software{HasanRatul2026banglish,
  author    = {Hasan Ratul, Shahriar and Hossain, Md. Zaid and Islam, Md. Shahriar},
  title     = {Comparative Sentiment Analysis of Bangladeshi Restaurant Reviews
               -- Research Code Release},
  version   = {1.0.0},
  date      = {2026-09-08},
  url       = {https://github.com/mdzaideng/banglish-restaurant-sentiment},
  doi       = {10.5281/zenodo.22660964},
  license   = {MIT}
}
```

---

## Authors

<table>
<tr>
<td width="33%" valign="top">

**Shahriar Hasan Ratul**<br>
Department of Industrial Engineering and Management<br>
Khulna University of Engineering & Technology<br>
Khulna-9203, Bangladesh<br><br>
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--0155--5516-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-0155-5516)

</td>
<td width="33%" valign="top">

**Md. Zaid Hossain**<br>
Department of Industrial Engineering and Management<br>
Khulna University of Engineering and Technology<br>
Khulna-9203, Bangladesh<br><br>
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--3301--3609-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0003-3301-3609)

</td>
<td width="33%" valign="top">

**Md. Shahriar Islam**<br>
Department of Industrial Engineering and Management<br>
Khulna University of Engineering and Technology<br>
Khulna-9203, Bangladesh<br><br>
[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--7551--166X-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0005-7551-166X)

</td>
</tr>
</table>
</div>
