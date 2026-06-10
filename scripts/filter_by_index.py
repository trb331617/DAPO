"""Read a parquet file and print rows where extra_info.index equals a given value.

Usage:
    python filter_by_index.py --index 9a9b6eb4-a1cb-49d1-8c1e-62eaf2f74079
    python filter_by_index.py -i <value> --input dapo-math-17k-sample2.parquet
"""
import argparse
from pathlib import Path

import pandas as pd


def get_index(extra_info):
    if isinstance(extra_info, dict):
        return extra_info.get("index")
    # Fallback: structured records exposed via attribute access
    return getattr(extra_info, "index", None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "dapo-math-17k-sample2.parquet",
        help="Path to the parquet file.",
    )
    parser.add_argument(
        "-i",
        "--index",
        required=True,
        help="Value of extra_info.index to match.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    df = pd.read_parquet(args.input)
    if "extra_info" not in df.columns:
        raise ValueError(f"Column 'extra_info' not found. Available: {list(df.columns)}")

    mask = df["extra_info"].map(get_index) == args.index
    matched = df[mask]

    print(f"Matched {len(matched)} row(s) where extra_info.index == {args.index!r}")
    for idx, row in matched.iterrows():
        print(f"===== Row {idx} =====")
        for col in df.columns:
            print(f"--- {col} ---")
            print(row[col])
        print()


if __name__ == "__main__":
    main()
