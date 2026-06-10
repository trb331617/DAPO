"""Extract first 10 rows from dapo-math-17k.parquet and save as a new file."""
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "dapo-math-17k.parquet",
        help="Path to the source parquet file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "dapo-math-17k-sample10.parquet",
        help="Path to write the sampled parquet file.",
    )
    parser.add_argument(
        "-n",
        "--num-rows",
        type=int,
        default=10,
        help="Number of rows to extract from the head of the dataset.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    df = pd.read_parquet(args.input)
    sample = df.head(args.num_rows)
    sample.to_parquet(args.output, index=False)

    print(f"Read {len(df)} rows from {args.input}")
    print(f"Wrote {len(sample)} rows to {args.output}")


if __name__ == "__main__":
    main()
