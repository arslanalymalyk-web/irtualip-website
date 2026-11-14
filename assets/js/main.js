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
