#!/usr/bin/env python3
"""Generate catalog.json — machine-readable index of every PDF in the library.

Run after adding documents (update_index.py refreshes the human README;
this refreshes the machine catalog used by scripts/agents).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Vendor (partner) top-level folders; everything else is Rockwell literature.
PARTNER_PREFIX = re.compile(r"^(1[5-9]|2[0-3]|2[6-9]|3\d)_")
ROCKWELL_TOPS = {"24_CIP_EtherNetIP", "26_Application_Solutions"}


def category_names() -> dict:
    ns: dict = {"__file__": str(ROOT / "update_index.py")}
    src = (ROOT / "update_index.py").read_text(encoding="utf-8").split("MARKER =")[0]
    exec(compile(src, "update_index_header", "exec"), ns)
    return ns["CATEGORY_NAMES"]


def main() -> None:
    names = category_names()
    entries = []
    for p in sorted(ROOT.rglob("*.pdf")):
        if ".venv" in p.parts or ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT)
        top = rel.parts[0]
        pub = p.stem.split(" - ")[0].strip()
        desc = " - ".join(p.stem.split(" - ")[1:]).strip() or p.stem
        partner = bool(PARTNER_PREFIX.match(top)) and top not in ROCKWELL_TOPS
        entries.append({
            "publication": pub,
            "title": desc,
            "category": top,
            "category_name": names.get(top, top),
            "subpath": "/".join(rel.parts[1:-1]),
            "filename": p.name,
            "path": rel.as_posix(),
            "size_mb": round(p.stat().st_size / 1048576, 2),
            "source": "partner" if partner else "rockwell",
        })
    out = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(entries),
        "total_mb": round(sum(e["size_mb"] for e in entries), 1),
        "documents": entries,
    }
    (ROOT / "catalog.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    print(f"catalog.json: {len(entries)} docs, {out['total_mb']} MB")


if __name__ == "__main__":
    main()
