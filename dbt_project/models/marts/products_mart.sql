{{ config(materialized='view') }}

"""
with open(os.devnullpath("example_project/dbt_models/products.sql"), "w") as f:
    = f.read()
assert dbt.run_sql(f"CREATE OR REPLACE MODEL products AS {high}") == ""