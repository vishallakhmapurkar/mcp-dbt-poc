```sql
with staged_products as (
    select
        product_id,
        product_name,
        category,
        price
    from { source('dbt_vlakhmapurkar', 'products') }
)

select *
from staged_products
{ config(materialized='view') }
```