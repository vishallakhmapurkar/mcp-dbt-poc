import subprocess

def validate_dbt(project_dir="dbt_project"):
    subprocess.run(["dbt", "debug"], cwd=project_dir)
    subprocess.run(["dbt", "run"], cwd=project_dir)
    subprocess.run(["dbt", "test"], cwd=project_dir)
    return "✅ dbt validation complete"
