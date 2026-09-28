"""
update_repo_name_werredu.py
Systematically updates all references from 'werr-edu' and 'WERR-Edu'
to 'Werredu' across all source files, documentation, and configurations.
"""

import os
import re

BASE_DIR = r"c:\Users\TeknoSanat_3\Documents\antigravity\goofy-pasteur"

FILES_TO_UPDATE = [
    "README.md",
    ".zenodo.json",
    "SEAL_MANIFEST.json",
    "ZENODO_ARXIV_Q1_YUKLEME_REHBERI.md",
    "PFP_SIMULATOR_CONCEPTUAL_GUIDE.md",
    "PFP_SIMULATOR_TECHNICAL_MANUAL.md",
    os.path.join("latex", "main.tex"),
    os.path.join("latex", "camera_ready_manuscript.html"),
    os.path.join("lean4", "PFP_HorizonProof.lean"),
    os.path.join("sim", "generate_simulator_html.py"),
    os.path.join("sim", "process_real_student_datasets.py"),
    os.path.join("sim", "benchmark_pfp_saturn_paradox.py"),
    os.path.join("sim", "build_camera_ready_pdf.py"),
    os.path.join("sim", "package_zenodo_bundle.py"),
    os.path.join("sim", "audit_and_optimize_ecosystem.py"),
    os.path.join("sim", "push_werr_edu.py"),
    os.path.join("data", "pfp_saturn_benchmark_results.json")
]

REPLACEMENTS = [
    ("github.com/jesmaat/werr-edu", "github.com/jesmaat/Werredu"),
    ("jesmaat/werr-edu", "jesmaat/Werredu"),
    ("werr-edu.git", "Werredu.git"),
    ("werr-edu", "Werredu"),
    ("WERR-Edu", "Werredu"),
    ("WERR_Edu", "Werredu"),
    ("werr_edu", "werredu")
]

updated_count = 0
for rel_path in FILES_TO_UPDATE:
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(full_path):
        print(f"[SKIP] Not found: {full_path}")
        continue

    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    new_content = content
    for old, new in REPLACEMENTS:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[UPDATED] {rel_path}")
        updated_count += 1
    else:
        print(f"[NO CHANGE] {rel_path}")

print(f"\nSuccessfully updated {updated_count} files.")
