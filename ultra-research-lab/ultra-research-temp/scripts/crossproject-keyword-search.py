import os

# Define the folder names on your desktop
REPOS = {
    "ultra": os.path.expanduser("~/Desktop/ultra repo"),
    "exsat": os.path.expanduser("~/Desktop/exsat repo"),
    "vaulta": os.path.expanduser("~/Desktop/vaulta repo"),
    "cloak": os.path.expanduser("~/Desktop/cloak repo"),
}

KEYWORDS = ["ultra", "vaulta", "exsat", "cloak"]

# Output destination
DEST_FOLDER = os.path.expanduser("~/Desktop/search_results")
os.makedirs(DEST_FOLDER, exist_ok=True)

def search_repo(label, path):
    print(f"\n🔍 Searching in {label} repo...")
    for keyword in KEYWORDS:
        output_lines = []
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f):
                            if keyword.lower() in line.lower():
                                found = f"{file_path} [Line {i+1}]: {line.strip()}"
                                output_lines.append(found)
                                print(f"  ➤ {found}")
                except Exception as e:
                    continue  # Skip unreadable files

        # Save to results file
        result_file = os.path.join(DEST_FOLDER, f"{label}_{keyword}.txt")
        with open(result_file, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(output_lines))

        print(f"✅ Saved {len(output_lines)} results for '{keyword}' in {result_file}")

# Run the search
for label, path in REPOS.items():
    if os.path.exists(path):
        search_repo(label, path)
    else:
        print(f"⚠️ Repo path not found: {path}")

print("\n🎯 All keyword searches completed.")
