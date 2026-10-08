# Reproduction

## What can be reproduced from this repository

| Item | Reproducible here? | How |
|---|---|---|
| Screenshot geometry estimates | Yes | `measure_tcad_screenshots.py` |
| Report consistency checks | Yes | `report_consistency_check.py` |
| All SVG diagrams | Yes | `make_diagrams.py` |
| The Sentaurus process simulation | **No** | Command file and structures are not in the repository |
| Geometry extraction from `.tdr` | **No** | `.tdr` files are not in the repository |
| Electric field, leakage, stress, reliability | **No** | Never simulated |

No Sentaurus simulation was executed while preparing this repository.

## Environment

### For the analysis scripts

- Python 3.9 or newer
- `numpy` and `Pillow`, needed only by `measure_tcad_screenshots.py`

```bash
python3 -m pip install numpy Pillow
```

### For the TCAD simulation (not included)

- Synopsys Sentaurus Process. The structures in the screenshots were viewed in Sentaurus Visual W-2024.09.
- A licensed Synopsys installation. No process decks, technology files, or license details are, or should be, published here. Any material or model parameter files must come from your own licensed environment.

## Simulation setup (from the report)

| Item | Setting |
|---|---|
| Domain | A cross-section with one trench and adjacent active regions. The screenshots show a 3D block ≈ 1 × 1 × 1.5 µm |
| Substrate | Si (100), B 1.4 × 10¹⁵ cm⁻³ |
| Layers | Pad oxide 12 nm, Si₃N₄ 120 nm |
| Trench | 200 nm deep, 180 nm wide (reported) |
| Defect | Explicit cone-defect step, 100 nm height, ~10 nm tip (reported) |
| Fill | HDP oxide 400 nm |
| CMP | Stop on nitride |
| Meshing | Adaptive refinement near geometry and gradients. No numeric settings were reported |

## Process run

**Not available.** The command file was not supplied. Sentaurus syntax is deliberately not reconstructed here, because an invented deck would misrepresent what was simulated.

## Structure visualization (once `.tdr` files are added)

Open the saved structures in Sentaurus Visual, as the screenshots show: switch on the materials list, add a cut plane at Y = 0.5, and read geometry from the 2D cut. The three structure names in the screenshots are `ConeDefect_fps_geometry`, `Review1_Fig1_FinalSTI_fps_geometry`, and `final_structure_fps_geometry`.

## Analysis

```bash
# Geometry estimates from the three cropped cut-plane screenshots
python3 scripts/analysis/measure_tcad_screenshots.py --csv results/screenshot-measurements.csv

# Internal consistency of the reported numbers (standard library only)
python3 scripts/analysis/report_consistency_check.py > results/report-consistency-check.md

# Regenerate all conceptual diagrams in assets/ (standard library only)
python3 scripts/figures/make_diagrams.py
```

All three commands are deterministic. Running them leaves the committed outputs unchanged.

## Where to add the original simulation files

If you have the original files, add them so that the project can be reproduced. Sanitize home-directory paths, user names, and host names first.

```
process/        Sentaurus Process command file(s) (*.cmd) and any include files you are allowed to publish
structures/     Saved structures (*.tdr) for: after etch + defect, after fill, after CMP, final
results/        Cutline exports (*.plt / *.csv) for depth, widths, and oxide-over-tip
```

Then replace the "Estimated" values in [results.md](results.md) with direct extractions.
