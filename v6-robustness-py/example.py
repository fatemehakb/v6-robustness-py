import pandas as pd
from vantage6.algorithm.tools.mock_client import MockAlgorithmClient

# ---------------------------------------------------------------------
# Initialize Mock Client
# ---------------------------------------------------------------------
# Two organizations, each with a CSV file (simulating their local datasets)
client = MockAlgorithmClient(
    datasets=[
        [   # Organization 1
            {
                "database": "local/data.csv",
                "db_type": "csv",
            },
        ],
        [   # Organization 2
            {
                "database": "local/data.csv",
                "db_type": "csv",
            },
        ],
    ],
    module="v6-robustness-py"   # <-- must match your algorithm package name
)

# ---------------------------------------------------------------------
# Inspect available organizations
# ---------------------------------------------------------------------
organizations = client.organization.list()
org_ids = [organization["id"] for organization in organizations]

print("Organizations in mock client:", org_ids)

# ---------------------------------------------------------------------
# Test PARTIAL method directly
# ---------------------------------------------------------------------
# This will execute partial_average() on each organization

"""""
partial_task = client.task.create(
    input_={
        "method": "local_sensitivity_analysis",   # function name in __init__.py
        "kwargs": {
            "target_column": "survival",
            "age_column": "age",      # must match column in your CSV
            "delta": -10
        }
    },
    organizations=org_ids              # send to all orgs
)

partial_results = client.result.get(partial_task.get("id"))
print("Partial results:", partial_results)

"""

# ---------------------------------------------------------------------
# Test CENTRAL method
# ---------------------------------------------------------------------
# This executes central_average(), which will trigger partial_average
# on all organizations and then combine their results.
central_task = client.task.create(
    input_={
        "master": 1,                   # required for central function
        "method": "central_sensitivity_analysis",   # function name in __init__.py
        "kwargs": {
            "target_column": "survival",
            "age_column": "age",      # must match column in your CSV
            "delta": -15
        }
    },
    organizations=[org_ids[0]]         # central only needs one org to coordinate
)

central_results = client.result.from_task(central_task.get("id"))
print("Central results:", central_results)

