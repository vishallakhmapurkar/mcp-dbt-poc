{{ config(materialized='view') }}

CREATE MATERIALIZED TABLE products AS
SELECT *
FROM { ref('stg_products') };