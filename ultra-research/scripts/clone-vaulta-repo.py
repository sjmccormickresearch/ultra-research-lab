import requests
import subprocess
import os

USERNAME = "VaultaFoundation"  # Vaulta's GitHub org
DEST_FOLDER = os.path.expanduser("~/Desktop/vaulta")  # Folder to save to on Desktop

# Create the destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

page = 1
while True:
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
    response = requests.get(url)
    repos = response.json()

    # Break if no more repos or error
    if not repos or "message" in repos:
        break

    for repo in repos:
        name = repo["name"]
        clone_url = repo["clone_url"]
        repo_path = os.path.join(DEST_FOLDER, name)

        if not os.path.exists(repo_path):  # Avoid re-cloning
            print(f"Cloning {name}...")
            subprocess.run(["git", "clone", clone_url, repo_path])
        else:
            print(f"{name} already exists, skipping...")

    page += 1

print("✅ Done cloning all Vaulta repositories.")
