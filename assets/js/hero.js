/* Hero video: loads only where it earns its weight.
   - Skipped on small screens, Data Saver / slow connections, and prefers-reduced-motion (poster stays).
   - Pauses when scrolled away. A visible pause control satisfies WCAG 2.2.2. */
(function () {
  "use strict";
  var hero = document.querySelector("[data-hero]");
  if (!hero) return;
  var video = hero.querySelector("video");
  var toggle = hero.querySelector("[data-media-toggle]");
  if (!video) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var wide = window.matchMedia("(min-width: 48rem)");
  var conn = navigator.connection || {};
  var heavy = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || "");
  var userPaused = false;
  var loaded = false;

  function eligible() { return !reduce.matches && wide.matches && !heavy; }

  function load() {
    if (loaded) return;
    loaded = true;
    ["webm", "mp4"].forEach(function (ext) {
      var s = document.createElement("source");
      s.src = video.getAttribute("data-" + ext);
      s.type = "video/" + ext;
      video.appendChild(s);
    });
    video.load();
  }

  function play() {
    if (!eligible() || userPaused) return;
    load();
    var p = video.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked: poster remains */ });
  }
  function pause() { video.pause(); }

  video.addEventListener("playing", function () { hero.classList.add("is-playing"); video.style.opacity = "1"; if (toggle) toggle.setAttribute("data-ready", "true"); });

  if (toggle) {
    toggle.addEventListener("click", function () {
      userPaused = !userPaused;
      toggle.setAttribute("aria-pressed", String(userPaused));
      toggle.querySelector(".media-toggle__label").textContent = userPaused ? "Play background motion" : "Pause background motion";
      userPaused ? pause() : play();
    });
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.isIntersecting ? play() : pause(); });
    }, { threshold: 0.05 }).observe(hero);
  } else { play(); }

  function onPrefChange() { if (eligible()) play(); else { pause(); video.style.opacity = "0"; } }
  reduce.addEventListener("change", onPrefChange);
  wide.addEventListener("change", onPrefChange);
})();
