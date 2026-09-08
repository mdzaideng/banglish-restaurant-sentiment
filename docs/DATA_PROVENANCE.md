# Data provenance

## Original data flow (as found in the source project)

```
Google Maps (third-party platform, scraped)
        |
        v
Google map reviews (raw)/<brand>_google_map_reviews.csv   [title, url, stars, name, reviewUrl, text]
        |
        v
Clean data/<brand>/*_translated.py, *_bangla.py            (preprocessing; splits English vs Banglish rows)
        |
        +--> *_cleaned_ROBERTA.csv / *_cleaned_VADER  [name, stars, reviews]  -- English pipeline input
        +--> *_bangla_reviews.csv                                             -- Banglish candidate rows
        |
        v
Banglish Analysis/banglish_dataset_final.csv  [name, stars, review]  (975 rows, all brands merged)
```

A second, larger and apparently independent English compilation also exists
at `Final Outputs & Analysis/Raw data/english_raw_reviews.xlsx` (and its
merged/labeled counterpart `raw_data_lebeled.xlsx`), with per-brand sheets
of 6,369-8,334 rows each. Its relationship to the smaller
`Google map reviews (raw)` corpus used by the included scripts is not
established from the retained files -- see
docs/REPRODUCIBILITY_LIMITATIONS.md, item 10.

## Why none of this is included as row-level data in this release

Every file in the chain above that was inspected (headers plus a local,
non-printed sample) carries a `name` column populated with what appear to be
real Google Maps reviewer display names, paired with unredacted review
`text`/`reviews`. The raw file additionally carries a `reviewUrl` column,
which is a per-review URL potentially linkable to an individual reviewer's
profile. None of this was copied into the public package. See
`data/README.md` for the full classification and `data/LICENSE_DATA.md` for
the licensing statement on this excluded data.

## What *is* included

Nothing from the data chain above is included as a shipped artifact. This
release ships **no** row-level review data and **no** result figures or
tables at all (see `results/README.md`, "Why nothing here is released") --
only the code itself. RELEASE_MANIFEST.csv records, for every excluded
file, the reasoning behind its exclusion.
