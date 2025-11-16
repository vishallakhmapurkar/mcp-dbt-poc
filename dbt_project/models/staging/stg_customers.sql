{{ config(materialized='view') }}

SELECT
    customer_id AS customer_id,
    first_name AS first_name,
    last_name AS last_name,
    email AS email,
    signup_date AS signup_date
FROM {{ source('sales_data', 'customers') }}