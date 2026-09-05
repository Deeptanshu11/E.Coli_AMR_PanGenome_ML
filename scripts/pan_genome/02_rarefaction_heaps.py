#!/usr/bin/env python3
"""Generate pan/core/accessory rarefaction curves and fit Heaps' law."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def heaps_law(n, k, beta):
    return k * (n ** beta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-table", type=Path, required=True)
    parser.add_argument("--output-figure", type=Path, required=True)
    parser.add_argument("--core-threshold", type=float, default=0.99)
    parser.add_argument("--iterations", type=int, default=10)
    args = parser.parse_args()

    df = pd.read_hdf(args.input, key="pan_genome_table")

    records = []
    rng = np.random.default_rng(42)

    for _ in range(args.iterations):
        order = rng.permutation(len(df))
        shuffled = df.iloc[order]

        for n in range(1, len(shuffled) + 1):
            current = shuffled.iloc[:n]
            sums = current.sum(axis=0)
            pan = (sums >= 1).sum()
            core = (sums >= args.core_threshold * n).sum()
            accessory = ((sums > 0) & (sums < args.core_threshold * n)).sum()
            records.append((n, pan, core, accessory))

    result = (
        pd.DataFrame(records, columns=["Genome", "Pan", "Core", "Accessory"])
        .groupby("Genome", as_index=False)
        .mean()
    )

    genomes = result["Genome"].to_numpy()
    pan = result["Pan"].to_numpy()

    popt, _ = curve_fit(heaps_law, genomes, pan, p0=[1, 0.5], maxfev=10000)
    k, beta = popt
    fit = heaps_law(genomes, k, beta)

    args.output_table.parent.mkdir(parents=True, exist_ok=True)
    args.output_figure.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_table, index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(genomes, pan, label="Pan genes")
    plt.plot(genomes, result["Core"], label="Core genes")
    plt.plot(genomes, result["Accessory"], label="Accessory genes")
    plt.plot(genomes, fit, "--", label=f"Heaps' law fit (β={beta:.2f})")
    plt.xlabel("Number of genomes")
    plt.ylabel("Gene count")
    plt.title("E. coli pan-genome rarefaction")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_figure, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Heaps' law: k={k:.4f}, beta={beta:.4f}")
    print(f"Saved table: {args.output_table}")
    print(f"Saved figure: {args.output_figure}")


if __name__ == "__main__":
    main()
