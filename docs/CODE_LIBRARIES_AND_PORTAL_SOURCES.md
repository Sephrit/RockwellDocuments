# Code Libraries & Portal-Only Sources

The deterministic downloader (`download_backlog.py`) only grabs public **literature-library PDFs**
(the `…/documents/{type}/{pub}_-en-p.pdf` pattern). The items below are **code/config artifacts**
or live on **sign-in portals**, so they can't be auto-fetched. This file is the map for grabbing
them by hand (or with a browser/local-model agent). The *documentation* for most of them is already
archived in this repo (see the `PROCES-*`, `1756-PM010`, `1756-RM006` publications).

Legend: 🟢 direct ZIP/download · 🔑 free Rockwell account sign-in · 🏢 AVEVA/partner account

---

## 1. Rockwell AOIs — Library of Process Objects (the standard blocks)
The AOIs (`.L5X`) **plus** matching FactoryTalk View SE/ME faceplates and global objects ship together
as the **Rockwell Automation Library of Process Objects**.

| Artifact | Where | Notes |
|:--|:--|:--|
| Library of Process Objects (AOIs + SE/ME faceplates) | 🔑 [Product Compatibility & Download Center (PCDC)](https://compatibility.rockwellautomation.com/) → search "Library of Process Objects" | Version must match your PlantPAx / Studio 5000 revision |
| Docs for every object (analog, discrete, motor, valve, PID, etc.) | 🟢 **already in this repo** → `07_Software/PlantPAx/Process_Library/` (`PROCES-RM001–014`) | Reference manuals per object family |
| Add-On Instructions design/usage | 🟢 in repo → `1756-PM010` (Add-On Instructions), `1756-RM006` (Process Control & Drives Instructions) | |
| Machine Builder / independent libraries | 🔑 PCDC → "Application Content" / "Machine Builder Libraries" | Conveyors, common machine objects |
| Rockwell sample code | 🔑 [Sample Code / Application Content](https://www.rockwellautomation.com/en-us/support/documentation/sample-code.html) | Searchable snippets & routines |

## 2. EDS files (Electronic Data Sheets)
Register a device's identity/params in Studio 5000 & FactoryTalk Linx/RSLinx.

| Artifact | Where | Notes |
|:--|:--|:--|
| Per-device EDS ZIPs | 🟢/🔑 [EDS download portal](https://www.rockwellautomation.com/en-us/support/product/product-downloads/electronic-data-sheets.html) | Search by catalog number; many download without sign-in |
| Bulk / register tool | Studio 5000 **EDS Hardware Installation Tool** (`Tools → EDS Hardware Installation`) | Installs EDS + icons locally |
| Third-party device EDS | Vendor site or [ODVA](https://www.odva.org/) | For non-RA EtherNet/IP devices |

## 3. Add-On Profiles (AOP)
Module profiles so hardware appears correctly in the Studio 5000 I/O tree.

| Artifact | Where |
|:--|:--|
| AOP packages | 🔑 [PCDC](https://compatibility.rockwellautomation.com/) → "Add-On Profiles" |

## 4. Standard HMI blocks / faceplates
| Platform | Artifact | Where |
|:--|:--|:--|
| FactoryTalk View SE/ME | Process Objects faceplates + global objects | 🔑 PCDC (bundled with Library of Process Objects) |
| Drives / motor control | PowerFlex, E300, SMC faceplate bundles | 🔑 Product download page per device (search catalog + "faceplate") |
| Studio 5000 View Designer (PV5000) | Standard graphic library | Ships **inside** View Designer; docs = `9324-UM…` (portal) |

## 5. FactoryTalk Optix objects
Optix is a newer platform — **not** in the `-en-p` literature library.

| Artifact | Where |
|:--|:--|
| Optix product + library objects | 🔑 [FactoryTalk Optix](https://www.rockwellautomation.com/en-us/products/software/factorytalk/optix.html) → Downloads |
| Optix online documentation | 🔑 Rockwell Optix docs portal (in-product Help → Documentation) |
| Optix community templates | 🔑 Rockwell Optix community / sample projects |

## 6. Wonderware / AVEVA objects
| Artifact | Where |
|:--|:--|
| ArchestrA Symbol Library / Situational Awareness Library | 🏢 [AVEVA Support](https://www.aveva.com/en/support-and-success/support/) |
| Application Server object toolkit, Symbol Factory | 🏢 [AVEVA Docs](https://docs.aveva.com/) |
| DAServer for Allen-Bradley (DASABCIP) | 🏢 AVEVA Support → search "DASABCIP" |

*(See also [VENDOR_DOWNLOAD_QUEUE.md](VENDOR_DOWNLOAD_QUEUE.md) for the full AVEVA/partner link set.)*

---

### Suggested folders for the artifacts once downloaded
```
07_Software/
  PlantPAx/Process_Library/           # PROCES-* docs (done) + AOI .L5X + SE faceplates
  Studio_5000/AOI_Library/            # standalone AOIs / sample code
  Studio_5000/EDS_AOP/                # EDS files + Add-On Profiles
  FactoryTalk/Optix/Library_Objects/  # Optix templates/objects
23_Wonderware_AVEVA/ArchestrA_Objects/ # symbols, SAL, object toolkit
```
