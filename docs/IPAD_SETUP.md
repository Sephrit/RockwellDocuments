# iPad Field Setup

Carry the whole library on an iPad, annotate freely, and keep your markups
**out of the repo and off iCloud**. Three pieces:

```
Working Copy app  (on-device)          Files > On My iPad  (on-device)
└── RockwellDocuments/  read-only      └── Rockwell Notes/  yours alone
    pull to update                         ├── 02_Drives/
                                           ├── 04_Safety/
                                           └── Job Notes/
                        Syncthing (optional, one-way iPad -> computer backup)
```

## 1. The library — Working Copy

1. Install **Working Copy** from the App Store.
2. Clone `Sephrit/RockwellDocuments`.
3. Repo settings → enable **LFS: download on demand**. The clone stays ~10 MB;
   each PDF downloads the first time you open it and stays cached on device.
4. Update anytime with **Pull** — the library only ever gains files, so pulling
   never disturbs anything you've downloaded.

Working Copy stores repos in on-device app storage. iCloud is not involved.

## 2. Your notes — a separate local folder

1. Files app → **On My iPad** → create **Rockwell Notes** (subfolders to taste —
   mirroring the library's numbered categories keeps sorting familiar).
2. To mark up a document: open it from Working Copy → Share → your PDF app
   (or plain Files Markup) → annotate → **Save to Files → On My iPad →
   Rockwell Notes/...** under your own name, e.g. `755 STO - startup gotchas.pdf`.

The library copy stays pristine; your annotated copy lives only on the iPad.
"On My iPad" is local flash storage — it never touches an iCloud quota.

## 3. Backup for the notes — Syncthing, one-way

Local-only notes die with the iPad. A one-way Syncthing share backs them up to
your computer **without** iCloud and **without** ever entering the repo:

1. On the computer: create a folder *outside* the repo (e.g.
   `~/Documents/Rockwell Notes`) and add it in Syncthing with folder ID
   `rockwell-notes`, type **Receive Only**.
2. On the iPad: install **Synctrain** (or Möbius Sync) → add your computer as a
   device using its Syncthing device ID → share the iPad's `Rockwell Notes`
   folder to it as **Send Only**.
3. Accept the device + folder on the computer side once. Done — notes flow
   iPad → computer only. The receive-only/send-only pairing makes it
   impossible for the computer (or the repo) to change anything on the iPad.

## Space budget

| Piece | Size |
|:--|:--|
| Working Copy clone (LFS on demand) | ~10 MB + whatever PDFs you open |
| Full library if you download everything | ~6.5 GB |
| Your notes | whatever you write |
| iCloud usage | **zero** |
