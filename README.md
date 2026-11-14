# Virtual IP website

Plain HTML/CSS/JS, no build step to run the site. Open `index.html` or serve the folder (`python3 -m http.server`).

- `tools/build.py` + `tools/build2.py` generate the HTML pages; `tools/visuals.py` draws the SVG visuals. Run `python3 tools/build2.py`.
- Motion is vendored as a trimmed bundle in `assets/js/vendor/motion.lite.js`.
- Case studies, team, roles and articles are sample content and must be replaced before launch.
- The contact form opens the visitor's email app (mailto). Add a backend to send directly.

To add Motion's skills to your AI agent, run `npx motion-ai` in a terminal from this folder.
