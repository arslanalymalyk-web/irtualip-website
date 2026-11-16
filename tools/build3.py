#!/usr/bin/env python3
"""Post-pass: service detail pages, 404, sitemap.xml, robots.txt. Called at the end of build2's main."""
import re, datetime
import build as b
import build2 as b2
from build import OUT, SITE, escape, write

STEPS = [("Assess", "We start with your goal, your systems and your constraints, and agree what success looks like before any build begins."),
         ("Design", "A written plan with scope, risks and a first milestone you can review with your own team."),
         ("Build", "Small releases you can see and test, with the people doing the work in contact with yours."),
         ("Run", "Handover or ongoing care, with monitoring, documentation and a named person to call.")]
FAQ = {
    "ai-data": [("Do you only build new AI, or also fix existing models?", "Both. We take over models that work in a notebook but not in production, and we start new ones from a defined decision and a baseline."),
                ("Where does our data go?", "We work inside your environment wherever possible. Where that isn't possible, we agree data handling, access and retention in writing before work starts.")],
    "cloud": [("Can you migrate without downtime?", "We plan every move with a cutover and rollback plan. Many workloads move with little or no downtime, and we say plainly when one cannot."),
              ("Which clouds do you work with?", "We work across AWS and Azure, and we design for the provider you already use before suggesting a change.")],
    "apps": [("Do you work with our in-house team?", "Yes. Many engagements run as a dedicated team alongside yours, using your tools and release process."),
             ("Can you modernize a legacy app without a rewrite?", "Often. We move legacy applications in stages, so the business keeps running while the architecture improves.")],
    "security": [("Is this a one-off test or ongoing work?", "Either. A single assessment or penetration test is a common start, and many clients continue with remediation support and regular testing."),
                 ("Will you work with our compliance requirements?", "We map the work to the frameworks you report against and say clearly what we can and cannot attest to.")],
    "implementation": [("Do you integrate with the ERP we already have?", "Yes. We start from the systems you run today and connect them so data is entered once."),
                       ("How do you handle cutover risk?", "With rehearsed cutover plans, test data and a fallback, agreed with your team before the date is set.")],
    "optimization": [("How do you find what to fix first?", "We measure before we change anything, then rank fixes by impact on speed, stability and cost."),
                     ("Will tuning affect reliability?", "Changes ship with tests and rollback, so savings do not come at the expense of uptime.")],
    "support": [("Is support available around the clock?", "We run 24/7 helpdesk and monitoring through our delivery hubs, with service levels written into the agreement."),
                ("Can you take over support from another vendor?", "Yes. We document the estate, agree service levels and transition in stages.")],
}
SHORT = {"ai-data": "AI and data", "cloud": "cloud", "apps": "application development", "security": "cybersecurity",
         "implementation": "implementation", "optimization": "optimization", "support": "managed IT"}


def pillars():
    src = open(b.__file__).read()
    m = re.search(r"    pillars = \[\n(.*?)\n    \]\n    blocks = \"\"", src, re.S)
    ns = {}; exec("pillars = [\n" + m.group(1) + "\n]", ns)
    return ns["pillars"]


def service_pages():
    P = pillars()
    meta = {"ai-data": ("ai", "gold"), "cloud": ("cloud", "blush"), "apps": ("app", "mint"), "security": ("shield", "gold"),
            "implementation": ("blocks", "blush"), "optimization": ("gauge", "mint"), "support": ("headset", "gold")}
    for pid, title, lead, items in P:
        ic, tn = meta[pid]
        page = f"service-{pid}.html"
        it = "".join(f"<div class=\"card\" style=\"padding:var(--s-5)\"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>" for t, d in items)
        steps = "".join(f'<li class="method__step"><h3>{s}</h3><p>{d}</p></li>' for s, d in STEPS)
        faq = "".join(f'<details><summary>{q}</summary><div class="faq__a">{a}</div></details>' for q, a in FAQ[pid])
        others = "".join(f'<li><a href="service-{a}.html">{escape(t)}</a></li>' for a, t, _, _ in P if a != pid)
        ld_faq = ('<script type="application/ld+json">' + __import__("json").dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[pid]]}, ensure_ascii=False) + "</script>")
        ld_svc = ('<script type="application/ld+json">' + __import__("json").dumps({"@context": "https://schema.org", "@type": "Service", "name": title, "description": lead,
            "provider": {"@id": f"{SITE}/#org"}, "serviceType": title}, ensure_ascii=False) + "</script>")
        h = b2.head(f"{title} | Virtual IP", lead, page).replace("</head>", ld_svc + ld_faq + "\n</head>")
        h += b2.header("services.html")
        h += f"""<main id="main">
{b2.page_head(escape(title), escape(lead), title, 'svc-' + pid)}
<section class="section--tight"><div class="container">
  <div class="section-head"><h2>What we do</h2><p class="lede">Each item can be bought on its own or as part of a larger programme.</p></div>
  <div class="svc-grid">{it}</div></div></section>
<section class="section section--alt"><div class="container">
  <div class="section-head"><h2>How we work</h2><p class="lede">The same four steps every time, so you always know what comes next.</p></div>
  <ol class="method method--4">{steps}</ol></div></section>
<section class="section--tight"><div class="container narrow">
  <h2>Questions we hear</h2><div class="faq">{faq}</div>
  <p style="margin-top:var(--s-5)">See what this looks like in practice in our <a href="case-studies.html">case studies</a>, or browse <a href="services.html">all services</a>.</p>
  <h2 style="margin-top:var(--s-6)">Other services</h2><ul>{others}</ul></div></section>
{b2.cta_band("Talk to us about " + SHORT[pid] + ".", "Tell us the goal and the systems involved. A person reads every message.")}
</main>
"""
        h += b2.footer()
        write(page, h)
    # link each pillar on services.html to its page
    s = (OUT / "services.html").read_text(encoding="utf-8")
    for pid, title, lead, _ in P:
        link = f'<a class="link-arrow" href="service-{pid}.html">Explore {escape(title)}<span class="sr-only"> in detail</span> {b.ARROW}</a>'
        s, n = re.subn(rf'(<h2 id="{pid}-t">.*?</h2><p>.*?</p>)', lambda m: m.group(1) + link, s, count=1, flags=re.S)
        assert n == 1, pid
    write("services.html", s)


def not_found():
    h = b2.head("Page not found | Virtual IP", "That page doesn't exist. Head back to the Virtual IP home page or get in touch.", "404.html")
    h = re.sub(r'<link rel="canonical"[^>]*>\n?', "", h).replace("<head>", '<head>\n<base href="/">\n<meta name="robots" content="noindex">', 1)
    h += b2.header("")
    h += f"""<main id="main"><section class="page-head"><div class="container narrow">
<h1>We can't find that page.</h1>
<p class="lede">The link may be old or mistyped. Try one of these instead.</p>
<p style="display:flex;gap:var(--s-3);flex-wrap:wrap"><a class="btn" href="index.html">Go to the home page</a><a class="btn btn--ghost" href="services.html">See services</a><a class="btn btn--ghost" href="contact.html">Contact us</a></p>
</div></section></main>
"""
    h += b2.footer()
    write("404.html", h)


def seo_files():
    pages = sorted(p.name for p in OUT.glob("*.html") if p.name != "404.html")
    prio = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.9", "case-studies.html": "0.8"}
    urls = "".join(f"<url><loc>{SITE}/{'' if n == 'index.html' else n}</loc><priority>{prio.get(n, '0.6' if n.startswith('service-') else '0.5')}</priority></url>\n" for n in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")


def run():
    service_pages(); not_found(); seo_files()
    print("post-pass: service pages, 404, sitemap, robots")
