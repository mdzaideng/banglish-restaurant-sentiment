# Environment notes

## What we actually found

The original project folder contained exactly one committed Python environment:
`Clean data/brand_d_classifier/venv/` (a full `venv`, ~40,000 files, ~1.1 GB). No
`requirements.txt`, `environment.yml`, `pyproject.toml`, or `Pipfile` existed
anywhere in the project.

## Why the venv is not simply copied here

1. It is a full virtual environment (compiled packages, `.pyc` caches, a
   `pyvenv.cfg` pointing at a specific local Python install) -- not a
   dependency manifest. Committing it would violate the exclusion rules for
   this release regardless.
2. It is **incomplete for this repository's own scripts**: it has no `nltk`,
   which every `src/vader/*.py` script imports (`from nltk.sentiment import
   SentimentIntensityAnalyzer`). That means the venv was built for the
   `brand_d_classifier` Transformer work specifically, not for the VADER/RoBERTa
   per-brand pipeline. Whatever environment actually ran the VADER/RoBERTa
   scripts historically was never captured anywhere in the retained project.

## Confidence levels in requirements.txt

| Package | Version stated | Confidence |
|---|---|---|
| torch, transformers, tokenizers, safetensors, accelerate | exact (`==`) | High -- read directly from the venv's `*.dist-info` directory names |
| pandas, numpy, matplotlib, seaborn, scikit-learn, datasets | bounded range | Low-medium -- the venv had a specific version, but since the venv did not run the VADER/RoBERTa/preprocessing scripts, we cannot confirm those scripts were ever run against these exact versions. A bounded range is given instead of a false pin. |
| nltk, openpyxl | minimum version only, no pin | None -- these packages were never found installed anywhere in the retained project. Required by source-code evidence only (`import nltk`, `.to_excel()`/`.xlsx` I/O). |
| scipy | minimum version only | Medium -- present in the venv (bundled with scikit-learn), used by `src/roberta/*.py` via `scipy.special.softmax`. |

## Required NLTK resource

VADER scripts call `nltk.download('vader_lexicon')` at runtime. To fetch it
ahead of time (recommended for a reproducible/offline run):

```bash
python -m nltk.downloader vader_lexicon
```

## GPU / internet requirement for the Banglish pipeline

`src/banglish/banglish_sentiment_pipeline.py` downloads `xlm-roberta-base`
from the Hugging Face Hub on first run and fine-tunes it. Per the script's
own header comment: "You need a machine with internet access to
huggingface.co (or a cached xlm-roberta-base) and ideally a GPU. This will
NOT run in a sandboxed environment with no internet access to HF." This
release package was built in an environment with no internet/GPU access, so
this script could not be executed end-to-end as part of validation (see
docs/REPRODUCIBILITY_LIMITATIONS.md and the smoke-test scope in
tests/smoke_test.py).
