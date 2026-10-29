# Technical Report: Iris Flower Classification Using AI

## 1. Problem statement

The objective is to build a supervised classification model that predicts the species of an Iris flower from its sepal and petal measurements. This project demonstrates an end-to-end machine-learning workflow suitable for an entry-level AI engineering or data-science portfolio.

## 2. Dataset understanding

The Iris benchmark contains 150 records, four numerical input features, and three balanced target classes: Setosa, Versicolor, and Virginica. The pipeline checks for missing values, records descriptive statistics, and exports a machine-readable profile.

## 3. Data preparation

The data is shuffled and split into 80% training and 20% testing subsets using stratification and a fixed random seed of 42. Standardization is fitted only as part of the training pipeline, preventing preprocessing leakage into the test evaluation.

## 4. Model selection

The selected algorithm is K-Nearest Neighbors (KNN), which classifies a new observation according to the majority class among its nearest training examples. Because KNN is distance-based, feature scaling is essential. The implementation explores odd values of `k` from 1 to 15 and trains the final requested configuration with `k=5`.

## 5. Evaluation approach

The final model is evaluated on the untouched test partition using accuracy, weighted precision, weighted recall, weighted F1 score, and a confusion matrix. The confusion matrix helps identify which species are confused with one another, while the class-level report provides a more complete view than accuracy alone.

## 6. Results

The reproducible pipeline was executed with `k=5`, `random_state=42`, and an 80/20 stratified split. The generated values are also stored in `artifacts/metrics.json`.

| Metric | Result |
|---|---:|
| Accuracy | 93.33% |
| Weighted precision | 94.44% |
| Weighted recall | 93.33% |
| Weighted F1 | 93.27% |

The model correctly classified 28 of 30 test samples. Setosa was classified perfectly; the remaining errors were between Versicolor and Virginica, which is consistent with their greater feature overlap in the Iris dataset.

The confusion matrix is available at `artifacts/confusion_matrix.png`, the KNN tuning plot at `artifacts/knn_tuning.png`, and the prediction visualization at `artifacts/prediction_scatter.png`.

## 7. Limitations and responsible use

The Iris dataset is small, clean, and balanced, so its results should not be interpreted as evidence that the model is ready for a high-risk real-world deployment. A production workflow would require cross-validation, larger representative data, monitoring, explainability, security controls, and domain-specific validation.

## 8. Conclusion

The completed pipeline meets the project requirements: dataset loading and understanding, train/test splitting, a simple classification algorithm, preprocessing, model training, prediction, and multi-metric evaluation. It also creates reusable model and reporting artifacts that can be extended into an API or deployment project.
