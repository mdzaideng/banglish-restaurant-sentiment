# Results inventory

This repository is a **research-code release**, not a results archive. No
manuscript figure, table, or numerical value is copied, recreated, or
recomputed here. This file inventories every Figure 1–9 and Table 1–12 in
the associated manuscript, with its exact caption, release status,
provenance status, and the reason it is not shipped as a separate
artifact.

The manuscript's own Data Availability statement confirms this repository's
scope: *"The aggregate results underlying every claim in this manuscript
are reported in full in Tables 1–12 and Figures 1–9."* There is no Table
13–16 or Figure 10–14 in the manuscript — an earlier project draft used
different, more extensive numbering, but that draft is **not**
authoritative and is not used anywhere in this inventory.

## Status legend

**Release status** (uniform across all 21 items, by policy — see
"Why nothing here is released" below):
- **Embedded in manuscript only** — the item exists as a table/figure
  inside the manuscript. No separate data or image file for it is shipped
  in this release, regardless of how well its provenance is understood.

**Provenance status** (varies per item — whether the release's own code
could regenerate this item, given authorized input data the release does
not itself ship):
- **Traceable** — a script in `src/` corresponds directly to this item's
  computation; reproducing it requires only supplying the documented input
  data (see `data/README.md`), not writing new code.
- **Traceable, procedure partly undocumented** — a script in `src/`
  produces the underlying scores, but a further step used in the
  manuscript (e.g. cross-corpus matching) is not implemented in any
  retained script.
- **Not traceable to release code** — no script anywhere in the retained
  project (released or excluded) corresponds to this item.

## Inventory

| # | Exact caption (verbatim from the manuscript) | Release status | Provenance status | Release rationale |
|---|---|---|---|---|
| Table 1 | *Corpus characteristics.* | Embedded in manuscript only | Traceable, procedure partly undocumented — Banglish row count traces to `src/banglish/banglish_sentiment_pipeline.py` and `data/README.md`'s schema (see the manuscript's own disclosed 975-vs-976 discrepancy, Section 3.2/6.2); the two English corpus sizes are not reconstructable from any script or data shipped or excluded in this project | Code release policy: no result table is shipped. See `docs/REPRODUCIBILITY_LIMITATIONS.md` item 11 for the Banglish count disclosure. |
| Table 2 | *Mapped branch distribution by brand.* | Embedded in manuscript only | Not traceable to release code — no geocoding/branch-mapping script exists anywhere in the retained project | Code release policy. |
| Figure 1 | *Spatial distribution of sampled restaurant branches: (a) national distribution, (b) Dhaka metropolitan detail.* | Embedded in manuscript only | Not traceable to release code | Code release policy. |
| Table 3 | *Year-wise review volume breakdown by restaurant brand (2020–2025).* | Embedded in manuscript only | Not traceable to release code — no script that reads a date/timestamp field exists anywhere in the retained project, but the manuscript confirms this data is legitimate, reported content (not a data-integrity concern) | Code release policy. See `docs/REPRODUCIBILITY_LIMITATIONS.md` item 3 (corrected) — describes collection volume only, not the analysis population. |
| Figure 2 | *Year-over-year customer review volume trends (2020–2025) across five restaurant brands in Bangladesh.* | Embedded in manuscript only | Not traceable to release code, same basis as Table 3 | Code release policy; same note as Table 3. |
| Figure 3 | *Data cleaning and preprocessing pipeline, from raw review collection through model-specific input preparation for VADER, RoBERTa, and XLM-RoBERTa.* | Embedded in manuscript only | Traceable — this diagram documents the same pipeline implemented in `src/preprocessing/`, `src/vader/`, `src/roberta/`, and `src/banglish/` | Code release policy; the pipeline it diagrams is exactly what `src/` implements, but the figure itself (an illustration) is not shipped. |
| Table 4 | *XLM-RoBERTa fine-tuning configuration.* | Embedded in manuscript only | Traceable — every listed parameter (seed, epochs, learning rates, class weighting, temperature, split ratio) is confirmed directly in `src/banglish/banglish_sentiment_pipeline.py` and mirrored in `config/model_registry.yaml`, which **is** shipped in this release | Table itself not shipped by policy, but its content is fully mirrored in `config/model_registry.yaml`. |
| Table 5 | *Reference and model class distributions, English reviews (star-derived reference vs. VADER and RoBERTa predicted distributions, each on its respective corpus).* | Embedded in manuscript only | Traceable — computation logic is in `src/vader/*.py` and `src/roberta/*.py`; requires the (unshipped) English corpora as input | Code release policy. |
| Figure 4 | *Sentiment class distribution: star-derived reference vs. VADER and RoBERTa (both label-derivation methods), respective English corpora.* | Embedded in manuscript only | Traceable, same basis as Table 5 | Code release policy. |
| Table 6 | *Per-class classification performance: VADER and RoBERTa vs. respective star-derived reference.* | Embedded in manuscript only | Traceable, same basis as Table 5 | Code release policy. |
| Figure 5 | *Per-class precision, recall, and F1 for VADER and both RoBERTa label-derivation methods, respective English corpora.* | Embedded in manuscript only | Traceable, same basis as Table 5 | Code release policy. |
| Table 7 | *English pipeline summary: accuracy and macro-averaged metrics, VADER and RoBERTa (threshold and argmax), each on its respective corpus.* | Embedded in manuscript only | Traceable, same basis as Table 5 | Code release policy. |
| Table 8 | *Inter-model agreement statistics, verified matched English subset (n = 9,892).* | Embedded in manuscript only | Traceable, procedure partly undocumented — VADER/RoBERTa scoring is in `src/`, but the composite-key matching procedure used to build the matched subset (brand, reviewer name, star rating, normalized text) is not implemented in any retained script | Code release policy. See `docs/REPRODUCIBILITY_LIMITATIONS.md` item 2 (aggregation gap). |
| Table 9 | *Inter-model agreement matrix, verified matched English subset (n = 9,892).* | Embedded in manuscript only | Traceable, procedure partly undocumented — same basis as Table 8 | Code release policy. |
| Figure 6 | *Inter-model agreement matrix, VADER vs. RoBERTa (argmax), verified matched English subset (n = 9,892).* | Embedded in manuscript only | Traceable, procedure partly undocumented — same basis as Table 8 | Code release policy. |
| Figure 7 | *Lexical frequency profiles: frequently occurring terms within positive and negative displayed groups. (a) VADER, (b) RoBERTa, (c) Banglish reviews.* | Embedded in manuscript only | Not traceable to release code — no word-frequency-counting script exists anywhere in the retained project; the manuscript itself notes the counting/tokenization procedure is undocumented (Section 6.2) | Code release policy. |
| Table 10 | *XLM-RoBERTa per-class validation performance, held-out Banglish validation split (n = 196).* | Embedded in manuscript only | Traceable — `src/banglish/banglish_sentiment_pipeline.py` computes and writes exactly this evaluation, on the same 80/20 split | Code release policy. |
| Table 11 | *Banglish model and baseline comparison, held-out validation split (n = 196).* | Embedded in manuscript only | Traceable — the same script trains and evaluates both the XLM-RoBERTa model and the TF-IDF+logistic-regression baseline (`baseline_tfidf_logreg()`) on this split | Code release policy. |
| Figure 8 | *XLM-RoBERTa per-class validation performance and Banglish baseline comparison, held-out validation split (n = 196).* | Embedded in manuscript only | Traceable, same basis as Table 11 | Code release policy. |
| Table 12 | *English and Banglish approaches summarized in two groups (not a combined ranking). English: star-derived reference, full respective corpus. Banglish: held-out validation split, n = 196. The two groups use different languages, corpora, and evaluation bases and are not presented as a single ranked comparison.* | Embedded in manuscript only | Traceable, procedure partly undocumented — combines the English basis (Table 7, matching-gap caveat applies) and the Banglish basis (Table 11, fully traceable); no script assembles the combined table | Code release policy. |
| Figure 9 | *English and Banglish approaches shown as two separate panels (not a combined ranking), each labeled with its own evaluation basis.* | Embedded in manuscript only | Traceable, procedure partly undocumented — same basis as Table 12 | Code release policy. |

## Why nothing here is released

This is deliberate, not an oversight. Even for the items marked
**Traceable** above — where a script in `src/` genuinely implements the
computation — the release ships no result artifact, for two independent
reasons:

1. **Data.** None of the underlying review corpora (English or Banglish,
   raw or cleaned) are shipped in this release; see `data/README.md` for
   why (reviewer names, raw review text, and — for the raw English
   corpora — per-review URLs). Without that data, none of these tables or
   figures can actually be regenerated from this repository alone.
2. **Policy.** This repository is explicitly scoped as a code release
   (see `README.md`, `RELEASE_NOTES.md`). Shipping a subset of result
   figures/tables — even fully traceable ones — would invite readers to
   treat this repository as a source of verified results, which it is
   not meant to be.

## What this release can and cannot say about the manuscript's numbers

The manuscript is the source for its own reported figures. Having its
text does not mean this release has independently reproduced or verified
those figures: this repository ships no raw review data and no
aggregation/matching script, so none of the manuscript's aggregate values
(English-corpus totals, the 9,892-row matched subset, the agreement
statistic, the year-wise volume figures) are recomputed or checked here.

What retained files *do* support directly, without needing to trust the
manuscript: two intermediate project files that were flagged as apparently
conflicting (`Sentiment_Analysis_Tables_Charts.xlsx`, `All_9_Tables.docx`,
neither shipped in this release) do not match each other, and neither
matches the totals the manuscript states -- a plain comparison of
retained files, not an independent check of whether the manuscript's own
totals are correct. See `docs/REPRODUCIBILITY_LIMITATIONS.md`, item 1, for
that comparison in full.

Two items remain open regardless, because the manuscript's own text
discloses them as unresolved:

- **The Banglish 975-vs-976 split** (Table 1, Table 4, Figure 3): the
  manuscript's own Abstract, Section 3.2, Section 3.5, and Section 6.2 all
  state this discrepancy is carried forward undisclosed-cause, not
  reconciled. This release's own reading of `training_metrics_v2.json`
  reports the same discrepancy independently, but neither source has been
  used to verify the other — see `docs/REPRODUCIBILITY_LIMITATIONS.md`,
  item 11.
- **The RoBERTa checkpoint's exact historical revision and label
  mapping** (Tables 5–9, Figures 4–6): retained code directly supports the
  checkpoint name (`cardiffnlp/twitter-roberta-base-sentiment-latest`,
  present verbatim in `src/roberta/*.py`); the manuscript's text states
  the same name. Neither the code nor the manuscript establishes the exact
  Hugging Face revision/commit in use at analysis time, or a pinned
  historical label mapping — see `docs/REPRODUCIBILITY_LIMITATIONS.md`,
  item 5, and `config/model_registry.yaml`.
