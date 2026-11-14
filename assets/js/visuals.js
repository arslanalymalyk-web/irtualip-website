/* Visual layer: draw-on charts, tabbed product mockups, light parallax.
   Everything degrades: without JS all panels and charts are simply visible. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- Reveal: charts, bars and sparklines draw when scrolled into view ---------- */
  var reveals = document.querySelectorAll("[data-reveal]");
  if (reduce.matches || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-drawn"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-drawn"); io.unobserve(en.target); }
      });
    }, { threshold: 0.2, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Tabs (WAI-ARIA tabs pattern, automatic activation) ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        if (panels[j]) {
          panels[j].hidden = !on;
          if (on) {
            panels[j].classList.remove("is-drawn");
            void panels[j].offsetWidth; // restart the draw-on
            requestAnimationFrame(function () { panels[j].classList.add("is-drawn"); });
          }
        }
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i, false); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = tabs.length, to = null;
        if (k === "ArrowDown" || k === "ArrowRight") to = (i + 1) % n;
        else if (k === "ArrowUp" || k === "ArrowLeft") to = (i - 1 + n) % n;
        else if (k === "Home") to = 0;
        else if (k === "End") to = n - 1;
        if (to !== null) { e.preventDefault(); select(to, true); }
      });
    });
    select(0, false);
  });

  /* ---------- Motion (vendored, tree-shaken build): scroll-linked depth + staggered entrances ----------
     Uses the independent `translate` property so it never fights the CSS hover transforms. */
  var M = window.VIPMotion;
  if (M && !reduce.matches) {
    var ease = [0.22, 1, 0.36, 1];
    // Staggered entrance, once per group
    document.querySelectorAll("[data-stagger]").forEach(function (group) {
      var kids = Array.prototype.slice.call(group.children);
      M.inView(group, function () {
        M.animate(kids, { opacity: [0, 1], translate: ["0 26px", "0 0"] }, { duration: 0.8, delay: M.stagger(0.07), ease: ease });
      }, { amount: 0.15 });
    });
    // Scroll-linked parallax for decorative layers
    document.querySelectorAll("[data-parallax]").forEach(function (el) {
      var f = parseFloat(el.getAttribute("data-parallax")) || 0.06;
      var d = Math.round(f * 520);
      M.scroll(M.animate(el, { translate: ["0 " + d + "px", "0 " + (-d) + "px"] }, { ease: "linear" }), { target: el, offset: ["start end", "end start"] });
    });
  }
})();
