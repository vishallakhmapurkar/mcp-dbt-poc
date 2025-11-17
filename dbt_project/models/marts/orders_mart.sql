{{ config(materialized='view') }}

'''
   _model = '''SELECT date_trunc('month', created_at) AS MONTH, COUNT(*) AS total_orders FROM ref('stg_orders') WHERE date_trunc('month', created_at) BETWEEN '2021-04-01' AND CURRENT_DATE AND status = 'completed' GROUP BY MONTH ORDER BY MONTH NULLS LAST;'''