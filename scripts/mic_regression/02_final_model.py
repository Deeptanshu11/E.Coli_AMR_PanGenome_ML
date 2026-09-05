#!/usr/bin/env python3
"""Final XGBoost MIC regression using the selected importance threshold."""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr
from xgboost import XGBRegressor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.005)
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    X = data.drop(columns=["genome_id", "normalized_MIC"])
    y = data["normalized_MIC"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    selector = XGBRegressor(
        n_estimators=100, max_depth=6,
        random_state=42, n_jobs=8
    )
    selector.fit(X_train, y_train)

    importance = selector.feature_importances_
    selected = importance > args.threshold
    if not selected.any():
        raise RuntimeError("No features passed the threshold.")

    final_model = XGBRegressor(
        n_estimators=100, max_depth=6,
        random_state=42, n_jobs=8
    )
    final_model.fit(X_train.loc[:, selected], y_train)
    pred = final_model.predict(X_test.loc[:, selected])

    pearson, p_value = pearsonr(y_test, pred)

    results = pd.DataFrame([{
        "Threshold": args.threshold,
        "Num_Features": int(selected.sum()),
        "MSE": mean_squared_error(y_test, pred),
        "MAE": mean_absolute_error(y_test, pred),
        "R_squared": r2_score(y_test, pred),
        "Pearson_Correlation": pearson,
        "P_value": p_value
    }])

    features = pd.DataFrame({
        "Feature": X.columns[selected],
        "Importance": importance[selected]
    }).sort_values("Importance", ascending=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output.with_name(args.output.stem + "_metrics.csv"), index=False)
    features.to_csv(args.output.with_name(args.output.stem + "_selected_features.csv"), index=False)


if __name__ == "__main__":
    main()
