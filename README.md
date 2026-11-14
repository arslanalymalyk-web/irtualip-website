# Virtual IP website

Plain HTML/CSS/JS, no build step to run the site. Open `index.html` or serve the folder (`python3 -m http.server`).

- `tools/build.py` + `tools/build2.py` generate the HTML pages; `tools/visuals.py` draws the SVG visuals. Run `python3 tools/build2.py`.
- Motion is vendored as a trimmed bundle in `assets/js/vendor/motion.lite.js`.
- Case studies, team, roles and articles are sample content and must be replaced before launch.
- The contact form opens the visitor's email app (mailto). Add a backend to send directly.

To add Motion's skills to your AI agent, run `npx motion-ai` in a terminal from this folder.

## Ponytail (active in this project)

Claude Code hooks in `.claude/settings.json` load Ponytail's "lazy senior dev" mode at session start, track `/ponytail lite|full|ultra|off`, and pass the mode to subagents. The scripts live in `.claude/ponytail/` and need `node` on your PATH. They run from `$CLAUDE_PROJECT_DIR`, so no plugin install is needed. The six skills are in `.claude/skills/ponytail*`.

Not included: the task-board band and webhook ledger. Those ship only with the plugin (`/plugin install ponytail@ponytail`, marketplace already registered). Do not install the plugin too, or the hooks run twice.

The scripts keep their mode flag and a statusline script copy in `~/.claude/`.

## Brand

`brand/` holds the Virtual IP logo pack (SVG, PNG, favicon, social avatars, `brand-sheet.pdf`). The site itself still uses the earlier green and gold mark; the logo uses midnight #0A1330 and electric blue #2F6BFF. Generator scripts are in `brand/source/` (need `fonttools`, `brotli`, `pillow`, `rsvg-convert`).

## Launch settings

- **Contact form**: posts to `api/contact.js` (Vercel function) and sends through Resend. Set `RESEND_API_KEY` (required), `CONTACT_TO` and `CONTACT_FROM` (optional) in Vercel. Without a key the page falls back to the visitor's email app.
- **Analytics and booking**: edit `assets/js/config.js`. Analytics stays off, with no banner, until a provider and id are set; once on, it loads only after the visitor accepts.
- **Domain**: `SITE_URL=https://your-domain python3 tools/build2.py` rebuilds canonical URLs, sitemap and share tags.
- **Checks**: `npm test` (links, anchors, ids, meta, JSON-LD, sitemap). CI also fails if built HTML is stale.
- **Share image**: `PYTHONPATH=brand/source python3 brand/source/og.py` from `tools/`.
