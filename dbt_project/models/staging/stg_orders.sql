{{ config(materialized='view') }}

with materialized='view':
    orders AS (SELECT order_id, customer_id, order_date, total_amount FROM dbt_vlaghmapurkar.orders) SELECT order_id, customer_id, order_date, total_amount FROM orders