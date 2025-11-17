{{ config(materialized='view') }}

Model:
SELECT product_id, product_name, category, price FROM products;