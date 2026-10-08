# Simulation Methodology

> No Sentaurus command file is in this repository. This page describes the workflow **as documented in the report and as visible in the screenshots**. It does not reproduce any Sentaurus syntax, because none was available to copy, and syntax will not be invented here.

## Tools

| Tool | Role | Evidence |
|---|---|---|
| Synopsys Sentaurus Process | Process simulation (deposition, etch, defect insertion, fill, CMP) | Report §4.1 |
| Sentaurus Visual (W-2024.09) | Structure visualization; 3D view and 2D cut planes | Screenshot window titles |
| Sentaurus Device | **Not used.** Listed as future work in report §10.1 | – |

## Workflow

1. **Define the domain.** A cross-section that contains one complete trench plus portions of the adjacent active regions (Reported, §4.2). The screenshots show a 3D block about 1 µm × 1 µm × 1.5 µm with a centred square opening, inspected through a 2D cut at Y = 0.5 (Estimated).
2. **Define the substrate.** Silicon, (100), boron 1.4 × 10¹⁵ cm⁻³, uniform, defect-free (Reported).
3. **Set materials.** Silicon, Oxide, Nitride, and Gas appear in the materials list. Aluminum also appears in `final_structure`, but the report does not explain it.
4. **Set process parameters.** The thicknesses and dimensions come from the §4.3 table. No process conditions are reported.
5. **Build the hard mask.** Deposit the 12 nm pad oxide, then the 120 nm nitride.
6. **Pattern the isolation region.** Define the mask and open the nitride and pad oxide.
7. **Etch the trench.** Anisotropic etch into the Si.
8. **Introduce the residue-mask defect.** An explicit defect step at the trench floor (Reported: "the analytical distinguishing step").
9. **Optional liner oxidation.** Status unknown.
10. **Deposit the HDP oxide.** 400 nm.
11. **CMP.** Planarize to the nitride, then strip the nitride per the report. The nitride remains in the screenshots.
12. **Extract the geometry.** Inspect the cut planes. The report gives geometric numbers (§6.1) but no extraction procedure.

## Simulation domain and meshing

- **Domain.** One trench with part of an active region on each side, deep enough to include the substrate below the trench. In the screenshots the silicon block is 1.5 µm deep and the trench sits in the top ≈ 0.35 µm.
- **Adaptive meshing.** The mesh "is adaptively refined in regions of geometric complexity and steep physical gradients" (Reported, §4.2). In this structure that means the trench corners, the sidewalls, the defect, and the material interfaces.
- **Not reported:** mesh element counts, minimum spacing, refinement boxes, and solver settings. None are invented here.

## Physical models

The report names no etch, deposition, oxidation, or CMP model. The defect is introduced geometrically. No electrical, stress, or reliability model was run.

## Geometry extraction in this repository

The `.tdr` files are not available, so geometry was re-estimated from the screenshots:

- [`scripts/analysis/measure_tcad_screenshots.py`](../scripts/analysis/measure_tcad_screenshots.py) classifies pixel colours (Si, nitride, oxide, gas) in each cut-plane crop. It calibrates pixels per µm from the silicon block (1.0 µm wide, 1.5 µm deep, per the axis ticks) and reports depth, widths, sidewall angle (linear fit), recess size, and planarity proxies. The horizontal and vertical calibrations agree to within 5 %.
- [`scripts/analysis/report_consistency_check.py`](../scripts/analysis/report_consistency_check.py) checks the report's numbers against each other.

See [reproduction.md](reproduction.md) for commands.
