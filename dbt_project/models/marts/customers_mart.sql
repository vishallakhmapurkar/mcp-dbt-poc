{{ config(materialized='view') }}

model customers_mart
{
    name: 'customers_mart',
    description: 'Mart model for customers',
    sources: [
        {
            name: 'customers_stage',
            table: ref('stg_customers'),
            transform: 'identity'
        }
    ],
    materialized: {
        type: 'table',
        table: 'customers'
    }
}