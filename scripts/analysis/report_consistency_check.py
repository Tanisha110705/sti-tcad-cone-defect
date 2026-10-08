#!/usr/bin/env python3
"""Cross-check the numbers stated in the project report against each other.

Every input below is a value REPORTED in the project report (VLSI Technology
Submission, sections 4.3 and 6.1). Nothing here is a TCAD extraction. The
script only performs transparent arithmetic so that a reader can see which
reported numbers are mutually consistent and which cannot be reconciled with
the stated geometry.

Usage:
    python3 scripts/analysis/report_consistency_check.py

Requires: Python 3 standard library only.
"""

import math

Q = 1.602e-19  # C

# ---- Reported values (report section 4.3 table and section 6.1) -------------
N_A = 1.4e15            # cm^-3, boron
PAD_OX = 12.0           # nm
NITRIDE = 120.0         # nm
DEPTH = 200.0           # nm
TOP_W = 180.0           # nm
BOTTOM_W = 170.0        # nm (6.1)
SIDEWALL = 88.0         # deg from horizontal (6.1)
CONE_H = 100.0          # nm
CONE_BASE = 50.0        # nm (6.1)
TIP_R = (8.0, 10.0, 12.0)  # nm (6.1 gives 8-12, table gives ~10)
OX_NOMINAL = 150.0      # nm, "oxide thickness at the trench bottom" (6.1)
OX_TIP = (50.0, 60.0, 70.0)  # nm, "oxide above the cone tip" (6.1; 60 nm in 6.3/9)
BETA = 10.0             # reported estimate (6.2)


def row(check, value, reported, verdict):
    print(f"| {check} | {value} | {reported} | {verdict} |")


def main():
    print("| Check | Calculated | Reported | Verdict |")
    print("|---|---:|---:|---|")

    ar = DEPTH / TOP_W
    row("Trench aspect ratio = depth / top width", f"{ar:.2f}", "~1.1", "consistent")

    bw = TOP_W - 2 * DEPTH / math.tan(math.radians(SIDEWALL))
    row("Bottom width implied by 88 deg sidewalls", f"{bw:.0f} nm", "170 nm", "consistent within rounding")

    ang = math.degrees(math.atan(DEPTH / ((TOP_W - BOTTOM_W) / 2)))
    row("Sidewall angle implied by 180 -> 170 nm over 200 nm", f"{ang:.1f} deg", "88 deg", "consistent")

    row("Cone height / base diameter", f"{CONE_H / CONE_BASE:.1f}", "2:1", "consistent")

    betas = [CONE_H / r for r in TIP_R]
    row("First-order beta ~ h / r_tip (r = 12, 10, 8 nm)",
        f"{betas[2]:.1f} / {betas[1]:.1f} / {betas[0]:.1f}", "~10",
        "consistent with h/r; report does not state its method")

    red = [(OX_NOMINAL - t) / OX_NOMINAL * 100 for t in OX_TIP]
    row("Oxide reduction 150 nm -> 50 / 60 / 70 nm", f"{red[0]:.0f} / {red[1]:.0f} / {red[2]:.0f} %",
        "> 50 %, -60 %", "consistent")

    # Hole mobility (Masetti model, 300 K) -> resistivity
    mu = 44.9 + (470.5 - 44.9) / (1 + (N_A / 2.23e17) ** 0.719)
    rho = 1 / (Q * N_A * mu)
    row("Resistivity of 1.4e15 cm^-3 boron (Masetti mobility)", f"{rho:.1f} ohm-cm", "~10 ohm-cm", "consistent")

    # Oxide-thickness geometry
    row("Oxide from trench floor to Si surface (fill level with Si)", f"{DEPTH:.0f} nm", "~150 nm",
        "NOT reproduced: definition of 'nominal' thickness unclear")
    over_tip_si = DEPTH - CONE_H
    over_tip_stack = over_tip_si + PAD_OX + NITRIDE
    row("Vertical oxide above tip (fill level with Si surface)", f"{over_tip_si:.0f} nm", "50-70 nm",
        "NOT reproduced")
    row("Vertical oxide above tip (fill level with nitride top)", f"{over_tip_stack:.0f} nm", "50-70 nm",
        "NOT reproduced")
    half_w = (TOP_W - 2 * (DEPTH - CONE_H) / math.tan(math.radians(SIDEWALL))) / 2
    row("Lateral tip-to-sidewall distance at tip height (minus r = 10 nm)",
        f"{half_w - 10:.0f} nm", "50-70 nm", "closest interpretation, still not equal")

    row("Average oxide field implied by 80-100 MV/cm local field at beta = 10",
        "8-10 MV/cm", "no bias stated", "not derivable: no applied voltage in report")

    print("\nAll inputs are reported values; outputs are calculations, not simulations.")


if __name__ == "__main__":
    main()
