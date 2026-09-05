#!/usr/bin/env python3
"""Create the E. coli MIC subset used for quantitative MIC processing."""

from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", low_memory=False)
    name = df["genome_name"].astype(str).str.strip().str.replace('"""', '', regex=False)

    out = df[
        (df["laboratory_typing_method"].astype(str).str.strip() == "MIC")
        & name.str.contains("Escherichia", case=False, na=False)
    ].copy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, sep="\t", index=False)
    print(f"MIC rows retained: {len(out):,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
