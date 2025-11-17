{{ config(materialized='view') }}

- Generate a SQLAl model that returns a view called orders: SELECT order_id, customer_id, order_date, total_amount FROM orders.
Model should not have any trailing or leading whitespace.