{{ config(materialized='view') }}

CREATE OR REPLACE VIEW customers_staging AS
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    signup_date
FROM
    { source('dbt_vlakhmapurkar', 'customers') }
{ config(materialized='view') }


**Explanation:**

* The model is named customers_staging.
* The data is sourced from the customers table in the dbt_vlakhmapurkar schema.
* The { config(materialized='view') } clause indicates that the model should be materialized as a view. This means that it will not store any data itself, but will instead create a virtual view that queries the underlying source data.
* The SELECT statement selects all columns from the customers table.