#!/usr/bin/env python3
"""Keep AMR records whose genome IDs are present in the final genome list."""

from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--genome-ids", type=Path, required=True)
    parser.add_argument("--amr-table", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.genome_ids.open() as fh:
        genome_ids = {line.strip() for line in fh if line.strip()}

    df = pd.read_csv(args.amr_table, sep="\t", dtype=str, low_memory=False)
    if "genome_id" not in df.columns:
        raise KeyError("Column 'genome_id' was not found.")

    df["genome_id"] = df["genome_id"].str.strip()
    out = df[df["genome_id"].isin(genome_ids)].copy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, sep="\t", index=False)

    print(f"AMR rows: {len(df):,}")
    print(f"Rows retained: {len(out):,}")
    print(f"Unique genomes retained: {out['genome_id'].nunique():,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
