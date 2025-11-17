{{ config(materialized='view') }}

Model: [{ name: 'stg_products' }, { columns: ['product_id', 'category_id'] }]