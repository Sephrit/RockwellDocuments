"""Audit all PDFs in this repository for LFS pointers and corruption."""

import glob
import os
import sys

from pypdf import PdfReader

directory = os.path.dirname(os.path.abspath(__file__))
pdf_files = sorted(glob.glob(os.path.join(directory, "**", "*.pdf"), recursive=True))

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ok = 0
issues = []

for pdf_path in pdf_files:
    rel = os.path.relpath(pdf_path, directory)
    filename = os.path.basename(pdf_path)

    with open(pdf_path, "rb") as f:
        header = f.read(8)

    if header.startswith(b"version "):
        issues.append((rel, "Git LFS pointer — run: git lfs pull"))
        continue

    if not header.startswith(b"%PDF"):
        issues.append((rel, f"Not a PDF (header: {header!r})"))
        continue

    try:
        reader = PdfReader(pdf_path, strict=False)
        pages = len(reader.pages)
        if pages == 0:
            issues.append((rel, "Zero pages"))
            continue

        reader.pages[0].extract_text()
        if pages > 1:
            reader.pages[-1].extract_text()

        meta = reader.metadata
        title = meta.title if meta and meta.title else "No Title Metadata"
        print(f"OK: {filename} ({pages} pages)\n  Title: {title}\n---")
        ok += 1
    except Exception as e:
        issues.append((rel, str(e)))

print(f"\n=== SUMMARY: {ok}/{len(pdf_files)} OK, {len(issues)} issues ===")
for path, issue in issues:
    print(f"FAIL: {path}\n  -> {issue}")

sys.exit(1 if issues else 0)
