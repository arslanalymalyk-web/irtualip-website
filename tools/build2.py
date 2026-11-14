#!/usr/bin/env python3
"""Visual-pass page builder. Reuses shared helpers/data from build.py, redefines the page builders with the visual system."""
import build as b
import visuals as V
from build import OUT, EMAIL, LINKEDIN, SITE, ARROW, ARROW_UR, MARK, escape, write, CASES, POSTS

_head0, _footer0 = b.head, b.footer
_COMP = '<link rel="stylesheet" href="assets/css/components.css">'
_VIS = _COMP + '\n<link rel="stylesheet" href="assets/css/visuals.css">'
_JS = ('<script src="assets/js/vendor/motion.lite.js" defer></script>\n<script src="assets/js/visuals.js" defer></script>\n')


def head(*a, **k):
    return _head0(*a, **k).replace(_COMP, _VIS)


def footer(scripts=""):
    return _footer0(_JS + scripts)


header = b.header


def page_head(title_html, lede, crumb, art=None):
    art_html = V.page_art(art) if art else ""
    grid = "page-head__grid" if art else ""
    return f"""<section class="page-head"><div class="container {grid}"><div>
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{escape(crumb)}</li></ol>
  <h1>{title_html}</h1><p class="lede">{lede}</p></div>{art_html}</div></section>"""


cta_band = lambda *a, **k: b.cta_band(*a, **k).replace('class="cta-band on-dark"', 'class="cta-band on-dark"')


def stats_block():
    return """<section class="section on-dark has-rings" aria-labelledby="stats-title"><div class="container">
  <div class="stats-intro"><h2 id="stats-title">More than seventeen years of building systems that stay up.</h2>
    <a class="btn btn--ghost" href="about.html">How we work</a></div>
  <p class="stats-note"><span class="sample-badge">Sample content</span> Placeholder figures for the preview. Replace them with verified numbers before launch.</p>
  <div class="stats">
    <div class="stat"><p class="stat__num"><span data-count="17">17</span><small>+</small></p><p class="stat__label">Years building digital solutions</p></div>
    <div class="stat"><p class="stat__num"><span data-count="800">800</span><small>+</small></p><p class="stat__label">Engineers and specialists</p></div>
    <div class="stat"><p class="stat__num"><span data-count="73">73</span><small>%</small></p><p class="stat__label">Client retention</p></div>
    <div class="stat"><p class="stat__num"><span data-count="4">4</span></p><p class="stat__label">Global delivery hubs</p></div>
  </div></div></section>"""


def industries(dark=False):
    items = [("fintech", "coins", "Fintech", "Payments, risk and compliance systems that stand up to audit."),
             ("health", "pulse", "Healthcare", "Data platforms and applications that respect privacy and clinical reality."),
             ("logistics", "route", "Logistics", "Tracking, planning and automation for operations that never close.")]
    cards = "".join(f'<article class="industry">{V.scene(k)}<div class="industry__body"><h3>{V.tile(ic, "gold" if dark else "dark", 20)}{t}</h3><p>{p}</p></div></article>' for k, ic, t, p in items)
    return f'<div class="industries" data-stagger>{cards}</div>'


def marquee(items):
    li = "".join(f'<li class="badge">{V.tile(i, t, 18)}<span>{escape(x)}</span></li>' for i, t, x in items)
    return (f'<div class="marquee" role="group" aria-label="Certifications and partners"><div class="marquee__track">'
            f'<ul class="marquee__group">{li}</ul><ul class="marquee__group" aria-hidden="true">{li}</ul></div></div>')


CERTS = [("shield", "gold", "ISO 27001 certified"), ("check", "blush", "SOC 2 Type II"), ("cloud", "mint", "AWS Advanced Consulting Partner"),
         ("layers", "gold", "Microsoft Solutions Partner"), ("globe", "blush", "Google Cloud Premier Partner"), ("award", "mint", "Forbes Technology Council member")]


# =============================================================== HOME
def build_home():
    words = "AI that your team can actually trust.".split()
    h1 = "".join(f'<span class="w" style="--i:{i}">{w}</span> ' for i, w in enumerate(words)).strip()

    def tl(cls, href, icon_n, tone, title, desc, mini_k=None, chips=None, extra=""):
        ch = "".join(f'<li class="chip">{c}</li>' for c in chips) if chips else ""
        chips_h = f'<ul class="chips" aria-label="Includes">{ch}</ul>' if ch else ""
        mini_h = V.mini(mini_k) if mini_k else ""
        return (f'<a class="tile {cls}" href="{href}"><div class="tile__top">{V.tile(icon_n, tone)}{ARROW_UR}</div><h3>{title}</h3><p>{desc}</p>{extra}{mini_h}{chips_h}</a>')

    bento = (
        f'<a class="tile tile--ai" href="services.html#ai-data"><div class="tile__top">{V.tile("ai", "gold")}{ARROW_UR}</div>'
        f'<h3>AI &amp; data innovation</h3><p>Enterprise AI that automates tasks, sharpens daily decisions and connects to the systems and data you already have.</p>'
        f'{V.arch_diagram()}<ul class="chips" aria-label="Includes"><li class="chip">Machine learning &amp; MLOps</li><li class="chip">Data engineering</li><li class="chip">AI automation</li></ul></a>'
        + tl("tile--6", "services.html#cloud", "cloud", "blush", "Cloud &amp; infrastructure", "Secure, scalable environments, and migrations that cut downtime instead of causing it.", "cloud")
        + tl("tile--6", "services.html#apps", "app", "mint", "Application development", "Web, mobile and SaaS products built around real users and fast growth.", "app")
        + tl("", "services.html#security", "shield", "gold", "Cybersecurity", "Threat detection, audits and compliance work that keeps pace as you grow.", "security")
        + tl("", "services.html#implementation", "blocks", "blush", "Solution implementation", "ERP integration, system migration and legacy modernization with minimal disruption.", "blocks")
        + tl("", "services.html#optimization", "gauge", "mint", "Optimization &amp; quality", "Testing and tuning that keep systems fast and stable as demand grows.", "gauge"))

    tabs = [("claims", "ai", "gold", "Claims triage console", "AI that ranks work and shows its reasoning.", V.mock_triage()),
            ("cost", "cloud", "blush", "Cloud cost overview", "Spend, forecast and idle resources in one view.", V.mock_cost()),
            ("pipe", "pipeline", "mint", "Delivery pipeline", "Every release tested, scanned and traceable.", V.mock_pipeline())]
    tabbtn = "".join(
        f'<button class="ftab" type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{V.tile(ic, tn, 20)}<span><strong>{t}</strong><span>{d}</span></span></button>'
        for i, (k, ic, tn, t, d, _) in enumerate(tabs))
    panels = "".join(f'<div class="tabpanel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" data-reveal tabindex="0"{"" if i == 0 else ""}>{m}</div>' for i, (k, _, _, _, _, m) in enumerate(tabs))

    why = [("ai", "gold", "AI experts", "Engineers who build production systems, not just models: clean data pipelines, real use cases and measurable impact."),
           ("target", "blush", "Product mindset", "Every build starts from real users and a clear business goal, so it keeps paying off long after launch."),
           ("pipeline", "mint", "Delivery discipline", "Short, focused cycles keep work on track, lower risk and protect quality from planning to production."),
           ("briefcase", "gold", "Industry depth", "We know the rules and realities of fintech, healthcare and logistics, so solutions fit inside real-world limits from day one."),
           ("globe", "blush", "Global reach", "Distributed teams and cloud infrastructure support projects across time zones without slowing delivery."),
           ("lock", "mint", "Security from the start", "Security is part of design, development and deployment, so systems stay protected as they scale.")]
    why_h = "".join(f'<div class="why-card">{V.tile(i, t, 20)}<h3>{h}</h3><p>{p}</p></div>' for i, t, h, p in why)

    trust = (f'<div class="trust" data-stagger><div class="cred-tile cred-tile--hero">{V.tile("shield", "gold")}<h3>Audited controls, not promises.</h3>'
             f'<p>ISO 27001 certified for information security management, and SOC 2 Type II for security, availability and confidentiality.</p>{V.mini("security")}</div>'
             + "".join(f'<div class="cred-tile">{V.tile(i, t, 20)}<h3>{h}</h3><p>{p}</p></div>' for i, t, h, p in [
                 ("cloud", "blush", "AWS Advanced Consulting Partner", "Verified AWS delivery expertise."),
                 ("layers", "mint", "Microsoft Solutions Partner", "Digital and app innovation."),
                 ("globe", "gold", "Google Cloud Premier Partner", "Part of Google Cloud's premier partner ecosystem."),
                 ("award", "blush", "Forbes Technology Council", "Official member.")]) + '</div>')

    faqs = [
        ("What should I look for in a technology consultancy for custom software?", "<p>Look for a team that starts from your business goal, shows working software early, is open about trade-offs and is still answering the phone after launch.</p><p>Ask who will do the work, how they handle security, and what you own at the end, including code and data.</p>"),
        ("How can AI make enterprise software more efficient?", "<p>By taking on repetitive work, such as classifying documents, routing requests and flagging anomalies, and by giving people better information at the moment they decide.</p><p>The gains are largest when AI connects to your existing systems and data instead of sitting beside them.</p>"),
        ("What is cloud migration?", "<p>Moving applications, data and workloads from on-premises servers, or from one cloud to another, into a cloud environment. It ranges from a straight move to redesigning an application so it uses cloud-native services.</p>"),
        ("Why should I consider moving to the cloud?", "<p>Common reasons are scalability, resilience, faster delivery and paying for what you use. It also makes AI services easier to adopt.</p><p>Not every workload belongs in the cloud, so we assess each one on its merits.</p>"),
        ("How long does cloud migration take?", "<p>It depends on how many applications you have, how tangled their dependencies are and how much you want to change along the way. We size it after an assessment instead of quoting a number up front.</p>"),
        ("How does cloud migration affect data security?", "<p>Done well, it improves it. Encryption, identity controls, logging and automated compliance checks are easier to apply consistently.</p><p>The risk sits in the move itself, so we plan access, data handling and rollback before anything shifts.</p>"),
        ("How do you protect our data when building AI?", "<p><span class='sample-badge'>Sample content</span> Security is part of design, build and deployment. We work under ISO 27001 and SOC 2 Type II controls, and we agree how your data is accessed, stored and used before work begins.</p>"),
        ("What happens after launch?", "<p>We can provide managed support and monitoring, or hand the system over to your team with documentation and training. We agree which at the start, so there are no surprises.</p>")]
    faq_h = "".join(f'<details><summary>{q}</summary><div class="faq__a">{a}</div></details>' for q, a in faqs)

    org = ('{"@context":"https://schema.org","@type":"Organization","name":"Virtual IP","url":"%s","email":"%s","sameAs":["%s"],'
           '"description":"Enterprise AI, cloud, application development and cybersecurity services."}') % (SITE, EMAIL, LINKEDIN)

    def case_card(cls, cid, meta, metric, title, ba, p=""):
        return (f'<a class="case {cls}" href="case-studies.html#{cid}" data-reveal><div class="case__meta"><span>{meta}</span><span class="sample-badge">Sample</span></div>'
                f'<p class="case__metric">{metric}</p><h3>{title}</h3>{p}{ba}</a>')

    cases = (case_card("case--lead", "claims-triage", "Insurance &middot; Machine learning", "38%", "Faster claims triage with a model that explains its calls",
                       V.before_after(100, 62, "Triage time (index)"), "<p>A regional insurer routes claims with a model that flags the ones needing a person and shows why.</p>" + '<div class="case__trend">' + V.area_chart([100, 98, 95, 90, 84, 76, 70, 66, 63, 62], 520, 120, "lead") + '<span>Weekly triage time, illustrative</span></div>')
             + case_card("", "logistics-releases", "Logistics &middot; DevOps", "4x", "More frequent releases after a pipeline rebuild", V.before_after(1, 4, "Release frequency", unit="x"))
             + case_card("", "healthcare-cloud", "Healthcare &middot; Cloud", "31%", "Lower cloud spend with no change in uptime", V.before_after(100, 69, "Cloud spend (index)")))

    html = head("Virtual IP | Enterprise AI, cloud and software that holds up in production",
                "Virtual IP designs, builds and runs enterprise AI, cloud, application and security systems that fit your data, your rules and your people.",
                "index.html", f'<script type="application/ld+json">{org}</script>\n')
    html += header("index.html", hero=True)
    html += f"""<main id="main">
<section class="hero" data-hero aria-labelledby="hero-title">
  <div class="hero__media" aria-hidden="true"><div class="hero__poster"></div>
    <video muted loop playsinline preload="none" tabindex="-1" data-mp4="assets/media/hero-loop.mp4" data-webm="assets/media/hero-loop.webm" poster="assets/media/hero-poster.jpg"></video></div>
  <button class="media-toggle" type="button" data-media-toggle aria-pressed="false">
    <svg class="i-pause" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1"/><rect x="9.5" y="2" width="3.5" height="12" rx="1"/></svg>
    <svg class="i-play" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg>
    <span class="media-toggle__label">Pause background motion</span></button>
  <aside class="hero__trace" aria-hidden="true"><div class="hero__trace-head">Decision trace <span>Illustrative</span></div>
    <dl><div><dt>Signals read</dt><dd data-count="1284">1,284</dd></div><div><dt>Confidence</dt><dd>0.93</dd></div>
    <div><dt>Route</dt><dd>Senior adjuster</dd></div><div><dt>Top factor</dt><dd><span class="meter"><i style="--w:82%"></i></span></dd></div></dl>
    <span class="hero__trace-foot">A person reviews this</span></aside>
  <div class="container hero__body"><h1 id="hero-title">{h1}</h1>
    <p class="hero__sub">We design, build and run enterprise AI that fits your data, your rules and your people.</p>
    <div class="hero__actions"><a class="btn" href="contact.html#contact-form">Plan your AI roadmap</a><a class="btn btn--ghost" href="#readiness">Take the 2-minute readiness check</a></div></div>
  <div class="hero__proof"><div class="container hero__proof-inner"><p class="hero__proof-title">Certified and partnered <span class="sample-badge">Sample</span></p>{marquee(CERTS)}</div></div>
</section>

<section class="section" id="services" aria-labelledby="services-title"><div class="container">
  <div class="section-head"><h2 id="services-title">Start with AI. Build everything it needs to run.</h2>
    <p class="lede">AI is the part people see. Most of the work is the data, cloud, application and security layers underneath, so we cover all of them.</p></div>
  <div class="bento" data-reveal data-stagger>{bento}</div>
</div></section>

<section class="section section--alt bg-dots" id="work" aria-labelledby="work-t"><div class="container showcase" data-tabs>
  <div class="showcase__intro"><h2 id="work-t">See the work, not just the pitch.</h2>
    <p class="lede">Three kinds of interface we build for clients, drawn here as illustrations.</p>
    <div class="ftabs" role="tablist" aria-label="Product examples" aria-orientation="vertical">{tabbtn}</div></div>
  <div class="showcase__stage" data-parallax="0.02">{panels}<p class="note">Illustrative interfaces with sample data. They are not client screenshots.</p></div>
</div></section>

{stats_block()}

<section class="section" aria-labelledby="method-title"><div class="container">
  <div class="section-head"><h2 id="method-title">From first idea to something your team runs.</h2><p class="lede">Every step ends with something you can use or decide on.</p></div>
  <ol class="method" data-stagger>
    <li class="method__step">{V.method_art("map")}<h3>Map it</h3><p>We find the decision or workflow worth improving, check that your data can support it and agree how success will be measured.</p><ul><li>Use-case workshop</li><li>Data and security readiness check</li><li>Baseline and target</li></ul></li>
    <li class="method__step">{V.method_art("prove")}<h3>Prove it</h3><p>We build a small working system on your own data and test it against the baseline. You see results before you commit to scale.</p><ul><li>Working prototype</li><li>Results against the baseline</li><li>A clear go or no-go</li></ul></li>
    <li class="method__step">{V.method_art("run")}<h3>Run it</h3><p>We take the proven system to production with security, monitoring and cost controls built in, then support it or hand it over.</p><ul><li>Production build</li><li>Monitoring and cost controls</li><li>Managed support or team handover</li></ul></li>
  </ol></div></section>

<section class="section section--alt" aria-labelledby="cases-title"><div class="container">
  <div class="section-head"><h2 id="cases-title">Results first, then the story.</h2>
    <p class="lede"><span class="sample-badge">Sample content</span> Illustrative placeholders for this preview. Swap in approved client results before launch.</p></div>
  <div class="cases" data-stagger>{cases}</div>
  <p style="margin-top:var(--s-5)"><a class="text-link" href="case-studies.html">Read all case studies {ARROW}</a></p></div></section>

<section class="section" aria-labelledby="ind-title"><div class="container">
  <div class="section-head"><h2 id="ind-title">Industries where the rules are real.</h2>
    <p class="lede">We understand the regulatory, operational and technical limits of the sectors we serve.</p></div>{industries()}</div></section>

<section class="section section--alt" aria-labelledby="why-title"><div class="container why">
  <div class="why__intro"><h2 id="why-title">Built for real results, not just prototypes.</h2>
    <p class="lede">We'd rather ship a smaller thing that works than present a bigger thing that doesn't.</p>
    <a class="btn btn--ghost" href="about.html" style="justify-self:start">About Virtual IP</a></div>
  <div class="why__grid" data-stagger>{why_h}</div></div></section>

<section class="section--tight" id="readiness" aria-labelledby="quiz-title"><div class="container"><div class="quiz-wrap">
  <div class="quiz-intro"><h2 id="quiz-title">Where does your organization stand on AI?</h2>
    <p class="lede">Six questions. You get a stage, a profile across six areas and a suggested first step.</p>
    <ul><li>No email needed</li><li>Answers stay in your browser</li><li>About two minutes</li></ul></div>
  <div class="quiz" data-quiz aria-live="polite"><noscript><p>The readiness check needs JavaScript. To talk it through instead, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></noscript></div>
</div></div></section>

<section class="section" aria-labelledby="creds-title"><div class="container">
  <div class="section-head"><h2 id="creds-title">Proof your security team can check.</h2><p class="lede"><span class="sample-badge">Sample content</span> Placeholder credentials for the preview. Replace them with verified certifications and partnerships before launch.</p></div>{trust}</div></section>

<section class="section section--alt" aria-labelledby="faq-title"><div class="container">
  <div class="section-head"><h2 id="faq-title">Questions buyers ask first.</h2></div><div class="faq">{faq_h}</div></div></section>

{cta_band()}
</main>
"""
    html += footer('<script src="assets/js/hero.js" defer></script>\n<script src="assets/js/quiz.js" defer></script>\n')
    write("index.html", html)


# =============================================================== SERVICES
PILLARS = None


def build_services():
    import re
    src = open(b.__file__).read()
    # reuse the pillar copy from build.py without duplicating it
    ns = {}
    m = re.search(r"    pillars = \[\n(.*?)\n    \]\n    blocks = \"\"", src, re.S)
    exec("pillars = [\n" + m.group(1) + "\n]", ns)
    pillars = ns["pillars"]
    meta = {"ai-data": ("ai", "gold", "cloud"), "cloud": ("cloud", "blush", "cloud"), "apps": ("app", "mint", "app"), "security": ("shield", "gold", "security"),
            "implementation": ("blocks", "blush", "blocks"), "optimization": ("gauge", "mint", "gauge"), "support": ("headset", "gold", None)}
    blocks = ""
    for pid, title, lead, items in pillars:
        ic, tn, mk = meta[pid]
        it = "".join(f"<div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>" for t, d in items)
        art = V.mini(mk) if mk and pid != "ai-data" else (V.arch_diagram() if pid == "ai-data" else "")
        blocks += (f'<section class="pillar" id="{pid}" aria-labelledby="{pid}-t"><div class="pillar__lead">{V.tile(ic, tn)}<h2 id="{pid}-t">{escape(title)}</h2><p>{escape(lead)}</p>{art}</div>'
                   f'<div class="pillar__items">{it}</div></section>')
    engage = [("people", "Dedicated team", "A team that works as an extension of yours, on your roadmap."), ("server", "Offshore development center", "A stable, long-term team in one of our delivery hubs."),
              ("target", "Fixed-price projects", "Defined scope, schedule and cost for well-understood work."), ("layers", "Hybrid delivery", "A mix of the above, shaped around your project and budget.")]
    eng = "".join(f"<div>{V.tile(i, 'gold', 20)}<h3>{t}</h3><p>{d}</p></div>" for i, t, d in engage)
    html = head("Services | Virtual IP", "AI and data, cloud, application development, cybersecurity, implementation, optimization and managed IT services from Virtual IP.", "services.html")
    html += header("services.html")
    html += f"""<main id="main">
{page_head('Everything AI needs to run in production.', 'Six service lines and a managed support practice, so the data, cloud, application and security work behind your AI comes from one accountable team.', 'Services', 'services')}
<section class="section--tight"><div class="container">{blocks}</div></section>
<section class="section on-dark has-rings" aria-labelledby="eng-t"><div class="container">
  <div class="section-head"><h2 id="eng-t">Four ways to work with us.</h2><p class="lede">Pick the model that fits the work. You can change it as the project changes.</p></div>
  <div class="engage" data-stagger>{eng}</div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("services.html", html)


# =============================================================== CASE STUDIES
def build_cases():
    charts = {"claims-triage": (V.before_after(100, 62, "Triage time (index)"), V.area_chart([100, 98, 95, 90, 84, 76, 70, 66, 63, 62], 520, 130, "c1"), "Weekly triage time, index"),
              "logistics-releases": (V.before_after(1, 4, "Release frequency", unit="x"), V.bars([1, 1, 2, 2, 2, 3, 3, 4, 4, 4], 520, 120), "Releases per period"),
              "healthcare-cloud": (V.before_after(100, 69, "Cloud spend (index)"), V.area_chart([100, 104, 103, 98, 92, 84, 78, 73, 70, 69], 520, 130, "c3"), "Monthly cloud spend, index"),
              "fintech-fraud": (V.before_after(100, 38, "False alerts (index)"), V.bars([100, 96, 88, 74, 60, 52, 46, 42, 40, 38], 520, 120, 9), "False alerts, index")}
    icons = {"claims-triage": "ai", "logistics-releases": "pipeline", "healthcare-cloud": "cloud", "fintech-fraud": "coins"}
    blocks = ""
    for cid, metric, title, meta, ch, did, res in CASES:
        ba, ch_svg, cap = charts[cid]
        blocks += f"""<article class="case-full" id="{cid}" aria-labelledby="{cid}-t" data-reveal>
  <div class="case-full__side">{V.tile(icons[cid], "gold")}<p class="case__meta"><span>{escape(meta)}</span></p><p class="case__metric">{metric}</p><span class="sample-badge" style="justify-self:start">Sample content</span></div>
  <div><h2 id="{cid}-t">{escape(title)}</h2>
  <div class="case-full__charts">{ba}<div class="mock-chart"><div class="mock__head"><strong>{cap}</strong><span>Illustrative</span></div>{ch_svg}</div></div>
  <dl style="margin-top:var(--s-5)"><div><dt>The challenge</dt><dd>{escape(ch)}</dd></div><div><dt>What we did</dt><dd>{escape(did)}</dd></div><div><dt>The result</dt><dd>{escape(res)}</dd></div></dl></div></article>"""
    html = head("Case studies | Virtual IP", "Outcome-led examples of AI, cloud and delivery work from Virtual IP.", "case-studies.html")
    html += header("case-studies.html")
    html += f"""<main id="main">
{page_head('Results first, then the story.', 'Each story leads with what changed. <span class="sample-badge">Sample content</span> Placeholders for the preview. Replace them with approved client results before launch.', 'Case studies', 'cases')}
<section class="section--tight"><div class="container">{blocks}</div></section>
{cta_band("Want results like these?", "Tell us what you're trying to improve and we'll take it from there.")}
</main>
"""
    html += footer()
    write("case-studies.html", html)


# =============================================================== ABOUT
def build_about():
    vals = [("bolt", "gold", "Ship what works", "We prefer a smaller system in production over a bigger one in a slide deck, and we measure every build against a baseline."),
            ("eye", "blush", "Say the trade-off out loud", "Every option costs something in time, money or risk. We name it early so you can choose with open eyes."),
            ("layers", "mint", "Build it to last", "Security, monitoring and documentation are part of the first release, so the system is easy to run and easy to hand over.")]
    vh = "".join(f"<div>{V.tile(i, t, 20)}<h3 style='margin-top:var(--s-3)'>{h}</h3><p>{p}</p></div>" for i, t, h, p in vals)
    html = head("About | Virtual IP", "Virtual IP is a technology partner with more than 17 years of experience, 800+ engineers and specialists and four global delivery hubs.", "about.html")
    html += header("about.html")
    html += f"""<main id="main">
{page_head('We build the systems behind your decisions.', 'Virtual IP is a technology partner for teams that need AI, cloud and software to work in the real world, not only in a demo.', 'About', 'about')}
<section class="section"><div class="container split">
  <h2>Practical execution, measurable impact, long-term reliability.</h2>
  <div class="prose"><p><span class="sample-badge">Sample content</span> The figures and credentials on this page are placeholders until verified.</p><p>For more than seventeen years we have built digital systems for organizations in fintech, healthcare, logistics and beyond. Today more than 800 engineers and specialists work across four global delivery hubs.</p>
    <p><strong>We focus on what ships.</strong> That means clear scope, short cycles, honest trade-offs and security from the first design decision. It also means staying involved after launch, which is part of why 73% of clients stay with us.</p>
    <p>We're an ISO 27001 certified, SOC 2 Type II audited partner of AWS, Microsoft and Google Cloud, and a member of the Forbes Technology Council.</p></div></div></section>
{stats_block()}
<section class="section" aria-labelledby="val-t"><div class="container"><div class="section-head"><h2 id="val-t">How we work.</h2></div><div class="values" data-stagger>{vh}</div></div></section>
<section class="section section--alt" aria-labelledby="ind-t"><div class="container"><div class="section-head"><h2 id="ind-t">Industries where the rules are real.</h2>
  <p class="lede">We understand the regulatory, operational and technical limits of the sectors we serve.</p></div>{industries()}</div></section>
<section class="section"><div class="container split"><h2>Meet the people doing the work.</h2>
  <div class="prose"><p>Our teams combine AI engineers, cloud architects, designers and security specialists.</p><p><a class="btn" href="team.html">Meet the team</a> &nbsp; <a class="btn btn--ghost" href="careers.html">Join us</a></p></div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("about.html", html)


# =============================================================== INSIGHTS
def build_insights():
    items = ""
    for i, (f, tag, title, sub, rt, _) in enumerate(POSTS):
        items += (f'<article class="post">{V.post_cover(i)}<div class="post__meta"><p class="post__kicker">{escape(tag)}</p><h2><a href="{f}">{escape(title)}</a></h2><p>{escape(sub)}</p></div>'
                  f'<p class="post__read">{rt}</p></article>')
    html = head("Insights | Virtual IP", "Practical guidance on AI readiness, cloud migration and getting projects into production.", "insights.html")
    html += header("insights.html")
    html += f"""<main id="main">
{page_head('Plain advice for people shipping technology.', '<span class="sample-badge">Sample content</span> Draft articles for the preview. Have the team review and approve them before launch.', 'Insights', 'insights')}
<section class="section--tight"><div class="container"><div class="post-list" data-stagger>{items}</div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("insights.html", html)
    for i, (f, tag, title, sub, rt, body) in enumerate(POSTS):
        parts = ""
        for kind, val in body:
            if kind in ("intro", "p"): parts += f"<p>{val}</p>"
            elif kind == "h": parts += f"<h2>{val}</h2>"
            elif kind == "ul": parts += "<ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>"
        h = head(f"{title} | Virtual IP", sub, f) + header("insights.html")
        h += f"""<main id="main">
<section class="page-head"><div class="container"><ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="insights.html">Insights</a></li><li aria-current="page">{escape(tag)}</li></ol>
<h1 style="font-size:var(--step-4);max-width:22ch">{escape(title)}</h1></div></section>
<article class="container article"><div class="post-cover post-cover--lg">{V.post_cover(i).split('>', 1)[1].rsplit('</div>', 1)[0]}</div>
<div class="byline"><span>Virtual IP team</span><span>{rt}</span><span class="sample-badge">Sample content</span></div>{parts}
<p><a class="btn" href="index.html#readiness">Take the readiness check</a></p></article>
{cta_band()}
</main>
"""
        h += footer()
        write(f, h)


# =============================================================== TEAM / CAREERS / CONTACT
def build_team():
    people = [("Alex Morgan", "AM", "Chief Executive Officer", "Sets direction and keeps delivery honest."), ("Sam Rivera", "SR", "Chief Technology Officer", "Owns architecture and engineering standards."),
              ("Priya Nair", "PN", "Head of AI", "Leads machine learning and data engineering."), ("Chris Okafor", "CO", "Head of Delivery", "Keeps projects on plan and on quality."),
              ("Dana Whitfield", "DW", "Head of Security", "Leads security design, audits and compliance."), ("Lee Tran", "LT", "Head of Cloud", "Leads cloud architecture and operations."),
              ("Maya Haddad", "MH", "Head of Design", "Leads product and interface design."), ("Jordan Ellis", "JE", "Head of People", "Builds the teams that do the work.")]
    cards = "".join(f'<li class="person">{V.avatar(i, n)}<h3>{n}</h3><p class="role-title">{r}</p><p>{bio}</p></li>' for i, (n, ini, r, bio) in enumerate(people))
    html = head("Team | Virtual IP", "The leadership team behind Virtual IP.", "team.html") + header("about.html")
    html += f"""<main id="main">
{page_head('The people doing the work.', 'Leaders who still review the work. <span class="sample-badge">Sample content</span> Names, roles and bios are placeholders, and the portraits are illustrations. Replace both with the real team.', 'Team', 'team')}
<section class="section--tight"><div class="container"><ul class="team" data-stagger>{cards}</ul></div></section>
{cta_band("Want to work with us?", "See open roles or tell us about your project.")}
</main>
"""
    html += footer()
    write("team.html", html)


def build_careers():
    roles = [("Senior machine learning engineer", "AI & data", "Build and deploy models that run in production.", "ai", "gold"), ("Cloud and DevOps engineer", "Cloud", "Automate infrastructure, delivery and operations.", "cloud", "blush"),
             ("Security engineer", "Security", "Assess, test and harden client systems.", "shield", "mint"), ("Product designer", "Design", "Design interfaces for complex enterprise products.", "app", "gold"),
             ("Delivery manager", "Delivery", "Keep multi-team projects clear, on plan and honest.", "pipeline", "blush")]
    rows = ""
    for t, team, d, ic, tn in roles:
        subj = escape(f"Application: {t}").replace(" ", "%20").replace(":", "%3A")
        rows += (f'<li class="role">{V.tile(ic, tn, 20)}<div><h3>{t}</h3><p>{d}</p></div><p class="role__meta">{team}</p>'
                 f'<a class="btn btn--ghost btn--sm" href="mailto:{EMAIL}?subject={subj}">Apply by email<span class="sr-only"> for {escape(t)}</span></a></li>')
    vals = [("target", "gold", "Real problems", "Projects span fintech, healthcare and logistics, with real users and real constraints."), ("people", "blush", "Strong peers", "800+ engineers and specialists, with room to learn from people who've done it before."),
            ("globe", "mint", "Global teams", "Four delivery hubs and distributed teams that work across time zones.")]
    vh = "".join(f"<div>{V.tile(i, t, 20)}<h3 style='margin-top:var(--s-3)'>{h}</h3><p>{p}</p></div>" for i, t, h, p in vals)
    html = head("Careers | Virtual IP", "Join Virtual IP and build AI, cloud and software that stay up.", "careers.html") + header("careers.html")
    html += f"""<main id="main">
{page_head('Build things that stay up.', 'Work with senior engineers and designers on systems that run in production for real organizations.', 'Careers', 'careers')}
<section class="section"><div class="container"><div class="values" data-stagger>{vh}</div></div></section>
<section class="section section--alt" aria-labelledby="open-t"><div class="container"><div class="section-head"><h2 id="open-t">Open roles.</h2>
  <p class="lede"><span class="sample-badge">Sample content</span> Placeholder roles for the preview. Connect this list to your hiring system or update it by hand.</p></div>
  <ul class="roles">{rows}</ul><p style="margin-top:var(--s-5)">Don't see your role? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> and tell us what you'd build.</p></div></section>
</main>
"""
    html += footer()
    write("careers.html", html)


def build_contact():
    html = head("Contact | Virtual IP", "Tell Virtual IP what you're trying to improve. Plan your AI roadmap, or ask about cloud, software, security and support.", "contact.html") + header("contact.html")
    html += f"""<main id="main">
{page_head("Tell us what you're trying to improve.", 'A short note is enough. Tell us the goal, the systems involved and any deadline.', 'Contact', 'contact')}
<section class="section--tight"><div class="container contact">
  <form class="form card" id="contact-form" novalidate aria-labelledby="form-title" style="padding:clamp(1.25rem,1rem+2vw,2.5rem)">
    <h2 id="form-title" class="sr-only">Contact form</h2>
    <div class="form__row"><div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required></div></div>
    <div class="form__row"><div class="field"><label for="company">Company <span class="hint">(optional)</span></label><input id="company" name="company" type="text" autocomplete="organization"></div>
      <div class="field"><label for="topic">What do you need?</label><select id="topic" name="topic">
        <option value="ai-roadmap">Plan an AI roadmap</option><option value="cloud">Cloud and infrastructure</option><option value="software">Software development</option>
        <option value="security">Cybersecurity</option><option value="support">Support and managed services</option><option value="careers">Careers</option><option value="other">Something else</option></select></div></div>
    <div class="field"><label for="message">How can we help?</label><textarea id="message" name="message" required></textarea></div>
    <div><button class="btn" type="submit">Send message</button></div>
    <p class="form__status" id="form-status" role="status" tabindex="-1" hidden></p></form>
  <aside class="contact__side" aria-label="Other ways to reach us">
    <div class="card" style="padding:var(--s-5)">{V.tile("check", "gold")}<h2 style="margin-top:var(--s-3)">What happens next</h2><ol><li>A person reads your message.</li><li>We reply to the email you give us.</li><li>If it's a fit, we set up a working session.</li></ol></div>
    <div class="card" style="padding:var(--s-5)">{V.tile("mail", "blush")}<h2 style="margin-top:var(--s-3)">Prefer to write directly?</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p><a href="{LINKEDIN}" rel="noopener" target="_blank">Virtual IP on LinkedIn<span class="sr-only"> (opens in a new tab)</span></a></p></div>
  </aside></div></section>
</main>
"""
    html += footer('<script src="assets/js/contact.js" defer></script>\n')
    write("contact.html", html)


if __name__ == "__main__":
    b.page_head = page_head  # legal pages pick up the new header
    build_home(); build_services(); build_cases(); build_about(); build_insights(); build_team(); build_careers(); build_contact()
    # legal pages: rebuild through build.py with the visual head/footer wired in
    b.head, b.footer = head, footer
    b.build_legal()
    print("built", len(list(OUT.glob("*.html"))), "pages")
