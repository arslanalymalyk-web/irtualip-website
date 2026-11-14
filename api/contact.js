// Vercel serverless function: receives the contact form and emails it through Resend.
// Env vars (Vercel project settings): RESEND_API_KEY (required), CONTACT_TO, CONTACT_FROM (optional).
// Without RESEND_API_KEY it answers 503 and the page falls back to the visitor's email app.
const hits = new Map(); // best-effort per-instance rate limit
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ error: "method" }); }
  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== "object") return res.status(400).json({ error: "body" });
  if (b.website) return res.status(200).json({ ok: true }); // honeypot: pretend success to bots

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  const now = Date.now(), recent = (hits.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
  if (recent.length >= 5) return res.status(429).json({ error: "rate" });
  hits.set(ip, [...recent, now]);

  const name = String(b.name || "").trim().slice(0, 120), email = String(b.email || "").trim().slice(0, 200);
  const company = String(b.company || "").trim().slice(0, 160), topic = String(b.topic || "other").trim().slice(0, 40);
  const message = String(b.message || "").trim().slice(0, 5000);
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || message.length < 10) return res.status(422).json({ error: "invalid" });

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(503).json({ error: "not_configured" });
  const to = (process.env.CONTACT_TO || "contact@virtualip.com").split(",").map((s) => s.trim());
  const from = process.env.CONTACT_FROM || "Virtual IP Website <onboarding@resend.dev>";
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({
        from, to, reply_to: email,
        subject: `Website enquiry: ${topic}${company ? " (" + company + ")" : ""}`,
        text: `${message}\n\n${name}${company ? ", " + company : ""}\n${email}\nTopic: ${topic}`,
        html: `<p>${esc(message).replace(/\n/g, "<br>")}</p><p><strong>${esc(name)}</strong>${company ? ", " + esc(company) : ""}<br>${esc(email)}<br>Topic: ${esc(topic)}</p>`,
      }),
    });
    if (!r.ok) return res.status(502).json({ error: "send" });
    return res.status(200).json({ ok: true });
  } catch {
    return res.status(502).json({ error: "send" });
  }
};
