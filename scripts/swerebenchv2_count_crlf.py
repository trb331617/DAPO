"""Count rows where language == 'python' and test_patch contains '\\r\\n'.

Usage:
    python count_python_crlf.py
    python count_python_crlf.py --input swe-rebench-v2.parquet
Output:
Total rows           : 32079
language == 'python'  : 7243
test_patch has CRLF  : 198
Both conditions      : 99
"""
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "swe-rebench-v2.parquet",
        help="Path to the parquet file.",
    )
    parser.add_argument(
        "--language",
        default="python",
        help="Value to match in the 'language' column (default: python).",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    df = pd.read_parquet(args.input)
    for col in ("language", "test_patch"):
        if col not in df.columns:
            raise ValueError(
                f"Column '{col}' not found. Available: {list(df.columns)}"
            )

    total = len(df)
    lang_mask = df["language"] == args.language
    # Treat NaN/None as no match; require literal '\r\n' substring.
    crlf_mask = df["test_patch"].fillna("").astype(str).str.contains("\r\n", regex=False)
    matched = df[lang_mask & crlf_mask]

    print(f"Total rows           : {total}")
    print(f"language == {args.language!r:<10}: {lang_mask.sum()}")
    print(f"test_patch has CRLF  : {crlf_mask.sum()}")
    print(f"Both conditions      : {len(matched)}")


if __name__ == "__main__":
    main()
