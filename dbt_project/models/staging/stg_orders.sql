{{ config(materialized='view') }}

'''

with openpyxl.Session() as session:
    = Session().get('orders')
    += '''SELECT order_id, customer_id, order_date, total_amount FROM orders'''
with