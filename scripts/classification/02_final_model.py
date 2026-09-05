#!/usr/bin/env python3
"""Final XGBoost classification using the selected importance threshold."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, matthews_corrcoef
from xgboost import XGBClassifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.002)
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    X, y = data.iloc[:, :-1], data.iloc[:, -1]
    if y.dtype == object:
        y = pd.factorize(y)[0]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=1.0, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    model.fit(X_train, y_train)

    selected = np.flatnonzero(model.feature_importances_ > args.threshold)
    if len(selected) == 0:
        raise RuntimeError("No features passed the threshold.")

    final_model = XGBClassifier(
        n_estimators=100, max_depth=6,
        reg_alpha=1.0, reg_lambda=1.0,
        random_state=42, n_jobs=8
    )
    final_model.fit(X_train.iloc[:, selected], y_train)

    pred = final_model.predict(X_test.iloc[:, selected])
    prob = final_model.predict_proba(X_test.iloc[:, selected])[:, 1]
    report = classification_report(y_test, pred, output_dict=True)

    results = pd.DataFrame([{
        "Threshold": args.threshold,
        "Num_Features": len(selected),
        "Accuracy": accuracy_score(y_test, pred),
        "ROC_AUC": roc_auc_score(y_test, prob),
        "Precision": report["weighted avg"]["precision"],
        "Recall": report["weighted avg"]["recall"],
        "F1_Score": report["weighted avg"]["f1-score"],
        "MCC": matthews_corrcoef(y_test, pred),
    }])

    selected_df = pd.DataFrame({
        "Feature": X.columns[selected],
        "Importance": model.feature_importances_[selected]
    }).sort_values("Importance", ascending=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output.with_name(args.output.stem + "_metrics.csv"), index=False)
    selected_df.to_csv(args.output.with_name(args.output.stem + "_selected_features.csv"), index=False)


if __name__ == "__main__":
    main()
