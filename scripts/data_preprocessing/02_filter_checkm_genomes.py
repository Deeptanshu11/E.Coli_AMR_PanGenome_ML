#!/usr/bin/env python3
"""Select E. coli genome IDs passing CheckM quality thresholds."""

from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--genome-summary", type=Path, required=True)
    parser.add_argument("--ecoli-ids", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-completeness", type=float, default=95.0)
    parser.add_argument("--max-contamination", type=float, default=5.0)
    args = parser.parse_args()

    summary = pd.read_csv(args.genome_summary, sep="\t", low_memory=False)
    required = {"genome_id", "checkm_completeness", "checkm_contamination"}
    missing = required - set(summary.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    ids = pd.read_csv(args.ecoli_ids, header=None, names=["genome_id"], dtype=str)
    qualified = summary[
        (summary["checkm_completeness"] > args.min_completeness)
        & (summary["checkm_contamination"] < args.max_contamination)
    ]

    out = ids[ids["genome_id"].isin(qualified["genome_id"].astype(str))]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False, header=False)

    print(f"Qualified genomes: {len(out):,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
