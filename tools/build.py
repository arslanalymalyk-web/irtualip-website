#!/usr/bin/env python3
"""Static page generator for the Virtual IP site. Output is plain HTML/CSS/JS at the repo root."""
from pathlib import Path
import re
import shutil
from html import escape

OUT = Path(__file__).resolve().parent.parent
SITE = "https://virtualipus.com"
EMAIL = "contact@virtualip.com"
LINKEDIN = "https://www.linkedin.com/company/virtualip"

ARROW = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10h12M11 5l5 5-5 5"/></svg>'
ARROW_UR = '<svg class="arrow" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14L14 6M7 6h7v7"/></svg>'
def _logo():
    """Inline the brand-sheet logo; colours come from --logo-* tokens so one file serves light, dark and hero."""
    svg = (Path(__file__).resolve().parent.parent / "brand/svg/logo-color.svg").read_text()
    svg = re.sub(r' width="\d+" height="\d+"', "", svg, count=1)
    svg = svg.replace('fill="#2F6BFF"', 'class="l-spark"', 1).replace('fill="#2F6BFF"', 'class="l-ip"')
    svg = svg.replace('fill="#0A1330" stroke="#0A1330"', 'class="l-ink l-body"').replace('fill="#0A1330"', 'class="l-ink"')
    return svg.replace("<svg ", '<svg class="brand__logo" aria-hidden="true" focusable="false" ', 1)


MARK = _logo()

NAV = [("services.html", "Services"), ("case-studies.html", "Case studies"), ("about.html", "About"),
       ("insights.html", "Insights"), ("careers.html", "Careers"), ("contact.html", "Contact")]

THEME_INIT = ("(function(){var d=document.documentElement;d.classList.add('js');"
              "try{var t=localStorage.getItem('vip-theme');if(t==='light'||t==='dark')d.setAttribute('data-theme',t)}catch(e){}})();")


def head(title, desc, page, extra=""):
    t = escape(title)
    d = escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#0a1330">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Virtual IP">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}/{'' if page == 'index.html' else page}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<script>{THEME_INIT}</script>
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/components.css">
{extra}</head>
"""


def header(page, hero=False):
    items = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ""
        items += f'<li><a class="nav__link" href="{href}"{cur}>{label}</a></li>'
    return f"""<body class="{'has-hero' if hero else ''}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html" aria-label="Virtual IP, home">{MARK}</a>
    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list">{items}</ul>
      <a class="btn btn--sm nav__cta" href="contact.html#contact-form">Plan your AI roadmap</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="Switch to dark theme">
        <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z"/></svg>
        <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <span class="theme-toggle__label" aria-hidden="true">Dark theme</span>
      </button>
    </nav>
  </div>
</header>
"""


SERVICE_LINKS = [("ai-data", "AI & data"), ("cloud", "Cloud & infrastructure"), ("apps", "Application development"),
                 ("security", "Cybersecurity"), ("implementation", "Solution implementation"),
                 ("optimization", "Optimization & quality"), ("support", "IT support & managed services")]


def footer(scripts=""):
    svc = "".join(f'<li><a href="services.html#{a}">{escape(b)}</a></li>' for a, b in SERVICE_LINKS)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="index.html" aria-label="Virtual IP, home">{MARK}</a>
        <p>Enterprise AI, cloud and software, built to hold up in production and run by people you can reach.</p>
        <div class="footer__contact">
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn<span class="sr-only"> (opens in a new tab)</span></a>
        </div>
      </div>
      <div class="footer__col"><h2>Services</h2><ul>{svc}</ul></div>
      <div class="footer__col"><h2>Company</h2><ul>
        <li><a href="about.html">About</a></li><li><a href="team.html">Team</a></li><li><a href="case-studies.html">Case studies</a></li>
        <li><a href="insights.html">Insights</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul></div>
      <div class="footer__col"><h2>Legal</h2><ul>
        <li><a href="privacy.html">Privacy policy</a></li><li><a href="terms.html">Terms of service</a></li><li><a href="cookies.html">Cookie policy</a></li></ul></div>
    </div>
    <div class="footer__bottom">
      <p>&copy; <span data-year>2026</span> Virtual IP. All rights reserved.</p>
      <ul><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li><li><a href="cookies.html">Cookies</a></li></ul>
    </div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
{scripts}</body>
</html>
"""


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")


def page_head(title_html, lede, crumb):
    return f"""<section class="page-head"><div class="container">
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{escape(crumb)}</li></ol>
  <h1>{title_html}</h1><p class="lede">{lede}</p></div></section>"""


def cta_band(title="Your pilot shouldn't stay a pilot.", side="Tell us what you're trying to improve and we'll take it from there."):
    return f"""<section class="cta-band on-dark" aria-labelledby="cta-title"><div class="container cta-band__inner">
  <h2 id="cta-title">{title}</h2>
  <div class="cta-band__side"><p>{side}</p>
    <a class="btn" href="contact.html#contact-form">Plan your AI roadmap</a>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section>"""


# =========================================================================================
# HOME
# =========================================================================================
def build_home():
    words = "AI that your team can actually trust.".split()
    h1 = "".join(f'<span class="w" style="--i:{i}">{w}</span> ' for i, w in enumerate(words)).strip()
    proof = ["ISO 27001 certified", "SOC 2 Type II", "AWS Advanced Consulting Partner",
             "Microsoft Solutions Partner", "Google Cloud Premier Partner", "Forbes Technology Council member"]
    proof_li = "".join(f"<li>{p}</li>" for p in proof)

    svc_rows = [
        ("cloud", "Cloud & infrastructure", "Secure, scalable environments and migrations that keep downtime low.", ["AWS & Azure", "Kubernetes", "DevOps"]),
        ("apps", "Application development", "Web, mobile and SaaS products built around real users and fast growth.", ["Web & mobile apps", "Product design", "SaaS"]),
        ("security", "Cybersecurity", "Threat detection, audits and compliance work that keeps pace as you grow.", ["Threat detection", "Compliance & governance", "Security audits"]),
        ("implementation", "Solution implementation", "ERP integration, system migration and legacy modernization with minimal disruption.", ["ERP integration", "System migration", "Legacy modernization"]),
        ("optimization", "Optimization & quality", "Testing and tuning that keep systems fast and stable as demand grows.", ["Performance tuning", "QA automation", "Cost optimization"]),
    ]
    rows = ""
    for a, t, p, chips in svc_rows:
        ch = "".join(f'<li class="chip">{c}</li>' for c in chips)
        rows += (f'<li class="service-row"><h3><a href="services.html#{a}">{t}</a>{ARROW_UR}</h3><p>{p}</p>'
                 f'<ul class="chips" aria-label="Includes">{ch}</ul></li>')

    faqs = [
        ("What should I look for in a technology consultancy for custom software?",
         "<p>Look for a team that starts from your business goal, shows working software early, is open about trade-offs and is still answering the phone after launch.</p><p>Ask who will do the work, how they handle security, and what you own at the end, including code and data.</p>"),
        ("How can AI make enterprise software more efficient?",
         "<p>By taking on repetitive work, such as classifying documents, routing requests and flagging anomalies, and by giving people better information at the moment they decide.</p><p>The gains are largest when AI connects to your existing systems and data and your workflows.</p>"),
        ("What is cloud migration?",
         "<p>Moving applications, data and workloads from on-premises servers, or from one cloud to another, into a cloud environment. It ranges from a straight move to redesigning an application so it uses cloud-native services.</p>"),
        ("Why should I consider moving to the cloud?",
         "<p>Common reasons are scalability, resilience, faster delivery and paying for what you use. It also makes AI services easier to adopt.</p><p>Not every workload belongs in the cloud, so we assess each one on its merits.</p>"),
        ("How long does cloud migration take?",
         "<p>It depends on how many applications you have, how tangled their dependencies are and how much you want to change along the way. We size it after an assessment and give a number only then.</p>"),
        ("How does cloud migration affect data security?",
         "<p>Done well, it improves it. Encryption, identity controls, logging and automated compliance checks are easier to apply consistently.</p><p>The risk sits in the move itself, so we plan access, data handling and rollback before anything shifts.</p>"),
        ("How do you protect our data when building AI?",
         "<p>Security is part of design, build and deployment. We work under ISO 27001 and SOC 2 Type II controls, and we agree how your data is accessed, stored and used before work begins.</p>"),
        ("What happens after launch?",
         "<p>We can provide managed support and monitoring, or hand the system over to your team with documentation and training. We agree which at the start, so there are no surprises.</p>"),
    ]
    faq_html = "".join(f'<details><summary>{q}</summary><div class="faq__a">{a}</div></details>' for q, a in faqs)

    why = [
        ("AI experts", "Engineers who build production systems: clean data pipelines, real use cases and measurable impact."),
        ("Product mindset", "Every build starts from real users and a clear business goal, so it keeps paying off long after launch."),
        ("Delivery discipline", "Short, focused cycles keep work on track, lower risk and protect quality from planning to production."),
        ("Industry depth", "We know the rules and realities of fintech, healthcare and logistics, so solutions fit inside real-world limits from day one."),
        ("Global reach", "Distributed teams and cloud infrastructure support projects across time zones without slowing delivery."),
        ("Security from the start", "Security is part of design, development and deployment, so systems stay protected as they scale."),
    ]
    why_html = "".join(f'<div class="why__item"><h3>{t}</h3><p>{p}</p></div>' for t, p in why)

    creds = [("ISO 27001", "Information security management."), ("SOC 2 Type II", "Controls for security, availability and confidentiality."),
             ("AWS Advanced Consulting Partner", "Verified AWS delivery expertise."), ("Microsoft Solutions Partner", "Digital and app innovation."),
             ("Google Cloud Premier Partner", "Part of Google Cloud's premier partner ecosystem."), ("Forbes Technology Council", "Official member.")]
    creds_html = "".join(f'<div class="cred"><h3>{t}</h3><p>{p}</p></div>' for t, p in creds)

    org = ('{"@context":"https://schema.org","@type":"Organization","name":"Virtual IP","url":"%s","email":"%s",'
           '"sameAs":["%s"],"description":"Enterprise AI, cloud, application development and cybersecurity services."}') % (SITE, EMAIL, LINKEDIN)

    html = head("Virtual IP | Enterprise AI, cloud and software that holds up in production",
                "Virtual IP designs, builds and runs enterprise AI, cloud, application and security systems that fit your data, your rules and your people.",
                "index.html", f'<script type="application/ld+json">{org}</script>\n')
    html += header("index.html", hero=True)
    html += f"""<main id="main">
<section class="hero" data-hero aria-labelledby="hero-title">
  <div class="hero__media" aria-hidden="true">
    <div class="hero__poster"></div>
    <video muted loop playsinline preload="none" tabindex="-1" data-mp4="assets/media/hero-loop.mp4" data-webm="assets/media/hero-loop.webm" poster="assets/media/hero-poster.jpg"></video>
  </div>
  <button class="media-toggle" type="button" data-media-toggle aria-pressed="false">
    <svg class="i-pause" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1"/><rect x="9.5" y="2" width="3.5" height="12" rx="1"/></svg>
    <svg class="i-play" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg>
    <span class="media-toggle__label">Pause background motion</span>
  </button>
  <div class="container hero__body">
    <h1 id="hero-title">{h1}</h1>
    <p class="hero__sub">We design, build and run enterprise AI that fits your data, your rules and your people.</p>
    <div class="hero__actions">
      <a class="btn" href="contact.html#contact-form">Plan your AI roadmap</a>
      <a class="btn btn--ghost" href="#readiness">Take the 2-minute readiness check</a>
    </div>
  </div>
  <div class="hero__proof"><div class="container hero__proof-inner">
    <p class="hero__proof-title">Certified and partnered</p><ul>{proof_li}</ul></div></div>
</section>

<section class="section" id="services" aria-labelledby="services-title"><div class="container">
  <div class="section-head"><h2 id="services-title">Start with AI. Build everything it needs to run.</h2>
    <p class="lede">AI is the part people see. Most of the work is the data, cloud, application and security layers underneath, so we cover all of them.</p></div>
  <div class="services">
    <article class="service-feature">
      <h3>AI &amp; data innovation</h3>
      <p>Enterprise AI that automates tasks, sharpens daily decisions and connects to the systems and data you already have.</p>
      <svg class="service-feature__art" viewBox="0 0 400 220" fill="none" aria-hidden="true"><g stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity=".55"><path d="M0 10 C 140 10, 210 110, 322 110"/><path d="M0 40 C 140 40, 210 110, 322 110"/><path d="M0 70 C 140 70, 210 110, 322 110"/><path d="M0 100 C 140 100, 210 110, 322 110"/><path d="M0 130 C 140 130, 210 110, 322 110"/><path d="M0 160 C 140 160, 210 110, 322 110"/><path d="M0 190 C 140 190, 210 110, 322 110"/><path d="M0 210 C 140 210, 210 110, 322 110"/></g><g stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity=".55"><path d="M338 110 C 360 110, 380 90, 400 70"/><path d="M338 110 C 360 110, 380 130, 400 150"/><path d="M338 110 H400"/></g><circle cx="330" cy="110" r="14" fill="#2f6bff" opacity=".35"/><circle cx="330" cy="110" r="6" fill="#2f6bff"/></svg>
      <ul class="chips" aria-label="Includes"><li class="chip">Machine learning &amp; MLOps</li><li class="chip">Data engineering</li><li class="chip">AI automation</li></ul>
      <a class="text-link" href="services.html#ai-data">See AI &amp; data services {ARROW}</a>
    </article>
    <ul class="service-list">{rows}</ul>
  </div>
</div></section>

<section class="section on-dark" aria-labelledby="stats-title"><div class="container">
  <div class="stats-intro"><h2 id="stats-title">More than seventeen years of building systems that stay up.</h2>
    <a class="btn btn--ghost" href="about.html">How we work</a></div>
  <div class="stats">
    <div class="stat"><p class="stat__num"><span data-count="17">17</span><small>+</small></p><p class="stat__label">Years building digital solutions</p></div>
    <div class="stat"><p class="stat__num"><span data-count="800">800</span><small>+</small></p><p class="stat__label">Engineers and specialists</p></div>
    <div class="stat"><p class="stat__num"><span data-count="73">73</span><small>%</small></p><p class="stat__label">Client retention</p></div>
    <div class="stat"><p class="stat__num"><span data-count="4">4</span></p><p class="stat__label">Global delivery hubs</p></div>
  </div>
</div></section>

<section class="section" aria-labelledby="method-title"><div class="container">
  <div class="section-head"><h2 id="method-title">From first idea to something your team runs.</h2>
    <p class="lede">Every step ends with something you can use or decide on.</p></div>
  <ol class="method">
    <li class="method__step"><h3>Map it</h3><p>We find the decision or workflow worth improving, check that your data can support it and agree how success will be measured.</p>
      <ul><li>Use-case workshop</li><li>Data and security readiness check</li><li>Baseline and target</li></ul></li>
    <li class="method__step"><h3>Prove it</h3><p>We build a small working system on your own data and test it against the baseline. You see results before you commit to scale.</p>
      <ul><li>Working prototype</li><li>Results against the baseline</li><li>A clear go or no-go</li></ul></li>
    <li class="method__step"><h3>Run it</h3><p>We take the proven system to production with security, monitoring and cost controls built in, then support it or hand it over.</p>
      <ul><li>Production build</li><li>Monitoring and cost controls</li><li>Managed support or team handover</li></ul></li>
  </ol>
</div></section>

<section class="section section--alt" aria-labelledby="cases-title"><div class="container">
  <div class="section-head"><h2 id="cases-title">Results first, then the story.</h2>
    <p class="lede">A few of the results we have delivered.</p></div>
  <div class="cases">
    <a class="case case--lead" href="case-studies.html#claims-triage">
      <div class="case__meta"><span>Insurance &middot; Machine learning</span></div>
      <div><p class="case__metric">38%</p>
      <h3>Faster claims triage with a model that explains its calls</h3></div>
      <p>A regional insurer routes claims with a model that flags the ones needing a person and shows why.</p>
      <div class="case__bar" aria-hidden="true"><i style="--w:38%"></i></div>
    </a>
    <a class="case" href="case-studies.html#logistics-releases">
      <div class="case__meta"><span>Logistics &middot; DevOps</span></div>
      <p class="case__metric">4x</p><h3>More frequent releases after a delivery pipeline rebuild</h3>
      <div class="case__bar" aria-hidden="true"><i style="--w:80%"></i></div>
    </a>
    <a class="case" href="case-studies.html#healthcare-cloud">
      <div class="case__meta"><span>Healthcare &middot; Cloud</span></div>
      <p class="case__metric">31%</p><h3>Lower cloud spend with no change in uptime</h3>
      <div class="case__bar" aria-hidden="true"><i style="--w:31%"></i></div>
    </a>
  </div>
  <p style="margin-top:var(--s-6)"><a class="text-link" href="case-studies.html">Read all case studies {ARROW}</a></p>
</div></section>

<section class="section" aria-labelledby="why-title"><div class="container why">
  <div class="why__intro"><h2 id="why-title">Built to deliver results in production.</h2>
    <p class="lede">We'd rather ship a smaller thing that works than present a bigger thing that doesn't.</p>
    <a class="btn btn--ghost" href="about.html" style="justify-self:start">About Virtual IP</a></div>
  <div class="why__list">{why_html}</div>
</div></section>

<section class="section--tight" id="readiness" aria-labelledby="quiz-title"><div class="container">
  <div class="quiz-wrap">
    <div class="quiz-intro">
      <h2 id="quiz-title">Where does your organization stand on AI?</h2>
      <p class="lede">Six questions. You get a stage, a profile across six areas and a suggested first step.</p>
      <ul><li>No email needed</li><li>Answers stay in your browser</li><li>About two minutes</li></ul>
    </div>
    <div class="quiz" data-quiz aria-live="polite"><noscript><p>The readiness check needs JavaScript. To talk it through instead, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></noscript></div>
  </div>
</div></section>

<section class="section" aria-labelledby="creds-title"><div class="container">
  <div class="section-head"><h2 id="creds-title">Proof your security team can check.</h2>
    <p class="lede">Independent certifications and partnerships back how we build, secure and deliver.</p></div>
  <div class="creds">{creds_html}</div>
</div></section>

<section class="section section--alt" aria-labelledby="faq-title"><div class="container">
  <div class="section-head"><h2 id="faq-title">Questions buyers ask first.</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>

{cta_band()}
</main>
"""
    html += footer('<script src="assets/js/hero.js" defer></script>\n<script src="assets/js/quiz.js" defer></script>\n')
    write("index.html", html)


# =========================================================================================
# SERVICES
# =========================================================================================
def build_services():
    pillars = [
        ("ai-data", "AI & data innovation", "Enterprise AI that automates tasks, improves daily decisions and connects cleanly to your systems and data.", [
            ("AI & machine learning", "Models for prediction, classification and language, built around a specific decision."),
            ("MLOps & infrastructure", "Pipelines that train, deploy and monitor models so they keep working after launch."),
            ("Data science & analytics", "Analysis that turns your data into answers people can act on."),
            ("Data engineering & integration", "Reliable pipelines that bring data from many systems into one usable place."),
            ("Data governance & BI", "Ownership, quality rules and dashboards so everyone trusts the same numbers."),
            ("AI proof of concept & MVP", "A small working system on your data, tested against a baseline."),
            ("AI software development", "Production applications with AI built into the product, not bolted on."),
        ]),
        ("cloud", "Cloud & infrastructure", "Secure, scalable cloud environments, and migrations planned to cut downtime.", [
            ("Cloud strategy & architecture", "A target design and roadmap that match your workloads and budget."),
            ("Cloud migration", "Planned moves to AWS or Azure with rollback built in."),
            ("Infrastructure modernization", "Replacing aging infrastructure with managed, automated platforms."),
            ("Cloud engineering", "Hands-on build of networks, platforms and services as code."),
            ("CloudOps & DevOps", "Pipelines, automation and operations that speed up safe delivery."),
            ("Managed cloud services", "Day-to-day running, monitoring and support of your environment."),
            ("Cloud cost optimization (FinOps)", "Visibility and controls that bring spend in line with value."),
            ("Multi-cloud security & compliance", "Consistent controls across providers and regions."),
        ]),
        ("apps", "Application development", "Reliable digital products for web and mobile, built around real users and fast growth.", [
            ("UX/UI design", "Research-led interfaces tested with the people who will use them."),
            ("Application development", "Custom web and mobile software, from first release to scale."),
            ("Web development", "Fast, accessible sites and web applications."),
            ("Application modernization", "Moving legacy applications to current architectures without a big-bang rewrite."),
            ("Quality assurance & continuous delivery", "Automated testing and release pipelines that catch problems early."),
        ]),
        ("security", "Cybersecurity", "Practical security work that detects threats early, strengthens defenses and supports compliance.", [
            ("Consulting & risk assessment", "A clear view of where you are exposed and what to fix first."),
            ("Application security & penetration testing", "Testing that finds weaknesses before attackers do."),
            ("Cloud security", "Identity, network and data controls for cloud workloads."),
            ("Red teaming & adversary simulation", "Realistic attack exercises that test people, process and tools."),
            ("Security solutions", "Selection and rollout of the tooling your team will actually use."),
        ]),
        ("implementation", "Solution implementation", "Deploy and integrate enterprise systems with minimal disruption.", [
            ("ERP integration", "Connecting ERP with the systems around it so data flows once."),
            ("System migration", "Moving data and workloads with testing, cutover plans and fallbacks."),
            ("Legacy modernization", "Retiring or rebuilding legacy systems in stages."),
        ]),
        ("optimization", "Optimization & quality", "Continuous testing and tuning that keep systems fast, stable and efficient.", [
            ("Performance tuning", "Finding and fixing the bottlenecks that hurt speed and stability."),
            ("QA automation", "Automated regression and load testing wired into delivery."),
            ("Cost optimization", "Trimming waste in infrastructure and licensing without risking reliability."),
        ]),
        ("support", "IT support & managed services", "People and process to keep your systems running around the clock.", [
            ("L1, L2 and L3 IT support", "Tiered support from first response to deep technical fixes."),
            ("24/7 helpdesk & NOC", "Round-the-clock monitoring and response."),
            ("Application & infrastructure support", "Ongoing care for the systems you depend on."),
            ("SLA-based managed IT services", "Clear service levels with reporting you can hold us to."),
            ("Support & maintenance", "Fixes, updates and improvements after launch."),
            ("Incident, problem & change management", "Structured handling that cuts repeat outages."),
        ]),
    ]
    blocks = ""
    for pid, title, lead, items in pillars:
        it = "".join(f"<div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>" for t, d in items)
        blocks += (f'<section class="pillar" id="{pid}" aria-labelledby="{pid}-t"><div class="pillar__lead"><h2 id="{pid}-t">{escape(title)}</h2><p>{escape(lead)}</p></div>'
                   f'<div class="pillar__items">{it}</div></section>')
    engage = [("Dedicated team", "A team that works as an extension of yours, on your roadmap."),
              ("Offshore development center", "A stable, long-term team in one of our delivery hubs."),
              ("Fixed-price projects", "Defined scope, schedule and cost for well-understood work."),
              ("Hybrid delivery", "A mix of the above, shaped around your project and budget.")]
    eng = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in engage)
    html = head("Services | Virtual IP", "AI and data, cloud, application development, cybersecurity, implementation, optimization and managed IT services from Virtual IP.", "services.html")
    html += header("services.html")
    html += f"""<main id="main">
{page_head('Everything AI needs to run in production.', 'Six service lines and a managed support practice, so the data, cloud, application and security work behind your AI comes from one accountable team.', 'Services')}
<section class="section"><div class="container">{blocks}</div></section>
<section class="section on-dark" aria-labelledby="eng-t"><div class="container">
  <div class="section-head"><h2 id="eng-t">Four ways to work with us.</h2><p class="lede">Pick the model that fits the work. You can change it as the project changes.</p></div>
  <div class="engage">{eng}</div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("services.html", html)


# =========================================================================================
# CASE STUDIES
# =========================================================================================
CASES = [
    ("claims-triage", "38%", "Faster claims triage with a model that explains its calls", "Insurance · Machine learning",
     "Adjusters at a regional insurer spent hours sorting incoming claims by hand, and urgent cases waited in the same queue as routine ones.",
     "We built a triage model on historical claims, kept a person in the loop for uncertain cases and showed adjusters the factors behind each score.",
     "Triage time fell by 38% against the pre-project baseline, and adjusters reported they trusted the scores because they could see the reasons."),
    ("logistics-releases", "4x", "More frequent releases after a delivery pipeline rebuild", "Logistics · DevOps",
     "A freight-tracking platform shipped quarterly because every release needed a manual regression pass and a weekend deployment.",
     "We automated testing, introduced infrastructure as code and moved deployment to a pipeline with automatic rollback.",
     "The team now releases four times as often, with deployments during business hours and fewer incidents tied to releases."),
    ("healthcare-cloud", "31%", "Lower cloud spend with no change in uptime", "Healthcare · Cloud",
     "A healthcare network had grown its cloud estate without ownership tags or budgets, and monthly bills kept rising.",
     "We mapped spend to services and teams, right-sized workloads, set budgets and alerts and automated shutdown of idle environments.",
     "Cloud spend dropped 31% while availability held steady, and every team now sees its own costs."),
    ("fintech-fraud", "62%", "Fewer false fraud alerts for a payments platform", "Fintech · Data engineering",
     "A payments platform's rules-based fraud checks flagged too many legitimate transactions, overloading the review team.",
     "We consolidated transaction data into a governed pipeline and trained a model to rank alerts so analysts saw the riskiest first.",
     "False alerts fell by 62%, and analysts spend their time on genuine cases."),
]


def build_cases():
    blocks = ""
    for cid, metric, title, meta, ch, did, res in CASES:
        blocks += f"""<article class="case-full" id="{cid}" aria-labelledby="{cid}-t">
  <div class="case-full__side"><p class="case__meta"><span>{escape(meta)}</span></p><p class="case__metric">{metric}</p></div>
  <div><h2 id="{cid}-t">{escape(title)}</h2><dl style="margin-top:var(--s-6)">
    <div><dt>The challenge</dt><dd>{escape(ch)}</dd></div>
    <div><dt>What we did</dt><dd>{escape(did)}</dd></div>
    <div><dt>The result</dt><dd>{escape(res)}</dd></div></dl></div></article>"""
    html = head("Case studies | Virtual IP", "Outcome-led examples of AI, cloud and delivery work from Virtual IP.", "case-studies.html")
    html += header("case-studies.html")
    html += f"""<main id="main">
{page_head('Results first, then the story.', 'Each story leads with what changed.', 'Case studies')}
<section class="section--tight"><div class="container">{blocks}</div></section>
{cta_band("Want results like these?", "Tell us what you're trying to improve and we'll take it from there.")}
</main>
"""
    html += footer()
    write("case-studies.html", html)


# =========================================================================================
# ABOUT
# =========================================================================================
def build_about():
    html = head("About | Virtual IP", "Virtual IP is a technology partner with more than 17 years of experience, 800+ engineers and specialists and four global delivery hubs.", "about.html")
    html += header("about.html")
    html += f"""<main id="main">
{page_head('We build the systems behind your decisions.', 'Virtual IP is a technology partner for teams that need AI, cloud and software to work in the real world, not only in a demo.', 'About')}
<section class="section"><div class="container split">
  <h2>Practical execution, measurable impact, long-term reliability.</h2>
  <div class="prose">
    <p>For more than seventeen years we have built digital systems for organizations in fintech, healthcare, logistics and beyond. Today more than 800 engineers and specialists work across four global delivery hubs.</p>
    <p><strong>We focus on what ships.</strong> That means clear scope, short cycles, honest trade-offs and security from the first design decision. It also means staying involved after launch, which is part of why 73% of clients stay with us.</p>
    <p>We're an ISO 27001 certified, SOC 2 Type II audited partner of AWS, Microsoft and Google Cloud, and a member of the Forbes Technology Council.</p>
  </div></div></section>
<section class="section section--alt" aria-labelledby="val-t"><div class="container">
  <div class="section-head"><h2 id="val-t">How we work.</h2></div>
  <div class="values">
    <div><h3>Ship what works</h3><p>We prefer a smaller system in production over a bigger one in a slide deck, and we measure every build against a baseline.</p></div>
    <div><h3>Say the trade-off out loud</h3><p>Every option costs something in time, money or risk. We name it early so you can choose with open eyes.</p></div>
    <div><h3>Build it to last</h3><p>Security, monitoring and documentation are part of the first release, so the system is easy to run and easy to hand over.</p></div>
  </div></div></section>
<section class="section on-dark" aria-labelledby="ind-t"><div class="container">
  <div class="section-head"><h2 id="ind-t">Industries where the rules are real.</h2>
    <p class="lede">We understand the regulatory, operational and technical limits of the sectors we serve.</p></div>
  <div class="engage" style="grid-template-columns:repeat(3,1fr)">
    <div><h3>Fintech</h3><p>Payments, risk and compliance systems that stand up to audit.</p></div>
    <div><h3>Healthcare</h3><p>Data platforms and applications that respect privacy and clinical reality.</p></div>
    <div><h3>Logistics</h3><p>Tracking, planning and automation for operations that never close.</p></div>
  </div></div></section>
<section class="section"><div class="container split">
  <h2>Meet the people doing the work.</h2>
  <div class="prose"><p>Our teams combine AI engineers, cloud architects, designers and security specialists.</p>
  <p><a class="btn" href="team.html">Meet the team</a> &nbsp; <a class="btn btn--ghost" href="careers.html">Join us</a></p></div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("about.html", html)


# =========================================================================================
# INSIGHTS
# =========================================================================================
POSTS = [
    ("insights-ai-readiness-checklist.html", "AI readiness", "A short checklist for deciding if you're ready for AI",
     "Six questions that reveal whether your next AI project will reach production.", "4 min read",
     [("intro", "Most AI projects stall for ordinary reasons: unclear ownership, patchy data and no way to tell if the thing worked. Checking six areas before you start prevents most of them."),
      ("h", "The six checks"),
      ("ul", ["<strong>Use case.</strong> One decision or workflow, with an owner and a success metric.",
              "<strong>Data.</strong> Reachable, documented and owned by someone who cares about quality.",
              "<strong>Infrastructure.</strong> A managed environment with monitoring and cost controls.",
              "<strong>People.</strong> A named owner with engineering capacity after launch.",
              "<strong>Governance.</strong> A written approach to AI and sensitive data, with a review step.",
              "<strong>Measurement.</strong> A baseline for today's process so you can prove the change."]),
      ("p", "If three or more are weak, start there. A working proof of concept on shaky foundations usually becomes an expensive pilot.")]),
    ("insights-cloud-migration-plan.html", "Cloud", "How to plan a cloud migration without surprises",
     "A practical sequence from inventory to cutover, with rollback at every step.", "5 min read",
     [("intro", "Cloud migrations go wrong when teams move first and discover dependencies later. A simple sequence keeps surprises small."),
      ("h", "A practical sequence"),
      ("ul", ["<strong>Inventory.</strong> List every application, its data and what it depends on.",
              "<strong>Classify.</strong> Decide what to retire, move as-is, adapt or rebuild.",
              "<strong>Design security first.</strong> Plan identity, encryption, logging and data handling before anything moves.",
              "<strong>Move in waves.</strong> Start with a low-risk workload to prove the path.",
              "<strong>Keep a rollback.</strong> Define the point where you'd step back and how.",
              "<strong>Measure after.</strong> Compare performance and cost against the starting baseline."]),
      ("p", "The time it takes depends on how many applications you have and how tangled they are, which is why an assessment comes before a schedule.")]),
    ("insights-pilot-to-production.html", "Delivery", "Why AI pilots stall, and how to avoid it",
     "Five reasons pilots never reach production, and what to do about each.", "4 min read",
     [("intro", "A pilot that impresses in a demo can still fail in the real world. The causes are rarely about the model."),
      ("h", "Five common causes"),
      ("ul", ["<strong>No owner.</strong> Name a business owner before the first sprint.",
              "<strong>No baseline.</strong> Measure today's process so results mean something.",
              "<strong>Prototype data.</strong> Test on data that looks like production, not a clean sample.",
              "<strong>Late security review.</strong> Involve security and compliance at the start.",
              "<strong>No plan to run it.</strong> Decide who monitors, supports and improves the system after launch."]),
      ("p", "Every one of these is cheaper to fix in week one than in month six.")]),
]


def build_insights():
    items = ""
    for f, tag, title, sub, rt, _ in POSTS:
        items += (f'<article class="post"><p class="post__tag">{escape(tag)}</p><div><h2><a href="{f}">{escape(title)}</a></h2><p>{escape(sub)}</p></div>'
                  f'<p class="post__read">{rt}</p></article>')
    html = head("Insights | Virtual IP", "Practical guidance on AI readiness, cloud migration and getting projects into production.", "insights.html")
    html += header("insights.html")
    html += f"""<main id="main">
{page_head('Plain advice for people shipping technology.', 'Practical notes from the people who build and run these systems.', 'Insights')}
<section class="section--tight"><div class="container"><div class="post-list">{items}</div></div></section>
{cta_band()}
</main>
"""
    html += footer()
    write("insights.html", html)
    for f, tag, title, sub, rt, body in POSTS:
        parts = ""
        for kind, val in body:
            if kind == "intro" or kind == "p":
                parts += f"<p>{val}</p>"
            elif kind == "h":
                parts += f"<h2>{val}</h2>"
            elif kind == "ul":
                parts += "<ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>"
        h = head(f"{title} | Virtual IP", sub, f)
        h += header("insights.html")
        h += f"""<main id="main">
<section class="page-head"><div class="container"><ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="insights.html">Insights</a></li><li aria-current="page">{escape(tag)}</li></ol>
<h1 style="font-size:var(--step-4);max-width:22ch">{escape(title)}</h1></div></section>
<article class="container article"><div class="byline"><span>Virtual IP team</span><span>{rt}</span></div>{parts}
<p><a class="btn" href="index.html#readiness">Take the readiness check</a></p></article>
{cta_band()}
</main>
"""
        h += footer()
        write(f, h)


# =========================================================================================
# TEAM / CAREERS
# =========================================================================================
def build_team():
    people = [("Alex Morgan", "AM", "a", "Chief Executive Officer", "Sets direction and keeps delivery honest."),
              ("Sam Rivera", "SR", "b", "Chief Technology Officer", "Owns architecture and engineering standards."),
              ("Priya Nair", "PN", "c", "Head of AI", "Leads machine learning and data engineering."),
              ("Chris Okafor", "CO", "d", "Head of Delivery", "Keeps projects on plan and on quality."),
              ("Dana Whitfield", "DW", "d", "Head of Security", "Leads security design, audits and compliance."),
              ("Lee Tran", "LT", "a", "Head of Cloud", "Leads cloud architecture and operations."),
              ("Maya Haddad", "MH", "b", "Head of Design", "Leads product and interface design."),
              ("Jordan Ellis", "JE", "c", "Head of People", "Builds the teams that do the work.")]
    cards = "".join(f'<li class="person"><div class="avatar avatar--{c}" aria-hidden="true">{i}</div><h3>{n}</h3><p class="role-title">{r}</p><p>{b}</p></li>' for n, i, c, r, b in people)
    html = head("Team | Virtual IP", "The leadership team behind Virtual IP.", "team.html")
    html += header("about.html")
    html += f"""<main id="main">
{page_head('The people doing the work.', 'Leaders who still review the work.', 'Team')}
<section class="section--tight"><div class="container"><ul class="team">{cards}</ul></div></section>
{cta_band("Want to work with us?", "See open roles or tell us about your project.")}
</main>
"""
    html += footer()
    write("team.html", html)


def build_careers():
    roles = [("Senior machine learning engineer", "AI & data", "Build and deploy models that run in production."),
             ("Cloud and DevOps engineer", "Cloud", "Automate infrastructure, delivery and operations."),
             ("Security engineer", "Security", "Assess, test and harden client systems."),
             ("Product designer", "Design", "Design interfaces for complex enterprise products."),
             ("Delivery manager", "Delivery", "Keep multi-team projects clear, on plan and honest.")]
    rows = ""
    for t, team, d in roles:
        subj = escape(f"Application: {t}").replace(" ", "%20").replace(":", "%3A")
        rows += (f'<li class="role"><div><h3>{t}</h3><p>{d}</p></div><p class="role__meta">{team}</p>'
                 f'<a class="btn btn--ghost btn--sm" href="mailto:{EMAIL}?subject={subj}">Apply by email<span class="sr-only"> for {escape(t)}</span></a></li>')
    html = head("Careers | Virtual IP", "Join Virtual IP and build AI, cloud and software that stay up.", "careers.html")
    html += header("careers.html")
    html += f"""<main id="main">
{page_head('Build things that stay up.', 'Work with senior engineers and designers on systems that run in production for real organizations.', 'Careers')}
<section class="section" aria-labelledby="car-t"><div class="container">
  <div class="values"><div><h3>Real problems</h3><p>Projects span fintech, healthcare and logistics, with real users and real constraints.</p></div>
  <div><h3>Strong peers</h3><p>800+ engineers and specialists, with room to learn from people who've done it before.</p></div>
  <div><h3>Global teams</h3><p>Four delivery hubs and distributed teams that work across time zones.</p></div></div></div></section>
<section class="section section--alt" aria-labelledby="open-t"><div class="container">
  <div class="section-head"><h2 id="open-t">Open roles.</h2><p class="lede">Roles we are hiring for now.</p></div>
  <ul class="roles">{rows}</ul>
  <p style="margin-top:var(--s-6)">Don't see your role? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> and tell us what you'd build.</p></div></section>
</main>
"""
    html += footer()
    write("careers.html", html)


# =========================================================================================
# CONTACT
# =========================================================================================
def build_contact():
    html = head("Contact | Virtual IP", "Tell Virtual IP what you're trying to improve. Plan your AI roadmap, or ask about cloud, software, security and support.", "contact.html")
    html += header("contact.html")
    html += f"""<main id="main">
{page_head("Tell us what you're trying to improve.", 'A short note is enough. Tell us the goal, the systems involved and any deadline.', 'Contact')}
<section class="section--tight"><div class="container contact">
  <form class="form" id="contact-form" novalidate aria-labelledby="form-title">
    <h2 id="form-title" class="sr-only">Contact form</h2>
    <div class="form__row">
      <div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="form__row">
      <div class="field"><label for="company">Company <span class="hint">(optional)</span></label><input id="company" name="company" type="text" autocomplete="organization"></div>
      <div class="field"><label for="topic">What do you need?</label><select id="topic" name="topic">
        <option value="ai-roadmap">Plan an AI roadmap</option><option value="cloud">Cloud and infrastructure</option><option value="software">Software development</option>
        <option value="security">Cybersecurity</option><option value="support">Support and managed services</option><option value="careers">Careers</option><option value="other">Something else</option></select></div>
    </div>
    <div class="field"><label for="message">How can we help?</label><textarea id="message" name="message" required></textarea></div>
    <div><button class="btn" type="submit">Send message</button></div>
    <p class="form__status" id="form-status" role="status" tabindex="-1" hidden></p>
  </form>
  <aside class="contact__side" aria-label="Other ways to reach us">
    <div><h2>What happens next</h2><ol><li>A person reads your message.</li><li>We reply to the email you give us.</li><li>If it's a fit, we set up a working session.</li></ol></div>
    <div><h2>Prefer to write directly?</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p><a href="{LINKEDIN}" rel="noopener" target="_blank">Virtual IP on LinkedIn<span class="sr-only"> (opens in a new tab)</span></a></p></div>
  </aside>
</div></section>
</main>
"""
    html += footer('<script src="assets/js/contact.js" defer></script>\n')
    write("contact.html", html)


# =========================================================================================
# LEGAL (preview text; needs counsel review)
# =========================================================================================
def build_legal():
    notice = ''
    pages = {
        "privacy.html": ("Privacy policy", "How Virtual IP handles information you share through this site.", f"""
{notice}<h2>What we collect</h2><p>This site doesn't use analytics or advertising trackers. If you contact us, we receive the details you choose to send, such as your name, work email, company and message.</p>
<h2>How we use it</h2><ul><li>To reply to your enquiry.</li><li>To assess whether we can help.</li></ul>
<h2>The contact form</h2><p>In this version, submitting the form opens your email app with your message ready to send to {EMAIL}. Nothing is stored by the site itself.</p>
<h2>Your choices</h2><p>To ask what we hold about you, or to have it deleted, email {EMAIL}.</p>"""),
        "terms.html": ("Terms of service", "Terms for using the Virtual IP website.", f"""
{notice}<h2>Using this site</h2><p>The content is general information about Virtual IP's services and isn't a binding offer. Services are provided under a signed agreement.</p>
<h2>Intellectual property</h2><p>The site's text, design and code belong to Virtual IP unless stated otherwise.</p>

<h2>Contact</h2><p>Questions about these terms: {EMAIL}.</p>"""),
        "cookies.html": ("Cookie policy", "What this website stores in your browser.", f"""
{notice}<h2>What this site stores</h2><p>This site sets no cookies. It saves one preference in your browser's local storage: your light or dark theme choice, under the name <code>vip-theme</code>.</p>
<h2>What it doesn't do</h2><ul><li>No analytics or advertising cookies.</li><li>No cross-site tracking.</li></ul>
<h2>Clearing it</h2><p>Clear this site's data in your browser settings to remove the saved theme.</p>
<h2>If this changes</h2><p>If analytics or other cookies are added, this page and a consent control will be updated first.</p>"""),
    }
    for f, (t, d, body) in pages.items():
        h = head(f"{t} | Virtual IP", d, f) + header(f)
        h += f'<main id="main">{page_head(t, d, t)}<section><div class="container"><div class="legal">{body}</div></div></section></main>\n'
        h += footer()
        write(f, h)


def copy_favicons():
    (OUT / "assets/img").mkdir(parents=True, exist_ok=True)
    for f in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "favicon-32.png", "favicon-192.png"):
        shutil.copy(OUT / "brand/favicon" / f, OUT / "assets/img" / f)


if __name__ == "__main__":
    (OUT / "assets/img").mkdir(parents=True, exist_ok=True)
    copy_favicons()
    build_home(); build_services(); build_cases(); build_about(); build_insights(); build_team(); build_careers(); build_contact(); build_legal()
    print("built", len(list(OUT.glob("*.html"))), "pages")
