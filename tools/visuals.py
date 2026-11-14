"""Code-made visual system for Virtual IP: icons, diagrams, charts, scenes, avatars, product mockups.
Everything is inline SVG/HTML in the brand palette, so it stays sharp, tiny and fully original."""
from html import escape

GOLD, FOREST, BLUSH, MOSS, MINT, PAPER = "#2f6bff", "#0a1330", "#dbe5ff", "#2456d6", "#8fb0ff", "#f3f6ff"

# ------------------------------------------------------------------ icons (24px, 1.75 stroke)
ICON = {
    "ai": '<circle cx="6" cy="6" r="2.3"/><circle cx="18" cy="6" r="2.3"/><circle cx="12" cy="18.2" r="2.3"/><path d="M7.7 7.6l3.1 8.4M16.3 7.6l-3.1 8.4M8.3 6h7.4"/><circle cx="12" cy="10.4" r=".9" fill="currentColor"/>',
    "data": '<ellipse cx="12" cy="5.8" rx="7" ry="2.8"/><path d="M5 5.8v6.2c0 1.55 3.1 2.8 7 2.8s7-1.25 7-2.8V5.8M5 12v6.2c0 1.55 3.1 2.8 7 2.8s7-1.25 7-2.8V12"/>',
    "cloud": '<path d="M7.2 18.5a4.1 4.1 0 01-.6-8.15A5.6 5.6 0 0117.2 8.6a4.95 4.95 0 01.4 9.9H7.2z"/>',
    "app": '<rect x="3" y="4" width="18" height="16" rx="2.6"/><path d="M3 9h18M7 14.5h4M7 17h7"/><circle cx="6.2" cy="6.5" r=".6" fill="currentColor"/><circle cx="8.6" cy="6.5" r=".6" fill="currentColor"/>',
    "shield": '<path d="M12 3l7.2 2.9v5.6c0 4.3-2.9 7.9-7.2 9.5-4.3-1.6-7.2-5.2-7.2-9.5V5.9L12 3z"/><path d="M8.8 12l2.4 2.4 4.2-4.6"/>',
    "blocks": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/><path d="M11 7h2.5a3 3 0 013 3v3"/><path d="M14.2 11.2L16.5 13.5 18.8 11.2"/>',
    "gauge": '<path d="M4.4 17.2a8.6 8.6 0 1115.2 0"/><path d="M12 13.2l3.8-4.2"/><circle cx="12" cy="13.6" r="1.4"/><path d="M7 17.4h10"/>',
    "headset": '<path d="M4.5 14v-2.2a7.5 7.5 0 0115 0V14"/><path d="M4.5 14h3v5h-1.6a1.4 1.4 0 01-1.4-1.4V14zM19.5 14h-3v5h1.6a1.4 1.4 0 001.4-1.4V14z"/><path d="M17.5 19c0 1.6-2 2.2-5.5 2.2"/>',
    "pipeline": '<circle cx="4.5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19.5" cy="12" r="2"/><path d="M6.5 12h3.5M14 12h3.5"/><path d="M12 6V3.5M12 20.5V18"/>',
    "chart": '<path d="M4 4v16h16"/><rect x="7.5" y="11" width="3" height="6" rx=".8"/><rect x="12.5" y="7.5" width="3" height="9.5" rx=".8"/><path d="M17.5 9l2-2.4"/>',
    "doc": '<path d="M7 3h7l4 4v14H7V3z"/><path d="M14 3v4h4M10 12h5M10 15.5h5M10 8.5h2"/>',
    "people": '<circle cx="9" cy="8.5" r="3"/><path d="M3.5 20c.4-3.3 2.6-5.2 5.5-5.2s5.1 1.9 5.5 5.2"/><circle cx="17" cy="9.5" r="2.4"/><path d="M16.2 14.9c2.4-.2 4 1.3 4.5 4.1"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/>',
    "bolt": '<path d="M13 2.8L5 13.2h6l-1 8 8-10.6h-6l1-7.8z"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.4"/><path d="M8 10.5V8a4 4 0 018 0v2.5"/><circle cx="12" cy="15.5" r="1.3" fill="currentColor"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.8"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
    "coins": '<ellipse cx="9.5" cy="7" rx="6" ry="2.6"/><path d="M3.5 7v4c0 1.4 2.7 2.6 6 2.6s6-1.2 6-2.6V7M3.5 11v4c0 1.4 2.7 2.6 6 2.6"/><path d="M15.5 12.4c2.8.1 5 1.2 5 2.5v4c0 1.4-2.7 2.6-6 2.6-2.2 0-4.1-.5-5.1-1.3"/>',
    "pulse": '<path d="M2.5 12.5h4.2l2.2-5 3.4 10 2.4-5h6.8"/>',
    "route": '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8 18h5.5a3.5 3.5 0 000-7h-3a3.5 3.5 0 010-7H15.8"/>',
    "box": '<path d="M3 7.4l9-4.2 9 4.2-9 4.2-9-4.2zM3 7.4v9.2l9 4.2 9-4.2V7.4M12 11.6v9.2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.6"/><path d="M3.8 7l8.2 6 8.2-6"/>',
    "briefcase": '<rect x="3" y="7.5" width="18" height="12.5" rx="2.4"/><path d="M9 7.5V6a2 2 0 012-2h2a2 2 0 012 2v1.5M3 13h18"/>',
    "layers": '<path d="M12 3.5l9 4.6-9 4.6-9-4.6 9-4.6zM3 12.2l9 4.6 9-4.6M3 16.4l9 4.6 9-4.6"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.8 2.8 5.2-5.6"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.8 13.5L7.5 21l4.5-2.4 4.5 2.4-1.3-7.5"/><path d="M10 9l1.5 1.5L14.3 7.6"/>',
    "map": '<path d="M9 4L3.5 6v14L9 18l6 2 5.5-2V4L15 6 9 4zM9 4v14M15 6v14"/>',
    "server": '<rect x="3.5" y="4" width="17" height="6.5" rx="2"/><rect x="3.5" y="13.5" width="17" height="6.5" rx="2"/><circle cx="7.5" cy="7.2" r=".8" fill="currentColor"/><circle cx="7.5" cy="16.8" r=".8" fill="currentColor"/><path d="M11 7.2h6M11 16.8h6"/>',
}


def icon(name, size=24, cls="icon"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


def tile(name, tone="gold", size=22):
    return f'<span class="icon-tile icon-tile--{tone}">{icon(name, size)}</span>'


# ------------------------------------------------------------------ architecture diagram (AI tile)
def arch_diagram():
    srcs = [("CRM", 14), ("ERP", 70), ("Documents", 126), ("Logs & events", 182)]
    s = ['<svg class="diagram" viewBox="0 0 540 250" role="img" aria-label="Data from your CRM, ERP, documents and logs flows through a governed pipeline and a model to a decision with a reason.">']
    s.append('<g class="d-flow" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">')
    for _, y in srcs:
        s.append(f'<path d="M112 {y+22} C 138 {y+22}, 128 125, 156 125"/>')
    s.append('<path d="M256 125H298"/><path d="M398 125H440"/></g>')
    for label, y in srcs:
        s.append(f'<rect x="8" y="{y}" width="104" height="44" rx="12" class="d-box"/><text x="60" y="{y+27}" text-anchor="middle" class="d-t">{label}</text>')
    s.append('<rect x="156" y="68" width="100" height="114" rx="16" class="d-box"/><text x="206" y="112" text-anchor="middle" class="d-t d-b">Governed</text><text x="206" y="130" text-anchor="middle" class="d-t d-b">pipeline</text><text x="206" y="154" text-anchor="middle" class="d-s">clean · secure</text>')
    s.append(f'<rect x="298" y="68" width="100" height="114" rx="16" fill="{GOLD}"/><text x="348" y="112" text-anchor="middle" class="d-t d-b" style="fill:{FOREST}">Model</text><text x="348" y="130" text-anchor="middle" class="d-t d-b" style="fill:{FOREST}">+ rules</text><text x="348" y="154" text-anchor="middle" class="d-s" style="fill:{FOREST}">tested on baseline</text>')
    s.append('<rect x="440" y="52" width="92" height="146" rx="16" class="d-box d-strong"/><text x="486" y="100" text-anchor="middle" class="d-t d-b">Decision</text><text x="486" y="120" text-anchor="middle" class="d-s">+ reason</text><text x="486" y="150" text-anchor="middle" class="d-s">a person can</text><text x="486" y="164" text-anchor="middle" class="d-s">review it</text>')
    s.append('</svg>')
    return "".join(s)


# ------------------------------------------------------------------ mini illustrations for bento tiles
def mini(kind):
    h = '<svg class="mini" viewBox="0 0 220 110" fill="none" aria-hidden="true">'
    if kind == "cloud":
        h += ('<g class="m-line" stroke="currentColor" stroke-width="1.5"><rect x="38" y="64" width="144" height="30" rx="9" opacity=".5"/><rect x="26" y="40" width="168" height="30" rx="9" opacity=".75"/>'
              f'</g><rect x="14" y="14" width="192" height="30" rx="9" fill="{GOLD}"/>'
              '<g fill="currentColor" opacity=".7"><circle cx="34" cy="29" r="3"/><circle cx="46" cy="29" r="3"/></g>'
              f'<g fill="{FOREST}"><rect x="140" y="26" width="52" height="6" rx="3" opacity=".6"/></g>'
              '<g fill="currentColor" opacity=".55"><circle cx="46" cy="55" r="3"/><circle cx="58" cy="55" r="3"/><circle cx="58" cy="79" r="3"/><circle cx="70" cy="79" r="3"/></g>')
    elif kind == "app":
        h += ('<rect x="14" y="8" width="192" height="94" rx="12" class="m-fill"/><path d="M14 28h192" class="m-line" stroke="currentColor" stroke-width="1.4" opacity=".5"/>'
              '<g fill="currentColor" opacity=".6"><circle cx="26" cy="18" r="2.4"/><circle cx="35" cy="18" r="2.4"/><circle cx="44" cy="18" r="2.4"/></g>'
              f'<rect x="24" y="38" width="38" height="54" rx="6" fill="currentColor" opacity=".12"/><rect x="72" y="38" width="62" height="24" rx="7" fill="{GOLD}"/>'
              '<rect x="142" y="38" width="54" height="24" rx="7" fill="currentColor" opacity=".16"/><rect x="72" y="70" width="124" height="22" rx="7" fill="currentColor" opacity=".12"/>')
    elif kind == "security":
        h += ('<g class="m-pulse" stroke="currentColor" fill="none"><circle cx="110" cy="55" r="44" stroke-width="1.2" opacity=".25"/><circle cx="110" cy="55" r="32" stroke-width="1.2" opacity=".4"/></g>'
              f'<path d="M110 16l30 12v22c0 18-12.5 32-30 40-17.500-8-30-22-30-40V28l30-12z" fill="{GOLD}"/>'
              f'<path d="M96 56l10 10 19-21" stroke="{FOREST}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "blocks":
        h += ('<g stroke="currentColor" stroke-width="1.5" class="m-line"><path d="M72 40h24c8 0 12 4 12 12v6" opacity=".7"/><path d="M148 70h-24c-8 0-12-4-12-12" opacity=".7"/></g>'
              f'<rect x="20" y="22" width="52" height="40" rx="10" class="m-fill"/><rect x="84" y="58" width="52" height="40" rx="10" fill="{GOLD}"/><rect x="148" y="22" width="52" height="40" rx="10" class="m-fill"/>'
              '<g fill="currentColor" opacity=".5"><rect x="30" y="34" width="26" height="5" rx="2.5"/><rect x="30" y="45" width="16" height="5" rx="2.5"/><rect x="158" y="34" width="26" height="5" rx="2.5"/><rect x="158" y="45" width="16" height="5" rx="2.5"/></g>')
    elif kind == "gauge":
        h += ('<path d="M30 88a80 80 0 11160 0" class="m-line" stroke="currentColor" stroke-width="10" stroke-linecap="round" opacity=".14"/>'
              f'<path class="m-draw" d="M30 88a80 80 0 0176-80" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
              f'<path d="M110 88l36-34" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="110" cy="88" r="8" fill="currentColor"/>')
    h += '</svg>'
    return h


def method_art(kind):
    h = '<svg class="method-art" viewBox="0 0 240 96" fill="none" aria-hidden="true">'
    if kind == "map":
        h += ('<g stroke="currentColor" stroke-width="1.4" opacity=".4" stroke-dasharray="3 4"><path d="M24 70 L86 34 L146 64 L212 26"/></g>'
              f'<circle cx="24" cy="70" r="7" fill="currentColor" opacity=".2"/><circle cx="86" cy="34" r="7" fill="currentColor" opacity=".35"/><circle cx="146" cy="64" r="7" fill="currentColor" opacity=".5"/><circle cx="212" cy="26" r="9" fill="{GOLD}"/>'
              '<circle cx="212" cy="26" r="3" fill="#0a1330"/>')
    elif kind == "prove":
        h += ('<g fill="currentColor"><rect x="20" y="52" width="26" height="30" rx="6" opacity=".18"/><rect x="58" y="40" width="26" height="42" rx="6" opacity=".3"/>'
              f'<rect x="96" y="28" width="26" height="54" rx="6" opacity=".5"/></g><rect x="134" y="14" width="26" height="68" rx="6" fill="{GOLD}"/>'
              '<path d="M178 48l12 12 26-30" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        h += ('<g stroke="currentColor" stroke-width="1.5" opacity=".5"><path d="M16 70h208"/></g>'
              f'<rect x="20" y="30" width="64" height="40" rx="10" class="m-fill"/><rect x="94" y="22" width="64" height="48" rx="10" fill="{GOLD}"/><rect x="168" y="30" width="52" height="40" rx="10" class="m-fill"/>'
              '<g fill="currentColor" opacity=".6"><circle cx="34" cy="44" r="3"/><circle cx="182" cy="44" r="3"/></g><path d="M108 46l9 9 16-18" stroke="#0a1330" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return h + '</svg>'


# ------------------------------------------------------------------ charts
def area_chart(vals, w=520, h=170, uid="a", draw=True):
    n = len(vals); mx = max(vals) * 1.15; mn = 0
    pad = 8
    pts = [(pad + i * (w - 2 * pad) / (n - 1), h - 16 - (v - mn) / (mx - mn) * (h - 34)) for i, v in enumerate(vals)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, n):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]; cx = (x0 + x1) / 2
        d += f" C{cx:.1f} {y0:.1f}, {cx:.1f} {y1:.1f}, {x1:.1f} {y1:.1f}"
    area = d + f" L{pts[-1][0]:.1f} {h-16} L{pts[0][0]:.1f} {h-16} Z"
    grid = "".join(f'<path d="M0 {h-16-i*(h-34)/3:.1f}H{w}" stroke="currentColor" opacity=".12"/>' for i in range(4))
    return (f'<svg class="chart" viewBox="0 0 {w} {h}" fill="none" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="g{uid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".5"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<path d="{area}" fill="url(#g{uid})" class="c-area"/><path d="{d}" stroke="{GOLD}" stroke-width="2.5" stroke-linecap="round" class="{"c-line" if draw else ""}" pathLength="1"/>'
            f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="{GOLD}"/></svg>')


def bars(vals, w=260, h=110, hi=-1, cls="chart"):
    n = len(vals); mx = max(vals); bw = (w - (n - 1) * 6) / n
    r = []
    for i, v in enumerate(vals):
        bh = v / mx * (h - 6)
        fill = GOLD if (i == hi or (hi == -1 and i == n - 1)) else "currentColor"
        op = "" if fill == GOLD else ' opacity=".28"'
        r.append(f'<rect class="c-bar" style="--i:{i}" x="{i*(bw+6):.1f}" y="{h-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="{fill}"{op}/>')
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{"".join(r)}</svg>'


def donut(parts, size=120):
    r = 46; c = 2 * 3.14159 * r; off = 0; cols = [GOLD, "currentColor", MINT, BLUSH]
    out = [f'<svg class="donut" viewBox="0 0 120 120" width="{size}" height="{size}" aria-hidden="true"><g transform="rotate(-90 60 60)" fill="none" stroke-width="16">']
    for i, p in enumerate(parts):
        ln = c * p / 100
        op = ' opacity=".35"' if cols[i % 4] == "currentColor" else ""
        out.append(f'<circle cx="60" cy="60" r="{r}" stroke="{cols[i%4]}"{op} stroke-dasharray="{ln-2:.1f} {c-ln+2:.1f}" stroke-dashoffset="{-off:.1f}"/>')
        off += ln
    return "".join(out) + '</g></svg>'


def before_after(before, after, label, fmt="{}", unit="", better="lower"):
    """Index-style before/after bars, heights scaled to the larger value."""
    mx = max(before, after)
    hb, ha = before / mx * 100, after / mx * 100
    return (f'<figure class="ba" role="group" aria-label="{escape(label)}: before {fmt.format(before)}{unit}, after {fmt.format(after)}{unit}">'
            f'<div class="ba__cols"><div class="ba__col"><span class="ba__val">{fmt.format(before)}{unit}</span><i class="ba__bar" style="--h:{hb:.0f}"></i><span class="ba__lab">Before</span></div>'
            f'<div class="ba__col ba__col--after"><span class="ba__val">{fmt.format(after)}{unit}</span><i class="ba__bar" style="--h:{ha:.0f}"></i><span class="ba__lab">After</span></div></div>'
            f'<figcaption>{escape(label)}</figcaption></figure>')


def spark(vals, w=120, h=36):
    mx, mn = max(vals), min(vals)
    pts = " ".join(f"{i*w/(len(vals)-1):.1f},{h-3-(v-mn)/(mx-mn or 1)*(h-8):.1f}" for i, v in enumerate(vals))
    return f'<svg class="spark" viewBox="0 0 {w} {h}" fill="none" aria-hidden="true"><polyline points="{pts}" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" pathLength="1" class="c-line"/></svg>'


# ------------------------------------------------------------------ industry scenes (360x210)
def scene(kind):
    s = '<svg class="scene" viewBox="0 0 360 210" fill="none" role="img" aria-label="{}">'
    if kind == "fintech":
        s = s.format("Illustration of a payment card, coins and a rising line chart")
        s += (f'<rect width="360" height="210" rx="22" fill="{FOREST}"/><g stroke="{MINT}" opacity=".12"><path d="M0 60H360M0 110H360M0 160H360M60 0V210M130 0V210M200 0V210M270 0V210"/></g>'
              f'<path d="M24 160 C 80 150, 90 110, 140 112 S 210 80, 250 70 S 310 40, 340 30" stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round" class="c-line" pathLength="1"/>'
              f'<rect x="40" y="62" width="150" height="92" rx="14" fill="{BLUSH}"/><rect x="40" y="82" width="150" height="16" fill="{FOREST}" opacity=".85"/><rect x="54" y="116" width="52" height="8" rx="4" fill="{FOREST}" opacity=".6"/><rect x="54" y="130" width="34" height="8" rx="4" fill="{FOREST}" opacity=".35"/>'
              f'<circle cx="168" cy="136" r="9" fill="{GOLD}"/><circle cx="156" cy="136" r="9" fill="{GOLD}" opacity=".7"/>'
              f'<g fill="{GOLD}"><ellipse cx="262" cy="170" rx="30" ry="9"/><ellipse cx="262" cy="160" rx="30" ry="9" opacity=".8"/><ellipse cx="262" cy="150" rx="30" ry="9" opacity=".6"/></g><ellipse cx="262" cy="150" rx="30" ry="9" stroke="{FOREST}" stroke-opacity=".4"/>')
    elif kind == "health":
        s = s.format("Illustration of a heartbeat line over a medical cross and appointment tiles")
        s += (f'<rect width="360" height="210" rx="22" fill="{BLUSH}"/><g fill="{FOREST}" opacity=".08"><circle cx="300" cy="40" r="60"/><circle cx="40" cy="190" r="50"/></g>'
              f'<rect x="132" y="38" width="96" height="96" rx="24" fill="{FOREST}"/><path d="M180 62v48M156 86h48" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>'
              f'<path d="M20 168h84l16-28 24 52 20-38 14 14h182" stroke="{FOREST}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="c-line" pathLength="1"/>'
              f'<rect x="248" y="40" width="88" height="40" rx="12" fill="#fff" opacity=".85"/><rect x="258" y="52" width="40" height="6" rx="3" fill="{FOREST}" opacity=".5"/><rect x="258" y="64" width="26" height="6" rx="3" fill="{FOREST}" opacity=".3"/><circle cx="318" cy="60" r="7" fill="{MOSS}"/>'
              f'<rect x="24" y="48" width="84" height="40" rx="12" fill="#fff" opacity=".85"/><rect x="34" y="60" width="44" height="6" rx="3" fill="{FOREST}" opacity=".5"/><rect x="34" y="72" width="28" height="6" rx="3" fill="{FOREST}" opacity=".3"/>')
    else:
        s = s.format("Illustration of a route connecting three locations with a parcel")
        s += (f'<rect width="360" height="210" rx="22" fill="{MOSS}"/><g stroke="{PAPER}" opacity=".14"><path d="M0 70H360M0 140H360M90 0V210M180 0V210M270 0V210"/></g>'
              f'<path d="M50 150 C 110 150, 110 70, 170 70 S 250 150, 310 60" stroke="{PAPER}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round" class="d-flow"/>'
              f'<g fill="{GOLD}"><circle cx="50" cy="150" r="13"/><circle cx="170" cy="70" r="13"/><circle cx="310" cy="60" r="13"/></g><g fill="{FOREST}"><circle cx="50" cy="150" r="5"/><circle cx="170" cy="70" r="5"/><circle cx="310" cy="60" r="5"/></g>'
              f'<g transform="translate(206 112)"><rect width="52" height="40" rx="8" fill="{PAPER}"/><path d="M0 14h52M26 0v14" stroke="{FOREST}" stroke-opacity=".35" stroke-width="2"/><rect x="18" y="22" width="16" height="6" rx="3" fill="{FOREST}" opacity=".4"/></g>'
              f'<rect x="24" y="22" width="92" height="30" rx="10" fill="{PAPER}" opacity=".92"/><rect x="34" y="33" width="46" height="6" rx="3" fill="{FOREST}" opacity=".5"/>')
    return s + '</svg>'


# ------------------------------------------------------------------ page-head art: threads converging on a node, with floating icon tiles
_ART = {
    "services": [("ai", 12, 14, "gold"), ("cloud", 62, 6, "blush"), ("shield", 74, 56, "mint"), ("app", 8, 62, "blush")],
    "about": [("people", 14, 18, "gold"), ("globe", 66, 10, "blush"), ("award", 72, 58, "mint"), ("target", 10, 64, "blush")],
    "cases": [("chart", 12, 12, "gold"), ("bolt", 66, 8, "blush"), ("target", 74, 58, "mint"), ("gauge", 8, 62, "blush")],
    "insights": [("doc", 12, 12, "gold"), ("eye", 66, 10, "blush"), ("ai", 74, 58, "mint"), ("map", 8, 62, "blush")],
    "careers": [("briefcase", 12, 12, "gold"), ("people", 66, 8, "blush"), ("blocks", 74, 58, "mint"), ("bolt", 8, 62, "blush")],
    "team": [("people", 12, 12, "gold"), ("ai", 66, 8, "blush"), ("shield", 74, 58, "mint"), ("cloud", 8, 62, "blush")],
    "contact": [("mail", 12, 14, "gold"), ("headset", 66, 8, "blush"), ("globe", 74, 58, "mint"), ("check", 8, 62, "blush")],
}


def page_art(kind):
    paths = ""
    for i, y in enumerate([10, 40, 72, 104, 136, 168, 196]):
        paths += f'<path d="M0 {y} C 120 {y}, 190 100, 300 100"/>'
    tiles = "".join(f'<span class="art-tile" style="left:{x}%;top:{y}%;--d:{i}">{tile(n, t, 22)}</span>' for i, (n, x, y, t) in enumerate(_ART[kind]))
    return (f'<div class="page-art" aria-hidden="true"><svg viewBox="0 0 360 200" fill="none" preserveAspectRatio="xMidYMid slice"><g stroke="currentColor" stroke-width="1.2" opacity=".35">{paths}</g>'
            f'<g stroke="currentColor" stroke-width="1.2" opacity=".35"><path d="M312 100 C 330 100, 345 86, 360 74"/><path d="M312 100 C 330 100, 345 114, 360 126"/></g>'
            f'<circle cx="306" cy="100" r="26" fill="{GOLD}" opacity=".22"/><circle cx="306" cy="100" r="9" fill="{GOLD}"/><circle cx="306" cy="100" r="3.2" fill="{FOREST}"/></svg>{tiles}</div>')


# ------------------------------------------------------------------ abstract portrait avatars (no faces, so nobody is misrepresented)
_TONES = [(FOREST, GOLD, BLUSH), (BLUSH, FOREST, "#fff"), (GOLD, FOREST, BLUSH), (MOSS, "#f3f6ff", MINT)]


def avatar(i, initials):
    bg, fg, skin = _TONES[i % 4]
    hair = [f'<path d="M62 62a28 28 0 0156 0c0-14-12-22-28-22s-28 8-28 22z" fill="{fg}"/>',
            f'<circle cx="90" cy="40" r="11" fill="{fg}"/><path d="M62 64a28 28 0 0156 0c-8-8-20-9-28-9s-20 1-28 9z" fill="{fg}"/>',
            f'<path d="M60 70c0-22 12-34 30-34s30 12 30 34c0 10-3 22-5 30h-6c3-14 2-34-19-34s-22 20-19 34h-6c-2-8-5-20-5-30z" fill="{fg}"/>',
            f'<path d="M60 62a30 30 0 0160 0z" fill="{fg}"/><rect x="58" y="60" width="64" height="7" rx="3.5" fill="{fg}"/>'][(i * 3 + 1) % 4]
    return (f'<svg class="avatar-svg" viewBox="0 0 180 225" role="img" aria-label="Illustrated portrait placeholder for {escape(initials)}"><rect width="180" height="225" fill="{bg}"/>'
            f'<circle cx="150" cy="30" r="70" fill="{fg}" opacity=".13"/><circle cx="20" cy="210" r="60" fill="{fg}" opacity=".1"/>'
            f'<path d="M22 225c2-44 28-64 68-64s66 20 68 64z" fill="{fg}" opacity=".9"/><path d="M72 160h36v14c-6 7-30 7-36 0z" fill="{skin}" opacity=".9"/>'
            f'<ellipse cx="90" cy="98" rx="26" ry="31" fill="{skin}"/>{hair}</svg>')


def post_cover(i):
    kinds = [("ai", "target", "data"), ("cloud", "server", "shield"), ("bolt", "layers", "check")]
    a, b, c = kinds[i % 3]
    return (f'<div class="post-cover" aria-hidden="true"><svg viewBox="0 0 160 110" fill="none"><g stroke="currentColor" opacity=".3" stroke-width="1.2"><path d="M0 20C50 20 70 55 120 55M0 55H120M0 90C50 90 70 55 120 55"/></g>'
            f'<circle cx="126" cy="55" r="16" fill="{GOLD}" opacity=".35"/><circle cx="126" cy="55" r="7" fill="{GOLD}"/></svg>'
            f'<span class="art-tile" style="left:8%;top:10%">{tile(a,"gold",20)}</span><span class="art-tile" style="left:8%;top:62%">{tile(b,"blush",20)}</span><span class="art-tile" style="left:44%;top:36%">{tile(c,"mint",20)}</span></div>')


# ------------------------------------------------------------------ product mockups (illustrative interfaces)
def _win(url, body, cls=""):
    return f'<div class="mock {cls}"><div class="mock__bar"><i></i><i></i><i></i><span class="mock__url">{url}</span></div><div class="mock__body">{body}</div></div>'


def mock_triage():
    rows = [("CL-4821", "Water damage, roof", 0.93, "Senior adjuster", "hi"), ("CL-4822", "Windscreen", 0.12, "Auto-approve", "lo"),
            ("CL-4823", "Vehicle theft", 0.77, "Fraud review", "mid"), ("CL-4824", "Minor collision", 0.35, "Standard queue", "lo"),
            ("CL-4825", "Commercial fire", 0.96, "Senior adjuster", "hi")]
    tr = "".join(f'<tr{" class=is-sel" if i == 0 else ""}><td>{c}</td><td>{d}</td><td><span class="meter"><i style="--w:{int(s*100)}%"></i></span> {s:.2f}</td><td><span class="pill pill--{t}">{r}</span></td></tr>' for i, (c, d, s, r, t) in enumerate(rows))
    body = (f'<div class="mock-triage"><div><div class="mock__head"><strong>Incoming claims</strong><span class="pill pill--lo">Live</span></div>'
            f'<table class="mock-table"><thead><tr><th>Claim</th><th>Type</th><th>Risk</th><th>Route</th></tr></thead><tbody>{tr}</tbody></table></div>'
            '<aside class="mock-why"><strong>Why CL-4821 scored 0.93</strong>'
            '<ul><li><span>Claim size vs. policy</span><span class="meter"><i style="--w:82%"></i></span></li><li><span>Damage photo match</span><span class="meter"><i style="--w:64%"></i></span></li>'
            '<li><span>Prior claims</span><span class="meter"><i style="--w:31%"></i></span></li></ul>'
            '<p>Routed to a senior adjuster. A person reviews every high score before any decision is final.</p></aside></div>')
    return _win("claims-console / triage", body)


def mock_cost():
    kp = [("Spend this month", "$184k", "−12%"), ("Forecast", "$171k", "on plan"), ("Idle resources", "42", "−18"), ("Savings found", "$57k", "this quarter")]
    k = "".join(f'<div class="kpi"><span>{a}</span><strong>{b}</strong><em>{c}</em></div>' for a, b, c in kp)
    body = (f'<div class="kpis">{k}</div><div class="mock-cost"><div class="mock-chart"><div class="mock__head"><strong>Monthly cloud spend</strong><span>12 months</span></div>'
            f'{area_chart([100,104,110,116,121,126,124,118,109,101,94,86], 520, 150, "cost")}</div>'
            f'<div class="mock-donut"><strong>By service</strong>{donut([46, 24, 18, 12], 108)}<ul class="legend"><li><i style="background:{GOLD}"></i>Compute</li><li><i style="background:currentColor;opacity:.4"></i>Storage</li><li><i style="background:{MINT}"></i>Data</li><li><i style="background:{BLUSH}"></i>Network</li></ul></div></div>')
    return _win("cloud-ops / cost overview", body)


def mock_pipeline():
    st = [("Commit", "done", "0m"), ("Test", "done", "6m"), ("Scan", "done", "3m"), ("Deploy", "run", "now"), ("Monitor", "wait", "")]
    s = "".join(f'<li class="stage stage--{t}"><span class="stage__dot">{"✓" if t == "done" else ""}</span><strong>{n}</strong><em>{d}</em></li>' for n, t, d in st)
    body = (f'<ol class="stages">{s}</ol><div class="mock-cost"><div class="mock-chart"><div class="mock__head"><strong>Deployments per week</strong><span>last 12 weeks</span></div>'
            f'{bars([2,2,3,3,4,5,5,6,7,8,8,9], 520, 130, 11)}</div><div class="mock-donut"><strong>Latest releases</strong><ul class="runs"><li><span class="pill pill--lo">Passed</span> v4.12.0</li><li><span class="pill pill--lo">Passed</span> v4.11.3</li><li><span class="pill pill--mid">Rolled back</span> v4.11.2</li><li><span class="pill pill--lo">Passed</span> v4.11.1</li></ul></div></div>')
    return _win("delivery / pipeline", body)
