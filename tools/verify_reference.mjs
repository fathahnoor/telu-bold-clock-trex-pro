// Read-only loader for the existing upstream ESM source. No package install.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root = process.argv[2];
const cache = new Map();
async function moduleAt(filename) {
  if (!path.extname(filename)) filename += '.js';
  if (cache.has(filename)) return cache.get(filename);
  const source = fs.readFileSync(filename, 'utf8');
  const m = filename.endsWith('.json')
    ? new vm.SyntheticModule(['default'], function () { this.setExport('default', JSON.parse(source)); }, {identifier: filename})
    : new vm.SourceTextModule(source, {identifier: filename});
  cache.set(filename, m);
  await m.link((specifier) => moduleAt(path.resolve(path.dirname(filename), specifier)));
  return m;
}
const parser = await moduleAt(path.join(root, 'src/watchFaceBinTools/watchFaceBinParser.js'));
await parser.evaluate();
const model = parser.namespace.getAvailableModels().find(m => m.id === 'amazfittrexpro');
const raw = fs.readFileSync('out/telu_trex_pro.bin');
const {parameters, images} = parser.namespace.parseWatchFaceBin(raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength), model.fileType);
const norm = value => Array.isArray(value) ? (value.length === 1 ? norm(value[0]) : value.map(norm)) : value && typeof value === 'object' ? Object.fromEntries(Object.entries(value).map(([k,v])=>[k,norm(v)])) : value;
assert.deepEqual(norm(parameters), norm(JSON.parse(fs.readFileSync('build/telu/firmware_params.json', 'utf8'))));
const srcCount = fs.readdirSync('build/telu').filter(f => /^[0-9]+\.png$/.test(f)).length;
assert.equal(images.length, srcCount + 1);
// Resolve by firmware ID, rather than simply comparing two copies of a JSON.
assert.equal(parameters.Background.ImageIndex, 1);
const previewId = parameters.Background.Preview.ImageRange.ImageIndex;
assert.deepEqual([images[previewId - 1].width, images[previewId - 1].height], [220, 220]);
assert.deepEqual([images[parameters.Background.ImageIndex - 1].width, images[parameters.Background.ImageIndex - 1].height], [360, 360]);
fs.mkdirSync('build/reference_current', {recursive:true});
for (const [i, im] of images.entries()) {
  fs.writeFileSync(`build/reference_current/${i}.rgba`, Buffer.from(im.pixels));
  fs.writeFileSync(`build/reference_current/${i}.json`, JSON.stringify([im.width, im.height]));
}
console.log(`Reference watchface-js: parameters identical, ${images.length} images decoded for T-Rex Pro.`);
