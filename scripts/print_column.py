"""Read a parquet file and print specified columns.

Usage:
    python print_columns.py --columns prompt ability
    python print_columns.py -c prompt -n 3
    python print_columns.py --list-columns
"""
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "dapo-math-17k-sample10.parquet",
        help="Path to the parquet file.",
    )
    parser.add_argument(
        "-c",
        "--columns",
        nargs="+",
        help="Column names to print. If omitted, all columns are printed.",
    )
    parser.add_argument(
        "-n",
        "--num-rows",
        type=int,
        default=None,
        help="Limit to first N rows. Default: all.",
    )
    parser.add_argument(
        "--list-columns",
        action="store_true",
        help="Only list available column names and exit.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    df = pd.read_parquet(args.input)

    if args.list_columns:
        print("Available columns:")
        for col in df.columns:
            print(f"  - {col}")
        return

    if args.columns:
        missing = [c for c in args.columns if c not in df.columns]
        if missing:
            raise ValueError(
                f"Column(s) not found: {missing}. Available: {list(df.columns)}"
            )
        df = df[args.columns]

    if args.num_rows is not None:
        df = df.head(args.num_rows)

    for idx, row in df.iterrows():
        print(f"===== Row {idx} =====")
        for col in df.columns:
            print(f"--- {col} ---")
            print(row[col])
        print()


if __name__ == "__main__":
    main()
