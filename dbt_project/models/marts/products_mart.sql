```sql
model products_mart
{
    select *
    from { ref('stg_products') }
}
```