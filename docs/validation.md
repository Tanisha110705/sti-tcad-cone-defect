# Validation

## What the report proposes (§4.4)

The report states it validates the simulation results against published experimental data and established process models, using these metrics:

| Metric | Proposed reference |
|---|---|
| Trench depth and sidewall angle | SEM cross-sections from literature |
| Oxide fill quality | Void-fill criteria |
| Surface planarity after CMP | Profilometry data |

## What actually exists

| Item | Present in report? | Present in repository? |
|---|---|---|
| SEM image or overlay | No | No |
| TEM image | No | No |
| Profilometry data | No | No |
| Literature numbers compared against simulated numbers | No | No |
| Defect-free reference simulation | No | No |
| Internal consistency of reported numbers | – | Yes ([`report-consistency-check.md`](../results/report-consistency-check.md)) |
| Comparison of reported numbers with the TCAD screenshots | – | Yes ([geometry-analysis.md](geometry-analysis.md)); they **disagree** |

## Conclusion

The report proposes validation against published experimental and process-model data, but no such comparison appears in the report or in this repository. The project is **not** experimentally validated. The one cross-check that could be made, report numbers against the report's own Sentaurus screenshots, shows significant differences in trench taper, width, and defect shape.

## Suggested validation plan

1. Restore the Sentaurus command file and `.tdr` files to the repository.
2. Extract trench depth, top and bottom width, and sidewall angle with cutlines, and compare them with published 180 nm STI SEM cross-sections (cite the source).
3. Compare simulated cone height and tip radius with the literature range the report quotes (r ≈ 5–20 nm).
4. Check fill: confirm there are no voids in the trench or around the defect.
5. Check planarity: extract the step height between oxide and Si after nitride strip.
