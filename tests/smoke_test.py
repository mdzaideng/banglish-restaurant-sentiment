"""Smoke test -- synthetic data only.

Does NOT import or execute anything under src/ (those scripts download
models from the Hugging Face Hub and/or an NLTK lexicon at runtime, which
this environment cannot do -- see docs/ENVIRONMENT_NOTES.md). Instead this
checks the one thing that can be verified offline: that the fabricated
schema-demo file matches the documented schema and that the documented
label-mapping rule is applied correctly, using no real review data.

Run with: python tests/smoke_test.py
"""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_CSV = REPO_ROOT / "data" / "example" / "synthetic_schema_example.csv"

EXPECTED_COLUMNS = {"name", "stars", "reviews"}


def stars_to_label(stars: int) -> str:
    """Mirrors the mapping documented in data/README.md and confirmed in
    src/banglish/banglish_sentiment_pipeline.py's stars_to_label()."""
    if stars <= 2:
        return "Negative"
    if stars == 3:
        return "Neutral"
    return "Positive"


def test_example_file_exists():
    assert EXAMPLE_CSV.exists(), f"missing {EXAMPLE_CSV}"


def test_example_schema_matches_documentation():
    with open(EXAMPLE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert set(reader.fieldnames) == EXPECTED_COLUMNS, (
        f"columns {reader.fieldnames} do not match documented schema {EXPECTED_COLUMNS}"
    )
    assert len(rows) > 0, "example file has no rows"
    for row in rows:
        assert 1 <= int(row["stars"]) <= 5, f"stars out of range: {row['stars']}"
        assert row["reviews"].strip() != "", "empty review text"


def test_label_mapping_matches_documented_rule():
    cases = {1: "Negative", 2: "Negative", 3: "Neutral", 4: "Positive", 5: "Positive"}
    for stars, expected in cases.items():
        got = stars_to_label(stars)
        assert got == expected, f"stars={stars}: expected {expected}, got {got}"


def test_example_data_is_not_mistaken_for_real_reviews():
    with open(EXAMPLE_CSV, encoding="utf-8") as f:
        content = f.read()
    assert "Example Reviewer" in content, (
        "synthetic example file no longer clearly labeled as fabricated"
    )


def main():
    tests = [
        test_example_file_exists,
        test_example_schema_matches_documentation,
        test_label_mapping_matches_documented_rule,
        test_example_data_is_not_mistaken_for_real_reviews,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
    if failures:
        print(f"\n{failures} test(s) failed.")
        sys.exit(1)
    print("\nAll smoke tests passed (synthetic data only; no model code was executed).")


if __name__ == "__main__":
    main()
