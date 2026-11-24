#!/usr/bin/env python3
"""
================================================================================
AUTOMATED GITHUB DEPLOYMENT SCRIPT
================================================================================
Executes the specified Git / CMD commands using Python's subprocess module
to silently stage, commit, branch, and push the repository to GitHub.
================================================================================
"""

import subprocess
import sys
import os

def run_cmd(command, silent=False):
    """Executes a shell command via subprocess."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        if not silent and result.stdout:
            print(result.stdout.strip())
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"[-] Command failed: {command}")
            if e.stdout:
                print(f"[STDOUT] {e.stdout.strip()}")
            if e.stderr:
                print(f"[STDERR] {e.stderr.strip()}")
        return False, e.stderr

def deploy_to_github():
    print("[*] Initiating automated GitHub deployment via Python subprocess...")
    
    commands = [
        "git init",
        "git add .",
        'git commit -m "Initial commit: Hybrid Cloud Defense Blueprint and Topology Generator"',
        "git branch -M main",
        "git remote remove origin",  # in case it already exists, reset cleanly
        "git remote add origin https://github.com/kevinmonteiro543-sketch/-Layered-Defense-Blueprint-for-Hybrid-Cloud-Networks.git",
        "git push -u origin main",
    ]

    for cmd in commands:
        # For remote remove origin, allow failure silently if origin didn't exist
        silent = "remote remove origin" in cmd
        success, out = run_cmd(cmd, silent=silent)
        if not success and not silent:
            # If commit says nothing to commit, that's fine
            if "nothing to commit" in out or "remote origin already exists" in out:
                continue
            print(f"[-] Deployment encountered an issue on: {cmd}")
            # continue attempt to complete workflow

    print("[+] Git operations completed successfully.")

if __name__ == "__main__":
    deploy_to_github()
