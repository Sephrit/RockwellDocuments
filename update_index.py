#!/usr/bin/env python3
"""Cross-platform README index generator (mirrors Update-Index.ps1)."""

from __future__ import annotations

import os
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
REPO_BASE = "https://github.com/Sephrit/RockwellDocuments/blob/main"
RAW_BASE = "https://github.com/Sephrit/RockwellDocuments/raw/main"

CATEGORY_NAMES = {
    "01_PLCs": "PLCs and Controllers",
    "02_Drives": "Variable Frequency Drives",
    "03_Servos": "Servo Drives",
    "04_Safety": "Safety Systems",
    "05_IO_Modules": "I/O Modules",
    "06_Networking": "Networking and Communications",
    "07_Software": "Software and Programming",
    "08_HMI": "HMI and Operator Interface",
    "09_Motor_Control": "Motor Control and Protection",
    "10_Pilot_Devices": "Pilot Devices Relays and Timers",
    "11_Sensors": "Sensors and Detection",
    "12_Panel_Components": "Panel Components and Wiring",
    "13_Motion": "Motion Control and Servo Motors",
    "14_Migration_Conversion": "Migration and Conversion Guides",
    "15_Cognex": "Cognex Vision Systems",
    "16_SICK": "SICK Sensors and Safety",
    "17_Banner": "Banner Engineering",
    "18_Festo": "Festo Pneumatics",
    "19_Keyence": "Keyence Sensors and Vision",
    "20_Endress_Hauser": "Endress+Hauser Process Instruments",
    "21_nVent_Hoffman": "nVent HOFFMAN Enclosures",
    "22_Belden": "Belden Industrial Networking",
    "23_Wonderware_AVEVA": "Wonderware AVEVA InTouch HMI",
    "24_CIP_EtherNetIP": "CIP and EtherNet/IP Protocol",
    "25_Redundancy": "High Availability and Redundancy",
}

MARKER = "<!-- AUTO-GENERATED-INDEX-START -->"


def anchor(name: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()).replace(" ", "-")


def parse_pdf(pdf: Path) -> tuple[str, str]:
    parts = pdf.stem.split(" - ", 2)
    pub = parts[0].strip() if parts else pdf.stem
    if len(parts) >= 3:
        desc = f"{parts[1].strip()} - {parts[2].strip()}"
    elif len(parts) == 2:
        desc = parts[1].strip()
    else:
        desc = pdf.stem
    return pub, desc


def main() -> None:
    pdfs = sorted(ROOT.rglob("*.pdf"))
    pdfs = [p for p in pdfs if ".venv" not in p.parts]
    total_mb = round(sum(p.stat().st_size for p in pdfs) / (1024 * 1024), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    existing = README.read_text(encoding="utf-8") if README.exists() else ""
    if MARKER in existing:
        header = existing.split(MARKER, 1)[0].rstrip()
    else:
        header = (
            "# Rockwell Automation Documentation Database\n\n"
            "Welcome to this reference repository! This collection is meant to serve as a fast, "
            "organized reference for controls engineers working with common and legacy "
            "Rockwell/Allen-Bradley platform components, as well as associated partner vendors."
        )

    lines: list[str] = [
        header,
        "",
        MARKER,
        "",
        f"> **{len(pdfs)} documents** | **{total_mb} MB** total | Last updated: **{timestamp}**",
        ">",
        "> This index is automatically updated via GitHub Actions.",
        "> You can also run `python3 update_index.py` or `.\\Update-Index.ps1` locally after adding documents.",
        "",
        "---",
        "",
        "## Quick Navigation",
        "",
        "| Category | Documents |",
        "|:---------|----------:|",
    ]

    top_dirs = sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name[:1].isdigit())
    for d in top_dirs:
        cat_pdfs = [p for p in pdfs if p.relative_to(ROOT).parts[0] == d.name]
        if not cat_pdfs:
            continue
        name = CATEGORY_NAMES.get(d.name, d.name)
        lines.append(f"| [{name}](#{anchor(name)}) | {len(cat_pdfs)} docs |")

    lines.extend(["", "---", ""])

    for d in top_dirs:
        cat_pdfs = [p for p in pdfs if len(p.parts) > len(ROOT.parts) and p.relative_to(ROOT).parts[0] == d.name]
        if not cat_pdfs:
            continue
        name = CATEGORY_NAMES.get(d.name, d.name)
        size_mb = round(sum(p.stat().st_size for p in cat_pdfs) / (1024 * 1024), 1)
        lines.extend([f"## {name}", "", f"*{len(cat_pdfs)} documents - {size_mb} MB*", ""])

        subdirs = sorted({p.parent for p in cat_pdfs if p.parent != d})
        for sub in subdirs:
            sub_pdfs = sorted(p for p in cat_pdfs if p.parent == sub)
            if not sub_pdfs:
                continue
            sub_name = sub.name.replace("_", " ")
            lines.extend([
                f"### {sub_name}",
                "",
                "| Publication | Document | Size | Action |",
                "|:------------|:---------|-----:|:-------|",
            ])
            for pdf in sub_pdfs:
                pub, desc = parse_pdf(pdf)
                rel = pdf.relative_to(ROOT).as_posix()
                encoded = "/".join(urllib.parse.quote(part) for part in rel.split("/"))
                view_url = f"{REPO_BASE}/{encoded}"
                download_url = f"{RAW_BASE}/{encoded}?download=true"
                fsize = f"{round(pdf.stat().st_size / (1024 * 1024), 1)} MB"
                lines.append(
                    f"| `{pub}` | {desc} | {fsize} | [View]({view_url}) &nbsp;&nbsp; [Download]({download_url}) |"
                )
            lines.append("")

        lines.extend(["---", ""])

    lines.extend([
        "## Notes",
        "",
        "- All documents sourced from [Rockwell Automation Literature Library](https://literature.rockwellautomation.com)",
        "- Publication numbers follow Rockwell standard format: `{Bulletin}-{Type}{Sequence}`",
        "- After cloning, run `git lfs pull` to download PDF content (files are stored with Git LFS)",
        "- To add new documents, place PDFs in the appropriate folder and push to GitHub (Action will run automatically)",
        "- File naming convention: `{PubNumber} - {Product} - {DocType}.pdf`",
        "- Verify PDFs with `python3 verify_pdfs.py`",
    ])

    README.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Index generated: {README}")
    print(f"Cataloged {len(pdfs)} documents, {total_mb} MB total")


if __name__ == "__main__":
    main()
