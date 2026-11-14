/* Virtual IP — site behaviour: theme, nav, header state, counters, reveals, cursor, magnetic buttons */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- Theme ---------- */
  var themeBtns = document.querySelectorAll("[data-theme-toggle]");
  function currentTheme() {
    var t = doc.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function syncThemeButtons() {
    var dark = currentTheme() === "dark";
    themeBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String(dark));
      b.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
      var label = b.querySelector(".theme-toggle__label");
      if (label) label.textContent = dark ? "Light theme" : "Dark theme";
    });
  }
  themeBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      doc.setAttribute("data-theme", next);
      try { localStorage.setItem("vip-theme", next); } catch (e) { /* storage unavailable */ }
      syncThemeButtons();
    });
  });
  syncThemeButtons();

  /* ---------- Mobile nav ---------- */
  var menuBtn = document.querySelector("[data-menu-btn]");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    var setMenu = function (open) {
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
    };
    menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setMenu(false); menuBtn.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    window.matchMedia("(min-width: 62.01rem)").addEventListener("change", function (e) { if (e.matches) setMenu(false); });
  }

  /* ---------- Header state over the hero ---------- */
  var header = document.querySelector(".site-header");
  if (header && document.body.classList.contains("has-hero")) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Counters + reveal-on-view ---------- */
  var counters = document.querySelectorAll("[data-count]");
  function format(n) { return Math.round(n).toLocaleString("en-US"); }
  function runCounter(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var dur = 1600, start = null;
    function tick(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = format(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        if (el.hasAttribute("data-count") && !reduceMotion.matches) runCounter(el);
        if (el.classList.contains("case")) el.classList.add("in-view");
        io.unobserve(el);
      });
    }, { threshold: 0.35 });
    counters.forEach(function (el) { if (!reduceMotion.matches) el.textContent = "0"; io.observe(el); });
    document.querySelectorAll(".case").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".case").forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---------- Cursor ring + magnetic buttons (fine pointers, motion allowed) ---------- */
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  if (fine.matches && !reduceMotion.matches) {
    var ring = document.createElement("div");
    ring.className = "cursor-ring";
    ring.setAttribute("aria-hidden", "true");
    document.body.appendChild(ring);
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    var loop = function () {
      cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2;
      ring.style.transform = "translate3d(" + cx.toFixed(1) + "px," + cy.toFixed(1) + "px,0)";
      raf = (Math.abs(tx - cx) > 0.3 || Math.abs(ty - cy) > 0.3) ? requestAnimationFrame(loop) : null;
    };
    window.addEventListener("pointermove", function (e) {
      tx = e.clientX; ty = e.clientY;
      ring.classList.add("is-on");
      if (!raf) raf = requestAnimationFrame(loop);
      var over = e.target.closest && e.target.closest("a, button, summary, label, input, select, textarea");
      ring.classList.toggle("is-active", !!over);
    }, { passive: true });
    document.addEventListener("pointerleave", function () { ring.classList.remove("is-on"); });

    /* Spotlight cards: a soft glow follows the cursor. Adapted from React Bits SpotlightCard
       (c) David Haz, MIT + Commons Clause, https://github.com/DavidHDev/react-bits */
    document.querySelectorAll(".card, .why-card, .industry, .cred-tile, .case").forEach(function (el) {
      el.classList.add("spot");
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--sx", (e.clientX - r.left).toFixed(0) + "px");
        el.style.setProperty("--sy", (e.clientY - r.top).toFixed(0) + "px");
      });
      el.addEventListener("pointerenter", function () { el.style.setProperty("--so", "1"); });
      el.addEventListener("pointerleave", function () { el.style.setProperty("--so", "0"); });
    });

    document.querySelectorAll(".btn:not(.btn--sm)").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / r.width;
        var dy = (e.clientY - (r.top + r.height / 2)) / r.height;
        btn.style.transform = "translate(" + (dx * 10).toFixed(1) + "px," + (dy * 8).toFixed(1) + "px)";
      });
      btn.addEventListener("pointerleave", function () { btn.style.transform = ""; });
    });
  }

  /* ---------- Footer year ---------- */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();

/* Scroll-lit statement: words light up as you read. Adapted from MotionSites web-builder (MIT). */
(function () {
  document.querySelectorAll(".scroll-reveal").forEach(function (el) {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    (function wrap(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var f = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { f.appendChild(document.createTextNode(t)); return; }
            var s = document.createElement("span"); s.className = "sp"; s.textContent = t; f.appendChild(s);
          });
          c.replaceWith(f);
        } else wrap(c);
      });
    })(el);
    var pieces = el.querySelectorAll(".sp"), N = pieces.length, tick = false;
    function update() {
      tick = false;
      var r = el.getBoundingClientRect(), vh = innerHeight;
      var p = Math.min(1, Math.max(0, (0.8 * vh - r.top) / (0.6 * vh + r.height)));
      pieces.forEach(function (s, i) {
        var a = i / N - 0.1, b = i / N + 0.05;
        s.style.opacity = (0.2 + 0.8 * Math.min(1, Math.max(0, (p - a) / (b - a)))).toFixed(3);
      });
    }
    addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(update); } }, { passive: true });
    addEventListener("resize", update); update();
  });
})();

/* Blur-rise page titles. Adapted from MotionSites web-builder (MIT). */
document.querySelectorAll(".page-head h1").forEach(function (h) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var n = 0;
  (function wrap(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (c) {
      if (c.nodeType === 3) {
        var f = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(function (t) {
          if (!t) return;
          if (/^\s+$/.test(t)) { f.appendChild(document.createTextNode(t)); return; }
          var s = document.createElement("span"); s.className = "bt"; s.style.setProperty("--i", n++); s.textContent = t; f.appendChild(s);
        });
        c.replaceWith(f);
      } else wrap(c);
    });
  })(h);
});

/* Ask Virtual IP: a small rule-based assistant. No server, no tracking; answers come from the site's own content. */
(function () {
  var mail = document.querySelector('a[href^="mailto:"]'); var email = mail ? mail.getAttribute("href").replace("mailto:", "").split("?")[0] : "";
  var KB = [
    { k: "service offer do what ai cloud software build", a: "We work across AI and data, cloud and infrastructure, application development, cybersecurity, solution implementation, optimization, and IT support and managed services.", l: ["services.html", "See all services"] },
    { k: "engage model work together team dedicated project hybrid offshore offshoring", a: "You can work with us as a dedicated team, on a project with a clear scope and timeline, in a hybrid model shared with your own team, or through an offshore development center that scales with your workload.", l: ["services.html", "Engagement models"] },
    { k: "partner openai anthropic aws microsoft google salesforce", a: "We partner with OpenAI and Anthropic for production-ready AI, and we work with AWS, Microsoft, Google Cloud and Salesforce.", l: ["index.html#creds-title", "Partnerships"] },
    { k: "security iso soc certified compliance data privacy", a: "We are ISO 27001 certified and SOC 2 Type II audited. Security is part of design, build and deployment, and we agree how your data is accessed, stored and used before work begins.", l: ["index.html#creds-title", "Our credentials"] },
    { k: "case study results clients customer example work", a: "Recent results include doubling lending capacity without extra headcount, cutting AWS costs by about 50% while scaling tax compliance, and 10x scalability for an analytics platform.", l: ["case-studies.html", "Read the case studies"] },
    { k: "years experience founded about who company size people", a: "We have 18 years in business, more than 800 professionals and over 10 years of launching and building AI products. 73% of our clients return for long-term partnerships.", l: ["about.html", "About us"] },
    { k: "ready readiness assess start roadmap begin", a: "A good first step is our two-minute AI readiness check. You get a stage, a profile across six areas and a suggested first step. No email needed.", l: ["index.html#readiness", "Take the readiness check"] },
    { k: "job career hiring join work role open", a: "You can see what we are hiring for on the careers page.", l: ["careers.html", "Open roles"] },
    { k: "cloud migration move migrate", a: "We assess each workload on its merits, plan access, data handling and rollback before anything moves, and size the work after an assessment.", l: ["services.html", "Cloud services"] },
    { k: "price cost quote budget how much", a: "We size and price work after a short conversation about your goals and constraints, so we do not quote a number up front. Write to us and we will take it from there.", l: null },
    { k: "contact email talk speak reach call human", a: "The quickest way is email. Tell us what you are trying to improve and we will reply.", l: null }
  ];
  var FALLBACK = "I do not have a good answer for that. Our team will, so please write to us.";
  var CHIPS = ["What do you offer?", "How can we work together?", "Are you certified?", "Show me results", "Where do we start?"];
  var wrap = document.createElement("div"); wrap.className = "chat";
  wrap.innerHTML = '<button class="chat__fab" type="button" aria-expanded="false" aria-controls="chat-panel"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5z"/></svg><span>Ask us</span></button>' +
    '<section class="chat__panel" id="chat-panel" role="dialog" aria-label="Ask Virtual IP" hidden><header><strong>Ask Virtual IP</strong><button type="button" class="chat__close" aria-label="Close chat">&times;</button></header>' +
    '<div class="chat__log" role="log" aria-live="polite"></div><div class="chat__chips"></div>' +
    '<form class="chat__form"><label class="sr-only" for="chat-in">Your question</label><input id="chat-in" autocomplete="off" placeholder="Ask about services, security, results"><button type="submit">Send</button></form></section>';
  document.body.appendChild(wrap);
  var fab = wrap.querySelector(".chat__fab"), panel = wrap.querySelector(".chat__panel"), log = wrap.querySelector(".chat__log"), form = wrap.querySelector("form"), input = wrap.querySelector("input"), chips = wrap.querySelector(".chat__chips");
  function say(text, who, link) {
    var d = document.createElement("div"); d.className = "chat__msg chat__msg--" + who; d.textContent = text;
    if (link) { var a = document.createElement("a"); a.href = link[0]; a.textContent = link[1]; d.appendChild(document.createElement("br")); d.appendChild(a); }
    log.appendChild(d); log.scrollTop = log.scrollHeight;
  }
  function answer(q) {
    var words = q.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter(function (w) { return w.length > 2; }), best = null, score = 0;
    KB.forEach(function (e) { var s = 0, keys = e.k.split(" "); words.forEach(function (w) { if (keys.some(function (k) { return k === w || (w.length > 4 && k.indexOf(w.slice(0, 5)) === 0); })) s++; }); if (s > score) { score = s; best = e; } });
    if (best) { say(best.a, "bot", best.l); }
    else { say(FALLBACK, "bot", email ? ["mailto:" + email, "Email " + email] : ["contact.html", "Contact us"]); }
  }
  function ask(q) { say(q, "me"); setTimeout(function () { answer(q); }, matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 350); }
  CHIPS.forEach(function (c) { var b = document.createElement("button"); b.type = "button"; b.textContent = c; b.addEventListener("click", function () { ask(c); }); chips.appendChild(b); });
  function toggle(open) { panel.hidden = !open; fab.setAttribute("aria-expanded", open); if (open) { if (!log.children.length) say("Hi, I can answer questions about what we do. I am an automated assistant, and a person will pick up anything I cannot answer.", "bot"); input.focus(); } else fab.focus(); }
  fab.addEventListener("click", function () { toggle(panel.hidden); });
  wrap.querySelector(".chat__close").addEventListener("click", function () { toggle(false); });
  wrap.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) toggle(false); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value.trim(); if (q) { input.value = ""; ask(q); } });
})();
