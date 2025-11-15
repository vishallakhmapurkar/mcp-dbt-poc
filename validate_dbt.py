import subprocess
def validate_dbt(project_dir="dbt_project"):
    try:
        subprocess.run(["dbt", "debug"],cwd=project_dir)
        subprocess.run(["dbt", "run"],cwd=project_dir)
        subprocess.run(["dbt", "docs", "generate"], cwd=project_dir)
        subprocess.run(["dbt", "test"], cwd=project_dir)
        # Step 5: Auto-generate schema.yml for sources
        subprocess.run([
            "dbt", "run-operation", "generate_source",
            "--args", '{"schema_name": "sales_data", "database_name": "your_database"}'
        ], cwd=project_dir)

        # Step 6: Auto-generate model properties
        # Example: generate for orders_mart model
        subprocess.run([
            "dbt", "run-operation", "generate_model_properties",
            "--args", '{"model_name": "orders_mart"}'
        ], cwd=project_dir)
        return "✅ dbt debug, run, docs generate, and test completed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ dbt validation failed: {str(e)}"