# Repository and Report Audit

This audit was performed before any documentation was written. It records what evidence exists, where every number comes from, and where the sources disagree.

## Sources examined

| Source | State at audit time |
|---|---|
| GitHub repository `Tanisha110705/sti-tcad-cone-defect` | **Empty.** No commits, no branches, no files. |
| Project report *"Shallow Trench Isolation (STI) with Cone Defect Modeling Using TCAD"* (VIT, 20 pages) | Complete. It contains 8 embedded images. Three of them are Sentaurus Visual screenshots (report p. 12). |

Search results for Sentaurus artefacts (`.cmd`, `.tdr`, `.plt`, `.log`, `.des`, `.par`, mesh or structure files, mask definitions, plots, logs): **none exist**. Every process, geometry, and reliability statement therefore traces back to the report.

## Confirmed from the repository

Nothing. The repository contained no files.

## Confirmed from the report's genuine TCAD screenshots

Three Sentaurus Visual (version W-2024.09, per the window title) screenshots appear in the report. They were cropped to their plot panels and saved in `assets/tcad/`. They establish the following:

- A **3D simulation domain**, roughly 1 µm × 1 µm in footprint and 1.5 µm deep, with a **square opening** in the hard mask. Each view shows a 2D cut plane at Y = 0.5.
- The materials present are Silicon, Oxide, Nitride, and Gas. The `final_structure` view also lists **Aluminum** and shows extra 3D features (stripes on top of the stack) that the process flow does not describe.
- Three named structures, `ConeDefect_fps_geometry`, `Review1_Fig1_FinalSTI_fps_geometry`, and `final_structure_fps_geometry`, which correspond to the stages after etch with the defect, after fill/planarization, and final.
- Geometry estimates (pixel measurement, ±10–15 nm; full table in [`results/screenshot-measurements.csv`](../results/screenshot-measurements.csv)):

| Quantity | ConeDefect | FinalSTI | final_structure |
|---|---:|---:|---:|
| Nitride thickness | 144 nm | 144 nm | 140 nm |
| Opening width at Si surface | 378 nm | 382 nm | 390 nm |
| Main trench depth | 220 nm | 226 nm | 232 nm |
| Main trench bottom width | 166 nm | 155 nm | 159 nm |
| Sidewall angle (L / R) | 62.0° / 63.9° | 62.6° / 62.8° | 62.5° / 62.8° |
| Recess below floor: depth | 113 nm | 106 nm | 104 nm |
| Recess below floor: width | 46 nm | 44 nm | 61 nm |
| Recess content | gas (empty) | oxide | oxide |
| Fill top relative to nitride top | – | −72 nm | −18 nm |
| Oxide remaining on nitride | – | 0 | ≈ 43 nm |

## Confirmed from the report

- Tool: Synopsys Sentaurus Process. Node: 180 nm CMOS (educational reference node).
- Flow: substrate → pad oxide → nitride → lithography → RIE trench → cone-defect introduction → (optional liner oxidation) → HDP-CVD fill → CMP (→ nitride strip in hot H₃PO₄).
- Parameter table (§4.3): B 1.4 × 10¹⁵ cm⁻³, pad oxide 12 nm, nitride 120 nm, trench 200 nm deep × 180 nm wide, aspect ratio ~1.1, cone height 100 nm, tip radius ~10 nm, HDP oxide 400 nm, CMP removal rate "Standard".
- Geometric analysis (§6.1): sidewall ≈ 88°, bottom width ≈ 170 nm, top-corner radius ≈ 15 nm, cone base ≈ 50 nm, tip radius ≈ 8–12 nm, height-to-base ratio 2 : 1, oxide over tip 50–70 nm vs ~150 nm at the trench bottom, post-CMP height variation < 5 nm.
- Physical interpretation (§6.2): β ≈ 10 is an estimate "using the shape". Stress, TAT/FN leakage, and breakdown are discussed qualitatively.
- Domain and meshing (§4.2): a cross-section with one trench and parts of the adjacent active regions, with adaptive refinement near geometric complexity and steep gradients.
- Defect insertion (§3.2 step 6): "the analytical distinguishing step". The defect is an explicitly modelled step.

## Supported by both

- The STI stack: Si substrate, a thin pad oxide, a nitride hard mask, an oxide-filled trench.
- A defect feature at the trench bottom, roughly 100 nm in its long dimension, that survives fill and planarization. The report says "remains untouched during the CMP process", and the screenshots show the feature after fill.
- Use of the Sentaurus toolchain.

## Missing evidence

- Sentaurus Process command file(s), `.tdr` structures, logs, mesh settings, model choices.
- Any electrical simulation (Sentaurus Device): electric field, potential, current. The report itself lists this as future work (§10.1).
- Any stress, leakage, breakdown, TDDB, SILC, or HCI simulation.
- Any SEM, TEM, profilometry, or literature-overlay comparison.
- A defect-free reference structure, which is needed for a simulated before/after comparison.
- An extraction method for the §6.1 numbers (cutline, measurement tool).

## Report / repository inconsistencies

The report's wording and numbers are left unchanged in this repository. The inconsistencies are listed here instead.

1. **Defect direction.** The report text describes a silicon spike rising from the trench floor. In all three screenshots the feature is a narrow recess extending ≈ 105–115 nm **below** the floor; it is gas before fill and oxide after. Its depth matches the reported 100 nm, but its sense is inverted. The report's own step description (*"A masking residue is then used and etched through to partially expose the silicon"*) is compatible with etching a hole.
2. **Sidewall angle.** Report ≈ 88°; screenshots ≈ 62–64°.
3. **Trench width and depth.** Report 180 nm × 200 nm; screenshots ≈ 380–390 nm opening × ≈ 220–230 nm, or ≈ 330–335 nm total including the recess.
4. **Nitride thickness.** Report 120 nm; screenshots ≈ 140–145 nm. That is about 4–5 px, slightly above the ±2 px measurement uncertainty.
5. **2D vs. 3D.** The abstract and §4.1 mention three-dimensional visualization, and §10.3 says "the present study employs a two-dimensional cross-sectional simulation". The screenshots show a 3D domain viewed through 2D cuts.
6. **Number of steps.** §2.2 lists 8 steps; §3.2 says nine, including the optional liner oxide. Whether the liner was simulated cannot be determined.
7. **Nitride removal.** §3.2 step 9 and §5.2 say the nitride is removed. All post-fill screenshots still show nitride.
8. **Planarity.** The report says < 5 nm. The screenshots show the fill ≈ 70 nm (FinalSTI) or ≈ 20 nm (final_structure) below the nitride top, and ≈ 43 nm of oxide left on the nitride in final_structure.
9. **Oxide thicknesses.** The ~150 nm "nominal" and 50–70 nm "over tip" values cannot be reproduced from the stated geometry. A 200 nm trench filled flush to Si gives 200 nm at the floor and 100 nm above a mid-depth tip; the closest interpretation, the lateral tip-to-sidewall gap, gives ≈ 77 nm. See [oxide-thinning.md](oxide-thinning.md).
10. **Field values.** "80–100 MV/cm at the tip" with β = 10 implies an 8–10 MV/cm average field, but no bias is defined. No field solution exists (§10.1).
11. **§6.3 comparison table and §9 conclusion.** These give breakdown voltage (≈ 15 V → 3–5 V), relative leakage (×100), and relative TDDB lifetime (×0.001), and the conclusion says a lifetime decrease "has been observed". No simulation, method, or data supports these figures. They are **excluded** from this repository's results.
12. **Validation wording.** §4.4 says "We validate our simulation results against published experimental data…", but no comparison appears anywhere.
13. **Doping notation.** The body text reads "1.410cm" and "10cm". Superscripts and the Ω symbol were evidently lost; the table gives 1.4 × 10¹⁵ cm⁻³. The resistivity is consistent: 9.7 Ω·cm calculated.
14. **"Implantation".** The conclusion mentions "implantation and oxide fill", but no implant step appears in the flow.
15. **Process-parameter ranges.** The text gives ranges (pad 10–15 nm, nitride 100–150 nm, trench 200–300 nm) and the table gives single values. This is not a contradiction; the table values are taken as the simulated ones.
16. **References.** The abstract cites "[33]", but only six references are listed.

## Claims that should NOT be made

- "Fabricated", "measured", "wafer data", or "silicon-validated".
- "Validated against SEM/TEM/profilometry".
- "Simulated electric field", "Sentaurus field map", or any MV/cm value as a result.
- Any breakdown voltage, leakage current, TDDB lifetime, or stress value as a result.
- "TAT/FN/TDDB/SILC/HCI simulated".
- "The TCAD structure shows an upward 100 nm silicon cone with a 10 nm tip". The available images do not show this.
- "88° sidewalls / 180 nm trench extracted from TCAD". These are reported values only.
- Presenting this as transistor-level IC design.

## Security and privacy

- The original screenshots' **window title bars** contain a private server path that includes a student registration number, and a university TCAD hostname. Only the plot panels were cropped into `assets/tcad/`, so neither appears in the repository. The PNGs were re-encoded without metadata.
- The **report PDF is not committed**. It contains student registration numbers, the uncropped screenshots, and third-party illustrative figures of unknown provenance. If you want it in the repository, export a sanitized copy first.
- No Sentaurus installation paths, license-server details, or technology/process decks were available, and none are included.
