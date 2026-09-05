#!/usr/bin/env python3
"""Classification feature-importance threshold sensitivity analysis."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, matthews_corrcoef
from xgboost import XGBClassifier


THRESHOLDS = [0.000, 0.001, 0.002, 0.003, 0.004, 0.005]


def evaluate(dataset, threshold):
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]
    if y.dtype == object:
        y = pd.factorize(y)[0]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    selector = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=1.0, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    selector.fit(X_train, y_train)

    importance = selector.feature_importances_
    selected = np.flatnonzero(importance > threshold)

    if len(selected) == 0:
        return {"Selected_Features": 0, "Accuracy": np.nan, "AUROC": np.nan,
                "Precision": np.nan, "Recall": np.nan, "F1_score": np.nan, "MCC": np.nan}

    model = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=1.0, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    model.fit(X_train.iloc[:, selected], y_train)

    pred = model.predict(X_test.iloc[:, selected])
    prob = model.predict_proba(X_test.iloc[:, selected])[:, 1]
    report = classification_report(y_test, pred, output_dict=True)

    return {
        "Selected_Features": len(selected),
        "Accuracy": accuracy_score(y_test, pred),
        "AUROC": roc_auc_score(y_test, prob),
        "Precision": report["weighted avg"]["precision"],
        "Recall": report["weighted avg"]["recall"],
        "F1_score": report["weighted avg"]["f1-score"],
        "MCC": matthews_corrcoef(y_test, pred),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True,
                        help="Directory containing one CSV per antibiotic.")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    datasets = sorted(args.input_dir.glob("*.csv"))
    if not datasets:
        raise FileNotFoundError(f"No CSV files found in {args.input_dir}")

    rows = []
    for path in datasets:
        antibiotic = path.stem
        data = pd.read_csv(path)
        for threshold in THRESHOLDS:
            metrics = evaluate(data, threshold)
            rows.append({"Antibiotic": antibiotic, "Threshold": threshold, **metrics})

    result = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_dir / "classification_threshold_metrics.csv", index=False)

    summary = (
        result.groupby("Threshold")
        .agg(["mean", "std"])
        .reset_index()
    )
    summary.to_csv(args.output_dir / "classification_threshold_summary.csv", index=False)

    print(f"Saved: {args.output_dir}")


if __name__ == "__main__":
    main()
