import asyncio, re, sys, subprocess, time, tempfile, shutil
from pathlib import Path
from playwright.async_api import async_playwright

SITE = Path(__file__).resolve().parent.parent
SHOTS = Path(tempfile.gettempdir()) / "virtualip-shots"; SHOTS.mkdir(parents=True, exist_ok=True)
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
BASE = "http://127.0.0.1:8123/"
server = subprocess.Popen([sys.executable, "-m", "http.server", "8123", "--bind", "127.0.0.1", "-d", str(SITE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

pages = sorted(p.name for p in SITE.glob("*.html"))

async def main():
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        # --- per-page console / network / link checks (desktop)
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        for name in pages:
            page = await ctx.new_page()
            errs = []
            page.on("console", lambda m, errs=errs: errs.append(m.text) if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e, errs=errs: errs.append("PAGEERROR " + str(e)))
            page.on("requestfailed", lambda r, errs=errs: errs.append("REQFAIL " + r.url))
            resp = await page.goto(BASE + name, wait_until="networkidle")
            if resp.status != 200: errs.append(f"status {resp.status}")
            # internal links
            hrefs = await page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
            for h in set(hrefs):
                if h.startswith(("http", "mailto:", "#")): continue
                path, _, frag = h.partition("#")
                path = path.split("?")[0]
                if path and not (SITE / path).exists(): errs.append("BROKEN LINK " + h)
                elif frag and path:
                    txt = (SITE / path).read_text()
                    if f'id="{frag}"' not in txt: errs.append("MISSING ANCHOR " + h)
                elif frag and f'id="{frag}"' not in (SITE / name).read_text(): errs.append("MISSING ANCHOR " + h)
            # horizontal overflow
            ow = await page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            if ow > 0: errs.append(f"HORIZONTAL OVERFLOW {ow}px")
            # images without alt
            noalt = await page.eval_on_selector_all("img:not([alt])", "e => e.length")
            if noalt: errs.append(f"{noalt} img without alt")
            print(f"{name:42s}", "OK" if not errs else errs)
            problems += [(name, e) for e in errs]
            await page.close()
        await ctx.close()

        # --- visual shots
        async def shot(url, name, w, h, scheme=None, full=True, theme=None, scroll=None):
            c = await b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme or "light")
            pg = await c.new_page()
            await pg.goto(BASE + url, wait_until="networkidle")
            if theme:
                await pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
            await pg.wait_for_timeout(2600)
            if full:
                # trigger observers by scrolling through
                H = await pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, H, 700):
                    await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120)
                await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(SHOTS / name), full_page=full)
            await c.close()
        await shot("index.html", "home-desktop.png", 1440, 900)
        await shot("index.html", "home-hero-desktop.png", 1440, 900, full=False)
        await shot("index.html", "home-mobile.png", 390, 844)
        await shot("index.html", "home-dark.png", 1440, 900, scheme="dark")
        await shot("services.html", "services-desktop.png", 1440, 900)
        await shot("contact.html", "contact-desktop.png", 1440, 900)
        await shot("about.html", "about-desktop.png", 1440, 900)
        await shot("team.html", "team-desktop.png", 1440, 900)
        await shot("insights.html", "insights-desktop.png", 1440, 900)
        await shot("case-studies.html", "cases-desktop.png", 1440, 900)
        await b.close()
    print("PROBLEMS:", problems)

try:
    asyncio.run(main())
finally:
    server.terminate()
