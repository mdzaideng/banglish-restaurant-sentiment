# Model weights

This GitHub release intentionally contains **no trained model weights**.

| Model | Base checkpoint (confirmed in code) | Weights in this repo? |
|---|---|---|
| RoBERTa (English) | `cardiffnlp/twitter-roberta-base-sentiment-latest` (pretrained, used as-is, not fine-tuned locally) | N/A -- downloaded from the Hugging Face Hub at runtime by `src/roberta/*.py` |
| XLM-RoBERTa (Banglish) | `xlm-roberta-base`, fine-tuned locally by `src/banglish/banglish_sentiment_pipeline.py` | **No.** Original fine-tuned checkpoints (`bert_model/checkpoint-69`, `xlm_banglish_model/checkpoint-{69,138,207}`, ~2-3.4 GB each) exist only in the original project folder and were excluded from this release per instruction. |
| mBERT | N/A | **Excluded entirely** -- not a manuscript-reported method. See docs/REPRODUCIBILITY_LIMITATIONS.md, item 7. |

## Future Zenodo deposit

`ZENODO DOI: NOT YET ASSIGNED`

A future Zenodo record is intended to host the fine-tuned XLM-RoBERTa
checkpoint(s), permitted data artifacts (pending the privacy/redistribution
review described in `data/README.md`), and SHA-256 checksums for each
uploaded file. This README will be updated with the real DOI, a citable
Zenodo badge, and checksums once that record exists. No placeholder DOI or
badge has been fabricated for this release.

## Re-fine-tuning instructions (until the Zenodo record exists)

Anyone who needs the trained Banglish XLM-RoBERTa model today must re-run
`src/banglish/banglish_sentiment_pipeline.py` against their own copy of
`banglish_dataset_final.csv` (see `data/README.md` for the expected
schema), using the exact hyperparameters recorded in
`config/model_registry.yaml`. Note that the retained scripts do not pin a
Hugging Face Hub revision for either base checkpoint, so bit-for-bit
reproduction of historical results is not guaranteed even with identical
code and data -- see docs/REPRODUCIBILITY_LIMITATIONS.md, item 5.
