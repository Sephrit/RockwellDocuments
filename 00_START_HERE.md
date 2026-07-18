# START HERE

A curated, verified reference library of **public** Rockwell/Allen-Bradley + partner-vendor
documentation for controls engineers. Built to be hoarded, searched, and shared.

## What's inside
- **225+ PDFs** organized into numbered category folders (`01_PLCs` … `25_Redundancy`, plus vendor folders `15`–`23`).
- **`README.md`** — human-readable index, auto-generated, with View/Download links per doc.
- **`catalog.json`** — machine-readable index (pub #, title, path, size, category). Query this from scripts/agents.
- **`component_backlog.json`** — the "recipe": every doc with its verified download URL. This is how the library rebuilds itself.
- **`download_backlog.py`** — zero-dependency, **no-AI** downloader. Reconstitutes the whole library from Rockwell for free.
- **`docs/CODE_LIBRARIES_AND_PORTAL_SOURCES.md`** — where to get AOIs, EDS files, HMI faceplates, Optix/Wonderware objects (sign-in portals — can't be auto-fetched).
- **`docs/OBSOLESCENCE_AND_LIFECYCLE.md`** — modernization/upgrade paths, lifecycle-status & AIM/installed-base tools, release-notes sources, interlocking & remote-racking notes.
- **`update_catalog.py`** — regenerates `catalog.json` after adding documents.

## Get the documents

**Option A — just the files (recommended for most people):**
Download the category ZIPs from the repo's [Releases](https://github.com/Sephrit/RockwellDocuments/releases) page. No tools, no LFS.

**Option B — rebuild from source (always current, free):**
```bash
python3 download_backlog.py            # fetch everything pending
python3 download_backlog.py --dry-run  # preview first
python3 update_index.py                # refresh README.md
```
The downloader verifies every file is a real PDF (`%PDF` header + size) before keeping it.

## How it's organized
```
NN_Category/            e.g. 02_Drives
  Sub_System/           e.g. PowerFlex_755
    Deeper_Layer/       e.g. Packaged_Drives
      {PUB} - {Product} - {DocType}.pdf
```
**Naming convention:** `{Publication} - {Product} - {DocType}.pdf`
(e.g. `750-UM006 - PowerFlex 755T Drive Products - User Manual.pdf`)

## Add a document
1. Find its Rockwell publication number (e.g. `1756-UM543`).
2. Rockwell URLs are deterministic:
   `https://literature.rockwellautomation.com/idc/groups/literature/documents/{type}/{pub-lowercase}_-en-p.pdf`
   where `{type}` = `um in rm pm td sg at qs wp rd pp`.
3. Add an entry to `component_backlog.json` (`status: "pending"`), run `download_backlog.py`, then `update_index.py`.
   Or just drop a correctly-named PDF in the right folder and run `update_index.py`.

## Storage model (for maintainers)
Git tracks the **text** (backlog, catalog, scripts, index) — small and free. The **PDF hoard**
is distributed via **GitHub Releases** (category ZIPs), which avoids Git LFS storage/bandwidth
limits. Anyone can also rebuild the PDFs from `download_backlog.py`. See the repo wiki/notes for the
release-bundling step.

## Scope
Everything here is **publicly downloadable** vendor documentation, collected for reference/education.
Publication numbers and content © their respective manufacturers (Rockwell Automation, SICK, Banner, etc.).
