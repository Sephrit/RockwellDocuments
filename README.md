# Rockwell Automation Documentation Database

A curated, verified reference library for controls engineers working on Rockwell/Allen-Bradley platforms and the partner hardware that lives alongside them. Every folder is a device family; inside it are all of that device's documents (manuals, install sheets, specs, selection guides) together.

> **1095 documents** | **6.41 GB** | Last updated **2026-07-18 14:29** | New here? Read [00_START_HERE.md](00_START_HERE.md)

## Find It Fast

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

## Categories

*Click a category to browse its full document tables.*

| # | Category | Docs | Size |
|:--|:--|--:|--:|
| 01 | [PLCs and Controllers](01_PLCs) | 225 | 774.1 MB |
| 02 | [Variable Frequency Drives](02_Drives) | 73 | 743.6 MB |
| 03 | [Servo Drives](03_Servos) | 70 | 474.6 MB |
| 04 | [Safety Systems](04_Safety) | 205 | 1802.9 MB |
| 05 | [I/O Modules](05_IO_Modules) | 71 | 234.1 MB |
| 06 | [Networking and Communications](06_Networking) | 63 | 472.3 MB |
| 07 | [Software and Programming](07_Software) | 60 | 298.0 MB |
| 08 | [HMI and Operator Interface](08_HMI) | 51 | 199.1 MB |
| 09 | [Motor Control and Protection](09_Motor_Control) | 57 | 193.3 MB |
| 10 | [Pilot Devices Relays and Timers](10_Pilot_Devices) | 5 | 60.0 MB |
| 11 | [Sensors and Detection](11_Sensors) | 15 | 157.7 MB |
| 12 | [Panel Components and Wiring](12_Panel_Components) | 32 | 172.3 MB |
| 13 | [Motion Control and Servo Motors](13_Motion) | 41 | 406.9 MB |
| 14 | [Migration and Conversion Guides](14_Migration_Conversion) | 53 | 50.3 MB |
| 15 | [Cognex Vision Systems](15_Cognex) | 2 | 10.1 MB |
| 16 | [SICK Sensors and Safety](16_SICK) | 3 | 36.8 MB |
| 17 | [Banner Engineering](17_Banner) | 6 | 25.3 MB |
| 18 | [Festo Pneumatics](18_Festo) | 2 | 1.5 MB |
| 20 | [Endress+Hauser Process Instruments](20_Endress_Hauser) | 3 | 14.7 MB |
| 21 | [nVent HOFFMAN Enclosures and Cooling](21_nVent_Hoffman) | 4 | 22.8 MB |
| 24 | [CIP and EtherNet/IP Protocol](24_CIP_EtherNetIP) | 11 | 54.2 MB |
| 25 | [High Availability and Redundancy](25_Redundancy) | 3 | 23.0 MB |
| 26 | [Application Solutions and OEM Toolkits](26_Application_Solutions) | 23 | 275.2 MB |
| 28 | [Phoenix Contact](28_Phoenix_Contact) | 2 | 8.8 MB |
| 40 | [Aruba HPE Networking](40_Aruba_HPE) | 2 | 3.5 MB |
| 41 | [Moxa Industrial Networking](41_Moxa) | 6 | 28.9 MB |
| 42 | [Cisco Industrial (Catalyst IE)](42_Cisco_Industrial) | 2 | 5.7 MB |
| 43 | [SEW-Eurodrive Drives](43_SEW_Eurodrive) | 2 | 7.7 MB |
| 44 | [HMS Ewon Remote Access](44_HMS_Ewon) | 1 | 3.6 MB |
| 45 | [Kepware OPC Connectivity](45_Kepware_OPC) | 1 | 4.2 MB |
| 46 | [Hardy Process Weighing](46_Hardy_Weighing) | 1 | 1.1 MB |

## Document Type Legend

| Code | Type | What it tells you |
|:--|:--|:--|
| `UM` | User Manual | how to configure and use it |
| `IN` | Installation Instructions | mounting, wiring, dimensions |
| `RM` | Reference Manual | deep technical reference |
| `PM` | Programming Manual | software / instruction programming |
| `TD` | Technical Data | specs, ratings, catalog numbers |
| `SG` | Selection Guide | choosing the right model |
| `AT` | Application Technique | worked example of a specific task |
| `QS` | Quick Start | step-by-step first setup |
| `RD/WP/PP` | Reference Data / White Paper / Profile | misc supporting docs |

## Notes

- Rockwell documents come from the [Rockwell Automation Literature Library](https://literature.rockwellautomation.com); partner docs from each vendor's official site.
- Files use Git LFS. Prefer the per-document Download links, or grab category bundles from Releases if published.
- Naming convention: `{PubNumber} - {Product} - {DocType}.pdf`
- Add documents via `component_backlog.json` + `python3 tools/download_backlog.py`, then `python3 tools/update_index.py` (see [docs/AUTOMATION.md](docs/AUTOMATION.md)).
