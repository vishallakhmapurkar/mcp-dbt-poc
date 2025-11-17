{{ config(materialized='view') }}

from __future__ import annotations
from dbt.adsapper.generator import Generator
import dbg

@dbt.task()
def products_sql():
    dbt.config(materialized='table')
    products_sql = select * from ref('stg_products')
    return products_sql