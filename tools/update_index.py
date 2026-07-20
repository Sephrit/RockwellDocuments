#!/usr/bin/env python3
"""Index generator.

Writes a human-first root README.md (overview, find-it-fast guide, category map)
plus a README.md inside every numbered category folder with the full document
tables. GitHub renders a folder's README when you browse into it, so navigation
is: root map -> click category -> full table for that device family.
"""

from __future__ import annotations

import re
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


def pdf_size(p: Path) -> int:
    """Real byte size, even when the file is a Git LFS pointer stub (CI without lfs pull)."""
    st = p.stat().st_size
    if st < 512:
        try:
            head = p.read_text(errors="ignore")
            if head.startswith("version https://git-lfs"):
                for line in head.splitlines():
                    if line.startswith("size "):
                        return int(line.split()[1])
        except Exception:
            pass
    return st


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
    "21_nVent_Hoffman": "nVent HOFFMAN Enclosures and Cooling",
    "22_Belden": "Belden Industrial Networking",
    "23_Wonderware_AVEVA": "Wonderware AVEVA InTouch HMI",
    "24_CIP_EtherNetIP": "CIP and EtherNet/IP Protocol",
    "25_Redundancy": "High Availability and Redundancy",
    "26_Application_Solutions": "Application Solutions and OEM Toolkits",
    "28_Phoenix_Contact": "Phoenix Contact",
    "40_Aruba_HPE": "Aruba HPE Networking",
    "41_Moxa": "Moxa Industrial Networking",
    "42_Cisco_Industrial": "Cisco Industrial (Catalyst IE)",
    "43_SEW_Eurodrive": "SEW-Eurodrive Drives",
    "44_HMS_Ewon": "HMS Ewon Remote Access",
    "45_Kepware_OPC": "Kepware OPC Connectivity",
    "46_Hardy_Weighing": "Hardy Process Weighing",
}

DOC_TYPES = [
    ("UM", "User Manual", "how to configure and use it"),
    ("IN", "Installation Instructions", "mounting, wiring, dimensions"),
    ("RM", "Reference Manual", "deep technical reference"),
    ("PM", "Programming Manual", "software / instruction programming"),
    ("TD", "Technical Data", "specs, ratings, catalog numbers"),
    ("SG", "Selection Guide", "choosing the right model"),
    ("AT", "Application Technique", "worked example of a specific task"),
    ("QS", "Quick Start", "step-by-step first setup"),
    ("RD/WP/PP", "Reference Data / White Paper / Profile", "misc supporting docs"),
]

FIND_IT_FAST = """## Find It Fast

**Search tips** — fastest ways to land on the right document:
- Press `t` on the GitHub repo page and type any product word (`755`, `kinetix 5300`, `guard locking`) — filenames are descriptive, so filename search usually nails it.
- Know the publication number? Search it directly (`1756-PM011`).
- [`catalog.json`](catalog.json) is the machine-readable index of every document (pub, title, path, size) if you want to grep locally.

**Common jobs and where to start:**

| I need to... | Go to |
|:--|:--|
| Wire or install a specific module | The device's folder — every family has its `IN` installation sheets alongside the manuals |
| Size/spec a drive, servo, breaker | The family's `TD` technical data and `SG` selection guides |
| Design a safety function (curtain, gate, e-stop...) | [04_Safety/Application_Techniques](04_Safety/Application_Techniques) — 112 complete worked designs (SAFETY-AT series) |
| Messaging between PLCs / produce-consume / CIP | [07_Software/Studio_5000](07_Software/Studio_5000) — `1756-PM012` (MSG), `1756-PM011` (produce/consume), `1756-PM020` (CIP data access), `1756-RM003` (connection budgets) |
| Build or use AOIs | `1756-PM010` + the PlantPAx object library in [07_Software/PlantPAx](07_Software/PlantPAx) |
| Replace obsolete hardware (PLC-5, SLC, Ultra 3000...) | [14_Migration_Conversion](14_Migration_Conversion) + [docs/OBSOLESCENCE_AND_LIFECYCLE.md](docs/OBSOLESCENCE_AND_LIFECYCLE.md) |
| Configure a Stratix switch / plan the network | [06_Networking](06_Networking) — per-model Stratix folders + CPwE design guides |
| Set up an MCC bucket or interlock | [09_Motor_Control](09_Motor_Control) (CENTERLINE) + `04_Safety/Trapped_Key_440T` |
| Get AOI/EDS/faceplate downloads (not PDFs) | [docs/CODE_LIBRARIES_AND_PORTAL_SOURCES.md](docs/CODE_LIBRARIES_AND_PORTAL_SOURCES.md) |

**Reading a publication number** — `1756-PM011`: `1756` = product bulletin (ControlLogix), `PM` = doc type, `011` = sequence.
"""


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


def doc_row(pdf: Path) -> str:
    pub, desc = parse_pdf(pdf)
    rel = pdf.relative_to(ROOT).as_posix()
    enc = "/".join(urllib.parse.quote(part) for part in rel.split("/"))
    return (f"| `{pub}` | {desc} | {round(pdf_size(pdf) / 1048576, 1)} MB | "
            f"[View]({REPO_BASE}/{enc}) &nbsp; [Download]({RAW_BASE}/{enc}?download=true) |")


def write_category_readme(d: Path, cat_pdfs: list[Path]) -> None:
    name = CATEGORY_NAMES.get(d.name, d.name)
    size_mb = round(sum(pdf_size(p) for p in cat_pdfs) / 1048576, 1)
    lines = [
        f"# {name}",
        "",
        f"*{len(cat_pdfs)} documents — {size_mb} MB — part of the "
        f"[Rockwell Documentation Database](../README.md)*",
        "",
    ]
    subdirs = sorted({p.parent for p in cat_pdfs}, key=lambda x: x.as_posix())
    if len(subdirs) > 6:
        lines += ["**Sections:** " + " · ".join(
            f"[{(' / '.join(q.replace('_',' ') for q in s.relative_to(d).parts) if s != d else 'General')}]"
            f"(#{anchor(' '.join(s.relative_to(d).parts) if s != d else 'general')})"
            for s in subdirs), ""]
    for sub in subdirs:
        sub_pdfs = sorted(p for p in cat_pdfs if p.parent == sub)
        if not sub_pdfs:
            continue
        sub_name = "General" if sub == d else " / ".join(
            part.replace("_", " ") for part in sub.relative_to(d).parts)
        lines += [f"## {sub_name}", "",
                  "| Publication | Document | Size | Links |",
                  "|:--|:--|--:|:--|"]
        lines += [doc_row(p) for p in sub_pdfs]
        lines.append("")
    (d / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    pdfs = [p for p in sorted(ROOT.rglob("*.pdf")) if ".venv" not in p.parts]
    total_mb = round(sum(pdf_size(p) for p in pdfs) / 1048576, 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    top_dirs = sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name[:1].isdigit())

    nav = ["| # | Category | Docs | Size |", "|:--|:--|--:|--:|"]
    written = 0
    for d in top_dirs:
        cat = [p for p in pdfs if p.relative_to(ROOT).parts[0] == d.name]
        if not cat:
            continue
        write_category_readme(d, cat)
        written += 1
        name = CATEGORY_NAMES.get(d.name, d.name)
        mb = round(sum(pdf_size(p) for p in cat) / 1048576, 1)
        num = d.name.split("_")[0]
        nav.append(f"| {num} | [{name}]({d.name}) | {len(cat)} | {mb} MB |")

    legend = ["| Code | Type | What it tells you |", "|:--|:--|:--|"]
    legend += [f"| `{c}` | {t} | {w} |" for c, t, w in DOC_TYPES]

    root = [
        "# Rockwell Automation Documentation Database",
        "",
        "A curated, verified reference library for controls engineers working on "
        "Rockwell/Allen-Bradley platforms and the partner hardware that lives alongside them. "
        "Every folder is a device family; inside it are all of that device's documents "
        "(manuals, install sheets, specs, selection guides) together.",
        "",
        f"> **{len(pdfs)} documents** | **{round(total_mb/1024, 2)} GB** | "
        f"Last updated **{timestamp}** | New here? Read [00_START_HERE.md](00_START_HERE.md)",
        "",
        FIND_IT_FAST,
        "## Categories",
        "",
        "*Click a category to browse its full document tables.*",
        "",
        *nav,
        "",
        "## Document Type Legend",
        "",
        *legend,
        "",
        "## Notes",
        "",
        "- Rockwell documents come from the [Rockwell Automation Literature Library]"
        "(https://literature.rockwellautomation.com); partner docs from each vendor's official site.",
        "- Files use Git LFS. Prefer the per-document Download links, or grab category "
        "bundles from Releases if published.",
        "- Naming convention: `{PubNumber} - {Product} - {DocType}.pdf`",
        "- Add documents via `component_backlog.json` + `python3 tools/download_backlog.py`, "
        "then `python3 tools/update_index.py` (see [docs/AUTOMATION.md](docs/AUTOMATION.md)).",
        "",
        "## Attribution and Legal",
        "",
        "This is an independent reference library. It is not affiliated with, sponsored by, "
        "or endorsed by Rockwell Automation or any other vendor whose documentation appears here.",
        "",
        "- Every document is redistributed unmodified from the vendor's own public literature "
        "portal, where each is offered as a free download. No paywalled, licensed, or "
        "confidential material is included.",
        "- All documents remain the property of their respective publishers. "
        "Allen-Bradley, ControlLogix, CompactLogix, GuardLogix, PowerFlex, Kinetix, Stratix, "
        "PanelView, and Studio 5000 are trademarks of Rockwell Automation, Inc. All other "
        "product names are trademarks of their respective owners.",
        "- Documentation is provided for engineering reference only. Always verify against "
        "the latest revision in the vendor's literature portal before using it for design, "
        "installation, or safety work.",
        "- If you hold rights to any document here and want it removed, open an issue and "
        "it will be taken down promptly.",
    ]
    README.write_text("\n".join(root) + "\n", encoding="utf-8")
    print(f"Root README + {written} category READMEs generated")
    print(f"Cataloged {len(pdfs)} documents, {total_mb} MB total")


if __name__ == "__main__":
    main()
