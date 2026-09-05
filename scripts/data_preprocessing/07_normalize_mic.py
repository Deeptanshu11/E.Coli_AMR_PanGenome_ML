#!/usr/bin/env python3
"""Normalize MIC measurements using the study's one-dilution handling rules."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd


def normalize_mic(row):
    value = row["measurement_value"]
    sign = row["measurement_sign"]

    if pd.isna(sign):
        sign = "=="
    else:
        sign = str(sign).strip()

    try:
        value = float(value)
    except (TypeError, ValueError):
        return np.nan

    if value <= 0:
        return np.nan

    if sign == ">":
        return np.log2(value) + 1
    if sign == "<":
        return np.log2(value) - 1
    if sign in {"=", "==", "<=", ">="}:
        return np.log2(value)

    return np.nan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", engine="python")
    required = {"measurement_value", "measurement_sign"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    df["normalized_MIC"] = df.apply(normalize_mic, axis=1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, sep="\t", index=False)

    print(f"Rows: {len(df):,}")
    print(f"Valid normalized MIC values: {df['normalized_MIC'].notna().sum():,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
