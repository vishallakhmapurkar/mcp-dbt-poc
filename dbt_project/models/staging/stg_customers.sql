```sql
```sql
create or replace view customers_staging as
select
    customer_id,
    first_name,
    last_name,
    email,
    signup_date
from { source('dbt_vlakhmapurkar', 'customers') }
{ config(materialized='view') };
```

**Explanation:**

* `create or replace view customers_staging as`: Creates or replaces the view `customers_staging` with the following select statement.
* `select customer_id, first_name, last_name, email, signup_date`: Selects the four specified columns from the `customers` table.
* `{ source('dbt_vlakhmapurkar', 'customers') }`: Specifies the source table as the `customers` table from the `dbt_vlakhmapurkar` schema.
* `{ config(materialized='view') }`: Indicates that the view should be materialized as a view in the database.