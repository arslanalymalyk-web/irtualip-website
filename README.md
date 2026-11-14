# Virtual IP website

Plain HTML/CSS/JS, no build step to run the site. Open `index.html` or serve the folder (`python3 -m http.server`).

- `tools/build.py` + `tools/build2.py` generate the HTML pages; `tools/visuals.py` draws the SVG visuals. Run `python3 tools/build2.py`.
- Motion is vendored as a trimmed bundle in `assets/js/vendor/motion.lite.js`.
- Case studies, team, roles and articles are sample content and must be replaced before launch.
- The contact form opens the visitor's email app (mailto). Add a backend to send directly.

To add Motion's skills to your AI agent, run `npx motion-ai` in a terminal from this folder.

## Optional: Ponytail hooks

The six Ponytail skills are committed under `.claude/skills/`. Its lifecycle hooks (mode tracking, optional task ledger) ship only with the plugin and are not enabled here. This repo registers the Ponytail marketplace, so in Claude Code you can run:

```
/plugin install ponytail@ponytail
```

Review what the hooks do first: they run Node scripts each turn and write a usage log under `~/.config/ponytail/`. Installing the plugin as well as the committed skills duplicates them.
