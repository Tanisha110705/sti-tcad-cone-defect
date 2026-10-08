# Local Oxide Thinning

![Oxide thinning](../assets/oxide-thinning.svg)

> All thickness values on this page are **reported in project documentation**. None were extracted from a TCAD structure in this repository.

## Reported values

| Quantity | Value | Report section |
|---|---:|---|
| Oxide thickness at the trench bottom ("nominal") | ~150 nm | §6.1, §6.3, §9 |
| Oxide thickness above the cone tip | 50–70 nm | §6.1 |
| Minimum oxide in the comparison table | ~60 nm | §6.3 |
| Stated reduction | "more than 50 %"; "−60 %" | §6.1, §6.3, §9 |

## Calculated consequences

| Calculation | Result |
|---|---:|
| Reduction 150 → 70 nm | 53 % |
| Reduction 150 → 60 nm | 60 % |
| Reduction 150 → 50 nm | 67 % |
| Field ratio for the same voltage, E ∝ 1 / t (150 / 70) | ×2.1 |
| Field ratio for the same voltage, E ∝ 1 / t (150 / 50) | ×3.0 |

The field ratios use a uniform parallel-plate approximation. They isolate the effect of thickness alone, **before** any geometric field enhancement at the tip.

## Why thinner oxide matters

For a voltage difference V across the isolation dielectric, the average field is E ≈ V / t_ox. Cutting t_ox by 53–67 % raises the field in that region 2–3×. Tunneling leakage (Fowler-Nordheim current rises steeply with E) and time-to-breakdown both depend strongly on field, so the thinnest point controls the reliability of the whole isolation structure. The sharp tip adds field crowding on top of this (see [electric-field-analysis.md](electric-field-analysis.md)).

The report explains the thinning through HDP-CVD redistribution: deposition plus sputter-etch leaves less oxide on top of a protrusion than on its flanks (§5.1).

## Geometric consistency caveat

The two reported thicknesses cannot be reproduced from the reported geometry under any single, obvious definition:

| Interpretation | Calculated thickness | Reported |
|---|---:|---:|
| Vertical oxide at the floor, fill flush with Si | 200 nm | ~150 nm |
| Vertical oxide above a tip at mid-depth, fill flush with Si | 100 nm | 50–70 nm |
| Same, fill flush with nitride top (before strip) | 232 nm | 50–70 nm |
| Lateral gap from tip to sidewall at tip height, minus r = 10 nm | ≈ 77 nm | 50–70 nm |

The report does not say how or where the thicknesses were measured, and the TCAD structure is not available to re-measure them. The values are therefore kept as **reported** and are not presented as extracted or simulated. The available screenshots show no upward silicon tip at all (see [cone-defect-formation.md](cone-defect-formation.md)), so they cannot be used to check the values either.

## What would settle it

Re-open the final `.tdr` and take a cutline straight up from the cone tip to the top oxide surface, plus a horizontal cutline at tip height to the sidewall. Report both, and compare with the same cutlines in a defect-free reference structure.
