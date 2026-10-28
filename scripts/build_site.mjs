import { cp, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const output = path.join(root, 'dist');
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
for (const entry of ['index.html', 'playground.html', 'Components', 'CSS', 'Images', 'Js', 'vendor']) {
  await cp(path.join(root, entry), path.join(output, entry), { recursive: true });
}
console.log('Static site copied to dist without bundling or runtime dependencies.');
