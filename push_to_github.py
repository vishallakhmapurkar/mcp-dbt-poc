from git import Repo, InvalidGitRepositoryError
import os

def push_to_github():
    # Get the root directory of the project
    root_dir = os.path.abspath(os.getcwd())

    try:
        # Try to load the existing repo
        repo = Repo(root_dir)
    except InvalidGitRepositoryError:
        # If not a repo, initialize one
        repo = Repo.init(root_dir)

    try:
        repo.git.add(A=True)
        repo.index.commit("Add dbt models")

        origin = repo.remote(name="origin")
        origin.push()
        return "✅ Pushed to GitHub successfully."
    except Exception as e:
        return f"❌ Git push failed: {str(e)}"
