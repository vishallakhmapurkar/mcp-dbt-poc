{{ config(materialized='view') }}

SELECT
    order_id AS order_id,\n    customer_id AS customer_id,\n    order_date AS order_date,\n    total_amount AS total_amount
FROM {{ source('sales_data', 'orders') }}