{{ config(materialized='view') }}

with openconfig(materialized="table") as f:
    = SELECT stg_orders.order_id, stg_orders.customer_email FROM ref('stg_orders') AS stg_orders
print(high.to_postgres_sql())