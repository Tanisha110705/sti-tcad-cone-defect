#!/usr/bin/env python3
"""Generate the conceptual SVG diagrams in assets/.

These are CONCEPTUAL engineering drawings, not Sentaurus output. Cross-sections
are drawn to the dimensions REPORTED in the project report (section 4.3 table and
section 6.1); the "TCAD screenshot" panel of defect-comparison.svg uses the
estimates produced by scripts/analysis/measure_tcad_screenshots.py.

Usage:
    python3 scripts/figures/make_diagrams.py

Requires: Python 3 standard library only.
"""

import math
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))

# ---- Reported geometry (nm) -------------------------------------------------
PAD, NIT = 12, 120
DEPTH, TOP_W = 200, 180
SIDEWALL = 88.0
BOT_W = TOP_W - 2 * DEPTH / math.tan(math.radians(SIDEWALL))  # ~166 nm
CONE_H, CONE_BASE, TIP_R = 100, 50, 10
ACTIVE = 150           # drawn width of each active region (schematic choice)
SUB = 330              # drawn substrate depth below surface (schematic choice)

# ---- Palette ----------------------------------------------------------------
C = {
    "si": "#8a9ea8", "si_edge": "#5d727c",
    "ox": "#a8e6f2", "ox_edge": "#3fa7bd",
    "pad": "#56c3d8",
    "nit": "#e6dc84", "nit_edge": "#a59a3a",
    "resist": "#d7a7d9", "resist_edge": "#8e5a91",
    "residue": "#7a2e1d",
    "ink": "#1f2a30", "muted": "#5b6770", "accent": "#c0392b",
    "blue": "#1f6fb2", "bg": "#ffffff", "panel": "#f5f7f8", "line": "#c9d2d7",
}
FONT = "Helvetica, Arial, sans-serif"


# ---- SVG helpers ------------------------------------------------------------
def svg(w, h, body, title, desc):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}" role="img" aria-labelledby="t d">\n'
        f"<title id=\"t\">{title}</title>\n<desc id=\"d\">{desc}</desc>\n"
        "<defs>\n"
        f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{C["ink"]}"/></marker>\n'
        f'<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{C["accent"]}"/></marker>\n'
        f'<marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{C["blue"]}"/></marker>\n'
        "</defs>\n"
        f'<rect width="{w}" height="{h}" fill="{C["bg"]}"/>\n{body}</svg>\n'
    )


def text(x, y, s, size=13, anchor="start", weight="normal", fill=None, italic=False):
    fill = fill or C["ink"]
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{st}>{escape(s)}</text>\n')


def rect(x, y, w, h, fill, stroke="none", sw=1, rx=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>\n')


def poly(pts, fill, stroke="none", sw=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>\n'


def path(d, fill="none", stroke=None, sw=1.5, marker=None, dash=None):
    stroke = stroke or C["ink"]
    m = f' marker-end="url(#{marker})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{m}{da}/>\n'


def line(x1, y1, x2, y2, stroke=None, sw=1.5, marker=None, dash=None, both=False):
    stroke = stroke or C["ink"]
    m = f' marker-end="url(#{marker})"' if marker else ""
    if both and marker:
        m += f' marker-start="url(#{marker})"'
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{sw}"{m}{da}/>\n')


def box(x, y, w, h, lines, fill=None, stroke=None, dash=None, size=13, bold_first=True):
    out = rect(x, y, w, h, fill or C["panel"], stroke or C["line"], 1.2, rx=8, dash=dash)
    n = len(lines)
    lh = size + 4
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        out += text(x + w / 2, y0 + i * lh, s, size, "middle", "bold" if (i == 0 and bold_first) else "normal",
                    C["ink"] if i == 0 else C["muted"])
    return out


def footer(w, h, s):
    return text(w / 2, h - 10, s, 11, "middle", fill=C["muted"], italic=True)


# ---- Cross-section builder (all inputs in nm, output in px) -----------------
class XS:
    """STI cross-section drawn at scale `k` px/nm with Si surface at (x0, y0).

    x = 0 is the left edge of the left active region; trench is centred.
    """

    def __init__(self, x0, y0, k, active=ACTIVE, sub=SUB):
        self.x0, self.y0, self.k, self.active, self.sub = x0, y0, k, active, sub
        self.W = 2 * active + TOP_W
        self.cx = active + TOP_W / 2

    def P(self, x, y):
        return (self.x0 + x * self.k, self.y0 + y * self.k)

    def pts(self, seq):
        return [self.P(x, y) for x, y in seq]

    def trench_pts(self):
        a, W = self.active, self.W
        bl = self.cx - BOT_W / 2
        br = self.cx + BOT_W / 2
        return [(0, 0), (a, 0), (bl, DEPTH), (br, DEPTH), (a + TOP_W, 0), (W, 0)]

    def silicon(self, trench=False, cone=False, notch=None):
        W, S = self.W, self.sub
        if not trench:
            seq = [(0, 0), (W, 0), (W, S), (0, S)]
            return poly(self.pts(seq), C["si"], C["si_edge"], 1)
        t = self.trench_pts()
        floor = [t[2]]
        if cone:
            half = CONE_BASE / 2
            floor += [(self.cx - half, DEPTH)] + self.cone_tip_pts() + [(self.cx + half, DEPTH)]
        if notch:
            nw, nd = notch
            floor += [(self.cx - nw / 2, DEPTH), (self.cx - nw / 2, DEPTH + nd),
                      (self.cx + nw / 2, DEPTH + nd), (self.cx + nw / 2, DEPTH)]
        floor += [t[3]]
        seq = [t[0], t[1]] + floor + [t[4], t[5], (W, S), (0, S)]
        return poly(self.pts(seq), C["si"], C["si_edge"], 1)

    def cone_tip_pts(self, n=9):
        """Left flank -> rounded tip (radius TIP_R) -> right flank."""
        half = CONE_BASE / 2
        tip_y = DEPTH - CONE_H
        # flank tangent to tip circle; approximate by arc between flank angles
        ang = math.atan2(CONE_H, half)  # flank angle from horizontal
        cy = tip_y + TIP_R
        # (approximation: arc spans the flank-normal directions; flanks join its ends)
        out = []
        # sweep from the left-flank normal over the top to the right-flank normal
        for i in range(n):
            th = (math.pi - ang) - i * (math.pi - 2 * ang) / (n - 1)
            out.append((self.cx + TIP_R * math.cos(th), cy - TIP_R * math.sin(th)))
        return out

    def pad_nitride(self, opened=False, nitride=True):
        a, W = self.active, self.W
        out = ""
        segs = [(0, a), (a + TOP_W, W)] if opened else [(0, W)]
        for x1, x2 in segs:
            out += poly(self.pts([(x1, -PAD), (x2, -PAD), (x2, 0), (x1, 0)]), C["pad"], C["ox_edge"], 0.8)
            if nitride:
                out += poly(self.pts([(x1, -PAD - NIT), (x2, -PAD - NIT), (x2, -PAD), (x1, -PAD)]),
                            C["nit"], C["nit_edge"], 1)
        return out

    def resist(self, opened=True, thick=60):
        a, W = self.active, self.W
        top = -PAD - NIT
        segs = [(0, a), (a + TOP_W, W)] if opened else [(0, W)]
        return "".join(poly(self.pts([(x1, top - thick), (x2, top - thick), (x2, top), (x1, top)]),
                            C["resist"], C["resist_edge"], 1) for x1, x2 in segs)

    def oxide_fill(self, top, cone=False, notch=None, overburden=False):
        """Oxide occupying the trench (and the hard-mask opening) up to y=top."""
        a, W = self.active, self.W
        t = self.trench_pts()
        floor = [t[2]]
        if cone:
            half = CONE_BASE / 2
            floor += [(self.cx - half, DEPTH)] + self.cone_tip_pts() + [(self.cx + half, DEPTH)]
        if notch:
            nw, nd = notch
            floor += [(self.cx - nw / 2, DEPTH), (self.cx - nw / 2, DEPTH + nd),
                      (self.cx + nw / 2, DEPTH + nd), (self.cx + nw / 2, DEPTH)]
        floor += [t[3]]
        if overburden:
            seq = [(0, top), (W, top), (W, -PAD - NIT), (a + TOP_W, -PAD - NIT), (a + TOP_W, 0)] \
                + list(reversed(floor)) + [(a, 0), (a, -PAD - NIT), (0, -PAD - NIT)]
        else:
            seq = [(a, top), (a + TOP_W, top), (a + TOP_W, 0)] + list(reversed(floor)) + [(a, 0)]
        return poly(self.pts(seq), C["ox"], C["ox_edge"], 1)

    def residue(self, w=24, h=10):
        x, y = self.P(self.cx - w / 2, DEPTH - CONE_H - h)
        return rect(x, y, w * self.k, h * self.k, C["residue"], rx=2)


# ---- Individual figures -----------------------------------------------------
def process_flow():
    steps = [
        ("1  Substrate", "p-Si (100), B 1.4e15 cm⁻³"),
        ("2  Pad oxide", "12 nm"),
        ("3  Nitride mask", "120 nm Si₃N₄"),
        ("4  Lithography", "pattern → hard mask"),
        ("5  RIE trench etch", "200 nm × 180 nm"),
        ("6  Cone defect", "residue micromask"),
        ("7  HDP oxide fill", "400 nm HDP-CVD SiO₂"),
        ("8  CMP", "stop on nitride"),
        ("9  Final STI", "embedded cone defect"),
    ]
    W, H = 1000, 320
    bw, bh, gap = 160, 70, 36
    body = text(W / 2, 30, "STI process flow simulated in the project", 18, "middle", "bold")
    body += text(W / 2, 50, "Values reported in the project report · green tag = a Sentaurus Visual screenshot of this stage exists",
                 12, "middle", fill=C["muted"])
    top = [(32 + i * (bw + gap), 82) for i in range(5)]
    bottom = [(32 + (4 - i) * (bw + gap), 200) for i in range(4)]  # steps 6..9, right -> left
    pos = top + bottom
    seen = {4, 5, 7, 8}  # ConeDefect, FinalSTI and final_structure screenshots
    for i, (label, sub) in enumerate(steps):
        x, y = pos[i]
        stroke = C["accent"] if i == 5 else C["line"]
        body += box(x, y, bw, bh, [label, sub], stroke=stroke, size=12.5)
        if i in seen:
            body += rect(x + bw - 50, y - 9, 46, 17, "#e8f4ea", "#5b9b6b", 1, rx=8)
            body += text(x + bw - 27, y + 3.5, "TCAD", 10, "middle", "bold", "#2f6b3d")
    for i in range(4):
        x, y = pos[i]
        body += line(x + bw + 4, y + bh / 2, pos[i + 1][0] - 6, y + bh / 2, marker="arr")
    x4, y4 = pos[4]
    body += line(x4 + bw / 2, y4 + bh + 4, x4 + bw / 2, 200 - 12, marker="arr")
    for i in range(5, 8):
        x, y = pos[i]
        body += line(x - 4, y + bh / 2, pos[i + 1][0] + bw + 6, y + bh / 2, marker="arr")
    body += footer(W, H, "Conceptual flow. Step 6 (red) is the project's distinguishing step; the report also lists an optional liner oxidation between steps 6 and 7.")
    return svg(W, H, body, "STI process flow",
               "Nine-step STI process flow from substrate to final STI with embedded cone defect.")


def process_evolution():
    k = 0.42
    panels = [
        ("1  Substrate", dict()),
        ("2  Pad oxide + nitride", dict(stack=True)),
        ("3  Litho + hard-mask open", dict(stack=True, opened=True, resist=True)),
        ("4  RIE trench etch", dict(stack=True, opened=True, trench=True)),
        ("5  Cone defect", dict(stack=True, opened=True, trench=True, cone=True, residue=True)),
        ("6  HDP oxide fill", dict(stack=True, opened=True, trench=True, cone=True, fill="over")),
        ("7  CMP (stop on nitride)", dict(stack=True, opened=True, trench=True, cone=True, fill="cmp")),
    ]
    pw = (2 * ACTIVE + TOP_W) * k
    gapx = 26
    W = int(4 * pw + 3 * gapx + 60)
    H = 600
    body = text(W / 2, 28, "Structure evolution through the STI flow", 18, "middle", "bold")
    body += text(W / 2, 47, "Conceptual cross-sections drawn to reported dimensions (pad 12 nm, nitride 120 nm, trench 200 × 180 nm, cone 100 nm)",
                 12, "middle", fill=C["muted"])
    for i, (label, o) in enumerate(panels):
        r, c = divmod(i, 4)
        x0 = 30 + c * (pw + gapx)
        y0 = 175 + r * 265
        xs = XS(x0, y0, k, sub=250)
        body += text(x0 + pw / 2, y0 - 92, label, 13, "middle", "bold")
        body += xs.silicon(trench=o.get("trench", False), cone=o.get("cone", False))
        if o.get("stack"):
            body += xs.pad_nitride(opened=o.get("opened", False))
        if o.get("resist"):
            body += xs.resist()
        if o.get("residue"):
            body += xs.residue()
            for dx in (-60, 0, 60):
                X, Y = xs.P(xs.cx + dx, -170)
                body += line(X, Y, X, Y + 28, stroke=C["blue"], sw=1.4, marker="arrB")
        if o.get("trench") and not o.get("cone") and not o.get("fill"):
            for dx in (-55, 0, 55):
                X, Y = xs.P(xs.cx + dx, -170)
                body += line(X, Y, X, Y + 28, stroke=C["blue"], sw=1.4, marker="arrB")
        if o.get("fill") == "over":
            body += xs.oxide_fill(-PAD - NIT - 50, cone=True, overburden=True)
        if o.get("fill") == "cmp":
            body += xs.oxide_fill(-PAD - NIT, cone=True)
    # legend in 8th slot
    lx = 30 + 3 * (pw + gapx)
    ly = 175 + 265 - 85
    body += text(lx, ly - 4, "Legend", 13, weight="bold")
    items = [(C["si"], "Silicon"), (C["pad"], "Pad oxide"), (C["nit"], "Si₃N₄ hard mask"),
             (C["resist"], "Photoresist"), (C["ox"], "HDP oxide"), (C["residue"], "Etch residue (micromask)")]
    for j, (col, s) in enumerate(items):
        body += rect(lx, ly + 10 + j * 22, 16, 14, col, C["si_edge"], 0.6)
        body += text(lx + 24, ly + 22 + j * 22, s, 12)
    body += line(lx, ly + 150, lx, ly + 172, stroke=C["blue"], sw=1.4, marker="arrB")
    body += text(lx + 12, ly + 166, "Directional ions (RIE)", 12)
    body += footer(W, H, "Conceptual drawing — not a Sentaurus output. Actual Sentaurus cut-planes: assets/tcad/. Nitride strip (report step 9) not drawn: screenshots still show nitride.")
    return svg(W, H, body, "STI structure evolution",
               "Seven conceptual cross-sections from bare substrate to CMP with embedded cone defect.")


def trench_etch():
    k = 0.95
    W, H = 760, 615
    xs = XS((W - (2 * 130 + TOP_W) * k) / 2, 300, k, active=130, sub=270)
    body = text(W / 2, 30, "Anisotropic RIE trench etch — reported geometry", 18, "middle", "bold")
    body += text(W / 2, 50, "Directional ion bombardment + chemical etch through the opened nitride / pad-oxide hard mask",
                 12, "middle", fill=C["muted"])
    body += xs.silicon(trench=True)
    body += xs.pad_nitride(opened=True)
    for dx in (-60, -20, 20, 60):
        X, Y = xs.P(xs.cx + dx, -PAD - NIT - 60)
        body += line(X, Y, X, Y + 50, stroke=C["blue"], sw=1.6, marker="arrB")
    X, Y = xs.P(xs.cx + 80, -PAD - NIT - 40)
    body += text(X + 6, Y, "ions", 12, fill=C["blue"])
    a, Wd = xs.active, xs.W
    # depth dimension, outside the structure on the right
    p1, p2 = xs.P(Wd + 22, 0), xs.P(Wd + 22, DEPTH)
    body += line(*p1, *p2, marker="arr", both=True)
    body += line(*xs.P(a + TOP_W, 0), p1[0] + 6, p1[1], stroke=C["muted"], sw=0.8, dash="3,3")
    body += line(*xs.P(xs.cx + BOT_W / 2, DEPTH), p2[0] + 6, p2[1], stroke=C["muted"], sw=0.8, dash="3,3")
    body += text(p1[0] + 10, (p1[1] + p2[1]) / 2 - 4, "200 nm", 13, weight="bold")
    body += text(p1[0] + 10, (p1[1] + p2[1]) / 2 + 12, "depth", 12, fill=C["muted"])
    # top width
    q1, q2 = xs.P(a, -PAD - NIT - 75), xs.P(a + TOP_W, -PAD - NIT - 75)
    body += line(q1[0], q1[1], q2[0], q2[1], marker="arr", both=True)
    body += line(*xs.P(a, -PAD - NIT - 80), *xs.P(a, 0), stroke=C["muted"], sw=0.8, dash="3,3")
    body += line(*xs.P(a + TOP_W, -PAD - NIT - 80), *xs.P(a + TOP_W, 0), stroke=C["muted"], sw=0.8, dash="3,3")
    body += text((q1[0] + q2[0]) / 2, q1[1] - 8, "180 nm top width", 13, "middle", "bold")
    # bottom width, inside the substrate below the floor
    bl, br = xs.cx - BOT_W / 2, xs.cx + BOT_W / 2
    r1, r2 = xs.P(bl, DEPTH + 18), xs.P(br, DEPTH + 18)
    body += line(*r1, *r2, marker="arr", both=True)
    body += text((r1[0] + r2[0]) / 2, r1[1] + 20, "≈ 170 nm bottom width", 13, "middle", "bold")
    # sidewall angle
    c0 = xs.P(bl, DEPTH)
    body += path(f"M{c0[0] + 36:.1f},{c0[1]:.1f} A36,36 0 0 0 {c0[0] + 36 * math.cos(math.radians(-88)):.1f},"
                 f"{c0[1] + 36 * math.sin(math.radians(-88)):.1f}", stroke=C["accent"], sw=1.4)
    body += text(c0[0] + 40, c0[1] - 22, "≈ 88°", 13, weight="bold", fill=C["accent"])
    # corner radius callout, outside on the left
    cpt = xs.P(a, 0)
    left_edge = xs.P(0, 0)[0]
    body += f'<circle cx="{cpt[0]:.1f}" cy="{cpt[1]:.1f}" r="9" fill="none" stroke="{C["accent"]}" stroke-width="1.4"/>\n'
    body += line(cpt[0] - 9, cpt[1] + 4, left_edge - 8, cpt[1] + 44, stroke=C["accent"], sw=1)
    body += text(left_edge - 12, cpt[1] + 48, "top corner", 12, "end", "bold", C["accent"])
    body += text(left_edge - 12, cpt[1] + 63, "radius ≈ 15 nm", 12, "end", "bold", C["accent"])
    body += text(left_edge - 12, cpt[1] + 78, "(stress / field", 11, "end", fill=C["muted"])
    body += text(left_edge - 12, cpt[1] + 92, "concentration)", 11, "end", fill=C["muted"])
    # labels
    body += text(*xs.P(a / 2, 130), "Active Si", 13, "middle", "bold")
    body += text(*xs.P(a + TOP_W + a / 2, 130), "Active Si", 13, "middle", "bold")
    body += text(*xs.P(a / 2, -PAD - NIT / 2 + 5), "Si₃N₄ 120 nm", 12, "middle")
    body += text(*xs.P(a + TOP_W + a / 2, -PAD - NIT / 2 + 5), "Si₃N₄ 120 nm", 12, "middle")
    body += text(W / 2, 580, "Aspect ratio 200 / 180 ≈ 1.1 (reported ~1.1)", 12, "middle", fill=C["muted"])
    body += footer(W, H, "Conceptual drawing at reported dimensions. The Sentaurus screenshots show a more tapered trench (≈ 62–64°); see docs/geometry-analysis.md.")
    return svg(W, H, body, "Anisotropic trench etch",
               "Trench cross-section with reported depth, widths, sidewall angle and corner radius.")


def defect_formation():
    k = 0.62
    W, H = 1000, 470
    act = 60
    titles = [("1  Residue lands on", "the trench floor"), ("2  Residue micromasks", "the Si below it"),
              ("3  Open floor keeps etching;", "residue erodes laterally"), ("4  Residual Si cone", "remains at the floor")]
    pw = (2 * act + TOP_W) * k
    body = text(W / 2, 30, "Cone-defect formation by residue micromasking during RIE", 18, "middle", "bold")
    body += text(W / 2, 50, "Mechanism as described in the project report (sections 2.2, 5.1, 7.1)", 12, "middle", fill=C["muted"])
    # (etch depth d, protrusion half-width at base, at top, residue width)
    stages = [(110, None, None, 26), (140, 14, 12, 22), (200, 25, 6, 14), (200, None, None, None)]
    for i, ((t1, t2), (d, hb, ht, rw)) in enumerate(zip(titles, stages, strict=True)):
        x0 = 40 + i * (pw + 60)
        xs = XS(x0, 225, k, active=act, sub=270)
        body += text(x0 + pw / 2, 82, t1, 12.5, "middle", "bold")
        body += text(x0 + pw / 2, 98, t2, 12.5, "middle", "bold")
        if i == 3:
            body += xs.silicon(trench=True, cone=True)
        else:
            bw_d = TOP_W - 2 * d / math.tan(math.radians(SIDEWALL))
            bl, br = xs.cx - bw_d / 2, xs.cx + bw_d / 2
            floor = [(bl, d)]
            if hb:  # protrusion from the residue level (110 nm) down to the current floor
                floor += [(xs.cx - hb, d), (xs.cx - ht, 110), (xs.cx + ht, 110), (xs.cx + hb, d)]
            floor += [(br, d)]
            seq = [(0, 0), (act, 0)] + floor + [(act + TOP_W, 0), (xs.W, 0), (xs.W, xs.sub), (0, xs.sub)]
            body += poly(xs.pts(seq), C["si"], C["si_edge"], 1)
            X, Y = xs.P(xs.cx - rw / 2, 110 - 9)
            body += rect(X, Y, rw * k, 9 * k, C["residue"], rx=1.5)
            for dx in (-55, 0, 55):
                Xa, Ya = xs.P(xs.cx + dx, -PAD - NIT - 40)
                body += line(Xa, Ya, Xa, Ya + 24, stroke=C["blue"], sw=1.4, marker="arrB")
            body += line(x0 + pw + 12, 300, x0 + pw + 48, 300, marker="arr")
        body += xs.pad_nitride(opened=True)
        if i == 3:
            tip = xs.P(xs.cx, DEPTH - CONE_H)
            body += line(tip[0] - 3, tip[1] - 2, tip[0] - 14, tip[1] - 22, stroke=C["accent"], sw=1)
            body += text(tip[0] - 16, tip[1] - 40, "sharp tip", 12, "end", "bold", C["accent"])
            body += text(tip[0] - 16, tip[1] - 26, "r ≈ 8–12 nm", 11, "end", fill=C["accent"])
    body += text(W / 2, 425, "Silicon under the residue survives while the exposed floor is etched; lateral erosion of the residue tapers the protrusion into a cone.",
                 12.5, "middle")
    body += footer(W, H, "Conceptual drawing. In the Sentaurus flow the defect is an explicit 'cone defect introduction' step, not a plasma-chemistry simulation.")
    return svg(W, H, body, "Cone defect formation",
               "Four-step sequence showing residue micromasking producing a silicon cone at the trench bottom.")


def cone_defect():
    k = 2.2
    W, H = 880, 480
    act = 40
    xs = XS(0, 0, k, active=act)
    xs.x0 = 600 - xs.cx * k
    xs.y0 = 390 - DEPTH * k
    body = text(W / 2, 30, "Cone-defect geometry (reported)", 18, "middle", "bold")
    body += text(W / 2, 50, "Silicon protrusion rising from the trench floor, tip at mid-trench depth", 12, "middle", fill=C["muted"])
    body += '<clipPath id="cl"><rect x="300" y="72" width="560" height="360"/></clipPath>\n<g clip-path="url(#cl)">\n'
    body += xs.oxide_fill(-PAD - NIT, cone=True)
    body += xs.silicon(trench=True, cone=True)
    body += "</g>\n"
    cx = xs.P(xs.cx, 0)[0]
    floor_y = xs.P(0, DEPTH)[1]
    tip_y = xs.P(0, DEPTH - CONE_H)[1]
    # height
    body += line(cx + 90, floor_y, cx + 90, tip_y, marker="arr", both=True)
    body += line(cx + 4, tip_y, cx + 96, tip_y, stroke=C["muted"], sw=0.8, dash="3,3")
    body += text(cx + 98, (floor_y + tip_y) / 2 - 2, "height", 12, fill=C["muted"])
    body += text(cx + 98, (floor_y + tip_y) / 2 + 14, "≈ 100 nm", 13, weight="bold")
    # base
    b1, b2 = xs.P(xs.cx - CONE_BASE / 2, DEPTH + 9), xs.P(xs.cx + CONE_BASE / 2, DEPTH + 9)
    body += line(*b1, *b2, marker="arr", both=True)
    body += text(cx, b1[1] + 20, "base ≈ 50 nm", 13, "middle", "bold")
    # tip radius
    body += f'<circle cx="{cx:.1f}" cy="{tip_y + TIP_R * k:.1f}" r="{TIP_R * k:.1f}" fill="none" stroke="{C["accent"]}" stroke-width="1.2" stroke-dasharray="3,2"/>\n'
    body += line(cx - 20, tip_y + 6, cx - 70, tip_y - 18, stroke=C["accent"], sw=1)
    body += text(cx - 74, tip_y - 30, "tip radius ≈ 8–12 nm", 12.5, "end", "bold", C["accent"])
    body += text(cx - 74, tip_y - 15, "(parameter table: ~10 nm)", 11.5, "end", fill=C["accent"])
    body += text(*xs.P(xs.cx - 52, 175), "HDP oxide", 13, "middle", "bold", "#1d6f80")
    # notes column
    notes = [("Height : base", "≈ 2 : 1"), ("Tip position", "≈ 100 nm above floor"), ("", "= mid-depth of 200 nm trench"),
             ("Core", "crystalline Si"), ("Flanks", "residue / native oxide"), ("", "(report §5.1)")]
    y = 110
    body += text(30, 92, "Reported cone parameters", 14, weight="bold")
    for k1, v in notes:
        if k1:
            body += text(30, y + 6, k1, 12.5, weight="bold")
        body += text(130, y + 6, v, 12.5, fill=C["muted"])
        y += 22
    body += text(30, y + 26, "First-order field enhancement", 12.5, weight="bold")
    body += text(30, y + 44, "β ≈ h / r = 100 / 10 ≈ 10", 12.5, fill=C["accent"])
    body += text(30, y + 62, "(matches the report's β ≈ 10;", 11.5, fill=C["muted"])
    body += text(30, y + 76, "the report does not state its method)", 11.5, fill=C["muted"])
    body += footer(W, H, "Conceptual drawing at reported dimensions; not extracted from a TCAD structure. Screenshot geometry differs — see defect-comparison.svg.")
    return svg(W, H, body, "Cone defect geometry",
               "Close-up of the reported cone defect: 100 nm height, 50 nm base, 8-12 nm tip radius.")


def cmp_flow():
    k = 0.6
    W, H = 1000, 400
    pw = (2 * ACTIVE + TOP_W) * k
    titles = [("After HDP-CVD fill", "oxide overburden above nitride"),
              ("After CMP", "polish stops on Si₃N₄"),
              ("After nitride strip", "described in report; not in screenshots")]
    body = text(W / 2, 30, "Planarization: HDP fill → CMP → hard-mask removal", 18, "middle", "bold")
    body += text(W / 2, 50, "CMP flattens the top surface but cannot reach the defect buried in the trench", 12, "middle", fill=C["muted"])
    for i, (t, s) in enumerate(titles):
        x0 = 30 + i * (pw + 45)
        xs = XS(x0, 210, k, sub=250)
        body += text(x0 + pw / 2, 90, t, 13.5, "middle", "bold")
        body += text(x0 + pw / 2, 108, s, 11.5, "middle", fill=C["muted"])
        body += xs.silicon(trench=True, cone=True)
        if i == 0:
            body += xs.pad_nitride(opened=True)
            body += xs.oxide_fill(-PAD - NIT - 60, cone=True, overburden=True)
        elif i == 1:
            body += xs.pad_nitride(opened=True)
            body += xs.oxide_fill(-PAD - NIT, cone=True)
            y = xs.P(0, -PAD - NIT)[1]
            body += line(x0 - 4, y, x0 + pw + 4, y, stroke=C["accent"], sw=1.2, dash="5,3")
            body += text(x0 + pw, y - 6, "polish stop", 11, "end", fill=C["accent"])
        else:
            body += xs.oxide_fill(0, cone=True)
        if i < 2:
            body += line(x0 + pw + 8, 200, x0 + pw + 38, 200, marker="arr")
        tip = xs.P(xs.cx, DEPTH - CONE_H)
        body += line(tip[0], tip[1] - 3, tip[0], tip[1] - 16, stroke=C["accent"], sw=1)
        body += text(tip[0], tip[1] - 20, "embedded cone", 11, "middle", "bold", C["accent"])
    body += footer(W, H, "Conceptual. Report: surface variation after CMP < 5 nm (reported). Screenshots show tens-of-nm steps between oxide and nitride (estimated).")
    return svg(W, H, body, "CMP planarization flow",
               "Three cross-sections: HDP overburden, CMP stopping on nitride, nitride removed with embedded cone remaining.")


def final_structure():
    k = 1.15
    W, H = 980, 470
    xs = XS(40, 110, k, sub=260)
    body = text(W / 2, 30, "Final STI structure with embedded cone defect", 18, "middle", "bold")
    body += text(W / 2, 50, "Planar surface on top; the defect is hidden inside the isolation oxide", 12, "middle", fill=C["muted"])
    body += xs.silicon(trench=True, cone=True)
    body += xs.oxide_fill(0, cone=True)
    a = xs.active
    right = xs.P(xs.W, 0)[0]
    # labels inside the structure
    body += text(*xs.P(a / 2, 50), "Active region", 14, "middle", "bold")
    body += text(*xs.P(a + TOP_W + a / 2, 50), "Active region", 14, "middle", "bold")
    body += text(*xs.P(a / 2, 68), "(device side A)", 11, "middle", fill=C["muted"])
    body += text(*xs.P(a + TOP_W + a / 2, 68), "(device side B)", 11, "middle", fill=C["muted"])
    body += text(*xs.P(xs.cx, 35), "STI oxide", 13, "middle", "bold", "#1d6f80")
    body += text(*xs.P(xs.W / 2, 240), "p-Si substrate (100), B 1.4 × 10¹⁵ cm⁻³", 13, "middle")
    # planar surface
    y0 = xs.P(0, 0)[1]
    body += line(xs.P(0, 0)[0], y0 - 12, right, y0 - 12, stroke=C["blue"], sw=1, dash="4,3")
    body += text(xs.P(0, 0)[0], y0 - 18, "planarized surface (report: < 5 nm variation after CMP)", 11.5, "start", fill=C["blue"])
    # callouts in the right-hand column
    cx_ = right + 30
    tip = xs.P(xs.cx, DEPTH - CONE_H)
    body += f'<ellipse cx="{tip[0]:.1f}" cy="{tip[1] - 6:.1f}" rx="30" ry="18" fill="{C["accent"]}" fill-opacity="0.14" stroke="{C["accent"]}" stroke-width="1" stroke-dasharray="3,2"/>\n'
    body += line(tip[0] + 30, tip[1] - 8, cx_ - 6, tip[1] - 40, stroke=C["accent"], sw=1)
    body += text(cx_, tip[1] - 52, "Thinnest dielectric region", 13, weight="bold", fill=C["accent"])
    body += text(cx_, tip[1] - 36, "oxide over tip 50–70 nm vs ~150 nm nominal", 11.5, fill=C["accent"])
    body += text(cx_, tip[1] - 21, "(reported; geometry of this value is ambiguous —", 11, fill=C["muted"])
    body += text(cx_, tip[1] - 7, "see docs/oxide-thinning.md)", 11, fill=C["muted"])
    flank = xs.P(xs.cx + 18, DEPTH - 30)
    body += line(flank[0] + 2, flank[1], cx_ - 6, flank[1] + 30, stroke=C["ink"], sw=1)
    body += text(cx_, flank[1] + 26, "Embedded Si cone", 13, weight="bold")
    body += text(cx_, flank[1] + 42, "h ≈ 100 nm, base ≈ 50 nm, r_tip ≈ 8–12 nm", 11.5, fill=C["muted"])
    body += text(cx_, flank[1] + 57, "survives fill and CMP untouched (report §5.1)", 11.5, fill=C["muted"])
    body += footer(W, H, "Conceptual drawing to reported dimensions. Nitride shown removed per report text; the Sentaurus screenshots still show nitride.")
    return svg(W, H, body, "Final STI structure",
               "Final STI cross-section: two active regions, oxide-filled trench, embedded silicon cone and the thin oxide above its tip.")


def oxide_thinning():
    W, H = 760, 420
    body = text(W / 2, 30, "Local oxide thinning above the cone tip", 18, "middle", "bold")
    body += text(W / 2, 50, "Reported in project documentation — not extracted from a TCAD structure in this repository",
                 12, "middle", fill=C["accent"])
    base_y = 330
    s = 1.4  # px per nm
    # nominal bar
    x1 = 140
    body += rect(x1, base_y - 150 * s, 120, 150 * s, C["ox"], C["ox_edge"], 1.2)
    body += text(x1 + 60, base_y - 150 * s - 10, "~150 nm", 16, "middle", "bold")
    body += text(x1 + 60, base_y + 22, "Nominal trench oxide", 13, "middle", "bold")
    body += text(x1 + 60, base_y + 38, "(trench bottom, defect-free)", 11.5, "middle", fill=C["muted"])
    # over tip range
    x2 = 380
    body += rect(x2, base_y - 70 * s, 120, 70 * s, C["ox"], C["ox_edge"], 1.2, dash="4,3")
    body += rect(x2, base_y - 50 * s, 120, 50 * s, C["ox"], C["ox_edge"], 1.2)
    body += text(x2 + 60, base_y - 70 * s - 10, "50–70 nm", 16, "middle", "bold", C["accent"])
    body += text(x2 + 60, base_y + 22, "Above cone tip", 13, "middle", "bold")
    body += text(x2 + 60, base_y + 38, "(≈ 60 nm used in report §6.3, §9)", 11.5, "middle", fill=C["muted"])
    body += line(100, base_y, 560, base_y, stroke=C["ink"], sw=1.2)
    body += line(x1 + 124, base_y - 150 * s, x2 - 4, base_y - 150 * s, stroke=C["muted"], sw=0.8, dash="3,3")
    body += line(x2 + 60, base_y - 150 * s + 4, x2 + 60, base_y - 70 * s - 28, stroke=C["accent"], sw=1.5, marker="arrR")
    body += text(x2 + 70, base_y - 150 * s + 30, "−53 % to −67 %", 13, weight="bold", fill=C["accent"])
    # side panel: field consequence
    px = 580
    body += rect(px, 120, 165, 168, C["panel"], C["line"], 1.2, rx=8)
    lines_ = [("Field for the same V", "bold", C["ink"]), ("E ≈ V / t_ox", "normal", C["ink"]),
              ("150 → 70 nm: ×2.1", "normal", C["accent"]), ("150 → 50 nm: ×3.0", "normal", C["accent"]),
              ("calculated, uniform-", "normal", C["muted"]), ("field (parallel-plate)", "normal", C["muted"]),
              ("approximation", "normal", C["muted"])]
    for j, (t_, w_, f_) in enumerate(lines_):
        body += text(px + 82, 146 + j * 20, t_, 12.5, "middle", w_, f_)
    body += footer(W, H, "Bar heights to scale (1.4 px/nm). Percentages and field ratios are calculated from the reported thicknesses.")
    return svg(W, H, body, "Oxide thinning above cone tip",
               "Bar comparison of reported nominal oxide thickness (about 150 nm) and oxide above the cone tip (50 to 70 nm).")


def electric_field():
    W, H = 900, 430
    body = text(W / 2, 30, "Why a sharp tip concentrates the electric field", 18, "middle", "bold")
    body += text(W / 2, 50, "Conceptual field-line sketch — NOT a Sentaurus Device solution (no device simulation in this project)",
                 12, "middle", fill=C["accent"])
    # left: parallel plate
    lx, ly, lw, lh = 60, 100, 330, 220
    body += rect(lx, ly, lw, 22, "#b9c4c9", C["si_edge"])
    body += rect(lx, ly + 22, lw, lh - 44, C["ox"], C["ox_edge"])
    body += rect(lx, ly + lh - 22, lw, 22, C["si"], C["si_edge"])
    for i in range(9):
        x = lx + 25 + i * 35
        body += line(x, ly + 26, x, ly + lh - 26, stroke=C["blue"], sw=1.2, marker="arrB")
    body += text(lx + lw / 2, ly - 10, "Flat interface: uniform field", 14, "middle", "bold")
    body += text(lx + lw / 2, ly + 15, "conductor above STI (illustrative)", 11, "middle", fill=C["ink"])
    body += text(lx + lw / 2, ly + lh - 7, "silicon", 11, "middle", fill="#ffffff")
    body += text(lx + lw / 2, ly + lh + 24, "E = V / t_ox  (β = 1)", 13, "middle")
    # right: cone
    rx, ry, rw, rh = 500, 100, 340, 220
    body += rect(rx, ry, rw, 22, "#b9c4c9", C["si_edge"])
    body += rect(rx, ry + 22, rw, rh - 44, C["ox"], C["ox_edge"])
    cx = rx + rw / 2
    base_y = ry + rh - 22
    tip_y = ry + 95
    cone = (f"M{rx},{base_y} L{cx - 32},{base_y} L{cx - 6},{tip_y + 8} "
            f"Q{cx},{tip_y - 2} {cx + 6},{tip_y + 8} L{cx + 32},{base_y} L{rx + rw},{base_y} "
            f"L{rx + rw},{ry + rh} L{rx},{ry + rh} Z")
    body += path(cone, fill=C["si"], stroke=C["si_edge"], sw=1)
    # crowded lines converging to tip
    for i in range(11):
        x = rx + 20 + i * 30
        tx = cx + (x - cx) * 0.05
        ty = tip_y - 2 if abs(x - cx) < 80 else None
        if ty is None:
            # lines far away end on flank / floor
            end_y = base_y - 4
            body += line(x, ry + 26, x + (cx - x) * 0.12, end_y, stroke=C["blue"], sw=1.0, marker="arrB")
        else:
            body += path(f"M{x},{ry + 26} Q{x},{tip_y - 30} {tx:.1f},{ty - 2:.1f}", stroke=C["blue"], sw=1.2, marker="arrB")
    body += f'<circle cx="{cx}" cy="{tip_y + 2}" r="14" fill="{C["accent"]}" fill-opacity="0.18" stroke="{C["accent"]}" stroke-width="1"/>\n'
    body += text(cx + 22, tip_y - 6, "E_tip ≈ β · E_avg", 13, weight="bold", fill=C["accent"])
    body += text(rx + rw / 2, ry - 10, "Cone tip: field lines crowd at small radius", 14, "middle", "bold")
    body += text(rx + rw / 2, ry + 15, "conductor above STI (illustrative)", 11, "middle", fill=C["ink"])
    body += text(rx + rw / 2, ry + rh + 24, "β ≈ 10 (reported estimate; = h / r_tip = 100 / 10)", 13, "middle")
    body += text(W / 2, 382, "Thin oxide (larger E_avg) and a sharp tip (larger β) multiply: the tip is the highest-stress point of the STI dielectric.",
                 12.5, "middle")
    body += footer(W, H, "β value from the report (method not stated); h/r interpretation is a first-order approximation. No field values were simulated.")
    return svg(W, H, body, "Electric-field enhancement",
               "Side-by-side conceptual field lines: uniform field across a flat oxide versus crowded field lines at a sharp silicon cone tip.")


def reliability_flow():
    W, H = 980, 470
    body = text(W / 2, 30, "From process defect to reliability risk", 18, "middle", "bold")
    body += text(W / 2, 50, "Solid boxes: geometry documented in the report  ·  Dashed boxes: mechanisms discussed, not simulated",
                 12, "middle", fill=C["muted"])
    solid = C["panel"]
    body += box(40, 80, 200, 60, ["Cone defect", "100 nm Si spike"], fill=solid)
    body += box(40, 180, 200, 60, ["Sharp tip", "r ≈ 8–12 nm"], fill=solid)
    body += box(280, 180, 200, 60, ["Field enhancement", "β ≈ 10 (estimate)"], fill=solid)
    body += box(280, 80, 200, 60, ["Oxide thinning", "~150 → 50–70 nm"], fill=solid)
    body += box(530, 130, 190, 60, ["Higher local", "dielectric stress"], fill="#fdecea", stroke=C["accent"])
    body += line(140, 140, 140, 176, marker="arr")
    body += line(244, 210, 276, 210, marker="arr")
    body += line(244, 110, 276, 110, marker="arr")
    body += line(484, 110, 526, 150, marker="arr")
    body += line(484, 210, 526, 172, marker="arr")
    # mechanisms
    mech = [
        (760, 70, ["Leakage", "TAT / FN tunneling"]),
        (760, 150, ["Mechanical stress", "Si/SiO₂ CTE mismatch"]),
        (760, 230, ["Premature breakdown", "TDDB-type failure"]),
    ]
    for x, y, l in mech:
        body += box(x, y, 190, 58, l, fill="#ffffff", stroke=C["muted"], dash="5,4")
        body += line(724, 160, x - 4, y + 29, marker="arr")
    body += box(530, 330, 420, 70, ["Reliability qualification context (report §8.2)",
                                      "TDDB · SILC · HCI — discussed as evaluation methods"],
                fill="#ffffff", stroke=C["muted"], dash="5,4")
    body += line(855, 292, 855, 326, marker="arr")
    body += box(40, 330, 440, 70, ["Not simulated in this project",
                                    "leakage current · breakdown voltage · stress field · lifetime"],
                fill="#fff8e6", stroke="#c9a227")
    body += footer(W, H, "Conceptual causal chain. No electrical, stress or reliability simulation results exist in this repository or the report's TCAD evidence.")
    return svg(W, H, body, "Reliability risk chain",
               "Flowchart linking cone defect, sharp tip and oxide thinning to dielectric stress and discussed reliability mechanisms.")


def defect_comparison():
    k = 0.62  # same px/nm for both panels
    W, H = 980, 520
    body = text(W / 2, 30, "Defect geometry: report description vs. Sentaurus screenshots", 18, "middle", "bold")
    body += text(W / 2, 50, "The available cut-plane images do not show an upward Si spike; they show a narrow oxide-filled recess below the trench floor",
                 12, "middle", fill=C["accent"])
    # left: report
    xl = XS(130, 150, k, active=90, sub=450)
    body += text(130 + xl.W * k / 2, 92, "A · Report text (§5.1, §6.1)", 14, "middle", "bold")
    body += text(130 + xl.W * k / 2, 110, "Si cone rises 100 nm from the floor into the oxide", 12, "middle", fill=C["muted"])
    body += xl.silicon(trench=True, cone=True)
    body += xl.oxide_fill(0, cone=True)
    tip = xl.P(xl.cx, DEPTH - CONE_H)
    body += line(tip[0], tip[1] - 3, tip[0], 142, stroke=C["accent"], sw=1)
    body += text(tip[0], 136, "Si tip pointing up", 12, "middle", "bold", C["accent"])
    body += text(130 + xl.W * k / 2, 470, "88° walls · 200 nm deep · 180 nm wide (reported)", 12, "middle")
    # right: screenshot-derived (estimates)
    est_depth, est_top, est_bot = 225, 385, 160
    notch_w, notch_d = 45, 108
    k2 = k
    x0, y0 = 515, 150
    act = 120
    Wd = 2 * act + est_top
    cx = act + est_top / 2

    def P(x, y):
        return (x0 + x * k2, y0 + y * k2)

    si = [(0, 0), (act, 0), (cx - est_bot / 2, est_depth), (cx - notch_w / 2, est_depth),
          (cx - notch_w / 2, est_depth + notch_d), (cx + notch_w / 2, est_depth + notch_d),
          (cx + notch_w / 2, est_depth), (cx + est_bot / 2, est_depth), (act + est_top, 0), (Wd, 0),
          (Wd, 450), (0, 450)]
    ox = [(act, 0)] + si[2:8] + [(act + est_top, 0)]
    body += poly([P(*p) for p in si], C["si"], C["si_edge"], 1)
    body += poly([P(*p) for p in ox], C["ox"], C["ox_edge"], 1)
    body += text(x0 + Wd * k2 / 2, 92, "B · Sentaurus cut-plane (estimated)", 14, "middle", "bold")
    body += text(x0 + Wd * k2 / 2, 110, "Narrow recess extends below the trench floor", 12, "middle", fill=C["muted"])
    n = P(cx + notch_w / 2, est_depth + notch_d / 2)
    body += rect(n[0] + 52, n[1] - 4, 140, 54, "#ffffff", C["accent"], 1, rx=6)
    body += line(n[0] + 2, n[1], n[0] + 52, n[1] + 10, stroke=C["accent"], sw=1)
    body += text(n[0] + 60, n[1] + 13, "oxide-filled notch", 12, weight="bold", fill=C["accent"])
    body += text(n[0] + 60, n[1] + 28, "≈ 105–115 nm deep", 11.5, fill=C["accent"])
    body += text(n[0] + 60, n[1] + 42, "≈ 40–60 nm wide", 11.5, fill=C["accent"])
    body += text(x0 + Wd * k2 / 2, 470, "≈ 62–64° walls · ≈ 220–230 nm deep · ≈ 380 nm opening", 12, "middle")
    body += text(x0 + Wd * k2 / 2, 486, "(pixel estimates from screenshots, ± ~10–15 nm)", 11, "middle", fill=C["muted"])
    body += line(490, 80, 490, 490, stroke=C["line"], sw=1)
    body += footer(W, H, "A: conceptual, reported dimensions. B: redrawn from scripts/analysis/measure_tcad_screenshots.py estimates (same scale). Original .tdr files unavailable.")
    return svg(W, H, body, "Reported versus observed defect geometry",
               "Left: report-described upward silicon cone. Right: geometry estimated from the Sentaurus Visual screenshots, a narrow oxide-filled recess below the trench floor.")


FIGS = {
    "process-flow.svg": process_flow,
    "process-evolution.svg": process_evolution,
    "trench-etch.svg": trench_etch,
    "defect-formation.svg": defect_formation,
    "cone-defect.svg": cone_defect,
    "cmp-flow.svg": cmp_flow,
    "final-structure.svg": final_structure,
    "oxide-thinning.svg": oxide_thinning,
    "electric-field.svg": electric_field,
    "reliability-flow.svg": reliability_flow,
    "defect-comparison.svg": defect_comparison,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGS.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", os.path.join("assets", name))


if __name__ == "__main__":
    main()
