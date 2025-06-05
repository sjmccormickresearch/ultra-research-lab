import subprocess
import os

## Analyse Cloak's repo

REPO_URL = "https://github.com/mschoenebeck/zeos-caterpillar"
DEST_FOLDER = os.path.expanduser("~/Desktop/cloak-zeos")

# Create the destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

print(f"Cloning Zeos-Caterpillar into {DEST_FOLDER}...")
subprocess.run(["git", "clone", REPO_URL, DEST_FOLDER])

print("✅ Done cloning Cloak's Zeos-Caterpillar repository.")


