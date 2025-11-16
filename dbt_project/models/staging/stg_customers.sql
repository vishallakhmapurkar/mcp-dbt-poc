{{ config(materialized='view') }}

SELECT
    customer_id AS customer_id,\n    first_name AS first_name,\n    last_name AS last_name,\n    email AS email,\n    signup_date AS signup_date
FROM {{ source('sales_data', 'customers') }}