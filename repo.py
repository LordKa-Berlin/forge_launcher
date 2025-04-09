import os
import subprocess
import requests
import json
import getpass  # Um das Token sicher abzufragen

# === Benutzerkonfiguration ===
GITHUB_USERNAME = "LordKa-Berlin"
GITHUB_TOKEN = getpass.getpass("Please enter your GitHub Personal Access Token: ")  # Sicher nach dem Token fragen
REPO_NAME = "forge_launcher"
DESCRIPTION = "🔥 Forge Launcher: GUI tool to manage Stable Diffusion FORGE (Start/Stop/Restart, RAM/VRAM, Tray, Auto-Restart)"
LOCAL_PATH = r"C:\Users\lordk\OneDrive\#Lordka\#SCRIPTE\PYTHON\GIT-PROJEKTE\forge_launcher"  # Pfad zu deinem Projekt

# === GitHub Repo erstellen ===
def create_github_repo():
    print("📡 Creating GitHub repository...")

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "name": REPO_NAME,
        "description": DESCRIPTION,
        "private": False,  # Setze auf True, wenn das Repo privat sein soll
        "auto_init": True  # Erstellt das Repo ohne README, wird später hinzugefügt
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print(f"✅ Repository '{REPO_NAME}' created successfully.")
    elif response.status_code == 422:
        print("⚠️ Repository already exists – continuing...")
    else:
        print(f"❌ Error creating repository: {response.status_code} {response.text}")
        exit(1)

# === Git Initialisierung & Push ===
def initialize_and_push():
    print("📁 Initializing local Git repository...")
    os.chdir(LOCAL_PATH)

    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "checkout", "-b", "main"], check=True)

    # Füge .gitignore hinzu (kann nach Bedarf angepasst werden)
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write("IGNORE-Entwicklung/\n")

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "🚀 Initial commit: Forge Launcher v1.8"], check=True)

    # Füge das Remote hinzu
    subprocess.run(["git", "remote", "add", "origin",
                    f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"], check=True)

    # Push auf GitHub
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    print("✅ Code pushed to GitHub successfully!")

# === Ausführung ===
if __name__ == "__main__":
    create_github_repo()
    initialize_and_push()
