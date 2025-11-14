import os
import json
from local_llm import generate_sql_model

def generate_dbt_files(spec, output_dir="dbt_project/models"):
    os.makedirs(output_dir, exist_ok=True)
    table = spec["table_name"]
    columns = spec["columns"]
    description = spec["description"]

    prompt = f"Table: {table}\nColumns: {columns}\nTask: {description}"
    sql_code = generate_sql_model(prompt)

    with open(f"{output_dir}/{table}.sql", "w") as f:
        f.write(sql_code)

    schema = {
        "version": 2,
        "models": [{
            "name": table,
            "description": description,
            "columns": [{"name": col, "description": "Generated"} for col in columns]
        }]
    }

    with open(f"{output_dir}/{table}_schema.yml", "w") as f:
        json.dump(schema, f, indent=2)

    return f"✅ Generated {table}.sql and schema.yml"
