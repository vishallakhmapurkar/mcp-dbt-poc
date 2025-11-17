import os
import yaml
import subprocess
import re

def generate_sql_model(prompt: str, table_name: str, columns: list, source_name: str, model: str = "sqlcoder:7b"):
    """
    Calls Ollama via subprocess with SQLCoder to generate SQL model code.
    Cleans, validates, and falls back to a safe skeleton if needed.
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
    sql_code = re.sub(r"\b(ASSERT|MODEL|annotations|Use)\b.*", "", sql_code, flags=re.IGNORECASE) # remove bad keywords
    sql_code = re.sub(r";\s*$", "", sql_code, flags=re.MULTILINE) # remove trailing semicolons
    sql_code = sql_code.replace('"', '').replace("'", "")   # remove stray quotes
    sql_code = sql_code.strip()

    # --- Validation step ---
    if not sql_code.startswith("{{ config") or "SELECT" not in sql_code.upper():
        # Fallback skeleton if LLM output is invalid
        sql_code = f"""{{{{ config(materialized='view') }}}}

SELECT
    {', '.join([c['name'] for c in columns])}
FROM {{{{ source('{source_name}', '{table_name}') }}}}
"""

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
You are a SQL generator. Output only valid BigQuery SQL for dbt.
Rules:
- Start with {{ config(materialized='view') }}.
- Output a single SELECT statement only.
- Select columns: {', '.join([c['name'] for c in columns])}.
- Source must be {{ source('{source_name}', '{table_name}') }}.
- Do not include CREATE, MODEL, ASSERT, annotations, Use, semicolons, or commentary.
"""
            staging_sql = generate_sql_model(staging_prompt, table_name, columns, source_name, model="sqlcoder:7b")
            with open(os.path.join(staging_path, f"stg_{table_name}.sql"), "w") as f:
                f.write(staging_sql)

            # --- Mart model prompt ---
            mart_prompt = f"""
You are a SQL generator. Output only valid BigQuery SQL for dbt.
Rules:
- Start with {{ config(materialized='table') }}.
- Must be a single SELECT statement.
- Select from {{ ref('stg_{table_name}') }} only.
- Do not include CREATE, MODEL, ASSERT, annotations, Use, semicolons, or commentary.
"""
            marts_sql = generate_sql_model(mart_prompt, table_name, columns, source_name, model="sqlcoder:7b")
            with open(os.path.join(marts_path, f"{table_name}_mart.sql"), "w") as f:
                f.write(marts_sql)

            # --- Add to schema.yml ---
            source_block["tables"].append({"name": table_name})
            schema_dict["models"].append({"name": f"stg_{table_name}", "description": f"Staging model for {table_name}"})
            schema_dict["models"].append({"name": f"{table_name}_mart", "description": f"Mart model for {table_name}"})

        schema_dict["sources"].append(source_block)

        with open(os.path.join(base_path, "schema.yml"), "w") as f:
            yaml.dump(schema_dict, f, sort_keys=False)

        return "✅ dbt models and schema.yml generated successfully using SQLCoder via Ollama with fallback."
    except Exception as e:
        return f"❌ Failed to generate dbt files: {str(e)}"
