{{ config(materialized='view') }}

SELECT
    customer_id, first_name, last_name, email, signup_date
FROM {{ source('dbt_vlakhmapurkar', 'customers') }}
