{{ config(materialized='view') }}

FROM ref('stg_orders') SELECT order_id, customer_id, order_date, order_status, product_sku, order_notes, order_currency, order_total, created_at, last_updated_at