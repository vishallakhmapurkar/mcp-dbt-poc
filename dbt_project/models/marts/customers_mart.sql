{{ config(materialized='view') }}

- Do not output any comments (--).
'''
from dbt.utils import check_env_var, check_dbt_var
check_env_var(locals=['dev', 'prod'])
check_dbt_var()