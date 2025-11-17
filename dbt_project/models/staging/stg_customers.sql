{{ config(materialized='view') }}

"""
assert dbutils.get_sql(models.sql_model("customers", "dbt_vlakhmapurkar")) == """SELECT customer_id AS column_0, first_name AS column_1, last_name AS column_2, email AS column_3, signup_date AS column_4 FROM customers"""

"""
Assert that dbt does not raise an exception when run against an invalid configuration.
"""
with_config = """{
    "materialized": "view"
}"""
assert dbutils.validate_sql(models.sql_model("customers", "dbt_vlaghmapurkar", with_config)) is None