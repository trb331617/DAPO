"""Deduplicate a parquet dataset by extra_info.index.

Usage:
    python dedup_by_index.py
    python dedup_by_index.py --input dapo-math-17k.parquet --output dapo-math-17k-dedup.parquet
    python dedup_by_index.py --keep last
"""
import argparse
from pathlib import Path

import pandas as pd


def get_index(extra_info):
    if isinstance(extra_info, dict):
        return extra_info.get("index")
    return getattr(extra_info, "index", None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "dapo-math-17k.parquet",
        help="Source parquet file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output parquet file. Default: <input-stem>-dedup.parquet",
    )
    parser.add_argument(
        "--keep",
        choices=["first", "last"],
        default="first",
        help="Which duplicate to keep (default: first).",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    output = args.output or args.input.with_name(f"{args.input.stem}-dedup.parquet")

    df = pd.read_parquet(args.input)
    if "extra_info" not in df.columns:
        raise ValueError(
            f"Column 'extra_info' not found. Available: {list(df.columns)}"
        )

    before = len(df)
    df["_idx_key"] = df["extra_info"].map(get_index)

    null_count = df["_idx_key"].isna().sum()
    if null_count:
        print(f"Warning: {null_count} row(s) have no extra_info.index; kept as-is.")

    deduped = df.drop_duplicates(subset="_idx_key", keep=args.keep).drop(columns="_idx_key")
    after = len(deduped)

    deduped.to_parquet(output, index=False)

    print(f"Read    : {before} rows from {args.input}")
    print(f"Removed : {before - after} duplicate(s)")
    print(f"Wrote   : {after} rows to {output}")


if __name__ == "__main__":
    main()
