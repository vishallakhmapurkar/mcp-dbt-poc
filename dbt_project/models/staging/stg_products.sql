{{ config(materialized='view') }}

create or replace view products_staging as
select
    product_id,
    product_name,
    category,
    price
from { source('dbt_vlakhmapurkar', 'products') }
{ config(materialized='view') };