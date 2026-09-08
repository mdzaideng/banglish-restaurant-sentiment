# Pipeline execution order

Each stage below is a set of independent scripts (one per brand, where
applicable), not a single driver program -- there is no top-level "run
everything" script in the original project, and none was added (see
docs/CODE_CHANGES.md). Run them in this order, supplying your own
authorized local data per `data/README.md`.

## 1. Preprocessing (`src/preprocessing/`)

Per brand: raw Google-review CSV -> language split (English / Banglish) ->
translated / cleaned CSV. Not every brand has every stage (e.g. Brand A
has no `*_bangla.py`/`*_translated.py` -- its reviews did not feed the
Banglish dataset).

## 2. English sentiment scoring

- `src/vader/<brand>_vader.py` -- reads `<brand>_cleaned_VADER[.csv]`,
  applies `nltk` VADER, writes a compound-score CSV/plot.
- `src/roberta/<brand>_roberta.py` -- reads `<brand>_cleaned_ROBERTA.csv`,
  applies `cardiffnlp/twitter-roberta-base-sentiment-latest`, writes a
  scored CSV/plot.

These two are independent of each other and can run in either order.

## 3. Banglish XLM-RoBERTa + TF-IDF/LogReg baseline

`src/banglish/banglish_sentiment_pipeline.py` -- reads
`banglish_dataset_final.csv`, computes the majority-class and
TF-IDF+LogReg baselines, then fine-tunes `xlm-roberta-base`. Requires
internet access to the Hugging Face Hub and, per the script's own comment,
"ideally a GPU." See docs/ENVIRONMENT_NOTES.md.

## 4. Utilities (`src/utilities/`)

CSV <-> Excel converters used ad hoc between stages 1-3; not part of the
analytical pipeline itself.

## 5. Aggregation (unresolved -- see docs/REPRODUCIBILITY_LIMITATIONS.md, item 2)

No script in this repository reconstructs the authoritative manuscript's
cross-brand English tables/figures (Tables 5-9 and 12, Figures 4-6 and 9;
see `results/README.md`) from the per-brand outputs of steps 2-3. This is
a manual/undocumented step in the original project that was not
reverse-engineered for this release.

## Expected outputs per stage

| Stage | Output |
|---|---|
| Preprocessing | `<brand>_cleaned_VADER`, `<brand>_cleaned_ROBERTA.csv` |
| VADER | `<brand>_VADER.xlsx`/`sentiment_output.csv`, compound-vs-star figure |
| RoBERTa | `<brand>_roberta_final.csv`, score-vs-star figure |
| Banglish pipeline | `banglish_sentiment_scored_v2.csv`, confusion-matrix + training-curve figures, `training_metrics_v2.json` |
