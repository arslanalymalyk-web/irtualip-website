#!/usr/bin/env python3
"""Virtual IP logo generator: outlined wordmark + three symbol concepts."""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import copy

NAVY = "#0A1330"      # midnight
BLUE = "#2F6BFF"      # electric blue
SKY = "#8FB0FF"       # light blue (overlaps, dark-mode accent)
MIST = "#F3F6FF"      # light surface
WHITE = "#FFFFFF"

_BASE = TTFont("../assets/fonts/bricolage.woff2")
_cache = {}


def font(wght):
    if wght not in _cache:
        _cache[wght] = instantiateVariableFont(copy.deepcopy(_BASE), {"wght": wght}, inplace=False)
    return _cache[wght]


def text_path(s, wght, size, x=0, y=0, track=0, fills=None):
    """Return (svg_paths, width). y is the baseline. fills: list of colours per char (or None)."""
    f = font(wght)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    k = size / upm
    out, cx = [], 0.0
    for i, ch in enumerate(s):
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x + cx * k, y)))
        d = pen.getCommands()
        if d:
            fill = fills[i] if fills else "currentColor"
            out.append(f'<path d="{d}" fill="{fill}"/>')
        cx += gs[g].width + track
    return "".join(out), (cx - track) * k


# ---------------------------------------------------------------- symbols (100 x 100 box)
def sym_person(c1=NAVY, c2=BLUE):
    """A: a person and a node in one shape. V = raised arms, dot = head / AI node."""
    return (f'<path d="M23 42 L50 80 L77 42" fill="none" stroke="{c1}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="50" cy="19" r="10.5" fill="{c2}"/>'
            f'<path d="M30 12.5 A24 24 0 0 1 70 12.5" fill="none" stroke="{c2}" stroke-width="3.2" stroke-linecap="round" opacity=".55"/>')


def sym_network(c1=NAVY, c2=BLUE, bg=WHITE):
    """B: three routed nodes forming a V (an address path)."""
    return (f'<path d="M20 24 L50 78 L80 24" fill="none" stroke="{c1}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="20" cy="24" r="11" fill="{bg}" stroke="{c1}" stroke-width="7"/>'
            f'<circle cx="80" cy="24" r="11" fill="{bg}" stroke="{c2}" stroke-width="7"/>'
            f'<circle cx="50" cy="78" r="13" fill="{c2}"/>')


def sym_fold(c1=NAVY, c2=BLUE, c3=SKY):
    """C: folded ribbon V; the overlap triangle is the premium detail."""
    j = 'stroke-linejoin="round" stroke-width="4"'
    return (f'<polygon points="10,14 36,14 58,84 42,84" fill="{c1}" stroke="{c1}" {j}/>'
            f'<polygon points="90,14 64,14 42,84 58,84" fill="{c2}" stroke="{c2}" {j}/>'
            f'<polygon points="50,58.5 58,84 42,84" fill="{c3}" stroke="{c3}" stroke-linejoin="round" stroke-width="2"/>')


SYMS = {"A": sym_person, "B": sym_network, "C": sym_fold}


# ---------------------------------------------------------------- lockups
def wordmark(size=64, ink=NAVY, accent=BLUE, track=-8):
    s = "Virtual IP"
    fills = [ink] * 7 + [ink] + [accent, accent]  # "Virtual", space, "IP"
    return text_path(s, 700, size, track=track, fills=fills)


def lockup(key, h=120, ink=NAVY, accent=BLUE, extra=None, bg=WHITE, sym_kwargs=None):
    """Horizontal lockup. Returns (svg_inner, width, height)."""
    sk = dict(sym_kwargs or {})
    fn = SYMS[key]
    symbol = fn(**sk) if sk else fn(ink, accent) if key != "B" else fn(ink, accent, bg)
    size = h * 0.56
    wm, ww = text_path("Virtual IP", 700, size, track=-8 * size / 64,
                       fills=[ink] * 8 + [accent] * 2)
    gap = h * 0.26
    sc = h / 100
    base = h / 2 + size * 0.36  # visually centre cap-height on symbol
    inner = (f'<g transform="scale({sc})">{symbol}</g>'
             f'<g transform="translate({h + gap},0)">{text_path("Virtual IP", 700, size, 0, base, -8 * size / 64, [ink] * 8 + [accent] * 2)[0]}</g>')
    return inner, h + gap + ww, h


def svg(inner, w, h, bg=None, pad=0):
    r = f'<rect x="{-pad}" y="{-pad}" width="{w + 2 * pad}" height="{h + 2 * pad}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" '
            f'width="{w + 2 * pad:.0f}" height="{h + 2 * pad:.0f}">{r}{inner}</svg>')


def label(s, x, y, size=22, wght=500, fill=NAVY, opacity=1):
    p, _ = text_path(s, wght, size, x, y)
    return f'<g color="{fill}" fill="{fill}" opacity="{opacity}">{p}</g>'


# ---------------------------------------------------------------- concept sheet
def sheet(path="concepts.svg"):
    W, H = 2400, 1500
    names = {"A": ("A  Person + node", "A person and an AI node, one shape. The warmest idea."),
             "B": ("B  Routed path", "Three nodes on one route. The most literal nod to IP."),
             "C": ("C  Folded V", "Two folded planes. The most premium and ownable.")}
    parts = [f'<rect width="{W}" height="{H}" fill="{MIST}"/>']
    parts.append(label("Virtual IP logo concepts", 90, 120, 56, 700))
    parts.append(label("Midnight #0A1330  ·  Electric blue #2F6BFF  ·  Sky #8FB0FF", 90, 172, 24, 400, NAVY, .7))
    colw = (W - 90 * 2 - 60 * 2) / 3
    for i, k in enumerate("ABC"):
        x0 = 90 + i * (colw + 60)
        # light card with full lockup
        parts.append(f'<rect x="{x0}" y="230" width="{colw}" height="400" rx="28" fill="{WHITE}"/>')
        inner, w, h = lockup(k, 120, bg=WHITE)
        parts.append(f'<g transform="translate({x0 + (colw - w) / 2},{230 + (400 - h) / 2})">{inner}</g>')
        # dark card
        parts.append(f'<rect x="{x0}" y="660" width="{colw}" height="400" rx="28" fill="{NAVY}"/>')
        inner, w, h = lockup(k, 120, ink=WHITE, accent=SKY if k != "C" else SKY, bg=NAVY,
                             sym_kwargs=({"c1": WHITE, "c2": "#5B8CFF", "c3": "#BFD2FF"} if k == "C" else
                                         {"c1": WHITE, "c2": "#5B8CFF", "bg": NAVY} if k == "B" else
                                         {"c1": WHITE, "c2": "#5B8CFF"}))
        parts.append(f'<g transform="translate({x0 + (colw - w) / 2},{660 + (400 - h) / 2})">{inner}</g>')
        # small-size row on light
        parts.append(f'<rect x="{x0}" y="1090" width="{colw}" height="170" rx="28" fill="{WHITE}"/>')
        sx = x0 + 60
        for s in (96, 56, 32, 20):
            sym = SYMS[k]() if k != "B" else sym_network(bg=WHITE)
            parts.append(f'<g transform="translate({sx},{1090 + (170 - s) / 2}) scale({s / 100})">{sym}</g>')
            sx += s + 50
        # titles
        t, d = names[k]
        parts.append(label(t, x0, 1330, 34, 700))
        parts.append(label(d, x0, 1376, 22, 400, NAVY, .75))
    parts.append(label("Light and dark versions above. Bottom row: the symbol alone at 96, 56, 32 and 20 px.", 90, 1450, 22, 400, NAVY, .6))
    open(path, "w").write(svg("".join(parts), W, H))
    return path


if __name__ == "__main__":
    print(sheet())
