# Data

## Why no public row-level review data is included yet

Every row-level review dataset found in the original project -- raw,
translated, cleaned, VADER/RoBERTa-scored, English, and Banglish alike --
was inspected (column headers and a small local sample, not printed here)
and found to include a `name` column populated with what appear to be real
Google Maps reviewer display names, directly paired with unredacted review
text scraped from a third-party platform. The raw source additionally
carries a per-review `reviewUrl`, a URL that can potentially be traced back
to an individual reviewer's public profile. No timestamp/date field exists
in any retained file.

Per this release's data-privacy rules, none of that is included, regardless
of whether the audit's earlier pass classified the containing file as a
"final" or "manuscript-facing" result. Two files in particular
(`ROBERTA_All_Restaurants_Sentiment_Score.xlsx`,
`VADER_All_Restaurants_Sentiment_Score.xlsx`) are named as if they were
aggregated summaries but were confirmed on inspection to be full row-level
exports with real reviewer names and raw text -- they are held back, not
included.

### Classification of every row-level dataset found

| Dataset (original location) | Classification | Why |
|---|---|---|
| `Google map reviews (raw)/*.csv` (5 brands) | `HOLD_FOR_ZENODO_AND_RIGHTS_REVIEW` | Raw third-party scrape: reviewer name, per-review URL, unredacted text; redistribution rights from the platform are unclear |
| `Clean data/<brand>/*_cleaned_*`, `*_translated.csv`, `*_bangla_reviews.csv` | `HOLD_FOR_PRIVACY_REVIEW` | Still carries `name` + raw review text after cleaning |
| `<brand>(ROBERTA)/*_final.csv`, `<brand>(VADER)/*_sentiment_output.csv`, `.xlsx` equivalents | `HOLD_FOR_PRIVACY_REVIEW` | Scored outputs retain `name` + raw text alongside model scores |
| `Banglish Analysis/banglish_dataset_final.csv`, `Real reviews 0{1,2,3}.csv`, `banglish_sentiment_scored_v2.{csv,xlsx}` | `HOLD_FOR_PRIVACY_REVIEW` | Same pattern: `name` + raw review text |
| `Final Outputs & Analysis/Raw data/*.xlsx` (bangla/english/labeled) | `HOLD_FOR_ZENODO_AND_RIGHTS_REVIEW` | Large (thousands of rows per brand) raw/labeled compilations, same PII pattern |
| `Final Outputs & Analysis/{ROBERTA,VADER}_All_Restaurants_Sentiment_Score.xlsx` | `HOLD_FOR_PRIVACY_REVIEW` | Confirmed on inspection: real reviewer full names + raw text rows, despite the "All_Restaurants" aggregate-sounding name |
| `Clean data/brand_d_classifier/brand_d_synthetic_reviews_v2.csv`, `real_banglish_scored.csv` | `EXCLUDE` | Out of manuscript scope (see docs/REPRODUCIBILITY_LIMITATIONS.md, item 7); the latter also carries real reviewer name + text |
| `catagories.csv/.xlsx`, `Brand_and_Items.xlsx` | `SAFE_FOR_GITHUB` | Business/category reference tables, no review-level or personal data. Not shipped in this release regardless -- result tables are excluded entirely under the code-only-release policy (see `results/README.md`) |
| `Sentiment_Analysis_Tables_Charts.xlsx`, `All_9_Tables.docx` | `SAFE_FOR_GITHUB` (privacy), but non-authoritative | Confirmed on inspection: aggregate counts/percentages/model metrics only, no row-level text or names. Not shipped -- and, independently of the code-only policy, their own dataset-size figures do not match the authoritative manuscript (see `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 1) |

No dataset was anonymized or transformed to make it "safe" -- per
instruction, questionable row-level data is excluded outright, not
silently redacted, and this table documents the expected schema instead so
the pipeline remains runnable against authorized local data.

## Required input schemas

### English pipeline (VADER / RoBERTa), per brand

`<brand>_cleaned_VADER` / `<brand>_cleaned_ROBERTA.csv`:

| column | type | notes |
|---|---|---|
| `name` | string | reviewer display name -- **do not commit real values** |
| `stars` | integer 1-5 | star rating |
| `reviews` | string | free-text review |

Scripts add an `Index No` column automatically if missing.

### Banglish pipeline

`banglish_dataset_final.csv`:

| column | type | notes |
|---|---|---|
| `name` | string | reviewer display name -- **do not commit real values** |
| `stars` | integer 1-5 | star rating |
| `review` | string | free-text, code-mixed Bangla/English |

## Label mapping (proxy/reference labels, not human-annotated gold standard)

| Stars | Label |
|---|---|
| 1-2 | Negative |
| 3 | Neutral |
| 4-5 | Positive |

Confirmed directly in `src/banglish/banglish_sentiment_pipeline.py`
(`stars_to_label`) and separately, the associated manuscript (Section 3.3)
states this same mapping is a rating-derived proxy for sentiment, not a
human-expert-annotated gold standard. Treat any accuracy/F1 figure computed
against it accordingly -- see docs/REPRODUCIBILITY_LIMITATIONS.md, item 8.

## Supplying your own authorized local data

1. Obtain your own review data under your own scraping/collection
   authorization (this repository does not grant or imply any right to
   scrape Google Maps or any other platform).
2. Match the schema above exactly (column names are read literally by the
   scripts).
3. Place files where `src/preprocessing/` and `src/vader/roberta/banglish`
   scripts expect them (same working directory as the script -- see
   docs/CODE_CHANGES.md and docs/PIPELINE.md), or point the script at your
   file if you've adapted it to accept a path argument.
4. `data/example/synthetic_schema_example.csv` is a **fabricated,
   3-row schema demonstration only** (invented names and text) for smoke-
   testing the expected columns -- it is not study data and must never be
   cited or analyzed as if it were.

## Future Zenodo deposit

A future Zenodo record may host permitted data artifacts -- for example, an
aggregated/de-identified version of the review data, or the raw data under
a restricted-access agreement -- once a privacy and third-party
redistribution-rights review has been completed by the authors. No such
record exists yet; nothing in this repository should be read as implying
one does.
