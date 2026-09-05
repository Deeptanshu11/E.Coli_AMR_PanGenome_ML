#!/usr/bin/env python3
"""L1 ablation for classification: reg_alpha=0 versus reg_alpha=1."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, matthews_corrcoef
from xgboost import XGBClassifier

SETTINGS = {"Without_L1": 0.0, "With_L1": 1.0}


def run(data, alpha, threshold=0.002):
    X, y = data.iloc[:, :-1], data.iloc[:, -1]
    if y.dtype == object:
        y = pd.factorize(y)[0]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    selector = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=alpha, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    selector.fit(X_train, y_train)

    selected = np.flatnonzero(selector.feature_importances_ > threshold)
    if len(selected) == 0:
        return {"Num_Features": 0, "Accuracy": np.nan, "ROC_AUC": np.nan,
                "Precision": np.nan, "Recall": np.nan, "F1_Score": np.nan, "MCC": np.nan}

    model = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=alpha, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    model.fit(X_train.iloc[:, selected], y_train)
    pred = model.predict(X_test.iloc[:, selected])
    prob = model.predict_proba(X_test.iloc[:, selected])[:, 1]
    report = classification_report(y_test, pred, output_dict=True)

    return {
        "Num_Features": len(selected),
        "Accuracy": accuracy_score(y_test, pred),
        "ROC_AUC": roc_auc_score(y_test, prob),
        "Precision": report["weighted avg"]["precision"],
        "Recall": report["weighted avg"]["recall"],
        "F1_Score": report["weighted avg"]["f1-score"],
        "MCC": matthews_corrcoef(y_test, pred),
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
                "Threshold": 0.002,
                **run(data, alpha)
            })

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
