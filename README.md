# V6 Robustness Algorithm
The V6 Robustness Algorithm provides tools for sensitivity analysis in a federated learning framework.
It measures how changes in a feature (e.g., age_column) affect model predictions across multiple local nodes.


# Installation
Clone the repository and install in editable mode:

git clone https://github.com/fatemehakb/v6-robustness-py.git
cd v6-robustness-py-main
pip install -e .


# Usage: Run an Example
cd v6-robustness-py
python example.py

------------------------------------------------------------------

The main algorithm is implemented in v6-robustness-py/__init__.py and provides two key functions:

# 1. local_sensitivity_analysis

This function runs on each local node (client) in a federated learning framework.

Inputs:

target_column: the label in the dataset that we want to predict using a machine learning model.

age_column: the column whose effect on predictions we want to test.

delta: the value by which to perturb the age_column.

Procedure:

1- Train a LogisticRegression model on the local training data.

2- Predict labels for the local test data.

3- Perturb the age_column in the test data by delta and predict labels again.

4- Count how many predictions changed due to the perturbation.

Outputs:

accuracy: accuracy of the model on the local test data.

n_samples: total number of test samples in the local node.

age_sensitivity: number of test samples whose prediction changed.

# 2. central_sensitivity_analysis

This function runs on the central node (server).

Procedure:

1- Receives the outputs of local_sensitivity_analysis from all local nodes.

2- Aggregates total test samples and the number of changed predictions across all nodes.

3- Calculates the percentage of prediction changes: aggregated_percentages = (aggregated_changes / total_samples) * 100


This allows the server to measure the overall sensitivity of the model predictions to changes in the age_column across the federated network.




