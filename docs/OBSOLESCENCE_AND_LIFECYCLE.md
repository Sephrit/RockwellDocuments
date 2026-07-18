# Obsolescence Upgrades, Lifecycle & Network Assessment

Working notes + source map for modernization work in a Rockwell-centric plant.
Literature-library PDFs are archived in `14_Migration_Conversion/`; everything below
is **portal-based** (needs a free Rockwell account or is an online-only tool) and can't
be auto-fetched by `download_backlog.py`.

## Lifecycle status & planning tools

| Tool | What it does | Where |
|:--|:--|:--|
| **Product Lifecycle Status** | Look up any catalog number → Active / Active Mature / End of Life / Discontinued, with announced discontinuation dates and replacement part | [rockwellautomation.com → Support → Product Lifecycle Status](https://www.rockwellautomation.com/en-us/support/product/product-lifecycle-status.html) |
| **AIM (Asset Inventory Management)** / Installed Base Evaluation | The network-scan-driven inventory + obsolescence-risk report we already use for planning | Rockwell services engagement / [myrockwellautomation.com](https://www.myrockwellautomation.com) portal |
| **PCDC** (Product Compatibility & Download Center) | Firmware downloads, version compatibility matrices, release notes per product/version | [compatibility.rockwellautomation.com](https://compatibility.rockwellautomation.com/) |
| **Migration/conversion selector** | ControlLogix/SLC/PLC-5 conversion tools, wiring-conversion kit data | Rockwell → Capabilities → Modernization |
| **Studio 5000 release notes (v33…v37, v38+)** | Per-version release notes & known anomalies moved to the online docs portal — grab per version from PCDC → "Studio 5000 Logix Designer" → your version → Release Notes | PCDC (sign-in) |

## Archived migration literature (in this repo, `14_Migration_Conversion/`)
- `MIGRAT-PP003` PLC-5 to ControlLogix modernization
- `IA-SG001` Integrated Architecture selection
- `1756-PM012` Logix5000 ↔ PLC-5/SLC mapping (programming-level conversion)
- `1785-*` PLC-5 legacy manuals (reference while converting)
- `1747-*` / `1746-*` SLC 500 legacy manuals
- Wiring-conversion & I/O swing-arm docs (see folder index)

## Practical upgrade paths (quick reference)
| Aging asset | Modern target | Key docs in repo |
|:--|:--|:--|
| PLC-5 | ControlLogix 5580 | `MIGRAT-PP003`, `1756-UM543`, `1756-PM012` |
| SLC 500 | CompactLogix 5380 | `5069-UM001`, `1747-*` |
| MicroLogix | Micro800 / CompactLogix | `2080-*`, `1766-*` |
| PowerFlex 40/400/70/700 | PowerFlex 525 / 755(T) | `520-UM001`, `750-UM006`, wiring `DRIVES-IN001` |
| Ultra 3000 servo | Kinetix 5300/5500/5700 | `2098-*` (legacy), `2198-UM003` (migration), `2198-UM005` |
| SLC/PLC-5 era HMI (PanelView Std) | PanelView Plus 7 / PanelView 5000 | `2711P-*`, `2715P-UM001` |
| Unmanaged/legacy switches | Stratix 5200/5400/5800 | `1783-UM*`, CPwE `ENET-TD*` |

## Network assessment / scanning references (in repo)
- `ENET-TD001` Converged Plantwide Ethernet (CPwE) design — segmentation targets
- `ENET-TD006` CPwE network **security** — what a scan should be judged against
- `SECURE-UM001` CIP Security deployment
- `1783-TD001` + Stratix UMs — approved switch replacement options

## Interlocking & electrical-safety hardware (remote racking et al.)
- Trapped-key interlocking: `440T-*` (04_Safety/Trapped_Key_Interlocks) — sequence keys for
  MCC bucket / breaker access without opening energized sections
- MCC structure & bucket docs: `2100-*` (09_Motor_Control/Motor_Control_Centers)
- **Remote racking / remote switching devices** (magnetic-mount breaker racking from outside
  the arc-flash boundary) are third-party: CBS ArcSafe (RRS/RSO series), Ampgard/E-A-T-N options,
  Ultra-Safe. Vendor literature portals; capture PDFs manually to `36_Electrical_Safety/Remote_Racking/`.
- NFPA 70E arc-flash boundary reference — standards body (purchase/portal).
