{{ config(materialized='view') }}

create or replace view dbt_vlakhmapurkar.orders_staging as
select
  order_id,
  customer_id,
  order_date,
  total_amount
from { source('dbt_vlakhmapurkar', 'orders') }