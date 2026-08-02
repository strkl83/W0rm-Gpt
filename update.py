#!/usr/bin/env python3
"""
Safe updater for W0rm-GPT
Previous version used `rm -rf main.py` + wget which is unsafe.
This version uses git and pip to update safely.
"""

import os
import sys
import subprocess
from pathlib import Path

def run(cmd, shell=False):
    print(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {e}")
        return False
    except FileNotFoundError:
        print(f"[!] Command not found: {cmd}")
        return False

def main():
    print("=== W0rm-GPT Safe Updater ===")
    root = Path(__file__).parent

    # Check if git repo
    if (root / ".git").exists():
        print("[*] Git repo detected. Pulling latest...")
        run(["git", "fetch", "origin"])
        # Don't auto merge hard; try pull with rebase safe
        run(["git", "pull", "--rebase", "origin", "main"])
    else:
        print("[!] Not a git repository. Skipping git pull.")
        print("    To update manually: git clone https://github.com/samay825/W0rm-Gpt")

    print("\n[*] Updating Python dependencies...")
    pip_cmd = [sys.executable, "-m", "pip", "install", "-r", str(root / "requirements.txt"), "--upgrade"]
    run(pip_cmd)

    print("\n[✓] Update finished. Run: python3 main.py")

if __name__ == "__main__":
    main()
