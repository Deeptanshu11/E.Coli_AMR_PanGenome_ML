#!/usr/bin/env python3
"""Create the resistant/susceptible phenotype subset."""

from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", low_memory=False)
    if "resistant_phenotype" not in df.columns:
        raise KeyError("Column 'resistant_phenotype' was not found.")

    df["resistant_phenotype"] = (
        df["resistant_phenotype"].astype(str).str.strip().str.title()
    )
    out = df[df["resistant_phenotype"].isin(["Resistant", "Susceptible"])].copy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, sep="\t", index=False)
    print(f"R/S rows retained: {len(out):,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
