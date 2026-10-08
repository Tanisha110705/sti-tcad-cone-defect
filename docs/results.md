# Results

Every number in this repository appears below with its source.

| Tag | Meaning |
|---|---|
| **Reported** | Stated in the project report; not re-extracted |
| **Estimated** | Pixel measurement of the Sentaurus Visual screenshots, ±10–15 nm ([csv](../results/screenshot-measurements.csv)) |
| **Calculated** | Arithmetic on reported values ([check](../results/report-consistency-check.md)) |

No value on this page is **Simulated** in the sense of being extracted from a TCAD structure file in this repository. No value is **Measured** on hardware.

## Process parameters

| Parameter | Value | Source |
|---|---:|---|
| Technology node | 180 nm CMOS (educational reference) | Reported |
| Substrate | p-Si (100), boron | Reported |
| Substrate doping | 1.4 × 10¹⁵ cm⁻³ | Reported |
| Substrate resistivity | ≈ 10 Ω·cm / 9.7 Ω·cm | Reported / Calculated |
| Pad oxide | 12 nm | Reported |
| Si₃N₄ hard mask | 120 nm | Reported |
| Si₃N₄ hard mask (screenshots) | ≈ 140–145 nm | Estimated |
| HDP oxide | 400 nm | Reported |
| CMP removal rate | "Standard" (no value) | Reported |

## Trench geometry

| Metric | Value | Source |
|---|---:|---|
| Depth | 200 nm | Reported |
| Top width | 180 nm | Reported |
| Bottom width | ≈ 170 nm | Reported |
| Bottom width implied by 88° | 166 nm | Calculated |
| Sidewall angle | ≈ 88° | Reported |
| Aspect ratio | ~1.1 / 1.11 | Reported / Calculated |
| Top-corner radius | ≈ 15 nm | Reported |
| Depth (screenshots) | ≈ 220–230 nm | Estimated |
| Opening at Si surface (screenshots) | ≈ 380–390 nm | Estimated |
| Bottom width (screenshots) | ≈ 155–165 nm | Estimated |
| Sidewall angle (screenshots) | ≈ 62–64° | Estimated |

## Cone geometry

| Metric | Value | Source |
|---|---:|---|
| Height | ≈ 100 nm | Reported |
| Base diameter | ≈ 50 nm | Reported |
| Tip radius | ≈ 8–12 nm (table ~10 nm) | Reported |
| Height : base | 2 : 1 | Reported / Calculated |
| Defect feature in screenshots | recess ≈ 105–115 nm deep, ≈ 40–60 nm wide, **below** floor | Estimated |

## Oxide thickness

| Metric | Value | Source |
|---|---:|---|
| Nominal trench-bottom oxide | ~150 nm | Reported |
| Oxide over cone tip | 50–70 nm (≈ 60 nm) | Reported |
| Local reduction | 53–67 % | Calculated |
| Field increase from thinning, same V | ×2.1–3.0 | Calculated |

## Surface planarity

| Metric | Value | Source |
|---|---:|---|
| Height variation after CMP | < 5 nm | Reported |
| Fill top vs. nitride top (FinalSTI) | ≈ −72 nm | Estimated |
| Fill top vs. nitride top (final_structure) | ≈ −18 nm, ≈ 43 nm oxide on nitride | Estimated |

## Electric field

| Metric | Value | Source |
|---|---:|---|
| Field-enhancement factor β | ≈ 10 | Reported estimate (method not stated) |
| h / r_tip | 10 (8.3–12.5 for r = 12–8 nm) | Calculated |
| Simulated field distribution | – | **None** |

## Reliability interpretation

| Item | Status |
|---|---|
| Thinned oxide plus sharp tip give the highest local dielectric stress at the cone | Reasoned from reported geometry |
| TAT / FN leakage increase | Discussed, not simulated |
| Tensile oxide / compressive Si stress near the tip | Discussed, not simulated |
| Premature breakdown | Discussed, not simulated |
| TDDB, SILC, HCI | Discussed as test methods, not simulated |
| Breakdown voltage, leakage ratio, lifetime ratio (report §6.3) | **Excluded**: no method or simulation behind them |
