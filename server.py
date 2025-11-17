from fastapi import FastAPI
import subprocess, os, yaml

app = FastAPI()
DBT_PROJECT_PATH = "./dbt_project/models"

@app.post("/generate_and_save_all")
def generate_and_save_all(spec: dict):
    source_name = spec["source_name"]
    tables = spec["tables"]

    schema_path = os.path.join(DBT_PROJECT_PATH, "schema.yml")
    schema_dict = {"version": 2, "sources": [], "models": []}
    if os.path.exists(schema_path):
        schema_dict = yaml.safe_load(open(schema_path))

    # Add source block
    source_entry = {
        "name": source_name,
        "description": f"Raw source schema for {source_name}",
        "tables": [{"name": t["name"], "description": f"Raw {t['name']} table"} for t in tables]
    }
    existing_sources = [s["name"] for s in schema_dict.get("sources", [])]
    if source_name not in existing_sources:
        schema_dict.setdefault("sources", []).append(source_entry)

    results = []
    for table in tables:
        table_name = table["name"]
        columns = [c["name"] for c in table["columns"]]

        # --- Staging model ---
        staging_model_name = f"stg_{table_name}"
        staging_filename = f"{staging_model_name}.sql"
        staging_path = os.path.join(DBT_PROJECT_PATH, "staging", staging_filename)
        os.makedirs(os.path.dirname(staging_path), exist_ok=True)
        staging_sql = f"""{{{{ config(materialized='view') }}}}

SELECT
    {", ".join(columns)}
FROM {{{{ source('{source_name}', '{table_name}') }}}}
"""
        with open(staging_path, "w") as f:
            f.write(staging_sql)

        schema_dict["models"].append({
            "name": staging_model_name,
            "description": f"Staging model for {table_name}",
            "columns": [{"name": c, "tests": ["not_null"] + (["unique"] if c.endswith("_id") else [])} for c in columns]
        })

        results.append({"table": table_name, "model_type": "staging", "filename": staging_filename, "status": "auto"})

        # --- Mart model ---
        prompt = f"Generate mart model for {table_name}"
        result = subprocess.run(
            ["ollama", "run", "sqlcoder:7b"],
            input=prompt.encode("utf-8"),
            capture_output=True,
        )
        sql_code = result.stdout.decode("utf-8").strip()
        status = "valid"
        if not sql_code.startswith("{{ config") or "SELECT" not in sql_code.upper():
            sql_code = f"""{{{{ config(materialized='table') }}}}

SELECT
    {", ".join(columns)}
FROM {{{{ ref('{staging_model_name}') }}}}
"""
            status = "fallback"

        mart_filename = f"{table_name}_mart.sql"
        mart_path = os.path.join(DBT_PROJECT_PATH, "marts", mart_filename)
        os.makedirs(os.path.dirname(mart_path), exist_ok=True)
        with open(mart_path, "w") as f:
            f.write(sql_code)

        schema_dict["models"].append({
            "name": f"{table_name}_mart",
            "description": f"Mart model for {table_name}",
            "columns": [{"name": c, "tests": ["not_null"] + (["unique"] if c.endswith("_id") else [])} for c in columns]
        })

        results.append({"table": table_name, "model_type": "mart", "filename": mart_filename, "status": status})

    # Save schema.yml
    with open(schema_path, "w") as f:
        yaml.dump(schema_dict, f, sort_keys=False)

    # Git commit + push
    try:
        subprocess.run(["git", "add", DBT_PROJECT_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "Generate staging + mart models and update schema.yml with sources"], check=True)
        subprocess.run(["git", "push"], check=True)
        git_status = "✅ Changes committed and pushed to remote."
    except subprocess.CalledProcessError as e:
        git_status = f"❌ Git push failed: {str(e)}"

    schema_preview = yaml.dump(schema_dict, sort_keys=False)
    return {"models": results, "schema_preview": schema_preview, "git_status": git_status}
