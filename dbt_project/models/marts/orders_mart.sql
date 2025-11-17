```sql
CREATE MATERIALIZED VIEW {{ model_name }} AS
SELECT *
FROM { ref('stg_orders') };
```