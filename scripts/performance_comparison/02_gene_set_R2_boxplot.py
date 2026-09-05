#!/usr/bin/env python3
"""Compare R-squared distributions across the four gene-set strategies."""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    expected = ["Antibiotic", "All genes", "Known AMR genes",
                "XGBoost-selected genes", "Common Intersection genes"]
    if len(df.columns) >= len(expected):
        df.columns = expected

    groups = expected[1:]
    plt.figure(figsize=(7.8, 6.2))
    plt.boxplot([df[c].dropna().values for c in groups], widths=0.5, showfliers=True)
    plt.xticks(range(1, len(groups)+1), groups, rotation=25)
    plt.ylabel("R-squared")
    plt.ylim(0.00, 1.00)
    plt.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
