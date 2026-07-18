#!/usr/bin/env python3
"""No-LLM backlog downloader.

Reads component_backlog.json, downloads every 'pending' item that has a
downloadUrl, verifies it is a real PDF, saves it with the backlog's exact
filename, and flips the item to 'done' (or 'failed' with a note).

This is deliberately dumb and deterministic: Rockwell literature URLs follow a
fixed pattern, so no model is needed. Run it for free, as often as you like.

    python3 download_backlog.py                # download everything pending
    python3 download_backlog.py --limit 20     # cap this run
    python3 download_backlog.py --source rockwell   # only one vendor
    python3 download_backlog.py --dry-run      # show what would happen
    python3 download_backlog.py --recheck-failed    # retry previously failed

Partner-vendor items with downloadUrl=null are skipped and reported; those need
the browser flow in _PRIVATE_TODO.md (bot-protected portals).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "component_backlog.json"
UA = "Mozilla/5.0 (compatible; RockwellDocsBot/1.0; +local-archive)"
MIN_BYTES = 10 * 1024


def load() -> dict:
    return json.loads(BACKLOG.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    BACKLOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch(url: str, dest: Path) -> tuple[bool, str]:
    """Download url -> dest. Returns (ok, message). Verifies %PDF magic + size."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 - report any transport error verbatim
        return False, f"{type(e).__name__}: {e}"

    if len(data) < MIN_BYTES:
        return False, f"too small ({len(data)} bytes)"
    if data[:4] != b"%PDF":
        # Likely an HTML "not found" / login page served with 200.
        return False, "not a PDF (no %PDF header)"

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True, f"{round(len(data) / (1024 * 1024), 2)} MB"


def main() -> int:
    ap = argparse.ArgumentParser(description="No-LLM Rockwell/partner backlog downloader")
    ap.add_argument("--limit", type=int, default=0, help="max items this run (0 = all)")
    ap.add_argument("--source", help="only this source (rockwell, cognex, ...)")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between downloads")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--recheck-failed", action="store_true", help="also retry 'failed' items")
    args = ap.parse_args()

    data = load()
    items = data["items"]
    wanted = {"pending", "failed"} if args.recheck_failed else {"pending"}

    todo = [it for it in items if it.get("status") in wanted]
    if args.source:
        todo = [it for it in todo if it.get("source") == args.source]
    todo.sort(key=lambda it: it.get("priority", 9_999))
    if args.limit:
        todo = todo[: args.limit]

    if not todo:
        print("Nothing to do.")
        return 0

    done = failed = skipped = 0
    for it in todo:
        target = ROOT / it["folder"] / it["filename"]
        pub = it.get("publication", it.get("id", "?"))

        if target.exists() and target.stat().st_size >= MIN_BYTES:
            it["status"] = "done"
            print(f"  = {pub:<14} already on disk")
            continue

        url = it.get("downloadUrl")
        if not url:
            skipped += 1
            print(f"  ~ {pub:<14} SKIP (no URL — needs browser, see _PRIVATE_TODO.md)")
            continue

        if args.dry_run:
            print(f"  ? {pub:<14} would GET {url}")
            continue

        ok, msg = fetch(url, target)
        if ok:
            it["status"] = "done"
            it["addedAt"] = None  # stamp externally; no clock in this script's callers
            done += 1
            print(f"  + {pub:<14} OK  {msg}  -> {it['folder']}/")
        else:
            it["status"] = "failed"
            note = it.get("notes", "")
            it["notes"] = (note + " | " if note else "") + f"auto-download failed: {msg}"
            failed += 1
            print(f"  x {pub:<14} FAIL {msg}")
        time.sleep(args.delay)

    if not args.dry_run:
        save(data)

    print(f"\n{done} downloaded, {failed} failed, {skipped} skipped (no URL).")
    if done and not args.dry_run:
        print("Next: python3 update_index.py   # regenerate README")
    return 0


if __name__ == "__main__":
    sys.exit(main())
