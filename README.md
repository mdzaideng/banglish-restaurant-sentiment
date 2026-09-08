# Banglish Restaurant Sentiment

### Comparative Sentiment Analysis of Bangladeshi Restaurant Reviews

*Rating-Derived Sentiment Classification of English and Code-Mixed Banglish
Restaurant Reviews: A Descriptive Comparison of Lexicon, Linear, and
Transformer Approaches*

[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776ab?style=flat-square&logo=python&logoColor=white)](requirements.txt)
[![Release type](https://img.shields.io/badge/release%20type-code%20only-lightgrey?style=flat-square)](#what-this-repository-is)

---

## What this repository is

This is a **research-code release**: the preprocessing, VADER, RoBERTa,
XLM-RoBERTa, and TF-IDF+LogReg-baseline code behind the manuscript above.

**It is not a reproducibility archive and not a results archive.** It ships
no row-level review data, no model checkpoints, and no final figures or
tables. See `results/README.md` for a full inventory of every manuscript
figure/table, each with its exact caption and why it is not shipped as a
separate artifact.

A future Zenodo record is intended to host trained model weights and
(pending a privacy/redistribution review) permitted data artifacts -- see
`models/README.md` and `data/README.md`. Neither exists yet.

> **Read this before running anything:** this repository ships code, not
> data and not results. See "Data & privacy" below and `data/README.md` for
> why, and what schema your own authorized data needs to match.

## Study overview

The study analyzes customer reviews across **five anonymized restaurant
brands** operating in Bangladesh, referred to throughout this repository
as **Brand A, Brand B, Brand C, Brand D, and Brand E**. Two review
populations are covered:

- **English reviews** -- scored with both a lexicon-based method (VADER)
  and a transformer model (RoBERTa), per brand.
- **Code-mixed Banglish reviews** -- scored with a fine-tuned transformer
  (XLM-RoBERTa) and a TF-IDF + Logistic Regression baseline, on a shared
  train/validation split.

Restaurant brand identities are not disclosed anywhere in this repository,
its code, its file names, or its documentation.

## What is not included

- **Raw or cleaned review data** -- no review text, star ratings tied to
  reviewer identity, or per-review URLs of any kind.
- **Reviewer names or any personally identifying information.**
- **Final figures or tables** -- no manuscript-reported number, chart, or
  table is shipped, copied, or recomputed here.
- **Trained model checkpoints** -- no `.bin`/`.safetensors`/`.pt` weight
  files. The fine-tuned XLM-RoBERTa weights are intended for a future
  Zenodo deposit (see `models/README.md`).

See `data/README.md` for the full data-exclusion rationale and schema, and
`docs/REPRODUCIBILITY_LIMITATIONS.md` for exactly what this release can
and cannot independently verify against the manuscript's reported numbers.

## Manuscript method scope

This release covers exactly the methods reported in the manuscript:

- **VADER** (lexicon-based) on English reviews, per restaurant brand
- **RoBERTa** (`cardiffnlp/twitter-roberta-base-sentiment-latest`) on
  English reviews, per restaurant brand
- **XLM-RoBERTa** (`xlm-roberta-base`, fine-tuned) on code-mixed Banglish
  reviews
- **TF-IDF + Logistic Regression** baseline, reported alongside XLM-RoBERTa
  on the same Banglish train/validation split
- Preprocessing required for the above (translation/language-splitting,
  cleaning)

An mBERT model and a separate synthetic-data classical-ML comparison exist
in the original project but are **not** manuscript-reported methods and are
excluded here -- see `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 7.

## Repository structure

```
README.md                    -- this file
LICENSE                       -- MIT license (code)
CITATION.cff                  -- how to cite this software
requirements.txt              -- reconstructed dependencies (see docs/ENVIRONMENT_NOTES.md)
.gitignore
RELEASE_MANIFEST.csv          -- every file copied/excluded/generated, with SHA-256 hashes and reasons
RELEASE_NOTES.md              -- what this release is/isn't, and validation results
config/
  model_registry.yaml          -- exact checkpoints/hyperparameters, confirmed in code
data/
  README.md                    -- why no row-level data is included, schemas, label mapping
  LICENSE_DATA.md               -- data licensing statement (no license granted for 3rd-party review data)
  example/synthetic_schema_example.csv  -- FABRICATED schema demo, not study data
src/
  preprocessing/                -- per-brand translation/cleaning scripts
  vader/                        -- per-brand VADER scoring scripts
  roberta/                      -- per-brand RoBERTa scoring scripts
  banglish/                     -- XLM-RoBERTa + TF-IDF/LogReg baseline (Banglish)
  baseline/                     -- see baseline/README.md (baseline lives inside banglish/ script)
  evaluation/                   -- see evaluation/README.md (aggregation gap, not implemented)
  utilities/                    -- CSV<->Excel helper scripts
archive/original_scripts/       -- byte-identical, unrenamed copies of every included script (originals, defects and all)
results/
  README.md                     -- inventory of every manuscript Table 1-12 / Figure 1-9, exact captions, status + provenance. No figures/tables shipped.
models/
  README.md                     -- model weight availability (future Zenodo deposit)
docs/
  REPRODUCIBILITY_LIMITATIONS.md -- read this: checkpoint status, data conflicts, aggregation gap, Banglish denominator, figure/table numbering
  CODE_CHANGES.md               -- exact code defects repaired for this release, before/after, and why
  ENVIRONMENT_NOTES.md
  DATA_PROVENANCE.md
  PIPELINE.md
tests/
  smoke_test.py                 -- synthetic-data-only smoke test
  test_preprocessing_output_contract.py -- fixture test: preprocessing output filenames match scorer input filenames
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

See `docs/ENVIRONMENT_NOTES.md` for which pins are exact-evidence vs.
best-effort bounded ranges.

### NLTK resource setup (required for VADER)

```bash
python -m nltk.downloader vader_lexicon
```

## Input-data schemas

See `data/README.md` for the full column-level schema for both the English
(`name, stars, reviews`) and Banglish (`name, stars, review`) pipelines, and
for the privacy reasons no real review data ships with this repository.

## Pipeline execution order

See `docs/PIPELINE.md`. In short: preprocessing -> VADER / RoBERTa (English,
independent of each other) -> Banglish XLM-RoBERTa + TF-IDF/LogReg baseline.
**Aggregation of per-brand outputs into the manuscript's final tables is an
unresolved manual step in the original project -- no script for it exists,
and none was invented here.** See `docs/REPRODUCIBILITY_LIMITATIONS.md`,
item 2.

Each script expects its input file(s) in its current working directory
(unchanged from the original project's convention -- see
`docs/CODE_CHANGES.md` for why no path-handling changes were made).

## Expected outputs

See the table in `docs/PIPELINE.md`.

## Label definitions

Star rating is mapped to a 3-class sentiment label as follows, confirmed
directly in `src/banglish/banglish_sentiment_pipeline.py`:

| Stars | Label |
|---|---|
| 1-2 | Negative |
| 3 | Neutral |
| 4-5 | Positive |

**This is a proxy/reference label derived from the star rating, not a
human-expert-annotated gold standard.** English-dataset accuracy/F1 figures
are computed against this proxy; only the Banglish XLM-RoBERTa validation
metrics are genuine held-out performance figures. See
`docs/REPRODUCIBILITY_LIMITATIONS.md`, item 8, and
`data/README.md`.

## Two independently compiled English corpora

The manuscript reports two independently compiled English corpora **by
design** -- a VADER-scored corpus and a separately compiled,
non-row-identical RoBERTa-scored corpus (Table 1) -- not a data-integrity
conflict; see `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 1. Separately,
the retained project also contains a much larger raw compilation (not
included in this repository). Neither of the manuscript's two corpora, nor
that larger raw file, is included in this repository (all hold real
reviewer names and raw text -- see `data/README.md`). Which retained raw
source, if either, was the actual input to the manuscript's two corpora is
**not established** from the retained files -- see
`docs/REPRODUCIBILITY_LIMITATIONS.md`, item 10.

## Why this release ships no results at all

This is a **policy choice**, made independently of whatever the
manuscript's own numbers turn out to be (see below: this release has not
independently verified the manuscript's English-corpus or matched-subset
figures either way). This repository draws a hard line at "code only"
because:

1. None of the underlying review corpora are shipped in this release (see
   `data/README.md`), so even fully-traceable computations cannot actually
   be regenerated from this repository alone.
2. Shipping a subset of result figures/tables -- even ones that look
   internally consistent -- would invite readers to treat this repository
   as a source of verified results, which it is not meant to be.

**English corpora and matched subset.** The manuscript reports separate
English-corpus totals (11,235 VADER-scored and 11,783 RoBERTa-scored) and
a 9,892-row matched subset. Because raw data and a retained
aggregation/matching script are not publicly available, this repository
cannot independently reproduce or verify these aggregate values or the
reported agreement statistic. See `docs/REPRODUCIBILITY_LIMITATIONS.md`,
item 1.

**Year-wise Table 3 / Figure 2.** The manuscript reports year-wise
review-volume results. Their underlying timestamped source data and
generation procedure are not included in this code release; therefore
these items are documented as manuscript-reported, not independently
reproducible from the release. See
`docs/REPRODUCIBILITY_LIMITATIONS.md`, item 3.

Two further items remain open, disclosed by the manuscript's own text:

**The Banglish denominator.** The manuscript's Abstract, Sections 3.2/3.5,
and Table 1/Table 4 all state that 975 valid Banglish reviews were used,
but that the documented 780/196 train/validation split sums to 976 --
described in the manuscript itself as "unresolved" and carried through the
Banglish results. This release's own reading of `training_metrics_v2.json`
reports the same discrepancy independently; neither source has been used
to verify the other. See `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 11.

**The exact RoBERTa checkpoint revision.** Retained code directly supports
the checkpoint name (`cardiffnlp/twitter-roberta-base-sentiment-latest`,
present verbatim in `src/roberta/*.py`); the manuscript's text states the
same name. Neither the code nor the manuscript records the exact
historical Hugging Face revision/commit or a pinned historical label
mapping. See `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 5.

See `results/README.md` for the complete, per-item inventory of all
Figures 1-9 and Tables 1-12, with exact captions.

**Bottom line: do not treat this repository as reproducing or verifying
any manuscript-reported number.** The manuscript's own agreement statistic
and performance figures are its own reported results, and this code
release neither recomputes nor confirms them.

## Current reproducibility limitations

Summarized here; full detail in `docs/REPRODUCIBILITY_LIMITATIONS.md`:

1. Two intermediate project files (neither shipped) disagreed with each
   other and with the manuscript's reported English-corpus totals (11,235
   VADER-scored, 11,783 RoBERTa-scored). This release cannot independently
   reproduce or verify the manuscript's own totals, or its 9,892-row
   matched-subset/agreement figures -- no raw data or aggregation/matching
   script is included. See `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 1.
2. No script reconstructs the manuscript's cross-brand aggregated tables
   (Tables 5-9/12, Figures 4-6/9) from per-brand outputs (documented as a
   manual/undocumented gap, not implemented).
3. Two figures (year-wise review-volume plots) remain excluded from this
   release, not because their data is untrustworthy: the manuscript itself
   reports this exact year-wise data as Table 3/Figure 2. They are
   excluded under the same code-only-release policy as every other
   manuscript figure.
4. Three additional figures existed only in a non-finalized scratch folder
   in the original project and were excluded as non-final.
5. The checkpoint name `cardiffnlp/twitter-roberta-base-sentiment-latest`
   is present verbatim in retained code and stated in the manuscript's own
   text; the exact Hugging Face Hub revision/commit is not pinned in
   either, and neither records a pinned historical label mapping.
6. The fine-tuned XLM-RoBERTa weights are excluded from this GitHub release
   entirely (future Zenodo deposit).
7. mBERT and a synthetic-data-only classical-ML comparison were judged
   out-of-scope relative to the manuscript's reported methods (an
   interpretive call the authors should confirm).
8. Static compilation and the synthetic smoke/contract tests were
   executed for this release (see `RELEASE_NOTES.md` for exact commands
   and results). No full raw-data or model-training/inference pipeline was
   executed -- no manuscript-reported number was reproduced or verified by
   running the modeling code.
9. This release ships **no** `results/figures/` or `results/tables/` at
   all, by policy -- see `results/README.md` for the complete,
   manuscript-verbatim inventory of Figures 1-9 and Tables 1-12.
10. It is not established from any retained file which raw English
    compilation, if either, underlies the manuscript's two reported
    English corpora.
11. The Banglish denominator discrepancy (975 vs. 976) is a genuine,
    still-open limitation, reported independently both by this release's
    own inspection of `training_metrics_v2.json` and by the manuscript's
    own Abstract and Sections 3.2/3.5/6.2 -- neither source has verified
    the other; both report the same open inconsistency.
12. The manuscript contains exactly Figures 1-9 and Tables 1-12,
    reproduced verbatim in `results/README.md`. Earlier project drafts
    used different, more extensive numbering that does not match the
    manuscript and are not used to determine manuscript structure
    anywhere in this repository.

## Exact checkpoint status

- **RoBERTa (English):** `cardiffnlp/twitter-roberta-base-sentiment-latest`
  -- confirmed explicitly in code (`MODEL = ...` in all five
  `src/roberta/*.py` scripts). Not a guess, not the plain
  `cardiffnlp/twitter-roberta-base-sentiment` model.
- **XLM-RoBERTa (Banglish):** `xlm-roberta-base` -- confirmed explicitly in
  code (`MODEL_NAME = ...` in `src/banglish/banglish_sentiment_pipeline.py`).
  Fine-tuned weights excluded from GitHub; see `models/README.md`.

## Data & privacy and third-party-platform limitations

No row-level review data (raw, cleaned, translated, or scored; English or
Banglish) is included in this repository. Every such file inspected in the
original project carried a real reviewer display name and unredacted
review text scraped from Google Maps; raw files additionally carried a
per-review URL. See `data/README.md` for the full classification table and
instructions for supplying your own authorized data.

Restaurant brand identities are likewise not disclosed: all five brands
are referred to only as **Brand A** through **Brand E** throughout this
repository, including in file names, folder names, code comments, and
configuration.

## Model-weight availability

`ZENODO DOI: NOT YET ASSIGNED`. See `models/README.md`.

## License

This project's code is licensed under the [MIT License](LICENSE). See
`data/LICENSE_DATA.md` for the separate data-licensing statement (no
license is granted for third-party review data, because none is shipped).

## Citation

If you use this code, please cite it using the metadata in
[`CITATION.cff`](CITATION.cff).

## Authors

- **Shahriar Hasan Ratul** -- Department of Industrial Engineering and
  Management, Khulna University of Engineering & Technology, Khulna-9203,
  Bangladesh. [ORCID: 0009-0000-0155-5516](https://orcid.org/0009-0000-0155-5516)
- **Md. Zaid Hossain** -- Department of Industrial Engineering and
  Management, Khulna University of Engineering and Technology,
  Khulna-9203, Bangladesh. [ORCID: 0009-0003-3301-3609](https://orcid.org/0009-0003-3301-3609)
- **Md. Shahriar Islam** -- Department of Industrial Engineering and
  Management, Khulna University of Engineering and Technology,
  Khulna-9203, Bangladesh. [ORCID: 0009-0005-7551-166X](https://orcid.org/0009-0005-7551-166X)
