# STI Process Flow

![STI process flow](../assets/process-flow.svg)

![Structure evolution](../assets/process-evolution.svg)

The report gives the sequence and layer thicknesses only. It specifies **no temperatures, pressures, gas chemistries, doses, times, or rates**, and none are added here. The source of each value is marked.

---

## 1. Silicon substrate preparation

### Purpose
Provide the starting wafer on which active regions and isolation are defined.

### Material
p-type silicon, boron-doped at **1.4 × 10¹⁵ cm⁻³** (Reported), (100) orientation (Reported).

### Process
Uniform bulk doping. The surface is assumed atomically smooth, like a polished wafer, and defect-free, so that only process-induced defects appear (Reported, §3.3, §5.1).

### Geometry change
None. The domain is a flat silicon block. The screenshots show it as about 1 × 1 µm in footprint and 1.5 µm deep (Estimated).

### Output
A bare Si block. The report quotes ≈ 10 Ω·cm, and 9.7 Ω·cm is calculated with Masetti hole mobility ([`report_consistency_check.py`](../scripts/analysis/report_consistency_check.py)).

---

## 2. Pad oxide formation

### Purpose
A buffer between Si and Si₃N₄. It relieves the stress from their different elastic properties and lattice constants, which would otherwise create crystal defects (Reported, §3.2).

### Material
SiO₂, **12 nm** (Reported; the design range is 10–15 nm).

### Process
"Grown/deposited" thermal oxide (Reported). No conditions are given.

### Geometry change
A thin conformal oxide layer on the Si surface. The Si/SiO₂ transition region is not resolved in the simulation (Reported, §5.1).

### Output
Si + 12 nm pad oxide. This layer is too thin to measure in the screenshots.

---

## 3. Nitride mask deposition

### Purpose
A hard mask that protects the active regions during the silicon RIE, and later the CMP polish stop (Reported, §3.2).

### Material
LPCVD Si₃N₄, **120 nm** (Reported; the design range is 100–150 nm). The screenshots suggest ≈ 140–145 nm (Estimated).

### Process
LPCVD. It is chosen because it resists the F/Cl silicon-etch chemistry (Reported).

### Geometry change
A blanket nitride layer on top of the pad oxide.

### Output
A two-layer hard-mask stack (pad oxide + nitride).

---

## 4. Lithography and patterning

### Purpose
Define where isolation trenches will be etched.

### Material
Photoresist (not otherwise specified).

### Process
Exposure through the isolation mask, development, and pattern transfer through the nitride and pad oxide. The resist is then stripped, leaving the stack on the active regions (Reported, §3.2, §5.1).

### Geometry change
An opening in the hard mask exposes the silicon. In the 3D screenshots the opening is a **square** about 0.4 µm across (Estimated).

### Output
A patterned hard mask over bare silicon in the isolation region.

---

## 5. Anisotropic trench etching (RIE)

### Purpose
Cut the isolation trench into the silicon.

### Material
Silicon removed; the hard mask is retained.

### Process
Reactive ion etching. Directional ion bombardment plus chemical etching give near-vertical sidewalls (Reported). The report gives a target depth range of 200–300 nm.

### Geometry change

| | Reported | Estimated (screenshots) |
|---|---:|---:|
| Depth | 200 nm | ≈ 220–230 nm |
| Top width | 180 nm | ≈ 380–390 nm |
| Bottom width | ≈ 170 nm | ≈ 155–165 nm |
| Sidewall | ≈ 88° | ≈ 62–64° |
| Top-corner radius | ≈ 15 nm | not resolvable |

The trench is wider at the top (positive taper). The sharp top corners at the active-region edges are stress points, and oxidation is sometimes used to round them (Reported, §5.1).

### Output
An open trench with a flat floor. See [trench-etch.svg](../assets/trench-etch.svg).

---

## 6. Cone defect formation (residue masking)

### Purpose
Introduce a representative plasma-etch defect to study its effect. This is the step that distinguishes the project (Reported).

### Material
Si protrusion, with a crystalline core and flanks of residue or native oxide (Reported, §5.1).

### Process
A residue micromask protects silicon under etch-byproduct deposits while the floor around it is etched (Reported). It is implemented as an **explicit defect-introduction step**, not a plasma-chemistry simulation.

### Geometry change
Reported: a cone ≈ 100 nm high, ≈ 50 nm base, 8–12 nm tip radius, centred, with the tip at mid-trench depth. Screenshots: a ≈ 105–115 nm deep, ≈ 40–60 nm wide **recess below** the trench floor. See [cone-defect-formation.md](cone-defect-formation.md).

### Output
A trench containing the defect feature (`ConeDefect_fps_geometry`).

---

## 7. Liner oxidation (optional)

### Purpose
A shallow thermal oxidation that anneals surface damage and rounds corners (Reported, §3.2).

### Status
Marked **optional** in the report. Whether it was simulated cannot be determined, because a liner would be indistinguishable from the fill oxide in the screenshots.

---

## 8. HDP oxide deposition

### Purpose
Fill the trench with isolation dielectric.

### Material
HDP-CVD SiO₂, **400 nm** (Reported), with trace fluorine doping for better gap fill (Reported).

### Process
Simultaneous deposition and sputter-etch fill the trench from the bottom up and limit void formation. Material redistributes from fast-deposition to slow-deposition areas (Reported, §5.1).

### Geometry change
The trench and hard-mask opening fill, with overburden above the nitride. The report states that the oxide **over the cone tip is thinner than on its flanks**.

### Output
A filled trench with overburden.

---

## 9. CMP planarization (and nitride removal)

### Purpose
Remove the oxide above the hard mask and planarize.

### Process
Abrasive polishing that stops on the nitride. The nitride is then removed selectively in hot phosphoric acid (Reported, §3.2). The CMP removal rate is given only as "Standard".

### Geometry change
Reported: a planar surface with < 5 nm variation, the STI oxide level with the silicon, and the cone untouched inside the trench. Screenshots: nitride still present; the fill top sits ≈ 70 nm (FinalSTI) or ≈ 20 nm (final_structure) below the nitride top, and final_structure has ≈ 43 nm of oxide on the nitride (Estimated).

### Output
The final STI structure with an embedded defect. See [cmp-flow.svg](../assets/cmp-flow.svg) and [final-structure.svg](../assets/final-structure.svg).
