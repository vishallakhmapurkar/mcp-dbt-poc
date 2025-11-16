{{ config(materialized='view') }}

SELECT
    product_id AS product_id,\n    product_name AS product_name,\n    category AS category,\n    price AS price
FROM {{ source('sales_data', 'products') }}