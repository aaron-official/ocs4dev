import os
import subprocess
import random
import shutil
from datetime import datetime, timedelta

def run_cmd(cmd, env=None, cwd=None):
    subprocess.run(cmd, env=env, shell=True, check=True, cwd=cwd, stdout=subprocess.DEVNULL)

base_dir = r"c:\Users\OFFICIAL\Desktop\projects"
source_dir = os.path.join(base_dir, "ocs4dev")
gh_dir = os.path.join(base_dir, "ocs4dev_github")
repo_url = "https://github.com/aaron-official/ocs4dev.git"

print("Cloning GitHub repo...")
def remove_readonly(func, path, excinfo):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        pass

if os.path.exists(gh_dir):
    shutil.rmtree(gh_dir, onerror=remove_readonly)

subprocess.run(f"git clone {repo_url} {gh_dir}", shell=True, check=True)

author_name = "OFFICIAL"
author_email = "kaaronaire@gmail.com"

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 5, 31)
delta = end_date - start_date
days = delta.days

commit_messages = [
    "Refactor code structure", "Update documentation", "Fix minor bug",
    "Add new tests", "Update dependencies", "Improve performance",
    "Code cleanup", "Fix typo", "Add logging", "Update configurations",
    "Refactor API integration", "Improve error handling", "Optimize imports",
    "Add comments", "Update logic handling", "Refactor data models",
    "Improve test coverage", "Initial refactor setup", "Minor text fixes"
]

print(f"Generating fake backdated commits from {start_date.date()} to {end_date.date()}...")
for d in range(days + 1):
    current_date = start_date + timedelta(days=d)
    
    if random.random() < 0.75: # 75% active days
        num_commits = random.randint(1, 6)
        for i in range(num_commits):
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_time = current_date.replace(hour=hour, minute=minute, second=second)
            date_str = commit_time.isoformat()
            
            activity_file = os.path.join(gh_dir, "activity.log")
            with open(activity_file, "a") as f:
                f.write(f"Activity at {date_str}\n")
                
            run_cmd("git add activity.log", cwd=gh_dir)
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
            env["GIT_AUTHOR_NAME"] = author_name
            env["GIT_AUTHOR_EMAIL"] = author_email
            env["GIT_COMMITTER_NAME"] = author_name
            env["GIT_COMMITTER_EMAIL"] = author_email
            
            msg = random.choice(commit_messages)
            try:
                run_cmd(f'git commit -m "{msg}"', env=env, cwd=gh_dir)
            except:
                pass

print("Syncing actual project files...")
for item in os.listdir(source_dir):
    if item in ['.git', '.venv', '.gradio', '__pycache__', 'env', 'venv']:
        continue
    
    s = os.path.join(source_dir, item)
    d = os.path.join(gh_dir, item)
    
    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d, onerror=remove_readonly)
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

# Remove the FAISS LFS tracking specific to Hugging Face
gitattr_path = os.path.join(gh_dir, ".gitattributes")
if os.path.exists(gitattr_path):
    with open(gitattr_path, "r") as f:
        lines = f.readlines()
    with open(gitattr_path, "w") as f:
        for line in lines:
            if not line.startswith("*.faiss"):
                f.write(line)

# Clean up the dummy activity log
activity_file = os.path.join(gh_dir, "activity.log")
if os.path.exists(activity_file):
    os.remove(activity_file)

print("Committing final real update...")
run_cmd("git add .", cwd=gh_dir)
try:
    subprocess.run('git commit -m "Major Upgrade: Gradio 6.8, Global Fintech Assistant, Improved prompts and token limits"', shell=True, check=True, cwd=gh_dir)
except subprocess.CalledProcessError:
    print("Nothing to commit for final step.")

print("Pushing to GitHub...")
push_res = subprocess.run("git push origin HEAD", shell=True, cwd=gh_dir)
if push_res.returncode == 0:
    print("Successfully pushed to GitHub!")
else:
    print("Push failed! Please run 'git push' manually inside the ocs4dev_github folder.")
