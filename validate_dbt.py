import subprocess
def validate_dbt(project_dir="dbt_project"):
    try:
        subprocess.run(["dbt", "debug"],cwd=project_dir)
        subprocess.run(["dbt", "run"],cwd=project_dir)
        subprocess.run(["dbt", "docs", "generate"], cwd=project_dir)
        subprocess.run(["dbt", "test"], cwd=project_dir)
        return "✅ dbt debug, run, docs generate, and test completed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ dbt validation failed: {str(e)}"