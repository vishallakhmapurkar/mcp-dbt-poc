```sql
model customers_mart
{
    source = {
        type = 'sql',
        sql = "SELECT * FROM { ref('stg_customers') }"
    },
    materialized = 'table',
    table = 'customers'
}
```