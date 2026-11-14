/* AI readiness check: six questions, one per dimension, scored 0-3.
   Produces a stage, a per-dimension profile and a pre-filled hand-off to the contact form. */
(function () {
  "use strict";
  var root = document.querySelector("[data-quiz]");
  if (!root) return;

  var DIMS = ["Use case", "Data", "Infrastructure", "People", "Governance", "Measurement"];
  var Q = [
    { d: 0, q: "How clearly defined is the first decision or workflow you want AI to improve?", o: [
      "We haven't picked one yet",
      "We have a long list and no priority",
      "We have one or two candidates, each with an owner",
      "One is scoped, with a business owner and a success metric"] },
    { d: 1, q: "How easy is it to get the data that use case needs?", o: [
      "It sits in spreadsheets, inboxes or systems nobody owns",
      "It exists, but pulling it is manual work every time",
      "Mostly in one place, with known quality gaps",
      "Governed, documented and available through pipelines or APIs"] },
    { d: 2, q: "Where would an AI system run today?", o: [
      "We have no cloud footprint",
      "Some workloads in the cloud, set up ad hoc",
      "A managed cloud environment with basic CI/CD",
      "A cloud platform with infrastructure as code, monitoring and cost controls"] },
    { d: 3, q: "Who would own the system after launch?", o: [
      "No one yet",
      "IT would absorb it alongside everything else",
      "A named product owner, with thin engineering support",
      "A product owner plus engineers or data staff with capacity"] },
    { d: 4, q: "What is your approach to AI and sensitive data?", o: [
      "We don't have one",
      "Informal guidance, with no review step",
      "A written policy, reviewed case by case",
      "A policy, a review process and an audit trail customers or regulators have seen"] },
    { d: 5, q: "How would you know the project worked?", o: [
      "We'd go by feel",
      "We'd compare before and after, loosely",
      "We have a baseline for today's process",
      "A baseline, a target and a dashboard that tracks both"] }
  ];
  var STAGES = [
    { max: 6, name: "Getting oriented", text: "You have appetite and some raw material. The fastest progress comes from choosing one use case and checking whether the data behind it is usable, before anyone writes a model.", next: "A short mapping workshop to pick the use case and test data readiness." },
    { max: 12, name: "Ready to prove it", text: "The basics are in place. You can test an idea on your own data and measure it against a baseline. The risk now is a pilot that never reaches production.", next: "A scoped proof of concept with a production path agreed up front." },
    { max: 18, name: "Ready to scale", text: "Your foundations are strong. The work is turning a working system into a dependable one: monitoring, cost control and a team that can run it.", next: "A production build with managed operations and a measurable target." }
  ];
  var FOCUS = [
    "Pick one use case and name its owner and metric.",
    "Make the data reachable and agree who owns its quality.",
    "Stand up a managed cloud baseline with monitoring.",
    "Name an owner and make sure they have engineering capacity.",
    "Write a short policy and add a review step before launch.",
    "Capture a baseline today so you can prove the change later."
  ];

  var step = 0, answers = [];
  var scoreMax = Q.length * 3;

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  function renderQuestion(focus) {
    var q = Q[step];
    root.textContent = "";
    var prog = el("div", "quiz__progress");
    prog.appendChild(el("span", null, "Question " + (step + 1) + " of " + Q.length));
    prog.appendChild(el("span", null, DIMS[q.d]));
    root.appendChild(prog);
    var track = el("div", "quiz__track"); track.setAttribute("aria-hidden", "true");
    var bar = el("i"); track.appendChild(bar); root.appendChild(track);
    requestAnimationFrame(function () { bar.style.width = ((step + (answers[step] != null ? 1 : 0)) / Q.length * 100) + "%"; });

    var fs = el("fieldset");
    var lg = el("legend", null, q.q); lg.tabIndex = -1; fs.appendChild(lg);
    var opts = el("div", "quiz__options");
    q.o.forEach(function (label, i) {
      var wrap = el("div", "quiz__option");
      var id = "q" + step + "o" + i;
      var inp = el("input"); inp.type = "radio"; inp.name = "q" + step; inp.id = id; inp.value = i;
      if (answers[step] === i) inp.checked = true;
      var lab = el("label", null, label); lab.setAttribute("for", id);
      inp.addEventListener("change", function () {
        answers[step] = i;
        next.disabled = false;
        bar.style.width = ((step + 1) / Q.length * 100) + "%";
      });
      wrap.appendChild(inp); wrap.appendChild(lab); opts.appendChild(wrap);
    });
    fs.appendChild(opts); root.appendChild(fs);

    var nav = el("div", "quiz__nav");
    var back = el("button", "btn btn--ghost btn--sm", "Back"); back.type = "button";
    back.disabled = step === 0; if (step === 0) back.style.visibility = "hidden";
    back.addEventListener("click", function () { step--; renderQuestion(true); });
    var next = el("button", "btn btn--sm", step === Q.length - 1 ? "See my result" : "Next"); next.type = "button";
    next.disabled = answers[step] == null;
    next.addEventListener("click", function () { if (step < Q.length - 1) { step++; renderQuestion(true); } else renderResult(); });
    nav.appendChild(back); nav.appendChild(next); root.appendChild(nav);
    if (focus) lg.focus({ preventScroll: true });
  }

  function renderResult() {
    var total = answers.reduce(function (a, b) { return a + b; }, 0);
    var stage = STAGES.filter(function (s) { return total <= s.max; })[0];
    var low = 0;
    answers.forEach(function (a, i) { if (a < answers[low]) low = i; });
    root.textContent = "";
    var res = el("div", "quiz__result"); res.setAttribute("tabindex", "-1");
    res.appendChild(el("p", "quiz__score", "Your readiness: " + total + " of " + scoreMax));
    res.appendChild(el("h3", "quiz__stage", stage.name));
    res.appendChild(el("p", null, stage.text));

    var dims = el("div", "dims");
    dims.setAttribute("role", "list");
    answers.forEach(function (a, i) {
      var row = el("div", "dim"); row.setAttribute("role", "listitem");
      row.appendChild(el("span", null, DIMS[Q[i].d]));
      var b = el("div", "dim__bar"); var f = el("i"); f.style.setProperty("--v", Math.round(a / 3 * 100)); f.style.setProperty("--n", i); b.appendChild(f);
      row.appendChild(b); row.appendChild(el("span", "dim__v", a + "/3")); dims.appendChild(row);
    });
    res.appendChild(dims);

    var focusText = answers[low] === 3 ? "Every area scored well. Keep your baseline current as the system grows." : "Start with " + DIMS[Q[low].d].toLowerCase() + ". " + FOCUS[Q[low].d];
    var p = el("p"); var strong = el("strong", null, "Where to start: "); p.appendChild(strong); p.appendChild(document.createTextNode(focusText)); res.appendChild(p);
    var p2 = el("p"); p2.appendChild(el("strong", null, "Suggested first step: ")); p2.appendChild(document.createTextNode(stage.next)); res.appendChild(p2);

    var qs = "topic=ai-roadmap&stage=" + encodeURIComponent(stage.name) + "&score=" + total + "&focus=" + encodeURIComponent(DIMS[Q[low].d]);
    var actions = el("div"); actions.style.cssText = "display:flex;flex-wrap:wrap;gap:.75rem";
    var cta = el("a", "btn", "Plan my AI roadmap"); cta.href = "contact.html?" + qs + "#contact-form";
    var again = el("button", "btn btn--ghost", "Retake the check"); again.type = "button";
    again.addEventListener("click", function () { step = 0; answers = []; renderQuestion(true); });
    actions.appendChild(cta); actions.appendChild(again); res.appendChild(actions);
    root.appendChild(res);
    res.focus({ preventScroll: true });
  }

  renderQuestion(false);
})();
