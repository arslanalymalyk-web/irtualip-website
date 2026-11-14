import asyncio, sys, subprocess, time, tempfile, shutil
from pathlib import Path
from playwright.async_api import async_playwright

SITE = Path(__file__).resolve().parent.parent
SHOTS = Path(tempfile.gettempdir()) / "virtualip-shots"; SHOTS.mkdir(parents=True, exist_ok=True)
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
server = subprocess.Popen([sys.executable, "-m", "http.server", "8124", "--bind", "127.0.0.1", "-d", str(SITE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
BASE = "http://127.0.0.1:8124/"

async def main():
    res = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        await pg.goto(BASE + "index.html", wait_until="networkidle")

        # hero video actually plays on desktop
        await pg.wait_for_timeout(2000)
        st = await pg.evaluate("(() => {const v=document.querySelector('.hero video'); return {paused:v.paused, t:v.currentTime, ready:v.readyState, op:getComputedStyle(v).opacity, src:v.currentSrc.split('/').pop()}})()")
        res.append(("hero video", st))
        await pg.click("[data-media-toggle]")
        await pg.wait_for_timeout(300)
        res.append(("pause works", await pg.evaluate("document.querySelector('.hero video').paused")))

        # stats counters end at the right numbers
        await pg.evaluate("document.querySelector('.stats').scrollIntoView()")
        await pg.wait_for_timeout(2200)
        res.append(("stats", await pg.eval_on_selector_all(".stat__num", "e => e.map(x => x.textContent)")))

        # quiz full flow
        await pg.evaluate("document.querySelector('#readiness').scrollIntoView()")
        for i in range(6):
            await pg.check(f"input[name=q{i}][value='{[3,2,1,3,0,2][i]}']", force=True)
            await pg.click(".quiz__nav .btn:last-child")
            await pg.wait_for_timeout(150)
        txt = await pg.inner_text(".quiz__result")
        res.append(("quiz result", txt.split("\n")[:3]))
        res.append(("quiz cta", await pg.get_attribute(".quiz__result a.btn", "href")))
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path=str(SHOTS / "quiz-result.png"), clip={"x": 0, "y": 0, "width": 1440, "height": 900})
        await pg.evaluate("document.querySelector('#readiness').scrollIntoView()"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=str(SHOTS / "quiz-result.png"))

        # theme toggle + persistence
        await pg.click(".theme-toggle");
        res.append(("theme after click", await pg.evaluate("document.documentElement.dataset.theme + ' / ' + localStorage.getItem('vip-theme')")))
        await pg.reload(wait_until="networkidle")
        res.append(("theme persists", await pg.evaluate("document.documentElement.dataset.theme")))
        await pg.screenshot(path=str(SHOTS / "home-dark-top.png"))
        await pg.evaluate("document.querySelector('#services').scrollIntoView()"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(SHOTS / "services-dark.png"))
        res.append(("home errors", errs))

        # contact form: validation, prefill, mailto
        c2 = await b.new_context(viewport={"width": 1280, "height": 900})
        cp = await c2.new_page()
        await cp.goto(BASE + "contact.html?topic=ai-roadmap&stage=Ready%20to%20prove%20it&score=11&focus=Data#contact-form", wait_until="networkidle")
        res.append(("prefill", (await cp.input_value("#message"))[:70]))
        await cp.click("button[type=submit]")
        res.append(("errors shown", await cp.eval_on_selector_all(".error", "e => e.map(x => x.textContent)")))
        res.append(("focus on first invalid", await cp.evaluate("document.activeElement.id")))
        await cp.screenshot(path=str(SHOTS / "contact-errors.png"))
        await cp.fill("#name", "Test User"); await cp.fill("#email", "t@example.com")
        await cp.click("button[type=submit]")
        await cp.wait_for_timeout(300)
        res.append(("status", await cp.inner_text("#form-status")))

        # mobile menu
        m = await b.new_context(viewport={"width": 390, "height": 844}, has_touch=True)
        mp = await m.new_page(); await mp.goto(BASE + "index.html", wait_until="networkidle")
        await mp.click("[data-menu-btn]"); await mp.wait_for_timeout(500)
        res.append(("menu open", await mp.get_attribute("[data-menu-btn]", "aria-expanded")))
        await mp.screenshot(path=str(SHOTS / "mobile-menu.png"))
        # reduced motion: no video src loaded
        r = await b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        rp = await r.new_page(); await rp.goto(BASE + "index.html", wait_until="networkidle"); await rp.wait_for_timeout(1000)
        res.append(("reduced-motion sources", await rp.evaluate("document.querySelectorAll('.hero video source').length")))
        res.append(("reduced-motion h1 visible", await rp.evaluate("getComputedStyle(document.querySelector('.hero h1 .w')).opacity")))
        await b.close()
    for r in res: print(r)

try: asyncio.run(main())
finally: server.terminate()
