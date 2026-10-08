# Electric-Field Analysis

![Electric field concept](../assets/electric-field.svg)

> **No electric-field simulation was performed in this project.** The figure above is a conceptual sketch. The only field-related number, β ≈ 10, is an estimate stated in the report, and the report itself lists Sentaurus Device field calculation as future work (§10.1).

## Physics

A silicon protrusion is a conductor (doped Si) embedded in a dielectric. Field lines from an opposing electrode end on its surface. Where the surface is sharply curved, they crowd together, so the local field at the tip exceeds the average field in the oxide:

```
E_tip ≈ β · E_avg ,   E_avg ≈ V / t_ox
```

Two independent factors raise E_tip:

| Factor | Effect | Value |
|---|---|---|
| Oxide thinning (t_ox 150 → 50–70 nm) | Raises E_avg | ×2.1–3.0 (Calculated, [oxide-thinning.md](oxide-thinning.md)) |
| Tip curvature (r ≈ 8–12 nm, h ≈ 100 nm) | Sets β | β ≈ 10 (Reported estimate) |

They multiply. That is why the report singles out the cone tip as the most vulnerable point in the STI structure.

## The β ≈ 10 estimate

| Item | Value | Status |
|---|---:|---|
| β stated in report (§6.2) | ≈ 10 | Reported estimate, "using the shape" |
| First-order protrusion estimate h / r | 100 / 10 = 10 | Calculated |
| Range for r = 8–12 nm | 8.3–12.5 | Calculated |
| Literature range cited in report (§2.3) | 3–8× | Reported literature context |

The report does not say which formula it used. h / r reproduces its number, but that is an assumption, and h / r is a crude upper-bound-style approximation for an isolated protrusion. A real β depends on the opposing electrode distance, the oxide thickness, and the cone angle, and needs a field solution.

## Field values in the report

The report states that, with β = 10, "local fields at the cone tip could reach 80–100 MV/cm" (§6.2). Working backwards, that requires E_avg = 8–10 MV/cm, which is about the SiO₂ breakdown field the report quotes (10 MV/cm). No applied voltage or operating condition is defined, so these numbers are **not** project results and are not repeated as such elsewhere in this repository.

## What would turn this into a result

1. Import the final structure into Sentaurus Device, with contacts on the active regions, substrate, and any conductor above the STI.
2. Apply a defined isolation bias.
3. Extract |E| along a cutline from the cone tip to the opposing electrode, and the peak |E| at the tip.
4. Compute β = E_tip / E_avg against a defect-free reference structure at the same bias.
5. Sweep the tip radius and height.
