import os

def generate_dbt_files(spec, base_path="dbt_project/models"):
    try:
        os.makedirs(base_path, exist_ok=True)

        # Create folders for staging and marts
        staging_path = os.path.join(base_path, "staging")
        marts_path = os.path.join(base_path, "marts")
        os.makedirs(staging_path, exist_ok=True)
        os.makedirs(marts_path, exist_ok=True)

        source_name = spec.get("source_name", "source")

        for table in spec.get("tables", []):
            table_name = table["name"]
            columns = table["columns"]

            # Generate staging model
            staging_sql = f"""{{{{ config(materialized='view') }}}}

SELECT
    {',\n    '.join([f"{col['name']} AS {col['name']}" for col in columns])}
FROM {{{{ source('{source_name}', '{table_name}') }}}}
"""
            staging_file = os.path.join(staging_path, f"stg_{table_name}.sql")
            with open(staging_file, "w") as f:
                f.write(staging_sql.strip())

            # Generate marts model
            marts_sql = f"""{{{{ config(materialized='table') }}}}

SELECT
    *
FROM {{ ref('stg_{table_name}') }}
"""
            marts_file = os.path.join(marts_path, f"{table_name}_mart.sql")
            with open(marts_file, "w") as f:
                f.write(marts_sql.strip())

        return "✅ dbt model files generated using best practices."
    except Exception as e:
        return f"❌ Failed to generate dbt files: {str(e)}"
