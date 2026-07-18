# Daily Documentation Automation

A scheduled Cursor Automation adds **two components per day** from `component_backlog.json`.

> **Shortcut:** for Rockwell items with a `downloadUrl`, `python3 tools/download_backlog.py`
> does steps 2–7 below deterministically (no agent needed) — it verifies `%PDF` magic,
> saves with the exact backlog filename, and flips statuses. Agents are only needed for
> vendor items with `downloadUrl: null` (bot-protected portals). After any batch, run
> `python3 tools/update_index.py` and `python3 tools/update_catalog.py`.
> **Be polite:** keep ≥1s between requests — the literature CDN rate-limits bursts (HTTP 403)
> for a while if hammered.

## What the agent does each run

1. **Pull latest** — `git pull` on `main` (ensure Git LFS is available).
2. **Read the backlog** — Open `component_backlog.json` at the repo root.
3. **Pick two items** — Select the next two entries with `"status": "pending"`, sorted by `priority` (lowest first). Skip any item whose target PDF already exists on disk.
4. **Download each PDF**
   - Rockwell: use `downloadUrl` from the backlog, or search [literature.rockwellautomation.com](https://literature.rockwellautomation.com) for the publication number.
   - Banner / Cognex / other vendors: follow `notes` in the backlog item; use the vendor product page if no direct URL.
   - Verify the file starts with `%PDF` and is larger than 10 KB.
5. **Save** — Create the target folder if missing. Save using the exact `filename` from the backlog.
6. **Verify** — Run `python3 tools/verify_pdfs.py` (install `pypdf` if needed). If a new PDF fails verification, delete it, mark the backlog item `"status": "failed"` with a note, and try the next pending item instead.
7. **Update backlog** — Set successfully added items to `"status": "done"` and add `"addedAt": "YYYY-MM-DD"`.
8. **Commit and push** — One commit per run, message format:
   ```
   Add documentation: {pub1}, {pub2}

   Daily backlog batch — verified with verify_pdfs.py
   ```
9. **Report** — Summarize what was added, file paths, sizes, and what is next in the queue.

## File naming convention

```
{Publication Number} - {Product Name} - {Document Type}.pdf
```

## Do not

- Commit Git LFS pointer stubs without pulling real PDF content first.
- Mark backlog items `done` if the PDF failed verification.
- Add more than two documents per run unless explicitly instructed.
- Modify unrelated files.

## After push

The existing GitHub Action (`.github/workflows/update-index.yml`) regenerates `README.md` when PDFs change on `main`. You can also run `python3 tools/update_index.py` locally.

## Adding more items to the queue

Edit `component_backlog.json` — append new objects with `"status": "pending"` and the next `priority` number. Rockwell PDF URLs typically follow:

```
https://literature.rockwellautomation.com/idc/groups/literature/documents/{type}/{pub-lowercase}_-en-p.pdf
```

Where `{type}` is `um`, `in`, `td`, `sg`, `pm`, `tg`, etc.
