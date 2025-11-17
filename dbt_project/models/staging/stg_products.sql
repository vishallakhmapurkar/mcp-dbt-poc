{{ config(materialized='view') }}

Model:
{ product_id: int4, product_name: text, category: text, price: double precision }
"""