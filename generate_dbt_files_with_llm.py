import os
import yaml
import subprocess
import re

def generate_sql_model(prompt: str, model: str = "sqlcoder:7b"):
    """
    Calls Ollama via subprocess with SQLCoder to generate SQL model code.
    Cleans and validates the output before returning.
    """
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True,
    )
    sql_code = result.stdout.decode("utf-8")

    # --- Cleanup step ---
    sql_code = re.sub(r"```sql|```|`", "", sql_code)        # remove markdown fences/backticks
    sql_code = sql_code.replace("{{{{", "{{").replace("}}}}", "}}")  # fix malformed braces
    sql_code = re.sub(r"^\s*[-*#]+\s*", "", sql_code, flags=re.MULTILINE) # remove bullets/headings
    sql_code = re.sub(r'"""|\'\'\'', '', sql_code)          # remove triple quotes
    sql_code = re.sub(r"^\s*(task|note|example)\b.*", "", sql_code, flags=re.MULTILINE) # remove stray words
    sql_code = re.sub(r";\s*$", "", sql_code, flags=re.MULTILINE) # remove trailing semicolons
    sql_code = sql_code.strip()

    # --- Jinja validation ---
    if "{{ config" not in sql_code:
        sql_code = "{{ config(materialized='view') }}\n\n" + sql_code

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

            # --- Staging model prompt ---
            staging_prompt = f"""
Generate a dbt SQL staging model for table {table_name}.
Requirements:
- Use {{ config(materialized='view') }} at the top.
- Select columns: {', '.join([c['name'] for c in columns])}.
- Source must be {{ source('{source_name}', '{table_name}') }}.
- Output only valid BigQuery SQL compatible with dbt.
- Do not include CREATE, MODEL, semicolons, other non-BigQuery syntax or commentary.
"""
            staging_sql = generate_sql_model(staging_prompt, model="sqlcoder:7b")
            with open(os.path.join(staging_path, f"stg_{table_name}.sql"), "w") as f:
                f.write(staging_sql)

            # --- Mart model prompt ---
            mart_prompt = f"""
Generate a dbt SQL mart model for table {table_name}.
Requirements:
- Use {{ config(materialized='table') }} at the top.
- Must be a single SELECT statement.
- Select from {{ ref('stg_{table_name}') }} only.
- Output only valid BigQuery SQL compatible with dbt.
- Do not include CREATE, MODEL, semicolons, other non-BigQuery syntax or commentary.
"""
            marts_sql = generate_sql_model(mart_prompt, model="sqlcoder:7b")
            with open(os.path.join(marts_path, f"{table_name}_mart.sql"), "w") as f:
                f.write(marts_sql)

            # --- Add to schema.yml ---
            source_block["tables"].append({"name": table_name})
            schema_dict["models"].append({"name": f"stg_{table_name}", "description": f"Staging model for {table_name}"})
            schema_dict["models"].append({"name": f"{table_name}_mart", "description": f"Mart model for {table_name}"})

        schema_dict["sources"].append(source_block)

        with open(os.path.join(base_path, "schema.yml"), "w") as f:
            yaml.dump(schema_dict, f, sort_keys=False)

        return "✅ dbt models and schema.yml generated successfully using SQLCoder via Ollama."
    except Exception as e:
        return f"❌ Failed to generate dbt files: {str(e)}"
