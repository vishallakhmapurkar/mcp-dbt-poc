from git import Repo

def push_to_github(repo_path="dbt_project", commit_msg="Add dbt model"):
    repo = Repo(repo_path)
    repo.git.add(A=True)
    repo.index.commit(commit_msg)
    origin = repo.remote(name='origin')
    origin.push()
    return "✅ Pushed to GitHub"
