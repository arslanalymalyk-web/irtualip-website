/* Contact form: accessible validation, quiz pre-fill, POST to /api/contact (see api/contact.js),
   and a mailto hand-off if the endpoint is not configured or unreachable. */
(function () {
  "use strict";
  var form = document.getElementById("contact-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var TO = "contact@virtualip.com";

  /* Pre-fill from the readiness check */
  var params = new URLSearchParams(window.location.search);
  var topic = params.get("topic");
  if (topic) {
    var sel = form.elements["topic"];
    if (sel) sel.value = topic;
    var stage = params.get("stage"), score = params.get("score"), focus = params.get("focus");
    if (stage && score && form.elements["message"] && !form.elements["message"].value) {
      form.elements["message"].value = "I took the AI readiness check and scored " + score + "/18 (" + stage + "). My weakest area was " + (focus || "n/a").toLowerCase() + ". I'd like to talk about a roadmap.";
    }
  }

  function setError(field, msg) {
    var wrap = field.closest(".field");
    var err = wrap.querySelector(".error");
    if (msg) {
      if (!err) {
        err = document.createElement("p"); err.className = "error"; err.id = field.id + "-error";
        wrap.appendChild(err);
      }
      err.textContent = msg;
      field.setAttribute("aria-invalid", "true");
      field.setAttribute("aria-describedby", err.id);
    } else {
      if (err) err.remove();
      field.removeAttribute("aria-invalid");
      field.removeAttribute("aria-describedby");
    }
  }
  var rules = {
    name: function (v) { return v.trim() ? "" : "Enter your name."; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? "" : "Enter a work email like name@company.com."; },
    message: function (v) { return v.trim().length >= 10 ? "" : "Tell us a little about what you need (10 characters or more)."; }
  };
  function validateField(f) { var r = rules[f.name]; if (!r) return true; var m = r(f.value); setError(f, m); return !m; }

  Object.keys(rules).forEach(function (n) {
    var f = form.elements[n];
    f.addEventListener("blur", function () { validateField(f); });
    f.addEventListener("input", function () { if (f.getAttribute("aria-invalid")) validateField(f); });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var firstBad = null;
    Object.keys(rules).forEach(function (n) { var f = form.elements[n]; if (!validateField(f) && !firstBad) firstBad = f; });
    if (firstBad) { firstBad.focus(); return; }
    var v = function (n) { return form.elements[n] ? form.elements[n].value.trim() : ""; };
    var topicLabel = form.elements["topic"].selectedOptions[0].textContent;
    var first = v("name").split(" ")[0];
    var btn = form.querySelector("button[type=submit]"); btn.disabled = true;
    function done(msg) { btn.disabled = false; status.hidden = false; status.textContent = msg; status.focus(); }
    function viaMail() {
      var subject = "Enquiry: " + topicLabel + (v("company") ? " (" + v("company") + ")" : "");
      var body = v("message") + "\n\n— " + v("name") + (v("company") ? ", " + v("company") : "") + "\n" + v("email");
      done("Thanks, " + first + ". Your email app should open with the message ready to send. If it doesn't, write to " + TO + ".");
      window.location.href = "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    }
    var payload = { name: v("name"), email: v("email"), company: v("company"), topic: form.elements["topic"].value, message: v("message"), website: v("website") };
    var ctl = window.AbortController ? new AbortController() : null, t = setTimeout(function () { if (ctl) ctl.abort(); }, 10000);
    fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctl ? ctl.signal : undefined })
      .then(function (r) {
        clearTimeout(t);
        if (r.ok) { form.reset(); done("Thanks, " + first + ". Your message is with us, and a person will reply to " + payload.email + "."); if (window.VIP && VIP.track) VIP.track("contact_submit", { topic: payload.topic }); }
        else if (r.status === 422 || r.status === 429) done(r.status === 429 ? "Too many messages from this connection. Please try again later or write to " + TO + "." : "Please check your details and try again.");
        else viaMail();
      })
      .catch(function () { clearTimeout(t); viaMail(); });
  });
})();

(function () {
  var url = (window.VIP_CONFIG || {}).booking, box = document.querySelector("[data-booking]");
  if (!box || !url) return;
  var a = box.querySelector("a"); a.href = url; box.classList.add("is-on");
})();
