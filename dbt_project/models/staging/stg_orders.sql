{{ config(materialized='view') }}

from dbt import task, macros as m
with m.config(materialized='view'):

SELECT order_id, customer_id, order_date, total_amount FROM dbt_vlakhmapurkar.orders