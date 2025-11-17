{{ config(materialized='view') }}

with open(os.devnullpath("/home/sql"), "w") as f:
    f.write(")