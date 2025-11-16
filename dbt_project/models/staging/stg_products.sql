{{ config(materialized='view') }}

SELECT
    product_id AS product_id,
    product_name AS product_name,
    category AS category,
    price AS price
FROM {{ source('sales_data', 'products') }}