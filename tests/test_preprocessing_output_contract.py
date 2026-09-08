"""Static fixture test: preprocessing output filenames must match scorer
input filenames -- synthetic/static only, no real review data involved.

This does NOT import or execute any src/ script (they need langdetect,
deep-translator, nltk, transformers/torch -- none of which are installed in
this environment, see docs/ENVIRONMENT_NOTES.md). Instead it statically
reads each script's source text and extracts the literal filename string
passed to `pd.to_csv(...)` (preprocessing) or `pd.read_csv(...)` (scoring),
then asserts the two match exactly (case-sensitive -- these are the exact
bugs fixed for this release: a stray backslash, a copy-pasted wrong name,
and two commented-out save lines that produced no file at all). See
docs/CODE_CHANGES.md, "Defects repaired", for the human-readable version
of what this test checks.

Run with: python tests/test_preprocessing_output_contract.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREPROCESSING_DIR = REPO_ROOT / "src" / "preprocessing"

# (brand, preprocessing_filename, scorer_dir, scorer_filename)
CONTRACTS = [
    ("brand_a", "brand_a_clean_roberta.py", "roberta", "brand_a_roberta.py"),
    ("brand_b",    "brand_b_clean_roberta.py",    "roberta", "brand_b_roberta.py"),
    ("brand_c",      "brand_c_clean_roberta.py",       "roberta", "brand_c_roberta.py"),
    ("brand_d",        "brand_d_clean_roberta.py",         "roberta", "brand_d_roberta.py"),
    ("brand_e",    "brand_e_clean_roberta.py",     "roberta", "brand_e_roberta.py"),
    ("brand_a", "brand_a_clean_vader.py",    "vader",   "brand_a_vader.py"),
    ("brand_b",    "brand_b_clean_vader.py",       "vader",   "brand_b_vader.py"),
    ("brand_c",      "brand_c_clean_vader.py",          "vader",   "brand_c_vader.py"),
    ("brand_d",        "brand_d_clean_vader.py",            "vader",   "brand_d_vader.py"),
    ("brand_e",    "brand_e_clean_vader.py",        "vader",   "brand_e_vader.py"),
]

# Matches df.to_csv("some_name.csv", ...) or df.to_csv('some_name.csv', ...)
# Ignores commented-out lines (a leading '#' before the call on that line).
TO_CSV_RE = re.compile(r'^[^\n#]*\.to_csv\(\s*["\']([^"\']+)["\']', re.MULTILINE)
READ_CSV_RE = re.compile(r'^[^\n#]*\.read_csv\(\s*["\']([^"\']+)["\']', re.MULTILINE)


def extract_first(pattern: re.Pattern, text: str, label: str, path: Path) -> str:
    match = pattern.search(text)
    assert match, f"no active (non-commented) {label} call found in {path}"
    return match.group(1)


def check_contract(brand: str, prep_file: str, scorer_subdir: str, scorer_file: str):
    prep_path = PREPROCESSING_DIR / prep_file
    scorer_path = REPO_ROOT / "src" / scorer_subdir / scorer_file

    assert prep_path.exists(), f"missing {prep_path}"
    assert scorer_path.exists(), f"missing {scorer_path}"

    prep_text = prep_path.read_text(encoding="utf-8")
    scorer_text = scorer_path.read_text(encoding="utf-8")

    output_name = extract_first(TO_CSV_RE, prep_text, "to_csv", prep_path)
    input_name = extract_first(READ_CSV_RE, scorer_text, "read_csv", scorer_path)

    assert output_name == input_name, (
        f"{brand}: {prep_file} writes {output_name!r} but {scorer_file} "
        f"reads {input_name!r} -- these must match exactly (case-sensitive) "
        f"for the pipeline to chain together"
    )


def main():
    failures = 0
    for brand, prep_file, scorer_subdir, scorer_file in CONTRACTS:
        label = f"{brand} / {scorer_subdir}"
        try:
            check_contract(brand, prep_file, scorer_subdir, scorer_file)
            print(f"PASS: {label}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {label}: {e}")

    if failures:
        print(f"\n{failures} contract(s) failed.")
        sys.exit(1)
    print(f"\nAll {len(CONTRACTS)} preprocessing-output/scorer-input contracts hold.")


if __name__ == "__main__":
    main()
