# Reproducibility limitations

This document lists every gap found while assembling this release, in order
of how much it affects trust in reported numbers. Nothing below was
"fixed" by guessing -- each item is either a missing artifact, an
unresolved procedure, or a genuine inconsistency found in the retained
project files.

The associated manuscript establishes the figure/table numbering used
throughout this release (Figures 1-9, Tables 1-12, reproduced with exact
captions in `results/README.md`), and **reports** figures for its English
corpora, a matched-subset agreement statistic, a Banglish train/validation
split, and year-wise review volume. Having the manuscript's text is not
the same as this release being able to independently verify those
figures: **this repository does not ship the raw review data or the
aggregation/matching scripts that would be needed to recompute any of
them, so none of these manuscript-reported values are independently
reproduced or verified here.** Item 1 states this precisely for the
English-corpus/matched-subset figures; item 3 states it for the year-wise
figures. **Authors should still resolve item 2** (no retained
aggregation/matching script) before anyone could independently reproduce
those values from released code -- see `results/README.md` for exactly
which manuscript table/figure each open item affects.

## 1. English corpora and the matched subset: manuscript-reported, not independently verified by this release

An earlier internal review flagged an apparent conflict between two
intermediate project files, neither of which is shipped in this release:

- `Sentiment_Analysis_Tables_Charts.xlsx`, Sheet "1 Dataset Overview"
  (Table 1), states: Total reviews (VADER-scored) = 2,357; RoBERTa-scored
  = 2,354, labeled as the whole "English Reviews" total (not per brand).
- `All_9_Tables.docx`, Table 1 ("Brand-Level Sentiment Distribution"),
  gives a per-brand breakdown whose "Overall" row sums to 11,235 reviews
  (VADER-scored) across the five brands -- and whose Brand A-only row
  is exactly 2,357 (VADER) / 2,354 (RoBERTa), the same figures the other
  file labels as the whole-dataset total. **This specific numeric
  coincidence between the two withheld files was established by directly
  opening and comparing them** -- that part is a plain reading of retained
  files, not an inference.

**The manuscript reports separate English-corpus totals (11,235
VADER-scored and 11,783 RoBERTa-scored) and a 9,892-row matched subset.
Because raw data and a retained aggregation/matching script are not
publicly available, this release cannot independently reproduce
or verify these aggregate values or the reported agreement statistic.**
What can be said from retained files alone: neither of the two
manuscript-reported English-corpus sizes (11,235 / 11,783) equals either
of `Sentiment_Analysis_Tables_Charts.xlsx`'s totals (2,357 / 2,354), so
that withheld file's "Dataset Overview" sheet does not match what the
manuscript states -- plausibly an earlier, single-brand (Brand A)
computation mislabeled as a whole-dataset total, though this release does
not have a script or record that establishes how that file was produced.
It remains withheld from every release (see `results/README.md`),
now with this discrepancy documented rather than left as an open
question about which of two withheld numbers might be right.

Separately, the manuscript's own text (Section 4.5) describes a
composite-key linking procedure used to build its reported matched
subset, distinct from anything in the withheld xlsx's "Table 9" (whose
2,354 "reviews compared" figure carries the same Brand A-only
mislabeling noted above). No script implementing that linking procedure,
or any other cross-brand matching/aggregation logic, exists anywhere in
the retained project (see item 2). This release therefore reports what
the manuscript states about its matched subset without independently
recomputing or checking it.

**On the reported "9,892-row matched subset":** this figure cannot be
traced to any retained project file. The manuscript's own text (Section
4.5, Table 8) reports 9,892 as its matched-subset size. This release did
not independently reproduce that figure and has no basis to verify it
beyond the manuscript's own statement.

## 2. No script reconstructs the manuscript's aggregated tables

Neither the manuscript's cross-brand English tables/figures (Tables 5-9
and 12, Figures 4-6 and 9) nor the withheld, now-superseded
`Sentiment_Analysis_Tables_Charts.xlsx` / `All_9_Tables.docx` /
`*_All_Restaurants_Sentiment_Score.xlsx` files are written by any retained
script. `grep` across every `.py` file in the original project for
`agreement`, `kappa`, `cohen`, or any VADER-RoBERTa merge/join logic found
no matches outside the venv's third-party library source code -- including
no implementation of the composite-key matching procedure the manuscript
describes in Section 4.5 for building its reported 9,892-review matched
subset. Per instruction, no aggregation script was invented for this
release (Option B was taken, not Option A): this is documented as an
unresolved manual/undocumented step. Anyone attempting to reproduce the
manuscript's Tables 5-9/12 or Figures 4-6/9 from the per-brand script
outputs in this repository will need to write that cross-brand aggregation
and matching logic themselves; see `results/README.md` for exactly which
items this affects.

## 3. Year-wise Table 3 / Figure 2: manuscript-reported, not independently reproducible from this release

`Final Outputs & Analysis/review_volume_year_wise.png` and
`Final Outputs & Analysis/img_07.png` (both original filenames) each plot
reviews per year, by brand, 2020-2025. This item originally excluded them
because the withheld `Sentiment_Analysis_Tables_Charts.xlsx`'s methodology
notes claimed *"No date/timestamp field exists in any source file. A
reviews-by-year table ... has intentionally been omitted rather than
fabricated, since no temporal data was collected."*

**The authoritative manuscript reports year-wise review-volume results**
as Table 3 ("Year-wise review volume breakdown by restaurant brand
(2020-2025)") and Figure 2 ("Year-over-year customer review volume
trends"), a per-brand, per-year breakdown totalling 38,180 reviews, with
values consistent with what the two excluded PNGs show. **Their
underlying timestamped source data and generation procedure are not
included in this code release; therefore these items are documented as
manuscript-reported, not independently reproducible from the release.**
This release did not verify how the manuscript's year-wise figures were
produced, and no raw file retained in the project carries a date/
timestamp column -- so while the withheld xlsx's specific claim ("no such
data exists") does not match what the manuscript reports, that does not
mean this release has independently confirmed the manuscript's year-wise
data is correct, only that the withheld xlsx's claim and the manuscript's
own reported table disagree with each other.

**These two files remain excluded from this release regardless**, for the
same reason every other manuscript figure is excluded (see
`results/README.md`, "Why nothing here is released" -- this is a
code-only release by policy, not a case-by-case judgment about which
figures are trustworthy). The manuscript itself is explicit that Table
3/Figure 2 describe collection volume only, are not the analytical sample,
and that the retained documentation does not establish how the smaller
modeling corpora relate to this larger collected volume (Section 3.2,
Section 6.2) -- a distinct, still-open point, separate from the
provenance question this item originally raised.

## 4. Three additional figures found only in a "Gemini" scratch folder were excluded

`Final Outputs & Analysis/Gemini/img_04.png`, `img_05.png`, `img_06.png`
exist only inside the `Gemini/` subfolder -- they were never copied into
the top-level `Final Outputs & Analysis/` folder the way `img_01-03` and
`img_07` were. `img_04.png` ("VADER/RoBERTa Sentiment by Restaurant Brand")
shows per-brand review counts in the ~1,300-2,700 range per brand
(summing to roughly 11,000+ across five brands) -- consistent with the
`All_9_Tables.docx` "Overall" figure of 11,235, not the 2,354-2,357 figure
in the Dataset Overview sheet. This is more evidence for item 1, but since
these three images were never promoted into the finalized output folder,
they were treated as non-final/exploratory and excluded rather than
second-guessing which figures the authors intended as final.

## 5. Exact historical RoBERTa checkpoint

**Confirmed, not guessed:** all five `src/roberta/*.py` scripts contain the
literal line `MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"`.
This is recorded in `config/model_registry.yaml`. What is *not* recoverable
is the exact Hugging Face Hub revision/commit hash that was live when these
scripts were originally run -- the scripts pin only the model name, not a
revision. If `cardiffnlp/twitter-roberta-base-sentiment-latest` is updated
upstream in the future, re-running these scripts will not necessarily
reproduce the historically reported numbers exactly. This is listed as a
limitation, not fabricated as a pinned revision.

## 6. XLM-RoBERTa: architecture confirmed, trained weights excluded

`config/model_registry.yaml` records `xlm-roberta-base` (confirmed directly
in `src/banglish/banglish_sentiment_pipeline.py`) and the full training
configuration as literally read from that file (seed, epochs, learning
rates, split ratio, etc.). The fine-tuned weights themselves (originally at
`Clean data/brand_d_classifier/xlm_banglish_model/checkpoint-{69,138,207}/`,
~3.1-3.4 GB each) are excluded from this GitHub package per instruction.
See `models/README.md` for the future-Zenodo placeholder.

## 7. mBERT and the brand_d_classifier synthetic-data experiments are out of scope

`Clean data/brand_d_classifier/` contained three additional scripts
(`brand_d_m_bert.py`, `brand_d_xlm_roberta.py`, `classical_ML.py`) plus a synthetic
1,000-row dataset (`brand_d_synthetic_reviews_v2.csv`) and a small ad-hoc
112-row "real Banglish" subset extracted from Brand D reviews via a keyword
heuristic (`is_real_banglish()` in `classical_ML.py`). All of this was
excluded:

- `brand_d_m_bert.py` trains mBERT, which is not a manuscript-reported method.
- `brand_d_xlm_roberta.py` trains a **second, separate** XLM-RoBERTa run, using
  only the synthetic dataset for both training and its "realistic" scoring
  step (`orig_df = pd.read_csv("brand_d_synthetic_reviews_v2.csv")` is used for
  both). This does not match the manuscript's reported Banglish pipeline,
  which is `src/banglish/banglish_sentiment_pipeline.py` operating on the
  real `banglish_dataset_final.csv` (976 data rows -- see item 11 for the
  976-vs-975 discrepancy between this file, the training run's own
  recorded output, and the Dataset Overview sheet's stated Banglish total;
  its 20% validation split does match the workbook's stated "196 reviews
  never seen in training" exactly, per `training_metrics_v2.json`'s
  recorded `val_rows: 196`).
- `classical_ML.py` does implement TF-IDF + Logistic Regression (among four
  other non-reported classifiers: Naive Bayes, SVM, Random Forest, Gradient
  Boosting), but trains on the excluded synthetic set and evaluates on the
  112-row Brand D-only keyword-filtered subset -- not the same TF-IDF+LogReg
  baseline the manuscript reports. **The manuscript's actual reported
  TF-IDF+LogReg baseline is the `baseline_tfidf_logreg()` function inside
  `src/banglish/banglish_sentiment_pipeline.py`**, run on the same
  975-row/80-20 split as the XLM-RoBERTa model, which is what's included in
  this release.

This is an interpretive judgment call, made from code evidence rather than
assumption, and should be confirmed by the authors: if `classical_ML.py`
or `brand_d_xlm_roberta.py` is in fact what the manuscript reports, they were
excluded in error and should be added back (they were not deleted from the
original project -- see RELEASE_MANIFEST.csv for their exact original
location).

## 8. Star-derived labels are proxies, not gold-standard annotations

Per `Sentiment_Analysis_Tables_Charts.xlsx`'s own methodology notes:
English-dataset accuracy/F1 figures are computed against a **star-derived
reference label** (a full-dataset proxy), *not* a human-expert-annotated
gold standard as in the base paper. The Banglish XLM-RoBERTa figures are
described as genuine held-out validation metrics. **These two evaluation
bases are not directly comparable to each other** -- this caveat is
reproduced verbatim from the source workbook and should be treated as
load-bearing, not an incidental footnote.

## 9. Static compilation and synthetic tests were executed; the full scientific pipeline was not

This environment has no internet access to the Hugging Face Hub and no
GPU. `src/banglish/banglish_sentiment_pipeline.py` explicitly states it
"will NOT run in a sandboxed environment with no internet access to HF."

**Precisely what this means:** static compilation
(`python -m py_compile`) was genuinely run against every script in `src/`
and `tests/`, and `tests/smoke_test.py` and
`tests/test_preprocessing_output_contract.py` were genuinely executed and
passed (both are synthetic-data-only: a fabricated schema-demo CSV and a
static filename-contract check, respectively -- see `RELEASE_NOTES.md`
for exact commands and results). **No full raw-data or
model-training/inference pipeline was executed** -- VADER, RoBERTa,
XLM-RoBERTa, and the TF-IDF+LogReg baseline were not run against any real
data, and no manuscript-reported number was reproduced, recomputed, or
verified by execution. Passing the synthetic/static checks confirms the
code is syntactically valid and its file-naming contracts hold; it does
not confirm the modeling code produces the manuscript's reported results.
See `RELEASE_NOTES.md`'s validation section for exact commands and
outputs.

## 10. Two independently compiled English corpora exist, and only the smaller is scored

`Google map reviews (raw)/*.csv` (5 files, one per brand, feeding the
included VADER/RoBERTa pipeline) is small relative to
`Final Outputs & Analysis/Raw data/english_raw_reviews.xlsx`, which contains
per-brand sheets of 6,369-8,334 rows each (tens of thousands of reviews
total) -- both held back from this release under the privacy rules (see
`data/README.md`), but their row counts were inspected (headers/sheet
dimensions only) to establish this fact. The authoritative manuscript
reports its two English corpora as 11,235 (VADER-scored) and 11,783
(RoBERTa-scored) reviews (Table 1) -- this release has not independently
verified those totals (see item 1) -- and it remains **not established
from any retained file** which of these two larger raw sources, if either
exclusively, was the actual input to those two corpora. This is left for
the authors to clarify. It is a separate question from item 1, which
concerns whether two withheld intermediate files' own totals were
internally consistent with each other and with the manuscript (they were
not, independent of whether the manuscript's totals are themselves
independently verifiable).

## 11. The Banglish dataset's own row count disagrees between the workbook and the actual recorded training run

Found while cross-checking the retained data against the actual run output
(`Banglish Analysis/training_metrics_v2.json`), not assumed:

- `banglish_dataset_final.csv` has 976 data rows (977 lines including the
  header).
- `Sentiment_Analysis_Tables_Charts.xlsx`'s methodology notes state: *"One
  review in the Banglish dataset had an invalid 0-star rating and was
  excluded (n=975 used)"* -- i.e., the workbook claims the actually-used
  Banglish sample size is **975**.
- But `training_metrics_v2.json` -- the literal JSON output written by
  `src/banglish/banglish_sentiment_pipeline.py` for the training run that
  produced the reported Banglish results -- records **`"rows": 976,
  "train_rows": 780, "val_rows": 196`**. 780 + 196 = 976, not 975. The
  actual recorded run used all 976 rows; it did not exclude the invalid-
  rating review the workbook says was excluded.
- `src/banglish/banglish_sentiment_pipeline.py`'s own header comment
  independently corroborates 976 (*"this small (~976 row) dataset"*), not
  975.

Unlike item 1 (which turned out to be a discrepancy between two withheld,
non-authoritative files rather than a manuscript defect), this
inconsistency is directly supported by retained code/data: the release's
own `training_metrics_v2.json` records 976 rows for the run that produced
the reported Banglish results. Separately, the manuscript's own Abstract,
Section 3.2, Section 3.5, Table 1, and Table 4 all state the same 780/196
split summing to 976 against a reported 975 valid reviews, describe it
explicitly as "unresolved," and carry it through the Banglish results
without correction -- the manuscript's text and this release's independent
reading of `training_metrics_v2.json` report the same discrepancy, but
this release has not used one to verify the other; both are reported here
as what each source states. It affects every Banglish-side reported
metric, since accuracy/F1/precision/recall are all computed over
`val_rows`, and it is not established which of "975" or "976" is the
number the manuscript's reported Banglish figures are actually built on.
Not resolved here, nor by the manuscript -- see `results/README.md` for
which manuscript items this affects.

## 12. Manuscript figure/table numbering

The associated manuscript contains exactly Figures 1-9 and Tables 1-12;
`results/README.md` inventories all 21 with their exact captions,
reproduced verbatim from that manuscript.

Earlier project drafts used different, more extensive, non-overlapping
numbering (up to Table 16 / Figure 14 in the more complete of the two).
Those drafts are **not** shipped in this release and are **not** used to
determine manuscript structure anywhere in this repository.
