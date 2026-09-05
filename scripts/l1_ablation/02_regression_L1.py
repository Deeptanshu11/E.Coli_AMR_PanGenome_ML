#!/usr/bin/env python3
"""L1 ablation for MIC regression: reg_alpha=0 versus reg_alpha=1."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr
from xgboost import XGBRegressor

SETTINGS = {"Without_L1": 0.0, "With_L1": 1.0}


def run(data, alpha, threshold=0.005):
    X = data.drop(columns=["genome_id", "normalized_MIC"])
    y = data["normalized_MIC"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    selector = XGBRegressor(
        n_estimators=100, max_depth=6,
        reg_alpha=alpha, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    selector.fit(X_train, y_train)

    importance = selector.feature_importances_
    selected = importance > threshold

    if not selected.any():
        return {"Number_of_Features": 0, "MSE": np.nan, "MAE": np.nan,
                "R_squared": np.nan, "Pearson_Correlation": np.nan,
                "Pearson_P_value": np.nan}

    model = XGBRegressor(
        n_estimators=100, max_depth=6,
        reg_alpha=alpha, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    model.fit(X_train.loc[:, selected], y_train)
    pred = model.predict(X_test.loc[:, selected])
    pearson, p_value = pearsonr(y_test, pred)

    return {
        "Number_of_Features": int(selected.sum()),
        "MSE": mean_squared_error(y_test, pred),
        "MAE": mean_absolute_error(y_test, pred),
        "R_squared": r2_score(y_test, pred),
        "Pearson_Correlation": pearson,
        "Pearson_P_value": p_value
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for path in sorted(args.input_dir.glob("*.csv")):
        data = pd.read_csv(path)
        for condition, alpha in SETTINGS.items():
            rows.append({
                "Antibiotic": path.stem,
                "Regularization": condition,
                "reg_alpha": alpha,
                "reg_lambda": 1.0,
                "Threshold": 0.005,
                **run(data, alpha)
            })

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
