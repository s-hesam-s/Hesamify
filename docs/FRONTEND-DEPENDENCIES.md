# Frontend dependency policy

Runtime script and stylesheet URLs in root HTML pages are recorded in [frontend-dependencies.json](frontend-dependencies.json). Exact versions, existing SRI values and anonymous CORS are checked offline in CI. A new CDN resource or changed integrity requires an explicit manifest review. Google Fonts CSS is the only dynamic stylesheet exception; it cannot authorize scripts. Local runtime asset hashes use LF-normalized text bytes to remain stable across Git checkout line endings.

```powershell
python scripts/check_site.py
python scripts/check_dependencies.py
python -m unittest discover -s tests -p test_dependencies.py
```

This guard checks declared resources and local drift. It does not fetch external URLs in CI, recursively validate resources imported by CDN CSS, or certify the absence of vulnerabilities. Bootstrap 5.1.3, jQuery 3.6.0 and Slick 1.9.0 are retained where used; exact-version advisory lookup found no reviewed advisory for those selected versions on 2026-10-28. Browser and integration coverage remain separate from these static checks.

AOS 2.3.4 is served from `vendor/aos/`, with its MIT license. It replaces the floating `aos@next` CDN tag. The official npm tarball integrity was verified before extracting the two runtime files. Inter fonts still require Google Fonts connectivity.

The previous unused Parcel 1 development graph produced 93 npm audit findings (3 low, 52 moderate, 28 high, 10 critical) on 2026-10-28. Removing that build-only graph leaves no npm dependencies; this is removal of unused tooling, not a claim that 93 shipped runtime defects were fixed. The checked-in static pages and assets remain the serving inputs. npm test invokes the actual Python checks instead of the previous failing placeholder.

`npm run build` copies the two pages and their static asset directories into `dist/` using Node's standard library. `netlify.toml` explicitly selects this command and publish directory so deployment does not depend on an old dashboard build command or Parcel. CI also builds this artifact. No provider account settings are changed.
