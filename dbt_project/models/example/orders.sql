```sql
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
    cr.customer_id,
    cr.customer_name,
    mr.order_month,
    mr.monthly_revenue
from customers cr
left join monthly_revenue mr on cr.customer_id = mr.customer_id and mr.order_month = date_trunc('month', current_date())
```

**Explanation:**

* **Monthly Revenue Subquery:**
    * Joins the `orders` table with itself to group orders by customer and month.
    * Uses `date_trunc('month', o.order_date)` to extract the month from the `order_date` column.
    * Calculates the sum of `total_amount` for each customer-month combination.


* **Main Query:**
    * Left joins the `customers` table with the `monthly_revenue` subquery on `customer_id` and `order_month`.
    * Filters for the current month using `date_trunc('month', current_date())`.
    * Selects the `customer_name`, `order_month`, and `monthly_revenue` for each customer in the current month.