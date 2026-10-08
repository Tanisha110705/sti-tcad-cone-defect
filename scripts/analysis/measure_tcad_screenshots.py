#!/usr/bin/env python3
"""Estimate STI geometry from the Sentaurus Visual cut-plane screenshots.

The original TCAD structure files (.tdr) are NOT in this repository. The only
genuine simulation evidence available is three low-resolution Sentaurus Visual
screenshots reproduced in the project report. This script measures the 2D
cut-plane panels of those screenshots (assets/tcad/*-2d.png) by classifying
pixel colours and converting pixel distances to micrometres using the plot's
own axis frame.

Calibration
-----------
In every cut plane the silicon block spans Z = 1 -> 0 um horizontally and
X = 0 -> 1.5 um vertically (tick labels at the block edges). Pixel-per-um is
therefore taken from the silicon block's width (1.0 um) and from the distance
between the silicon surface and the block bottom (1.5 um). Agreement between the
horizontal and vertical scales is printed as a sanity check.

Accuracy
--------
One pixel is roughly 5-7 nm. Region boundaries are drawn as 1-2 px dark lines,
so every length below carries an uncertainty of about +/-2 px (~ +/-10-15 nm).
Layers thinner than ~3 px (e.g. the pad oxide) cannot be resolved. All results
are ESTIMATES FROM SCREENSHOTS, not extractions from TCAD structure files.

Usage
-----
    python3 scripts/analysis/measure_tcad_screenshots.py [--csv results/screenshot-measurements.csv]

Requires: Python 3, numpy, Pillow.
"""

import argparse
import csv
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

IMAGES = [
    ("cone-defect-etch-2d.png", "ConeDefect_fps_geometry (after trench etch + defect, before fill)"),
    ("sti-after-fill-2d.png", "Review1_Fig1_FinalSTI_fps_geometry (after oxide fill / planarization)"),
    ("final-structure-2d.png", "final_structure_fps_geometry (final structure)"),
]

DOMAIN_WIDTH_UM = 1.0   # Z = 1 -> 0
DOMAIN_DEPTH_UM = 1.5   # X = 0 -> 1.5


def classify(img):
    """Return boolean masks for silicon, nitride and 'trench fill' (oxide or gas)."""
    a = img.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    silicon = (abs(r - 120) < 25) & (abs(g - 144) < 25) & (abs(b - 156) < 25)
    nitride = (r > 180) & (g > 180) & (b < 170)
    oxide = (b > 200) & (g > 180) & (r < 120)
    gas = (r > 235) & (g > 235) & (b > 235)
    return silicon, nitride, oxide, gas


def runs(mask_row):
    """Contiguous True runs as (start, end_exclusive)."""
    out, start = [], None
    for i, v in enumerate(mask_row):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(mask_row)))
    return out


def measure(path):
    img = np.array(Image.open(path).convert("RGB"))
    si, ni, ox, gas = classify(img)
    h, w = si.shape

    # Silicon block extents (columns/rows that are mostly silicon).
    # Take the widest contiguous band of silicon-rich columns (ignores frame lines).
    left, right = max(runs(si.sum(axis=0) > 0.3 * h), key=lambda t: t[1] - t[0])
    si_rows = np.where(si[:, left:right].sum(axis=1) > 0.3 * (right - left))[0]
    bottom = si_rows.max() + 1

    # Silicon surface away from the trench = first silicon row in the outer 10 % columns.
    # (skip columns crossed by vertical region-boundary lines)
    band = range(left + 2, left + max(4, (right - left) // 6))
    counts = {c: si[:, c].sum() for c in band}
    edge_cols = [c for c in band if counts[c] >= 0.98 * max(counts.values())]
    # (first row that starts >= 10 px of uninterrupted silicon; ignores title text)
    def first_solid(c):
        col = si[:, c]
        return next(y for y in range(h - 10) if col[y:y + 10].all())

    surface = int(np.median([first_solid(c) for c in edge_cols]))

    px_per_um_h = (right - left) / DOMAIN_WIDTH_UM
    px_per_um_v = (bottom - surface) / DOMAIN_DEPTH_UM
    nm_h = 1000.0 / px_per_um_h
    nm_v = 1000.0 / px_per_um_v

    # Nitride thickness in the outer columns.
    nit = [ni[:, c].sum() for c in edge_cols]
    nitride_nm = float(np.median(nit)) * nm_v

    # Trench: oxide/gas run straddling the domain centre, row by row, below the
    # surface. Each edge is extended over at most 3 px of non-silicon boundary line.
    centre = (left + right) // 2
    fill = ox | gas
    widths = []
    for y in range(surface + 3, bottom):
        row = fill[y, left:right]
        rr = [(s + left, e + left) for s, e in runs(row) if s + left <= centre + 15 and e + left >= centre - 15]
        if not rr:
            break
        s, e = max(rr, key=lambda t: t[1] - t[0])
        for _ in range(3):
            if s > left and not si[y, s - 1]:
                s -= 1
            if e < right and not si[y, e]:
                e += 1
        widths.append((y, s, e))
    if not widths:
        raise RuntimeError(f"no trench found in {path}")

    w_px = np.array([e - s for _, s, e in widths])
    # The narrow notch starts where the width collapses below 40 % of the opening width.
    opening = w_px[0]
    notch_idx = next((i for i, v in enumerate(w_px) if v < 0.4 * opening), len(w_px))
    main = widths[:notch_idx]
    notch = widths[notch_idx:]

    trench_depth_nm = (main[-1][0] - surface + 1) * nm_v if main else float("nan")
    bottom_width_nm = (main[-1][2] - main[-1][1]) * nm_h if main else float("nan")
    top_width_nm = opening * nm_h
    notch_depth_nm = len(notch) * nm_v
    notch_width_nm = float(np.median([e - s for _, s, e in notch])) * nm_h if notch else float("nan")

    # Sidewall angle: linear fit of each edge between 25 % and 75 % of main-trench depth.
    n = len(main)
    seg = main[n // 4: 3 * n // 4] if n >= 8 else main
    ys = np.array([y for y, _, _ in seg], float)
    angles = []
    for xs in (np.array([s for _, s, _ in seg], float), np.array([e for _, _, e in seg], float)):
        slope = np.polyfit(ys * nm_v, xs * nm_h, 1)[0]  # nm lateral per nm depth
        angles.append(math.degrees(math.atan2(1.0, abs(slope))))

    # Planarity proxies: oxide surface in the trench opening vs. nitride top,
    # and any oxide left on top of the nitride (outer columns).
    def first_run(mask, c, n=5):
        col = mask[:, c]
        return next((y for y in range(h - n) if col[y:y + n].all()), None)

    nit_top = int(np.median([first_run(ni, c) for c in edge_cols]))
    fill_top = first_run(ox, centre)
    step_nm = (nit_top - fill_top) * nm_v if fill_top is not None else float("nan")
    ox_on_nit = [ox[:nit_top, c].sum() for c in edge_cols]
    ox_on_nit_nm = float(np.median(ox_on_nit)) * nm_v

    return {
        "nm_per_px_h": nm_h,
        "nm_per_px_v": nm_v,
        "nitride_nm": nitride_nm,
        "opening_at_si_surface_nm": top_width_nm,
        "main_trench_depth_nm": trench_depth_nm,
        "main_trench_bottom_width_nm": bottom_width_nm,
        "sidewall_angle_left_deg": angles[0],
        "sidewall_angle_right_deg": angles[1],
        "notch_depth_below_floor_nm": notch_depth_nm,
        "notch_width_nm": notch_width_nm,
        "total_depth_nm": trench_depth_nm + notch_depth_nm,
        "fill_top_above_nitride_top_nm": step_nm,
        "oxide_on_nitride_nm": ox_on_nit_nm,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", help="write results to this CSV path")
    args = ap.parse_args()

    rows = []
    for fname, label in IMAGES:
        path = os.path.join(ROOT, "assets", "tcad", fname)
        m = measure(path)
        rows.append((fname, label, m))
        print(f"\n{fname}  [{label}]")
        for k, v in m.items():
            print(f"  {k:32s} {v:8.1f}")

    print("\nAll values are estimates from low-resolution screenshots (+/- ~2 px).")

    if args.csv:
        keys = list(rows[0][2].keys())
        with open(args.csv, "w", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["image", "panel"] + keys)
            for fname, label, m in rows:
                wr.writerow([fname, label] + [f"{m[k]:.1f}" for k in keys])
        print(f"wrote {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
