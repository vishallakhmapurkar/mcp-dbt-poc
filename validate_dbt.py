import subprocess
def validate_dbt(project_dir="dbt_project"):
    try:
        subprocess.run(["dbt", "debug"], check=True,cwd=project_dir)
        subprocess.run(["dbt", "run"], check=True,cwd=project_dir)
        subprocess.run(["dbt", "docs", "generate"], check=True,cwd=project_dir)
        subprocess.run(["dbt", "test"], check=True,cwd=project_dir)
        return "✅ dbt debug, run, docs generate, and test completed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ dbt validation failed: {str(e)}"