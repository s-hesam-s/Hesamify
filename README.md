# Hesamify — Hosting Landing Page

An educational responsive hosting-company landing page built with HTML, CSS and small JavaScript interactions.

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

The checked-in HTML/CSS can be previewed without installing npm packages. package.json contains legacy Parcel 1 tooling and package-lock.json; no start or build npm script is defined. The npm test script is an intentional failing placeholder, not a test suite. If you need the legacy bundler, use the locked dependency setup in a compatible Node environment; that tooling is not required for the static preview.

## External resources

The pages reference resources from `fonts.googleapis.com`, `fonts.gstatic.com`, `unpkg.com`. Internet access is needed for the referenced CDN scripts, fonts or remote images; the repository is not a fully offline asset bundle. Third-party resource availability can affect the preview.

## Verification and limitations

Check the navigation at narrow widths, pricing sections, component examples and scroll animations. The domain-search and pricing UI do not provision hosting or process payments.

No automated behavior-test suite is included. Preview instructions are not a claim that every third-party widget is compatible with current CDN responses. Application services, persistent storage and deployment are outside this UI exercise.

## Project scope and reuse

This is an educational repository. The implementation notes describe the code in this repository; they do not claim a deployed commercial service or measured production results. Third-party libraries and assets retain their own terms. No project-wide license is currently declared.
