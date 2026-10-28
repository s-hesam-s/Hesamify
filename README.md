# Hesamify — Hosting Landing Page

An educational responsive hosting-company landing page built with HTML, CSS and small JavaScript interactions.

## Captured preview

<picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/screenshots/portfolio-poster.png" /><source type="image/webp" srcset="docs/screenshots/portfolio.webp" /><img src="docs/screenshots/portfolio.gif" width="100%" alt="Hesamify — actual captured UI states" /></picture>

Hosting landing-page hero and pricing layout. Educational UI; search and purchase controls do not provision hosting.

[Reproduce this capture and view the static image](docs/PORTFOLIO-PREVIEW.md) · [Mobile capture](docs/screenshots/portfolio-mobile.png)

## Included UI

- Hosting hero, domain-search layout, pricing cards and feature sections.
- Reusable component examples, testimonials, collapsible navigation and AOS animations.

## Repository map

| Path | Purpose |
|---|---|
| [index.html](index.html) | Full landing page |
| [Components](Components) | Individual component exercises |
| [CSS](CSS) | Stylesheets |
| [Js](Js) | Client-side behavior |
| [Images](Images) | Local visual assets |

## Preview locally

Use a modern browser and Python 3 for a simple loopback-only static server. From a terminal:

```powershell
git clone https://github.com/s-hesam-s/Hesamify.git
cd Hesamify
```

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/index.html`. Keep the terminal open while previewing and press Ctrl+C to stop it. No database or application backend is needed.

The checked-in HTML/CSS and local AOS assets can be previewed without installing npm packages. The unused Parcel 1 development dependency and its old transitive lock entries were removed. No package installation or build step is required to serve these source pages. The optional npm test command now invokes the real static/dependency checks and their regression tests; it requires Python 3.

## External resources

The pages reference resources from `fonts.googleapis.com`, `fonts.gstatic.com`. Internet access is needed for the referenced CDN scripts, fonts or remote images; the repository is not a fully offline asset bundle. Third-party resource availability can affect the preview.

## Verification and limitations

Check the navigation at narrow widths, pricing sections, component examples and scroll animations. The domain-search and pricing UI do not provision hosting or process payments.

An isolated Chromium regression suite checks selected real interactions at desktop and mobile widths; dependency-policy regressions run separately. Preview instructions are not a claim that every third-party widget is compatible with current CDN responses. Application services, persistent storage and deployment are outside this UI exercise.

## Project scope and reuse

This is an educational repository. The implementation notes describe the code in this repository; they do not claim a deployed commercial service or measured production results. Third-party libraries and assets retain their own terms. No project-wide license is currently declared.

## Continuous integration

GitHub Actions checks root HTML documents for a doctype, document shell, nonempty title and duplicate IDs. It also verifies local href/src/poster targets, filename casing and HTML/SVG fragments using `python3 scripts/check_site.py`. Remote URLs and placeholder `#` links are not fetched; this is not a full HTML5 conformance, accessibility or browser interaction test. The structural check requires no npm installation. The separate browser job installs development-only tooling; no backend or deployment is involved.

The [CI workflow](.github/workflows/ci.yml) runs for pull requests and pushes to `main`, and can be started manually. It uses read-only repository permissions and does not deploy the project.

## Runtime dependency checks

[Dependency inventory, local asset policy and verification commands](docs/FRONTEND-DEPENDENCIES.md) describe the exact runtime resources and CI guard.

## Maintenance checks

The existing CI also runs weekly on Monday and checks tracked Markdown file destinations with `scripts/check_doc_links.py`. Its negative tests cover moved documents, missing picture variants, paths outside the repository and untracked local drafts. External URLs and heading fragments are intentionally outside this offline file check. Scheduled runs do not deploy or start original application hosts.

Browser regressions: [test scope and local commands](docs/BROWSER-TESTS.md). Exact reviewed runtime versions are also checked against current GitHub advisories; CDN coverage and API failure cases are tested separately.
