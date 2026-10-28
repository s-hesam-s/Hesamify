# Browser regression checks

Development-only Playwright 1.64.1 checks use a loopback static server, synthetic text and a fresh browser context. They do not log in, save application data, or contact payment/cloud providers. Existing CDN assets still need network access.

```sh
npm ci --ignore-scripts
npx playwright install chromium
npm run test:browser
```

CI runs desktop and 390px mobile projects on Chromium. Structural/dependency tests remain separate. No original application host is involved.
