#!/usr/bin/env python3
"""Final Virtual IP logo: concept E (spark person). Builds all files + brand sheet."""
import os, subprocess
import logo as L
import ai_human as A
from logo import NAVY, BLUE, SKY, MIST, WHITE, text_path, label, svg

OUT = "/home/claude/logo/final"
DARK_BLUE = "#5B8CFF"
VB = (14, -2, 72, 103)  # tight symbol viewBox (x, y, w, h)


def sym(c1, c2):
    return A.sym_spark_person(c1, c2)


def lockup_svg(c1, c2, ink, acc, h=103):
    """Horizontal lockup, transparent. symbol scaled so its viewBox height = h."""
    k = h / VB[3]
    size = h * 0.50
    wm, ww = text_path("Virtual IP", 700, size, 0, 0, -8 * size / 64, [ink] * 8 + [acc] * 2)
    gap = h * 0.30
    sw = VB[2] * k
    base = h / 2 + size * 0.36
    inner = (f'<g transform="scale({k}) translate({-VB[0]} {-VB[1]})">{sym(c1, c2)}</g>'
             f'<g transform="translate({sw + gap},{base})">{wm}</g>')
    return svg(inner, sw + gap + ww, h), sw + gap + ww, h


def symbol_svg(c1, c2, bg=None, pad=0):
    inner = f'<g transform="translate({-VB[0]} {-VB[1]})">{sym(c1, c2)}</g>'
    return svg(inner, VB[2], VB[3], bg=bg, pad=pad)


def stacked_svg(c1, c2, ink, acc):
    size = 40
    wm, ww = text_path("Virtual IP", 700, size, 0, 0, -8 * size / 64, [ink] * 8 + [acc] * 2)
    W = max(ww, VB[2] * 1.3) + 0
    sx = (W - VB[2]) / 2
    inner = (f'<g transform="translate({sx - VB[0]} {-VB[1]})">{sym(c1, c2)}</g>'
             f'<g transform="translate({(W - ww) / 2},{VB[3] + 12 + size * .72})">{wm}</g>')
    return svg(inner, W, VB[3] + 12 + size * .95)


def tile_svg(size, c_bg, c1, c2, radius_pct, sym_h_pct):
    s = size
    h = s * sym_h_pct
    k = h / VB[3]
    w = VB[2] * k
    inner = (f'<rect width="{s}" height="{s}" rx="{s * radius_pct}" fill="{c_bg}"/>'
             f'<g transform="translate({(s - w) / 2},{(s - h) / 2}) scale({k}) translate({-VB[0]} {-VB[1]})">{sym(c1, c2)}</g>')
    return svg(inner, s, s)


def w(name, content):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content)
    return p


def png(svgpath, width=None, height=None, bg=None):
    out = svgpath[:-4] + (f"-{width}" if width and not height else "") + ".png"
    cmd = ["rsvg-convert", svgpath, "-o", out]
    if width: cmd += ["-w", str(width)]
    if height: cmd += ["-h", str(height)]
    if bg: cmd += ["-b", bg]
    subprocess.run(cmd, check=True)
    return out


def build_files():
    v = {
        "logo-color": lockup_svg(NAVY, BLUE, NAVY, BLUE)[0],
        "logo-reverse": lockup_svg(WHITE, DARK_BLUE, WHITE, SKY)[0],
        "logo-mono-navy": lockup_svg(NAVY, NAVY, NAVY, NAVY)[0],
        "logo-mono-white": lockup_svg(WHITE, WHITE, WHITE, WHITE)[0],
        "logo-stacked-color": stacked_svg(NAVY, BLUE, NAVY, BLUE),
        "logo-stacked-reverse": stacked_svg(WHITE, DARK_BLUE, WHITE, SKY),
        "symbol-color": symbol_svg(NAVY, BLUE),
        "symbol-reverse": symbol_svg(WHITE, DARK_BLUE),
        "symbol-mono-navy": symbol_svg(NAVY, NAVY),
        "symbol-mono-white": symbol_svg(WHITE, WHITE),
    }
    for n, s in v.items():
        p = w(f"svg/{n}.svg", s)
        os.makedirs(f"{OUT}/png", exist_ok=True)
        wd = 2400 if n.startswith("logo") else 1024
        subprocess.run(["rsvg-convert", p, "-w", str(wd), "-o", f"{OUT}/png/{n}.png"], check=True)
    # favicon + avatars
    fav = w("favicon/favicon.svg", tile_svg(64, NAVY, WHITE, DARK_BLUE, 0.22, 0.74))
    for n in (16, 32, 48, 180, 192, 512):
        subprocess.run(["rsvg-convert", fav, "-w", str(n), "-h", str(n), "-o", f"{OUT}/favicon/favicon-{n}.png"], check=True)
    os.replace(f"{OUT}/favicon/favicon-180.png", f"{OUT}/favicon/apple-touch-icon.png")
    from PIL import Image
    im = Image.open(f"{OUT}/favicon/favicon-512.png")
    im.save(f"{OUT}/favicon/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    a1 = w("social/avatar-dark.svg", tile_svg(1000, NAVY, WHITE, DARK_BLUE, 0, 0.56))
    a2 = w("social/avatar-light.svg", tile_svg(1000, MIST, NAVY, BLUE, 0, 0.56))
    for a in (a1, a2):
        subprocess.run(["rsvg-convert", a, "-w", "1024", "-o", a[:-4] + ".png"], check=True)
    # open-graph / LinkedIn banner
    return list(v)


# ---------------------------------------------------------------- brand sheet
def brand_sheet():
    W, H = 2400, 3300
    p = [f'<rect width="{W}" height="{H}" fill="{MIST}"/>']
    p.append(label("Virtual IP", 120, 170, 84, 700))
    p.append(label("Logo guidelines. Concept: a person whose head is a spark. The collar is the V.", 120, 235, 30, 400, NAVY, .75))

    def card(x, y, wd, ht, fill, rx=28):
        p.append(f'<rect x="{x}" y="{y}" width="{wd}" height="{ht}" rx="{rx}" fill="{fill}"/>')

    def place(svgstr, x, y, scale=1.0, wd=None, ht=None):
        # embed a standalone svg via nested <svg> using its own viewBox
        import re
        m = re.search(r'viewBox="([-\d. ]+)"', svgstr)
        vx, vy, vw, vh = map(float, m.group(1).split())
        body = svgstr[svgstr.index(">") + 1: svgstr.rindex("</svg>")]
        return (f'<svg x="{x}" y="{y}" width="{vw * scale}" height="{vh * scale}" viewBox="{vx} {vy} {vw} {vh}">{body}</svg>', vw * scale, vh * scale)

    # 1 primary + reverse
    card(120, 300, 1080, 520, WHITE)
    s, wd, ht = lockup_svg(NAVY, BLUE, NAVY, BLUE, 103)[0], 0, 0
    g, wd, ht = place(s, 0, 0, 2.0)
    g, wd, ht = place(s, 120 + (1080 - wd) / 2, 300 + (520 - ht) / 2, 2.0)
    p.append(g)
    card(1260, 300, 1020, 520, NAVY)
    s = lockup_svg(WHITE, DARK_BLUE, WHITE, SKY, 103)[0]
    g, wd, ht = place(s, 0, 0, 2.0)
    g, wd, ht = place(s, 1260 + (1020 - wd) / 2, 300 + (520 - ht) / 2, 2.0)
    p.append(g)
    p.append(label("Primary logo, on light", 120, 870, 28, 700))
    p.append(label("Reverse logo, on midnight or photography", 1260, 870, 28, 700))

    # 2 clear space + min size
    y0 = 960
    card(120, y0, 1080, 640, WHITE)
    s = lockup_svg(NAVY, BLUE, NAVY, BLUE, 103)[0]
    g, wd, ht = place(s, 0, 0, 1.6)
    ox, oy = 120 + (1080 - wd) / 2, y0 + (640 - ht) / 2
    g, wd, ht = place(s, ox, oy, 1.6)
    p.append(g)
    x_unit = 70 * 1.6 * 0.5  # spark width ~ 38 units * 1.6 -> approx; use 56px
    x_unit = 56
    p.append(f'<rect x="{ox - x_unit}" y="{oy - x_unit}" width="{wd + 2 * x_unit}" height="{ht + 2 * x_unit}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="12 10" rx="6"/>')
    p.append(f'<rect x="{ox - x_unit}" y="{oy - x_unit}" width="{x_unit}" height="{x_unit}" fill="{BLUE}" opacity=".16"/>')
    p.append(label("x", ox - x_unit + 18, oy - x_unit + 38, 30, 700, BLUE))
    p.append(label("Clear space", 120, y0 + 700, 28, 700))
    p.append(label("Keep a margin of x on every side. x is the width of the spark.", 120, y0 + 742, 24, 400, NAVY, .75))

    card(1260, y0, 1020, 640, WHITE)
    s = lockup_svg(NAVY, BLUE, NAVY, BLUE, 103)[0]
    yy = y0 + 150
    for scale, caption in ((0.52, "Logo: 120 px wide minimum"), (0.34, "")):
        pass
    g, wd, ht = place(s, 0, 0, 0.52)
    g, wd, ht = place(s, 1320, y0 + 120, 0.52)
    p.append(g)
    p.append(label("Minimum logo width 120 px (print 30 mm)", 1320, y0 + 120 + ht + 50, 24, 400, NAVY, .8))
    sy = symbol_svg(NAVY, BLUE)
    sx = 1320
    for hh in (96, 64, 40, 24):
        k = hh / VB[3]
        g, wd, ht = place(sy, sx, y0 + 400, k)
        p.append(g)
        sx += wd + 44
    p.append(label("Symbol alone: 24 px minimum", 1320, y0 + 400 + 96 + 62, 24, 400, NAVY, .8))
    p.append(label("Minimum size", 1260, y0 + 700, 28, 700))
    p.append(label("Below 120 px wide, use the symbol alone.", 1260, y0 + 742, 24, 400, NAVY, .75))

    # 3 colour
    y1 = 1800
    p.append(label("Colour", 120, y1, 40, 700))
    cols = [("Midnight", NAVY, "#0A1330", "10 19 48", WHITE), ("Electric blue", BLUE, "#2F6BFF", "47 107 255", WHITE),
            ("Sky", SKY, "#8FB0FF", "143 176 255", NAVY), ("Dark-mode blue", DARK_BLUE, "#5B8CFF", "91 140 255", WHITE),
            ("Mist", MIST, "#F3F6FF", "243 246 255", NAVY)]
    cw = (W - 240 - 4 * 30) / 5
    for i, (n, c, hx, rgb, ink) in enumerate(cols):
        x = 120 + i * (cw + 30)
        stroke = f' stroke="#D5DDF2" stroke-width="2"' if c == MIST else ""
        p.append(f'<rect x="{x}" y="{y1 + 40}" width="{cw}" height="240" rx="24" fill="{c}"{stroke}/>')
        p.append(label(n, x + 24, y1 + 100, 28, 700, ink))
        p.append(label(hx, x + 24, y1 + 232, 26, 500, ink, .9))
        p.append(label("RGB " + rgb, x + 24, y1 + 264, 22, 400, ink, .8))
    p.append(label("Midnight and electric blue carry the logo. Sky and dark-mode blue are for dark backgrounds only.", 120, y1 + 330, 24, 400, NAVY, .75))

    # 4 variants
    y2 = 2250
    p.append(label("Versions", 120, y2, 40, 700))
    vs = [("One colour, midnight", lockup_svg(NAVY, NAVY, NAVY, NAVY, 103)[0], WHITE),
          ("One colour, white", lockup_svg(WHITE, WHITE, WHITE, WHITE, 103)[0], BLUE),
          ("Stacked", stacked_svg(NAVY, BLUE, NAVY, BLUE), WHITE),
          ("Symbol", symbol_svg(NAVY, BLUE), WHITE)]
    vw_ = (W - 240 - 3 * 30) / 4
    for i, (n, s, bg) in enumerate(vs):
        x = 120 + i * (vw_ + 30)
        card(x, y2 + 40, vw_, 340, bg)
        g, wd, ht = place(s, 0, 0, 1)
        sc = min((vw_ - 80) / wd, 190 / ht)
        g, wd, ht = place(s, x + (vw_ - wd * sc) / 2, y2 + 40 + (340 - ht * sc) / 2, sc)
        p.append(g)
        p.append(label(n, x, y2 + 430, 24, 700))

    # 5 don'ts
    y3 = 2760
    p.append(label("Do not", 120, y3, 40, 700))
    donts = [("Stretch or squash", 'transform="scale(1.5 .8)"', WHITE),
             ("Change the colours", None, WHITE),
             ("Rotate or tilt", 'transform="rotate(-12 100 50)"', WHITE),
             ("Place on a busy or low-contrast background", None, "#6F8FE8")]
    for i, (n, tr, bg) in enumerate(donts):
        x = 120 + i * (vw_ + 30)
        card(x, y3 + 40, vw_, 300, bg)
        if i == 1:
            s = lockup_svg("#E5484D", "#34C759", "#F5A524", "#8E4EC6", 103)[0]
        else:
            s = lockup_svg(NAVY, BLUE, NAVY, BLUE, 103)[0]
        g, wd, ht = place(s, 0, 0, 1)
        sc = (vw_ - (200 if i == 0 else 120)) / wd
        g, wd2, ht2 = place(s, x + (vw_ - wd * sc) / 2, y3 + 40 + (300 - ht * sc) / 2, sc)
        if tr:
            cx, cy = x + vw_ / 2, y3 + 190
            t = f"translate({cx} {cy}) scale(1.35 .7) translate({-cx} {-cy})" if "scale" in tr else f"rotate(-12 {cx} {cy})"
            g = f'<g transform="{t}">{g}</g>'
        p.append(g)
        # cross
        p.append(f'<circle cx="{x + vw_ - 36}" cy="{y3 + 76}" r="20" fill="#E5484D"/><path d="M{x + vw_ - 44} {y3 + 68} l16 16 M{x + vw_ - 28} {y3 + 68} l-16 16" stroke="#fff" stroke-width="4" stroke-linecap="round"/>')
        p.append(label(n, x, y3 + 390, 22, 700))
    p.append(label("Logo created for Virtual IP. Wordmark is Bricolage Grotesque Bold, converted to outlines.", 120, 3260, 22, 400, NAVY, .6))
    return svg("".join(p), W, H)


if __name__ == "__main__":
    names = build_files()
    s = brand_sheet()
    w("brand-sheet.svg", s)
    subprocess.run(["rsvg-convert", f"{OUT}/brand-sheet.svg", "-w", "2000", "-o", f"{OUT}/brand-sheet.png"], check=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", f"{OUT}/brand-sheet.svg", "-o", f"{OUT}/brand-sheet.pdf"], check=True)
    print("done", len(names))
