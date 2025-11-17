{{ config(materialized='view') }}

SELECT
    order_id AS order_id,
    customer_id AS customer_id,
    order_date AS order_date,
    total_amount AS total_amount
FROM {{ source('dbt_vlakhmapurkar', 'orders') }}