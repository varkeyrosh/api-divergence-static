import subprocess
import os
from pathlib import Path

def clone_or_pull_repo(git_url: str, dest: str, branch: str = "main"):
    """
    Clone the repo if not present.
    If present, pull latest changes.
    """

    dest_path = Path(dest)

    if dest_path.exists():
        print("Repo exists. Pulling latest changes...")
        subprocess.run(["git", "-C", dest, "pull"], check=True)
    else:
        print("Cloning repo fresh...")
        subprocess.run(["git", "clone", "-b", branch, git_url, dest], check=True)
