import subprocess

def clone_repo(git_url: str, branch: str, dest: str):
    cmd = ["git", "clone", "-b", branch, git_url, dest]
    subprocess.run(cmd, check=True)
