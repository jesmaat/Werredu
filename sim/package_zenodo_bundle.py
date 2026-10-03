#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cryptographic SHA-256 Sealer and Zenodo / arXiv Archive Packager
for Procedural Fractal Pedagogy (PFP / WerreduR v1.0).
"""

import os
import json
import shutil
import zipfile
import hashlib
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "zenodo_dist")
os.makedirs(DIST_DIR, exist_ok=True)

FILES_TO_SEAL = [
    "Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf",
    ".zenodo.json",
    "README.md",
    "PFP_SIMULATOR_CONCEPTUAL_GUIDE.md",
    "PFP_SIMULATOR_TECHNICAL_MANUAL.md",
    "ZENODO_ARXIV_Q1_YUKLEME_REHBERI.md",
    "HAKEM_SAVUNMASI_ZPD_GEOMETRI_REBUTTAL.html",
    "latex/main.tex",
    "latex/references.bib",
    "latex/camera_ready_manuscript.html",
    "lean4/PFP_HorizonProof.lean",
    "werr/__init__.py",
    "werr/modular_algebra.py",
    "werr/pedagogy.py",
    "werr/engine.py",
    "werr/fractal.py",
    "werr/datatypes.py",
    "werr/calibration.py",
    "werr/router.py",
    "werr/presets.py",
    "werr/telemetry.py",
    "tests/test_werredu_werr_core.py",
    "sim/benchmark_pfp_saturn_paradox.py",
    "sim/build_camera_ready_pdf.py",
    "sim/pfp_interactive_simulator.html",
    "data/pfp_saturn_benchmark_results.json",
    "data/pfp_student_trajectories_summary.csv",
    "figures/fig1_observer_horizon_zpd.png",
    "figures/fig2_saturn_paradox_trajectories.png",
    "figures/fig3_tamame_error_kernel.png",
    "figures/fig4_edge_latency_memory_pareto.png",
]



def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    manifest_entries = {}
    combined_hasher = hashlib.sha256()

    for rel_path in FILES_TO_SEAL:
        abs_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Missing required artifact: {abs_path}")
        digest = sha256_file(abs_path)
        size_bytes = os.path.getsize(abs_path)
        manifest_entries[rel_path] = {
            "sha256": digest,
            "size_bytes": size_bytes,
        }
        combined_hasher.update(f"{rel_path}:{digest}\n".encode("utf-8"))

    master_seal = combined_hasher.hexdigest()
    seal_manifest = {
        "package": "Procedural Fractal Pedagogy (PFP / WerreduR v1.0) — Zenodo & CAEAI Replication Suite",
        "authors": [
            {"name": "Zerrin Dağlı", "orcid": "0000-0001-9490-6425"},
            {"name": "Volkan Dağlı", "orcid": "0009-0000-1587-8703"},
            {"name": "Dağhan Dağlı", "orcid": "0009-0003-2492-8313"},
        ],
        "patent_priority": "TÜRKPATENT TR 2026/016285",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "master_merkle_sha256": master_seal,
        "files": manifest_entries,
    }

    seal_path = os.path.join(BASE_DIR, "SEAL_MANIFEST.json")
    with open(seal_path, "w", encoding="utf-8") as f:
        json.dump(seal_manifest, f, indent=2, ensure_ascii=False)

    # 1. Copy main PDF to zenodo_dist/
    pdf_src = os.path.join(BASE_DIR, "Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf")
    pdf_dst = os.path.join(DIST_DIR, "Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf")
    shutil.copy2(pdf_src, pdf_dst)

    # 2. Build Zenodo Replication Bundle ZIP
    zenodo_zip_path = os.path.join(DIST_DIR, "zenodo_bundle_pfp_werredu_v1.zip")
    with zipfile.ZipFile(zenodo_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel_path in FILES_TO_SEAL + ["SEAL_MANIFEST.json", "sim/package_zenodo_bundle.py"]:
            abs_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
            zf.write(abs_path, arcname=rel_path)

    # 3. Build arXiv LaTeX Submission ZIP (adjusting ../figures/ to figures/ for flat arXiv build)
    arxiv_zip_path = os.path.join(DIST_DIR, "arxiv_submission_pfp_v1.zip")
    tex_src = open(os.path.join(BASE_DIR, "latex", "main.tex"), encoding="utf-8").read()
    tex_arxiv = tex_src.replace("../figures/", "figures/")
    with zipfile.ZipFile(arxiv_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("main.tex", tex_arxiv.encode("utf-8"))
        zf.write(os.path.join(BASE_DIR, "latex", "references.bib"), arcname="references.bib")
        for fig_name in [
            "fig1_observer_horizon_zpd.png",
            "fig2_saturn_paradox_trajectories.png",
            "fig3_tamame_error_kernel.png",
            "fig4_edge_latency_memory_pareto.png",
        ]:
            zf.write(os.path.join(BASE_DIR, "figures", fig_name), arcname=f"figures/{fig_name}")

    print(f"[OK] Master SHA-256 Seal: {master_seal}")
    print(f"[OK] Zenodo PDF:  {pdf_dst} ({os.path.getsize(pdf_dst):,} bytes)")
    print(f"[OK] Zenodo ZIP:  {zenodo_zip_path} ({os.path.getsize(zenodo_zip_path):,} bytes)")
    print(f"[OK] arXiv ZIP:   {arxiv_zip_path} ({os.path.getsize(arxiv_zip_path):,} bytes)")


if __name__ == "__main__":
    main()
