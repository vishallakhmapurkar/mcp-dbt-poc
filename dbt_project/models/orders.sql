```sql
with monthly_revenue as (
    select 
        o.customer_id, 
        strftime('%Y-%m', o.order_date) as order_month, 
        sum(o.total_amount) as total_revenue
    from orders o
    group by o.customer_id, order_month
)

select 
    mr.customer_id, 
    mr.order_month, 
    mr.total_revenue / count(distinct mr.order_month) as monthly_revenue
from monthly_revenue mr
group by mr.customer_id, mr.order_month
```