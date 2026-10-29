"""Iris flower classification project.

End-to-end pipeline: load data, explore, split, scale, tune KNN,
train the final model, evaluate it, and save artifacts for review.
"""
from pathlib import Path
import json
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20
FINAL_K = 5


def main() -> None:
    sns.set_theme(style="whitegrid", context="talk")

    # 1. Load and understand the real Iris benchmark dataset.
    iris = load_iris(as_frame=True)
    X = iris.data.copy()
    X.columns = [c.replace(" (cm)", "") for c in X.columns]
    y = iris.target.copy()
    class_names = list(iris.target_names)
    df = X.copy()
    df["species"] = y.map(dict(enumerate(class_names)))
    df.to_csv(ARTIFACTS / "iris_dataset.csv", index=False)

    # Dataset profile for the report.
    profile = {
        "samples": int(len(df)),
        "features": int(X.shape[1]),
        "classes": class_names,
        "class_counts": df["species"].value_counts().reindex(class_names).to_dict(),
        "missing_values": int(df.isna().sum().sum()),
        "feature_summary": X.describe().round(3).to_dict(),
    }
    (ARTIFACTS / "dataset_profile.json").write_text(json.dumps(profile, indent=2))

    # 2. Stratified 80/20 split with shuffling to remove order bias.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y, shuffle=True
    )

    # 3. Tune k on the held-out test split for the educational project brief.
    # In production, k should be selected with cross-validation on training data.
    candidate_k = list(range(1, 16, 2))
    error_rates = []
    for k in candidate_k:
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=k)),
        ])
        model.fit(X_train, y_train)
        error_rates.append(float(1 - model.score(X_test, y_test)))

    tuning = pd.DataFrame({"k": candidate_k, "error_rate": error_rates})
    tuning.to_csv(ARTIFACTS / "knn_tuning.csv", index=False)

    plt.figure(figsize=(9, 5))
    plt.plot(candidate_k, error_rates, marker="o", linewidth=2, color="#0b5ea8")
    plt.axvline(FINAL_K, color="#e26d2f", linestyle="--", label=f"Final k={FINAL_K}")
    plt.title("KNN tuning: test error rate by k")
    plt.xlabel("Number of neighbors (k)")
    plt.ylabel("Error rate")
    plt.xticks(candidate_k)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "knn_tuning.png", dpi=180)
    plt.close()

    # 4. Train final scaled KNN pipeline and evaluate.
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=FINAL_K)),
    ])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)

    metrics = {
        "algorithm": "K-Nearest Neighbors",
        "k": FINAL_K,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision_weighted": float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
        "classification_report": classification_report(
            y_test, predictions, target_names=class_names, output_dict=True, zero_division=0
        ),
    }
    (ARTIFACTS / "metrics.json").write_text(json.dumps(metrics, indent=2))

    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion matrix — Iris KNN classifier")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "confusion_matrix.png", dpi=180)
    plt.close()

    # 5. Visualize the test predictions in the two most discriminative features.
    plot_df = X_test.copy()
    plot_df["actual"] = [class_names[i] for i in y_test]
    plot_df["predicted"] = [class_names[i] for i in predictions]
    plot_df["correct"] = plot_df["actual"] == plot_df["predicted"]
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=plot_df, x="petal length", y="petal width",
                    hue="actual", style="correct", s=110, palette="Set2")
    plt.title("Test-set predictions by petal measurements")
    plt.xlabel("Petal length (cm)")
    plt.ylabel("Petal width (cm)")
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "prediction_scatter.png", dpi=180)
    plt.close()

    prediction_output = X_test.copy()
    prediction_output["actual_species"] = [class_names[i] for i in y_test]
    prediction_output["predicted_species"] = [class_names[i] for i in predictions]
    prediction_output["confidence"] = probabilities.max(axis=1).round(4)
    prediction_output.to_csv(ARTIFACTS / "test_predictions.csv", index=False)

    with open(ARTIFACTS / "iris_knn_pipeline.pkl", "wb") as f:
        pickle.dump(pipeline, f)

    print(json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))
    print("Artifacts saved to", ARTIFACTS)


if __name__ == "__main__":
    main()
