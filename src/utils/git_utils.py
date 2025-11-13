import os
import git

def clone_or_pull_repo(repo_url: str, dest: str = "repos") -> str:
    """
    Clone the repository if not already present,
    or pull the latest changes if it exists.
    Returns the local path to the repo folder.
    """

    # Ensure destination folder exists
    os.makedirs(dest, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(dest, repo_name)

    if os.path.exists(repo_path):
        print("Repo exists. Pulling latest changes...")
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        print(f"Cloning repo from {repo_url} ...")
        git.Repo.clone_from(repo_url, repo_path)

    print(f"Repo ready at: {repo_path}")
    return repo_path
