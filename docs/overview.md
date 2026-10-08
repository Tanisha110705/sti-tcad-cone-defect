# Overview

## What the project is

This is a process-level TCAD study of Shallow Trench Isolation at a 180 nm educational reference node. A full STI module was modelled in Synopsys Sentaurus Process, and one process-induced defect was inserted on purpose: a residue-micromasked **cone (spike) defect** at the trench bottom. The study then looks at how that defect changes the isolation dielectric, through **local oxide thinning** and **electric-field enhancement**, and what that means for reliability.

This is **not** a transistor or circuit design project. Its subject is a front-end isolation process module.

## The story

```
STI process flow → trench formation → residue / micromasking → cone defect
   → HDP oxide fill → CMP → final STI geometry → geometric analysis
   → local oxide thinning → electric-field enhancement → reliability risk
```

## Evidence map

| Link in the story | Evidence available | Status |
|---|---|---|
| Process flow | Report §2.2, §3.2, §5.1 | Reported |
| Trench formation | Report §6.1, plus 3 Sentaurus screenshots | Reported, with a screenshot estimate that **differs** |
| Micromasking → cone | Report §2.2, §5.1, §7.1 | Reported mechanism; the defect was inserted explicitly |
| Cone geometry | Report §4.3, §6.1 | Reported; the screenshots show a recess instead |
| HDP fill, CMP | Report §3.2, §5.1; screenshots after fill | Reported, with a screenshot estimate that **differs** (planarity) |
| Oxide thinning | Report §6.1, §6.3 | Reported; not reproducible from the stated geometry |
| Field enhancement | Report §6.2 (β ≈ 10 estimate) | Estimate; **no field simulation** |
| Reliability | Report §6.2, §8.2 | Discussion only; **nothing simulated** |
| Validation | Report §4.4 (proposed) | **Not performed** |

## Where to look next

- [audit.md](audit.md): what exists, what is missing, every inconsistency
- [sti-process-flow.md](sti-process-flow.md): stage-by-stage flow
- [geometry-analysis.md](geometry-analysis.md): numbers, reported vs. estimated
- [results.md](results.md): one table with every number and its source
