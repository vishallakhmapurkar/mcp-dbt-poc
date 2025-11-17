```sql
```sql
create or replace view dbt_vlakhmapurkar.orders_staging AS
select
    order_id,
    customer_id,
    order_date,
    total_amount
from { source('dbt_vlakhmapurkar', 'orders') }
{ config(materialized='view') }
```

**Explanation:**

* The model is named `dbt_vlakhmapurkar.orders_staging`.
* The `create or replace` statement ensures that the view is created or refreshed if changes are detected in the underlying table.
* The `select` statement retrieves the `order_id`, `customer_id`, `order_date`, and `total_amount` columns from the `orders` source table.
* The `{ config(materialized='view') }` clause indicates that this is a materialized view, which means that the results of the query are stored in a table for faster performance.
* The `{ source('dbt_vlakhmapurkar', 'orders') }` clause specifies the source table, which is `orders` in the `dbt_vlakhmapurkar` schema.