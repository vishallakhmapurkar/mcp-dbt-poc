{{ config(materialized='view') }}

model orders_mart {
  source = {
    type = 'table',
    schema = 'stg',
    name = 'orders'
  },
  materialized = {
    type = 'table',
    schema = 'tgt',
    name = 'orders'
  },
  sql = """
  SELECT *
  FROM { ref('stg_orders') }
  """
}