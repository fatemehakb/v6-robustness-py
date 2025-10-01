import pandas as pd

from vantage6.algorithm.tools.util import info
from vantage6.algorithm.client import AlgorithmClient
from vantage6.algorithm.tools.decorators import algorithm_client, data

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


@algorithm_client
def central_sensitivity_analysis(client: AlgorithmClient, target_column: str, age_column: str, delta: int):
    """
    Aggregate logistic regression sensitivity results from all nodes.
    For each perturbation delta, compute the total changes and
    the percentage relative to total samples across all nodes.
    """
    info("Collecting participating organizations")
    organizations = [org["id"] for org in client.organization.list()]

    # Send task to all organizations to run local_logreg_sensitivity
    info("Requesting local sensitivity analysis")
    task = client.task.create(
        input_={
            "method": "local_sensitivity_analysis",
            "kwargs": {"target_column": target_column, "age_column": age_column, "delta": delta}
        },
        organizations=organizations,
    )

    info("Waiting for node results")
    results = client.wait_for_results(task.get("id"))
    info("Node results received!")

    
    
    
    # Initialize aggregated counters
    aggregated_changes = 0
    total_samples = 0
    
    # Sum changes for each delta across nodes
    for node_result in results:
        total_samples += node_result["n_samples"]
        changes_count = node_result["age_sensitivity"]
        aggregated_changes += changes_count
        info(f"central-----total_samples = {total_samples:.3f}")
        info(f"central-----changes_count = {changes_count:.3f}")
        info(f"central-----aggregated_changes = {aggregated_changes:.3f}")
    

    # Compute percentages
    aggregated_percentages = (aggregated_changes / total_samples) * 100 
    info(f"central-----aggregated_percentages = {aggregated_percentages:.3f}")

    return {
        "total_samples": total_samples,
        "changes": aggregated_changes,
        "percentages": aggregated_percentages
    }









@data(1)
def local_sensitivity_analysis(df: pd.DataFrame, target_column: str, age_column: str, delta: int):
    """
    Train a Logistic Regression model on local node data and test sensitivity
    of predictions to perturbations in the Age column.
    """
    info("Starting Logistic Regression training on local data")

    # Features and labels
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    info(f"Finished training. Local accuracy={accuracy:.3f}")
    
    info(f"baseline_preds: {y_pred}")

    # ---- Perturb Age column ----
    baseline_preds = model.predict(X_test)  # original predictions
    #perturbations = range(-5, 6)  # [-5, -4, ..., 5]
    
    n_test_samples=int(len(baseline_preds))
    info(f"n_test_samples={n_test_samples:.3f}")
    
    
    info(f"local__delta: {delta}")

    #delta=-10
    X_perturbed = X_test.copy()

    X_perturbed[age_column] = X_perturbed[age_column] + delta
    perturbed_preds = model.predict(X_perturbed)
    info(f"perturbed_preds: {perturbed_preds}")
    # count how many predictions changed
    n_changed = (perturbed_preds != baseline_preds).sum()
    changes= int(n_changed)
    info(f"local -----changes = {changes}")



    return {
        "accuracy": accuracy,
        "n_samples": n_test_samples,
        "age_sensitivity": changes
    }
