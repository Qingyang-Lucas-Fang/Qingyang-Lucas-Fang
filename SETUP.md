# Put this on your GitHub profile

The profile is designed for **lucialuka**. All artwork is stored in this folder; the README has no required badge, chart, font, or animation service.

1. This repository is already connected to the **`lucialuka`** profile repository. GitHub displays its root README on your personal profile.
2. Keep the README, assets, stats script, and workflow together at the repository root. The local `preview/` folder and this setup guide are optional.
3. Open **Actions → Refresh profile statistics → Run workflow** to refresh the statistics immediately. Scheduled refreshes run at 00:17, 06:17, 12:17, and 18:17 UTC (08:17, 14:17, 20:17, and 02:17 Asia/Shanghai).

The workflow runs every six hours and on manual dispatch. It uses GitHub’s built-in token; **no personal access token is required**. It refreshes both SVGs and rotates the cache key in the README and local preview so GitHub and the preview fetch the latest image. Repository settings must allow Actions to write contents. Scheduled runs can be delayed; use **Actions → Refresh profile statistics → Run workflow** to refresh immediately.

The README uses the five artwork files `hero.svg`, `openassembler.svg`, `grand-tool.svg`, `activity-dark.svg`, and `activity-light.svg`.

## Preview before publishing

Open `preview/index.html` in a browser, or serve the project folder:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then visit **http://127.0.0.1:8765/preview/**. The preview includes light/dark controls and the same expandable sections as the README. It approximates GitHub’s layout; GitHub’s final typography and image caching can differ. The preview toolbar belongs only to the local preview.

The preview is a saved rendering. After editing the README, regenerate it with `python3 scripts/build_preview.py` (requires the `markdown-it-py` package), then reload the browser.

## Refresh the statistics locally

```bash
python3 scripts/update_stats.py
```

Python 3.10+ and an internet connection are enough. With no token, the script reads public GitHub REST endpoints and GitHub’s public contribution-calendar HTML. With `GH_TOKEN` set, it tries the GraphQL contribution API first. It never writes the token to an artifact or includes it in a URL.

- Repository totals and stars include **owned, public, non-fork repositories**, including archived repositories.
- The language bar aggregates GitHub’s reported source bytes for those repositories. It is not a skill rating or a measure of time spent coding.
- The calendar follows GitHub’s public contribution display. GitHub may include anonymized private activity if the account owner enables that display.
- The update timestamp is UTC. The checked-in panel remains visible even if a later API request or workflow fails.
- If contribution data cannot be retrieved, the panel explicitly shows it as unavailable. Repository statistics still update. Metadata and language API failures stop the refresh before either panel is replaced.
- Forks of this profile will inherit the original README, artwork, and links. The workflow reads the fork owner’s statistics; customize the rest of the profile before using it for another person.

## Customize the design

- **Text and links:** `README.md`.
- **Hero and project illustrations:** `scripts/generate_artwork.py`; run it to rebuild the three SVGs.
- **Activity panels:** `scripts/update_stats.py`.
- **Local preview:** `scripts/build_preview.py`.

The visual palette uses pale butter, lavender, sky blue, and coral with dark ink for contrast. The hero and project illustrations are light-first; activity panels have coordinated light and dark variants. SVG animation respects `prefers-reduced-motion`. The README uses GitHub-supported links, images, tables, anchors, `<picture>`, and native `<details>` disclosures. GitHub does not run arbitrary JavaScript or custom page CSS in a README.

## Sources and editorial choices

Profile details and contact links come from the supplied LinkedIn-export PDF. OpenAssembler v0.3.0 details and latest status were reviewed against its public repository on **8 November 2026**; the earlier compiler benchmark snapshot and other featured-project descriptions were checked against their source repositories on **2 November 2026**:

- [OpenAssembler README and results](https://github.com/lucialuka/OpenAssembler)
- [OpenAssembler status and measurement notes](https://github.com/lucialuka/OpenAssembler/blob/main/docs/STATUS.md)
- [OpenAssembler command reference](https://github.com/lucialuka/OpenAssembler/blob/main/docs/COMMANDS.md)
- [OpenAssembler research catalogue](https://github.com/lucialuka/OpenAssembler/tree/main/docs/research)
- [OpenAssembler frontend scope](https://github.com/lucialuka/OpenAssembler/blob/main/docs/FRONTENDS.md)
- [Grand Tool README](https://github.com/lucialuka/AI-Automated-UI-Design-Workflow-From-Prompt-to-Demo)
- The README files of the four linked additional projects.

Benchmark numbers are attributed to the project, rather than presented as independently rerun results. Trading backtest returns and Sharpe ratios were omitted. Research interests are described without inventing publication venues, degrees, or paper links. The original PDF is not included in the public profile package.
