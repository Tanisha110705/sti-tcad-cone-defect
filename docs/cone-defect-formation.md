# Cone Defect Formation

![Cone defect formation](../assets/defect-formation.svg)

## Mechanism (as described in the report)

During silicon RIE the plasma holds etchant radicals (F, Cl), polymerizing species, and energetic ions. Small fragments of resist, nitride, or polymerized byproduct can redeposit on the trench floor. If a deposit resists the etch, it becomes a **micromask**:

1. **The residue lands** on the exposed silicon floor.
2. **The silicon under it is protected** from the directional, ion-assisted etch.
3. **The surrounding silicon keeps etching**, so the protected column stands proud of the receding floor. Lateral erosion of the residue narrows its top over time, which tapers the column.
4. **A silicon cone or spike remains**, with a sharp tip. Its final shape depends on the competition between the vertical Si etch rate and the lateral erosion of the mask deposit (Reported, §2.2, §7.1).

The report notes that literature SEM/TEM studies find tip radii of about 5–20 nm and heights from tens to hundreds of nanometres (§2.2). This is literature context, not a project measurement.

## How the defect was modelled in this project

| Question | Answer | Evidence |
|---|---|---|
| Emerges naturally from an etch-physics model? | **No** | Report §3.2: "Cone Defect Introduction: the analytical distinguishing step" |
| Inserted explicitly as a process step? | **Yes** | same |
| Physics of residue deposition modelled? | No | No such model is named |

## Reported geometry

![Cone geometry](../assets/cone-defect.svg)

| Parameter | Value | Source |
|---|---:|---|
| Height | ≈ 100 nm | Reported (§4.3, §6.1) |
| Base diameter | ≈ 50 nm | Reported (§6.1) |
| Tip radius | ≈ 8–12 nm (~10 nm in the table) | Reported |
| Height : base | 2 : 1 | Reported; 2.0 Calculated |
| Position | Centred on the trench floor; tip at mid-trench depth | Reported (§6.1) |
| Composition | Crystalline Si core; residue or native-oxide flanks | Reported (§5.1) |
| After fill | Coated by HDP oxide, thinner over the tip than on the flanks | Reported (§5.1) |
| After CMP | Embedded and untouched | Reported (§5.1, §6.4) |

## What the Sentaurus screenshots show

![Comparison](../assets/defect-comparison.svg)

In all three cut planes (`assets/tcad/*-2d.png`) the defect-related feature is a **narrow, vertical recess below the trench floor**, not an upward cone:

| | Estimate |
|---|---:|
| Depth below main trench floor | ≈ 105–115 nm |
| Width | ≈ 40–60 nm (2–4 px wide, the least certain value) |
| Content after etch | Gas (empty) |
| Content after fill | Oxide |
| Upward silicon spike visible? | No |

### Possible explanations (not resolvable without the command file)

- The defect was implemented by etching through an opening in a "residue" mask, which is compatible with the report's wording *"a masking residue is then used and etched through to partially expose the silicon"*. That would cut a hole rather than leave a pillar.
- The screenshots may show a different version of the structure than the one the report's §6.1 numbers describe.
- The Y = 0.5 cut plane may not pass through an upward feature. This is unlikely for a centred defect.

The report's text is **not** rewritten to match the screenshots, and the screenshots are **not** relabelled as showing a cone. Both are presented as they are.

## Why the defect matters

A conducting silicon protrusion with a ~10 nm tip, buried in the isolation oxide, causes two problems:

- **Less dielectric over the tip.** Oxide thinning gives a 1 / t field increase.
- **Field-line crowding at the tip.** Curvature gives an enhancement factor β.

See [oxide-thinning.md](oxide-thinning.md) and [electric-field-analysis.md](electric-field-analysis.md).

## Mitigation (from report §7.3; not simulated)

- **Plasma chemistry:** a higher etchant-to-passivant ratio means less redeposition, provided anisotropy is kept.
- **Post-etch cleaning:** wet acid and base sequences remove deposits before cones grow.
- **Sacrificial oxidation and strip:** this consumes small cones, and the report says it is most effective below ≈ 20 nm.
- **Trench-corner rounding:** this reduces perimeter stress and field, but does not address bottom cones.
- **High-quality liner oxide:** this gives a more uniform dielectric at the trench bottom and partly compensates for thinning.
