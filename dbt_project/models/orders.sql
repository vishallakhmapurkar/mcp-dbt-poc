```sql
with monthly_revenue as (
    select
        o.customer_id,
        date_trunc('month', o.order_date) as order_month,
        sum(o.total_amount) as monthly_revenue
    from orders o
    group by o.customer_id, order_month
)

select
    mr.customer_id,
    mr.order_month,
    mr.monthly_revenue / count(distinct mr.order_month) over (partition by mr.customer_id) as avg_monthly_revenue
from monthly_revenue mr
```