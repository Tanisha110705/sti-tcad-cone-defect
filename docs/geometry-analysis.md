# Geometric Analysis

Three sources are used and kept separate:

- **Reported:** report §4.3 and §6.1.
- **Estimated:** pixel measurement of the three Sentaurus Visual cut planes, from [`results/screenshot-measurements.csv`](../results/screenshot-measurements.csv). Resolution is 4.8–6.6 nm/px, and each length carries about ±2 px (±10–15 nm).
- **Calculated:** arithmetic on reported values, from [`results/report-consistency-check.md`](../results/report-consistency-check.md).

## Trench geometry

| Feature | Reported | Calculated from reported | Estimated: ConeDefect | Estimated: FinalSTI | Estimated: final_structure |
|---|---:|---:|---:|---:|---:|
| Depth (main trench) | 200 nm | – | 220 nm | 226 nm | 232 nm |
| Width at Si surface | 180 nm | – | 378 nm | 382 nm | 390 nm |
| Bottom width | ≈ 170 nm | 166 nm (from 88°) | 166 nm | 155 nm | 159 nm |
| Sidewall angle | ≈ 88° | 88.6° (from widths) | 62.0° / 63.9° | 62.6° / 62.8° | 62.5° / 62.8° |
| Aspect ratio | ~1.1 | 1.11 | ≈ 0.58 | ≈ 0.59 | ≈ 0.59 |
| Top-corner radius | ≈ 15 nm | – | not resolvable | not resolvable | not resolvable |

**Interpretation.** The reported numbers are self-consistent. The screenshots, however, show a trench about twice as wide at the top with a strong (~62–64°) taper. The two sets do not describe the same geometry. The README and diagrams show the reported values, labelled as reported, and give the screenshot values alongside.

## Cone geometry

| Feature | Reported | Calculated | Estimated (screenshots) |
|---|---:|---:|---|
| Height | ≈ 100 nm | – | No upward cone visible. The recess below the floor is ≈ 104–113 nm deep |
| Base diameter | ≈ 50 nm | – | Recess width ≈ 44–61 nm |
| Tip radius | ≈ 8–12 nm | – | Not resolvable (< 2 px) |
| Height : base | 2 : 1 | 2.0 | – |
| Tip height | mid-trench depth | 100 nm above the floor of a 200 nm trench | – |

## Oxide geometry

| Feature | Reported | Calculated / comment |
|---|---:|---|
| Nominal oxide at trench bottom | ~150 nm | A 200 nm trench filled flush with Si gives 200 nm. The definition of "nominal" is unclear |
| Oxide above cone tip | 50–70 nm (≈ 60 nm in §6.3, §9) | Vertical oxide above a mid-depth tip is 100 nm (flush with Si) or 232 nm (flush with nitride). The lateral tip-to-sidewall gap is ≈ 77 nm |
| Local thinning | "> 50 %", "−60 %" | 53–67 % |

See [oxide-thinning.md](oxide-thinning.md) for the discussion.

## Surface planarity

| Feature | Reported | Estimated (screenshots) |
|---|---:|---:|
| Height variation after CMP | < 5 nm | – |
| Fill top relative to nitride top (FinalSTI) | – | −72 nm |
| Fill top relative to nitride top (final_structure) | – | −18 nm |
| Oxide left on nitride (final_structure) | – | ≈ 43 nm |
| Nitride removed? | Yes (§3.2, §5.2) | No: nitride visible in all post-fill views |

The < 5 nm figure is a reported value that the screenshots do not reproduce. A step of tens of nanometres between fill and nitride is typical of an STI stage **before** nitride strip. The screenshots show no post-strip structure.

## Method notes (screenshot measurement)

- Material classes come from Sentaurus Visual's default colours: Si slate grey, nitride yellow, oxide cyan, gas white.
- Calibration: the silicon block spans Z = 1 → 0 µm and X = 0 → 1.5 µm. Horizontal and vertical scales agree to within 5 %.
- Sidewall angle: a linear fit of each trench edge over the middle 50 % of the main trench depth.
- Recess: the rows where the opening collapses below 40 % of the surface opening width.
- Region-boundary lines (1–2 px, dark) are counted as part of the trench edge. This biases widths by about +1 to 2 px.
