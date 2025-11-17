{{ config(materialized='view') }}

from dbt import task

with materialized='view' as (customer_id bigint, first_name text, last_name text, email text, signup_date timestamp):
    sql:
    "SELECT customer_id, first_name, last_name, email, signup_date FROM customers;"