#!/usr/bin/env python3
"""AI + Human symbol concepts D, E, F for Virtual IP."""
import math
import logo as L
from logo import NAVY, BLUE, SKY, WHITE, MIST, NAVY, label, svg, text_path


def sym_two_natures(c1=NAVY, c2=BLUE, **_):
    """D: one V, two natures. Left arm is a human stroke, right arm is machine blocks."""
    sq = "".join(f'<rect x="{x - 9.5}" y="{y - 9.5}" width="19" height="19" rx="4.2" fill="{c2}"/>'
                 for x, y in [(79, 22), (68, 45), (57.5, 67)])
    return (f'<path d="M21 22 L48 78" fill="none" stroke="{c1}" stroke-width="18" stroke-linecap="round"/>' + sq)


def sym_spark_person(c1=NAVY, c2=BLUE, **_):
    """E: a person whose head is a spark; the collar is a V."""
    spark = "M50 5 C52.4 17 57 22 69 24.5 C57 27 52.4 32 50 44 C47.6 32 43 27 31 24.5 C43 22 47.6 17 50 5Z"
    body = "M17 94 C17 68 32 55 43 55 L50 68 L57 55 C68 55 83 68 83 94 Z"
    return f'<g transform="translate(50 25) scale(1.3) translate(-50 -24.5)"><path d="{spark}" fill="{c2}"/></g><path d="{body}" fill="{c1}" stroke="{c1}" stroke-width="2" stroke-linejoin="round" transform="translate(0 4)"/>'


def sym_pixel_head(c1=NAVY, c2=BLUE, c3=SKY, **_):
    """F: a human head that dissolves into pixels."""
    cx = cy = 50
    r = 42
    left = f'<path d="M50 {cy - r} A{r} {r} 0 0 0 50 {cy + r} Z" fill="{c1}"/>'
    cells = []
    s, pitch = 13.2, 16.6
    x = 54.6
    col = 0
    while x < cx + r:
        y = cy - r + 2.4
        while y < cy + r:
            mx, my = x + s / 2, y + s / 2
            if math.hypot(mx - cx, my - cy) <= r - 1.0:
                fill = c2 if col < 2 else c3
                cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s}" height="{s}" rx="3" fill="{fill}"/>')
            y += pitch
        x += pitch
        col += 1
    return left + "".join(cells)


L.SYMS.update({"D": sym_two_natures, "E": sym_spark_person, "F": sym_pixel_head})


def dark_kw(k):
    return {"c1": WHITE, "c2": "#5B8CFF", "c3": "#BFD2FF"}


def lockup(k, h, dark=False):
    ink, acc = (WHITE, "#8FB0FF") if dark else (NAVY, BLUE)
    sym = L.SYMS[k](**(dark_kw(k) if dark else {}))
    size = h * 0.56
    wm, ww = text_path("Virtual IP", 700, size, 0, h / 2 + size * 0.36, -8 * size / 64, [ink] * 8 + [acc] * 2)
    gap = h * 0.26
    return f'<g transform="scale({h / 100})">{sym}</g><g transform="translate({h + gap},0)">{wm}</g>', h + gap + ww, h


def sheet(path="concepts-ai-human.svg"):
    W, H = 2400, 1500
    names = {"D": ("D  Two natures", "One V. The left arm is human, drawn by hand. The right arm is machine, built from blocks."),
             "E": ("E  Spark person", "A person whose head is a spark. The collar is the V."),
             "F": ("F  Pixel head", "A human head that dissolves into data. Half person, half system.")}
    p = [f'<rect width="{W}" height="{H}" fill="{MIST}"/>',
         label("Virtual IP: AI and human", 90, 120, 56, 700),
         label("Midnight #0A1330  ·  Electric blue #2F6BFF  ·  Sky #8FB0FF", 90, 172, 24, 400, NAVY, .7)]
    colw = (W - 180 - 120) / 3
    for i, k in enumerate("DEF"):
        x0 = 90 + i * (colw + 60)
        p.append(f'<rect x="{x0}" y="230" width="{colw}" height="400" rx="28" fill="{WHITE}"/>')
        inner, w, h = lockup(k, 130)
        p.append(f'<g transform="translate({x0 + (colw - w) / 2},{230 + (400 - h) / 2})">{inner}</g>')
        p.append(f'<rect x="{x0}" y="660" width="{colw}" height="400" rx="28" fill="{NAVY}"/>')
        inner, w, h = lockup(k, 130, dark=True)
        p.append(f'<g transform="translate({x0 + (colw - w) / 2},{660 + (400 - h) / 2})">{inner}</g>')
        p.append(f'<rect x="{x0}" y="1090" width="{colw}" height="170" rx="28" fill="{WHITE}"/>')
        sx = x0 + 60
        for s in (96, 56, 32, 20):
            p.append(f'<g transform="translate({sx},{1090 + (170 - s) / 2}) scale({s / 100})">{L.SYMS[k]()}</g>')
            sx += s + 50
        t, d = names[k]
        p.append(label(t, x0, 1330, 34, 700))
        # wrap description in two lines
        words, lines, cur = d.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) > 46:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            p.append(label(ln, x0, 1376 + j * 30, 22, 400, NAVY, .75))
    open(path, "w").write(svg("".join(p), W, H))
    return path


if __name__ == "__main__":
    print(sheet())
