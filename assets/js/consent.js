/* Consent-gated analytics. Does nothing (no banner, no cookies) until analytics is set in config.js. */
(function () {
  "use strict";
  var C = (window.VIP_CONFIG || {}).analytics || {};
  var KEY = "vip-consent", loaded = false;
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  window.VIP = window.VIP || {};
  window.VIP.track = function (name, props) {
    if (!loaded) return;
    try {
      if (C.provider === "plausible" && window.plausible) window.plausible(name, { props: props || {} });
      if (C.provider === "ga4" && window.gtag) window.gtag("event", name, props || {});
    } catch (e) {}
  };
  function load() {
    if (loaded || !C.provider || !C.id) return;
    var s = document.createElement("script"); s.async = true;
    if (C.provider === "plausible") { s.defer = true; s.setAttribute("data-domain", C.id); s.src = "https://plausible.io/js/script.tagged-events.js"; window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); }; }
    else if (C.provider === "ga4") { s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(C.id); window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); }; window.gtag("js", new Date()); window.gtag("config", C.id, { anonymize_ip: true }); }
    else return;
    document.head.appendChild(s); loaded = true;
  }
  function banner() {
    var d = document.createElement("section"); d.className = "consent"; d.setAttribute("aria-label", "Cookie consent");
    d.innerHTML = '<p>We use privacy-friendly analytics to see which pages help visitors. It stays off unless you accept. See the <a href="cookies.html">cookie policy</a>.</p><div class="consent__row"><button class="btn btn--sm" type="button" data-a>Accept analytics</button><button class="btn btn--sm btn--ghost" type="button" data-d>No thanks</button></div>';
    d.querySelector("[data-a]").onclick = function () { set("yes"); load(); d.remove(); };
    d.querySelector("[data-d]").onclick = function () { set("no"); d.remove(); };
    document.body.appendChild(d);
  }
  if (!C.provider || !C.id) return;
  var v = get(); if (v === "yes") load(); else if (v !== "no") banner();
  document.addEventListener("click", function (e) { var a = e.target.closest && e.target.closest("[data-track]"); if (a) window.VIP.track(a.getAttribute("data-track")); });
})();
