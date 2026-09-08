# Baseline (TF-IDF + Logistic Regression)

There is no separate script here. The manuscript's reported TF-IDF+LogReg
baseline is implemented as `baseline_tfidf_logreg()` inside
`../banglish/banglish_sentiment_pipeline.py`, run on the same train/
validation split as the XLM-RoBERTa model so the two are directly
comparable (this is required by the script's own header comment: *"A
'research grade' claim needs the transformer to beat both [baselines], on
the same split"*).

A different classical-ML script (`classical_ML.py`, training 5 classifiers
including Logistic Regression on a synthetic dataset) exists in the
original project but was judged out-of-scope for this release -- see
`../../docs/REPRODUCIBILITY_LIMITATIONS.md`, item 7.
