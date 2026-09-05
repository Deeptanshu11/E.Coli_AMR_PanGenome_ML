#!/usr/bin/env python3
"""Calculate the intersection features shared between regression and classification models.

Input files should contain a column named 'Feature'. One file per model/antibiotic.
"""

from pathlib import Path
import argparse
import pandas as pd


def read_features(path):
    df = pd.read_csv(path)
    if "Feature" not in df.columns:
        raise KeyError(f"{path}: expected a 'Feature' column.")
    return set(df["Feature"].astype(str))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--regression-dir", type=Path, required=True)
    parser.add_argument("--classification-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for reg in sorted(args.regression_dir.glob("*.csv")):
        antibiotic = reg.stem.split("_")[0]
        matches = sorted(args.classification_dir.glob(f"{antibiotic}*.csv"))
        if not matches:
            continue

        reg_set = read_features(reg)
        cls_set = read_features(matches[0])
        inter = reg_set & cls_set
        union = reg_set | cls_set

        rows.append({
            "Antibiotic": antibiotic,
            "Regression_Features": len(reg_set),
            "Classification_Features": len(cls_set),
            "Intersection": len(inter),
            "Union": len(union),
            "Jaccard": len(inter) / len(union) if union else float("nan")
        })

    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
