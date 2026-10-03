#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated GitHub Publisher for Werredu (Private Repository)
and Ecosystem Metadata Synchronizer for pCwOrM.
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

GH_USERNAME = "jesmaat"
REPO_NAME = "WerreduR"
REPO_DESC = "Procedural Fractal Pedagogy (PFP / WerreduR v1.0): Zero-Storage Mandelbrot Boundary Reflexes & Lean 4 Formal Verification for AIED"
HOMEPAGE = "https://doi.org/10.5281/zenodo.22774934"

TOPICS = [
    "aied",
    "intelligent-tutoring-systems",
    "educational-technology",
    "chaos-theory",
    "complex-systems",
    "vygotsky-zpd",
    "reigeluth",
    "procedural-generation",
    "mandelbrot",
    "zero-storage",
    "edge-ai",
    "lean4",
    "formal-verification",
    "pedagogy",
    "self-directed-learning",
    "cognitive-load",
    "tamame",
    "orbital-error-dynamics",
    "werr",
    "python"
]


def check_gh_cli():
    gh_path = r"C:\Program Files\GitHub CLI\gh.exe"
    if os.path.exists(gh_path):
        res = subprocess.run([gh_path, "auth", "status"], capture_output=True, text=True)
        if res.returncode == 0:
            print("[OK] GitHub CLI is authenticated!")
            return gh_path
    return None


def create_and_push_with_gh(gh_path, is_private=True):
    print(f"[1/4] Creating {'private' if is_private else 'public'} repository '{GH_USERNAME}/{REPO_NAME}' via GitHub CLI...")
    cmd = [
        gh_path, "repo", "create", f"{GH_USERNAME}/{REPO_NAME}",
        "--private" if is_private else "--public",
        "--description", REPO_DESC,
        "--homepage", HOMEPAGE
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout or res.stderr)

    print("[2/4] Setting 20 optimal topics/keywords...")
    topic_cmd = [gh_path, "repo", "edit", f"{GH_USERNAME}/{REPO_NAME}"]
    for t in TOPICS:
        topic_cmd.extend(["--add-topic", t])
    subprocess.run(topic_cmd, capture_output=True)

    print("[3/4] Configuring git remote...")
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{GH_USERNAME}/{REPO_NAME}.git"], check=True)

    print("[4/4] Pushing main branch to GitHub...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    print(push_res.stdout or push_res.stderr)
    if push_res.returncode == 0:
        print(f"[SUCCESS] Repository {GH_USERNAME}/{REPO_NAME} is live (PRIVATE) on GitHub!")
        return True
    return False


def create_and_push_with_pat(token, is_private=True):
    print(f"[1/4] Creating {'private' if is_private else 'public'} repository '{GH_USERNAME}/{REPO_NAME}' via GitHub REST API...")
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "WERR-Publisher"
    }
    payload = {
        "name": REPO_NAME,
        "description": REPO_DESC,
        "homepage": HOMEPAGE,
        "private": is_private,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": False
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[OK] Created repository: {data['html_url']}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        if "name already exists" in err_msg:
            print("[INFO] Repository already exists on GitHub. Proceeding to sync topics and push...")
        else:
            print(f"[ERROR] HTTP {e.code}: {err_msg}")
            return False

    print("[2/4] Setting 20 optimal topics/keywords...")
    topic_url = f"https://api.github.com/repos/{GH_USERNAME}/{REPO_NAME}/topics"
    topic_req = urllib.request.Request(topic_url, data=json.dumps({"names": TOPICS}).encode('utf-8'), headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(topic_req) as resp:
            print(f"[OK] Topics updated: {TOPICS}")
    except Exception as e:
        print(f"[WARN] Topic update notice: {e}")

    print("[3/4] Configuring authenticated git remote...")
    auth_remote = f"https://{GH_USERNAME}:{token}@github.com/{GH_USERNAME}/{REPO_NAME}.git"
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", auth_remote], check=True)

    print("[4/4] Pushing main branch to GitHub...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    # Sanitizing token from remote URL for security
    subprocess.run(["git", "remote", "set-url", "origin", f"https://github.com/{GH_USERNAME}/{REPO_NAME}.git"], check=True)
    
    print(push_res.stdout or push_res.stderr)
    if push_res.returncode == 0:
        print(f"\n[SUCCESS] Repository {GH_USERNAME}/{REPO_NAME} is live (PRIVATE) on GitHub!")
        return True
    return False


if __name__ == "__main__":
    gh_cli = check_gh_cli()
    if gh_cli:
        create_and_push_with_gh(gh_cli, is_private=True)
    elif len(sys.argv) > 1 and sys.argv[1].startswith("ghp_"):
        create_and_push_with_pat(sys.argv[1], is_private=True)
    else:
        print("Usage:")
        print("  1. python scripts/push_werredu.py <GITHUB_PERSONAL_ACCESS_TOKEN>")
        print("  or")
        print("  2. Authenticate GitHub CLI once: & 'C:\\Program Files\\GitHub CLI\\gh.exe' auth login -w")
