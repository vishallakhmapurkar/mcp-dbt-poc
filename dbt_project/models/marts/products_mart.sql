{{ config(materialized='view') }}

"""
from dbt_dev import task

task(
   =lambda: """SELECT product_id AS product_sku FROM stg_products"""
)