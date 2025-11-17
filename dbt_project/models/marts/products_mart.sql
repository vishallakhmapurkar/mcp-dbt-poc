{{ config(materialized='view') }}

OUTPUT =  /******/ SELECT * FROM ref('stg_products')