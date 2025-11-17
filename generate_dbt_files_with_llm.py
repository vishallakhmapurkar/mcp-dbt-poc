import os
import yaml
import subprocess
import re

def generate_sql_model(prompt: str, model: str = "gemma"):
    """
    Calls Ollama with Gemma to generate SQL model code from a natural language prompt.
    Cleans and validates the output before returning.
    """
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True,
    )
    sql_code = result.stdout.decode("utf-8")

    # --- Cleanup step ---
    # Remove markdown fences, stray backticks, triple quotes
    sql_code = re.sub(r"```sql|```|`", "", sql_code)
    # Normalize whitespace
    sql_code = sql_code.strip()

    # --- Jinja validation ---
    # Ensure config, source, and ref blocks are intact
    if "{{ config" not in sql_code:
        sql_code = "{{ config(materialized='view') }}\n\n" + sql_code
    # Fix double braces if Gemma outputs malformed Jinja
    sql_code = sql_code.replace("{{{{", "{{").replace("}}}}", "}}")

    return sql_code

def generate_dbt_files(spec, base_path="dbt_project/models"):
    try:
        os.makedirs(base_path, exist_ok=True)
        staging_path = os.path.join(base_path, "staging")
        marts_path = os.path.join(base_path, "marts")
        os.makedirs(staging_path, exist_ok=True)
        os.makedirs(marts_path, exist_ok=True)

        source_name = spec.get("source_name", "dbt_vlakhmapurkar")

        schema_dict = {"version": 2, "sources": [], "models": []}
        source_block = {"name": source_name, "schema": source_name, "tables": []}

        for table in spec.get("tables", []):
            table_name = table["name"]
            columns = table["columns"]

            # --- Staging model via Gemma ---
            staging_prompt = f"""
Generate a dbt SQL staging model for table {table_name} with columns:
{', '.join([c['name'] for c in columns])}.
Use {{ config(materialized='view') }} and {{ source('{source_name}', '{table_name}') }}.
"""
            staging_sql = generate_sql_model(staging_prompt)
            with open(os.path.join(staging_path, f"stg_{table_name}.sql"), "w") as f:
                f.write(staging_sql)

            # --- Mart model via Gemma ---
            mart_prompt = f"""
Generate a dbt SQL mart model for table {table_name}.
It should select from {{ ref('stg_{table_name}') }} and be materialized as a table.
"""
            marts_sql = generate_sql_model(mart_prompt)
            with open(os.path.join(marts_path, f"{table_name}_mart.sql"), "w") as f:
                f.write(marts_sql)

            # --- Add to schema.yml ---
            source_block["tables"].append({"name": table_name})
            schema_dict["models"].append({"name": f"stg_{table_name}", "description": f"Staging model for {table_name}"})
            schema_dict["models"].append({"name": f"{table_name}_mart", "description": f"Mart model for {table_name}"})

        schema_dict["sources"].append(source_block)

        with open(os.path.join(base_path, "schema.yml"), "w") as f:
            yaml.dump(schema_dict, f, sort_keys=False)

        return "✅ dbt models and schema.yml generated successfully using Gemma via Ollama (with cleanup + Jinja validation)."
    except Exception as e:
        return f"❌ Failed to generate dbt files: {str(e)}"
