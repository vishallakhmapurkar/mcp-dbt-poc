import subprocess

def validate_dbt():
    try:
        subprocess.run(["dbt", "debug"], check=True)
        subprocess.run(["dbt", "run"], check=True)
        subprocess.run(["dbt", "docs", "generate"], check=True)
        subprocess.run(["dbt", "test"], check=True)
        return "✅ dbt debug, run, docs generate, and test completed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ dbt validation failed: {str(e)}"
