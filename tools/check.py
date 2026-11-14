#!/usr/bin/env python3
"""Site checks (no dependencies): python3 tools/check.py. Exits 1 on any failure."""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(p for p in ROOT.glob("*.html"))
errors = []


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids = []; s.links = []; s.refs = []; s.h1 = 0; s.title = ""; s.in_title = False
        s.meta = {}; s.canon = None; s.ld = []; s.in_ld = False; s.imgs_no_alt = 0; s.lang = None; s._buf = ""
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t == "html": s.lang = a.get("lang")
        if t == "h1": s.h1 += 1
        if t == "title": s.in_title = True
        if t == "meta":
            k = a.get("name") or a.get("property")
            if k: s.meta[k] = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "link" and a.get("href"): s.refs.append(a["href"])
        if t == "script":
            if a.get("src"): s.refs.append(a["src"])
            if a.get("type") == "application/ld+json": s.in_ld = True; s._buf = ""
        if t == "a" and a.get("href"): s.links.append(a["href"])
        if t == "img":
            if "alt" not in a: s.imgs_no_alt += 1
            if a.get("src"): s.refs.append(a["src"])
    def handle_endtag(s, t):
        if t == "title": s.in_title = False
        if t == "script" and s.in_ld: s.ld.append(s._buf); s.in_ld = False
    def handle_data(s, d):
        if s.in_title: s.title += d
        if s.in_ld: s._buf += d


info = {}
for f in PAGES:
    p = P(); p.feed(f.read_text(encoding="utf-8")); info[f.name] = p

for name, p in info.items():
    e = lambda m: errors.append(f"{name}: {m}")
    if not p.lang: e("missing <html lang>")
    if not p.title.strip(): e("missing <title>")
    if not p.meta.get("description"): e("missing meta description")
    if p.h1 != 1: e(f"expected one h1, found {p.h1}")
    if name != "404.html":
        if not p.canon: e("missing canonical")
        if not p.meta.get("og:image"): e("missing og:image")
    if len(p.ids) != len(set(p.ids)): e("duplicate ids: " + ", ".join(sorted({i for i in p.ids if p.ids.count(i) > 1})))
    if p.imgs_no_alt: e(f"{p.imgs_no_alt} img without alt")
    if not p.ld: e("no JSON-LD")
    for raw in p.ld:
        try: json.loads(raw)
        except Exception as x: e(f"invalid JSON-LD: {x}")
    for href in p.links:
        u = urlparse(href)
        if u.scheme in ("http", "https", "mailto", "tel", "javascript") or href == "#": continue
        target = u.path or name
        if target.startswith("/"): target = target[1:] or "index.html"
        if not (ROOT / target).exists(): e(f"broken link {href}"); continue
        if u.fragment and target.endswith(".html") and u.fragment not in info.get(Path(target).name, P()).ids and info.get(Path(target).name):
            e(f"missing anchor {href}")
    for ref in p.refs:
        u = urlparse(ref)
        if u.scheme or ref.startswith("//") or ref.startswith("data:"): continue
        if name != "404.html" and not (ROOT / u.path.lstrip("/")).exists(): e(f"missing file {ref}")

sm = (ROOT / "sitemap.xml").read_text() if (ROOT / "sitemap.xml").exists() else ""
if not sm: errors.append("sitemap.xml missing")
for n in info:
    if n != "404.html" and (f"/{n}<" not in sm and not (n == "index.html" and re.search(r"/</loc>", sm))): errors.append(f"sitemap missing {n}")
if not (ROOT / "robots.txt").exists(): errors.append("robots.txt missing")
if not (ROOT / "assets/img/og.png").exists(): errors.append("assets/img/og.png missing")

print(f"checked {len(info)} pages")
if errors:
    print("\n".join("FAIL " + x for x in errors)); sys.exit(1)
print("all checks passed")
