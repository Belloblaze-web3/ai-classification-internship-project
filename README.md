# Iris Flower Classification Using AI

**Role:** AI Engineer / Data Scientist / Machine Learning Professional  
**Project:** DecodeLabs Artificial Intelligence Project 2 — Data Classification Using AI

## Executive summary

This project implements a reproducible supervised-learning pipeline that classifies Iris flowers into **Setosa, Versicolor, or Virginica** from four measured features. The solution follows the requested professional workflow: data loading and profiling, stratified train/test splitting, feature scaling, K-Nearest Neighbors (KNN) modeling, hyperparameter exploration, and evaluation with accuracy, precision, recall, F1 score, and a confusion matrix.

## Business and technical objective

Given measurements of an Iris flower's sepal and petal dimensions, predict its species accurately enough to demonstrate a complete, auditable machine-learning workflow. The project emphasizes reliable preprocessing and interpretable evaluation rather than only reporting a single accuracy number.

## Dataset

The project uses scikit-learn's canonical **Iris dataset** (150 observations, 4 numerical features, 3 balanced classes). The dataset is loaded programmatically, profiled, and exported to `artifacts/iris_dataset.csv` when the pipeline runs.

## Methodology

1. Load and inspect the dataset, including dimensions, class balance, and missing values.
2. Shuffle and stratify the data into 80% training and 20% testing partitions.
3. Standardize the four numerical features with `StandardScaler`.
4. Compare odd K values from 1 through 15 using test error rates.
5. Train the final `KNeighborsClassifier` with `k=5` as specified by the project brief.
6. Evaluate the predictions with accuracy, weighted precision, weighted recall, weighted F1, and a confusion matrix.
7. Save the trained preprocessing/model pipeline and reviewable visual artifacts.

> For a production system, hyperparameter selection should use cross-validation within the training set rather than tuning directly on the test set. The educational implementation keeps the brief's requested tuning demonstration visible and documents this trade-off.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/train_model.py
```

## Generated deliverables

- `artifacts/metrics.json` — evaluation metrics and per-class report
- `artifacts/confusion_matrix.png` — class-by-class error analysis
- `artifacts/knn_tuning.png` — K tuning/error-rate plot
- `artifacts/prediction_scatter.png` — test predictions by petal measurements
- `artifacts/test_predictions.csv` — row-level predictions and confidence
- `artifacts/iris_knn_pipeline.pkl` — serialized scaler + KNN pipeline
- `artifacts/dataset_profile.json` — dataset summary
- `REPORT.md` — submission-ready technical report
- `create_presentation.py` — Python script that generates the internship slide deck
- `Iris_AI_Classification_Internship_Submission.pptx` — editable 8-slide presentation
- `artifacts/presentation_preview/Iris_AI_Classification_Internship_Submission.pdf` — PDF preview/export

## Generate the presentation

```bash
python create_presentation.py
```

## Professional extensions

For a production-grade next iteration, I would add cross-validation, experiment tracking, model versioning, schema validation, drift monitoring, a REST prediction API, and automated unit/data-quality tests.
