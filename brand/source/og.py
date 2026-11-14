#!/usr/bin/env python3
"""Share image (1200x630) for Open Graph / Twitter. Run from tools/: PYTHONPATH=../brand/source python3 ../brand/source/og.py"""
import re, subprocess
from logo import text_path, NAVY, BLUE, SKY
rev = open("../brand/svg/logo-reverse.svg").read()
inner = re.search(r"<svg[^>]*>(.*)</svg>", rev, re.S).group(1)
lines = ["Enterprise AI, cloud and", "software that holds up", "in production."]
t = ""
for i, l in enumerate(lines):
    p, _ = text_path(l, 700, 68, 80, 330 + i * 80, track=-2)
    t += f'<g color="#FFFFFF">{p}</g>'
sub, _ = text_path("AI  ·  Cloud  ·  Applications  ·  Cybersecurity", 500, 26, 80, 570)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<defs><radialGradient id="g" cx="85%" cy="10%" r="70%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="{NAVY}"/><rect width="1200" height="630" fill="url(#g)"/>
<g transform="translate(80 70) scale(.95)">{inner}</g>{t}<g color="{SKY}">{sub}</g></svg>'''
open("../brand/source/og.svg", "w").write(svg)
subprocess.run(["rsvg-convert", "-w", "1200", "-h", "630", "../brand/source/og.svg", "-o", "../assets/img/og.png"], check=True)
