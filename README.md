# Qingyang Fang · Engineering across layers

A personal portfolio for Qingyang (Lucas) Fang, a hardware–software co-design engineer. Built with HTML, CSS, JavaScript, and SVG. No framework, build step, third-party scripts, or API keys.

**Website:** https://qingyang-lucas-fang.github.io/ · **Repository:** https://github.com/Qingyang-Lucas-Fang/Qingyang-Lucas-Fang.github.io

## Explore

- An interactive, layered isometric processor with software/hardware views, pointer parallax, and a signal animation.
- Filterable project cards and keyboard-accessible case studies for **OpenAssembler** and **Grand Tool**.
- PTX / IR / SASS previews and a **clearly labeled simulated** prompt-to-demo walkthrough.
- Experience accordions, résumé download, email copying, and **⌘K / Ctrl+K** quick navigation.
- Responsive layouts, reduced-motion support, native dialog focus management, a skip link, and locally hosted fonts.

## Run locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. The production site is entirely static.

## Publish with GitHub Pages

This checkout is connected to the existing `Qingyang-Lucas-Fang/Qingyang-Lucas-Fang.github.io` repository.

1. Commit the website and push the `main` branch.
2. In the repository, open **Settings → Pages → Build and deployment**.
3. Set **Source** to **GitHub Actions**.
4. The included **Deploy portfolio to GitHub Pages** workflow publishes on pushes to `main`. After first enabling Pages, rerun the workflow if necessary.
5. Check the deployment URL in the workflow’s `github-pages` environment.

The workflow copies only public website files into `_site/`; documentation, Git history, and browser-test outputs are excluded from the deployment artifact. The public URL is live only after a successful deployment.

Alternatively, choose **Deploy from a branch**, `main`, `/(root)` in Pages settings. The `.nojekyll` file supports direct static publishing. Use one publishing method consistently.

See the [official GitHub Pages guide](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Edit the content

| File | Purpose |
| --- | --- |
| `index.html` | Profile, project cards, experience, contact, and hero SVG |
| `app.js` | Case study copy and interaction behavior |
| `styles.css` | Design tokens, layouts, motion, and responsive styles |
| `assets/Qingyang-Fang-Resume.pdf` | User-provided résumé |
| `assets/social-card.png` | Social-sharing preview |
| `assets/fonts/` | Local Manrope and DM Mono fonts and their OFL licenses |
| `.github/workflows/pages.yml` | GitHub Pages deployment |
| `docs/content-sources.md` | Factual sources and metric qualifications |

Update contact links in `index.html` and the email-copy handler in `app.js` together. When changing the domain, update the canonical URL, social metadata, `robots.txt`, and `sitemap.xml`.

## Content boundaries

Project capabilities and benchmarks come from the linked repositories, reviewed November 2, 2026. Benchmark numbers are **repository-reported**, with conditions and limitations in the case study; they were not independently rerun for this portfolio. The UI workflow preview uses preset content and makes no model/API calls. Résumé details come from the PDF supplied by the owner. No profile photograph, employer, degree, or hardware employment history was invented.

Fonts retain their SIL Open Font License notices. The résumé and personal material belong to their respective owner. Project source code is linked, not vendored.
