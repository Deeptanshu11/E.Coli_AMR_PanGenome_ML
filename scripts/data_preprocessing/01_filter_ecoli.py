#!/usr/bin/env python3
"""Filter the BV-BRC AMR table to Escherichia coli records."""

from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", low_memory=False)
    if "genome_name" not in df.columns:
        raise KeyError("Column 'genome_name' was not found.")

    genome_name = df["genome_name"].astype(str).str.strip().str.replace('"""', '', regex=False)
    out = df[genome_name.str.contains("Escherichia coli", case=False, na=False)].copy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, sep="\t", index=False)
    print(f"Input rows: {len(df):,}")
    print(f"E. coli rows: {len(out):,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
