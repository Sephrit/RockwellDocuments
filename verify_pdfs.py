import os
import glob
from pypdf import PdfReader
import sys

# Ensure stdout uses utf-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

directory = r"d:\Rockwell"
pdf_files = glob.glob(os.path.join(directory, "**", "*.pdf"), recursive=True)

print("Verifying PDF titles...")
for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    try:
        reader = PdfReader(pdf_path)
        meta = reader.metadata
        title = meta.title if meta and meta.title else "No Title Metadata"
        print(f"File: {filename}\nMeta Title: {title}\n---")
    except Exception as e:
        print(f"File: {filename}\nError reading metadata: {e}\n---")
