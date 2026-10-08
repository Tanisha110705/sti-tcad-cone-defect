# Repository Guide

```
sti-tcad-cone-defect/
├── README.md
├── .gitignore
├── assets/
│   ├── *.svg                   conceptual diagrams (generated)
│   └── tcad/                   cropped genuine Sentaurus Visual screenshots
├── docs/                       technical documentation
├── results/                    analysis outputs (generated) + reported parameter table
└── scripts/
    ├── analysis/               screenshot measurement, report consistency check
    └── figures/                diagram generator
```

The `process/` and `structures/` directories from the target layout are **not** created. They would be empty, because the Sentaurus command files and `.tdr` structures are not in this repository. [reproduction.md](reproduction.md#where-to-add-the-original-simulation-files) describes where to put them if they are added later.

## Process scripts

None in the repository.

## Structure files

None in the repository.

## Analysis scripts

| File | Purpose |
|---|---|
| [`scripts/analysis/measure_tcad_screenshots.py`](../scripts/analysis/measure_tcad_screenshots.py) | Classifies pixel materials in the three cut-plane crops, calibrates to µm from the axis frame, and estimates trench depth, widths, sidewall angle, recess size, nitride thickness, and planarity proxies |
| [`scripts/analysis/report_consistency_check.py`](../scripts/analysis/report_consistency_check.py) | Arithmetic checks on the report's numbers: aspect ratio, taper, β ≈ h / r, thinning %, resistivity, and oxide-over-tip geometry |
| [`scripts/figures/make_diagrams.py`](../scripts/figures/make_diagrams.py) | Generates every SVG in `assets/` from the reported dimensions (and the screenshot estimates for `defect-comparison.svg`) |

## Simulation outputs / analysis results

| File | Purpose | Type |
|---|---|---|
| [`results/screenshot-measurements.csv`](../results/screenshot-measurements.csv) | Per-screenshot geometry estimates | Estimated (generated) |
| [`results/report-consistency-check.md`](../results/report-consistency-check.md) | Consistency table for reported numbers | Calculated (generated) |
| [`results/reported-parameters.csv`](../results/reported-parameters.csv) | Every reported numeric parameter with its report section | Reported (transcribed) |

## Images: genuine TCAD output

Cropped from the Sentaurus Visual screenshots embedded in the project report (report p. 12). The window title bars, which contained a private path and hostname, were removed. The resolution is the original's (≈ 5–7 nm/px).

| File | Structure shown |
|---|---|
| `assets/tcad/cone-defect-etch-2d.png` / `-3d.png` | `ConeDefect_fps_geometry`: after trench etch + defect, before fill |
| `assets/tcad/sti-after-fill-2d.png` / `-3d.png` | `Review1_Fig1_FinalSTI_fps_geometry`: after oxide fill / planarization |
| `assets/tcad/final-structure-2d.png` / `-3d.png` | `final_structure_fps_geometry`: final structure (includes Aluminum in the materials list) |

## Images: conceptual diagrams (not Sentaurus output)

| File | Shows |
|---|---|
| `assets/process-flow.svg` | Nine-step flow; marks stages with screenshots |
| `assets/process-evolution.svg` | Seven cross-sections from substrate to CMP |
| `assets/trench-etch.svg` | Reported trench dimensions, 88°, corner radius |
| `assets/defect-formation.svg` | Residue micromasking sequence |
| `assets/cone-defect.svg` | Reported cone dimensions |
| `assets/cmp-flow.svg` | HDP overburden → CMP → nitride strip |
| `assets/final-structure.svg` | Final STI with embedded cone and thin-oxide region |
| `assets/oxide-thinning.svg` | ~150 nm vs. 50–70 nm, with calculated field ratios |
| `assets/electric-field.svg` | Uniform vs. tip-crowded field lines |
| `assets/reliability-flow.svg` | Defect → stress → mechanisms (discussed vs. not simulated) |
| `assets/defect-comparison.svg` | Report-described cone vs. screenshot-observed recess, same scale |

## Reports

The project report PDF is **not committed**, because it contains student registration numbers and uncropped screenshots (see [audit.md](audit.md#security-and-privacy)).

## Documentation

| File | Topic |
|---|---|
| [audit.md](audit.md) | Evidence audit and inconsistencies |
| [overview.md](overview.md) | Summary and evidence map |
| [sti-process-flow.md](sti-process-flow.md) | Process stages |
| [simulation-methodology.md](simulation-methodology.md) | TCAD workflow, domain, meshing |
| [cone-defect-formation.md](cone-defect-formation.md) | Defect mechanism and modelling |
| [geometry-analysis.md](geometry-analysis.md) | Geometry, reported vs. estimated |
| [oxide-thinning.md](oxide-thinning.md) | Oxide thinning |
| [electric-field-analysis.md](electric-field-analysis.md) | Field enhancement |
| [reliability.md](reliability.md) | Reliability mechanisms |
| [validation.md](validation.md) | Validation status |
| [results.md](results.md) | All numbers with sources |
| [reproduction.md](reproduction.md) | How to reproduce |
