#!/usr/bin/env python3
"""MIC regression feature-importance threshold sensitivity analysis."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor

THRESHOLDS = [0.000, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009]


def evaluate(data, threshold):
    X = data.drop(columns=["genome_id", "normalized_MIC"])
    y = data["normalized_MIC"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    selector = XGBRegressor(
        n_estimators=100, max_depth=6, random_state=42, n_jobs=8
    )
    selector.fit(X_train, y_train)

    selected = selector.feature_importances_ > threshold
    if not selected.any():
        return {"Selected_Features": 0, "R_squared": np.nan,
                "MSE": np.nan, "MAE": np.nan}

    model = XGBRegressor(
        n_estimators=100, max_depth=6, random_state=42, n_jobs=8
    )
    model.fit(X_train.loc[:, selected], y_train)
    pred = model.predict(X_test.loc[:, selected])

    return {
        "Selected_Features": int(selected.sum()),
        "R_squared": r2_score(y_test, pred),
        "MSE": mean_squared_error(y_test, pred),
        "MAE": mean_absolute_error(y_test, pred),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for path in sorted(args.input_dir.glob("*.csv")):
        data = pd.read_csv(path)
        for threshold in THRESHOLDS:
            rows.append({
                "Antibiotic": path.stem,
                "Threshold": threshold,
                **evaluate(data, threshold)
            })

    result = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_dir / "regression_threshold_metrics.csv", index=False)

    summary = (
        result.groupby("Threshold")
        .agg(
            Average_R_squared=("R_squared", "mean"),
            SD_R_squared=("R_squared", "std"),
            Average_MSE=("MSE", "mean"),
            SD_MSE=("MSE", "std"),
            Average_MAE=("MAE", "mean"),
            SD_MAE=("MAE", "std"),
            Average_Selected_Features=("Selected_Features", "mean"),
            SD_Selected_Features=("Selected_Features", "std"),
        )
        .reset_index()
    )

    baseline = summary.loc[summary["Threshold"] == 0.0].iloc[0]
    summary["R2_Retained_Percent"] = (
        summary["Average_R_squared"] / baseline["Average_R_squared"] * 100
    )
    summary["Feature_Reduction_Percent"] = (
        (baseline["Average_Selected_Features"] - summary["Average_Selected_Features"])
        / baseline["Average_Selected_Features"] * 100
    )

    summary.to_csv(args.output_dir / "regression_threshold_summary.csv", index=False)


if __name__ == "__main__":
    main()
