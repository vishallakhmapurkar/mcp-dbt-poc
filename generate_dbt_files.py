import os
import yaml

def generate_dbt_files(spec):
    try:
        project_path = spec.get("project_path", ".")
        base_path = os.path.join(project_path, "models")
        staging_path = os.path.join(base_path, "staging")
        marts_path = os.path.join(base_path, "marts")
        os.makedirs(staging_path, exist_ok=True)
        os.makedirs(marts_path, exist_ok=True)

        source_name = spec.get("source_name", "source")

        # Collect schema.yml structure
        schema_dict = {"version": 2, "sources": [], "models": []}
        source_block = {
            "name": source_name,
            "schema": source_name,  # adjust if warehouse schema differs
            "tables": []
        }

        for table in spec.get("tables", []):
            table_name = table["name"]
            columns = table["columns"]

            # --- Staging model ---
            staging_sql = f"""
{{{{ config(materialized='view') }}}}

SELECT
    {",\n    ".join([f"{col['name']} AS {col['name']}" for col in columns])}
FROM {{{{ source('{source_name}', '{table_name}') }}}}
"""
            staging_file = os.path.join(staging_path, f"stg_{table_name}.sql")
            with open(staging_file, "w") as f:
                f.write(staging_sql.strip())

            # --- Mart model ---
            marts_sql = f"""
{{{{ config(materialized='table') }}}}

SELECT
    *
FROM {{{{ ref('stg_{table_name}') }}}}
"""
            marts_file = os.path.join(marts_path, f"{table_name}_mart.sql")
            with open(marts_file, "w") as f:
                f.write(marts_sql.strip())

            # --- Add to schema.yml ---
            source_block["tables"].append({"name": table_name})
            schema_dict["models"].append({
                "name": f"stg_{table_name}",
                "description": f"Staging model for {table_name}"
            })
            schema_dict["models"].append({
                "name": f"{table_name}_mart",
                "description": f"Mart model for {table_name}"
            })

        schema_dict["sources"].append(source_block)

        # Write schema.yml
        schema_file = os.path.join(base_path, "schema.yml")
        with open(schema_file, "w") as f:
            yaml.dump(schema_dict, f, sort_keys=False)

        return "✅ dbt models and schema.yml generated successfully."
    except Exception as e:
        return f"❌ Failed to generate dbt files: {str(e)}"
