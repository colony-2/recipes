const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(process.argv[2], 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
function setup(fetch) {
  const elements = Object.fromEntries(['text', 'status', 'note', 'open', 'save'].map(id => [id, {value: '', textContent: ''}]));
  vm.runInNewContext(source, {document: {querySelector: selector => elements[selector.slice(1)]}, fetch});
  return elements;
}
const response = (text, version) => ({ok: true, json: async () => ({text, version})});
(async () => {
  {
    const ui = setup(async path => response(path.endsWith('/a') ? 'Saved A' : 'Saved B', 1));
    ui.note.value = 'a'; await ui.open.onclick(); ui.text.value = 'Unfinished A';
    ui.note.value = 'b'; await ui.open.onclick();
    assert.equal(ui.text.value, 'Saved B');
    console.log('REPRODUCED: opening B replaces unfinished A; no save is requested.');
  }
  {
    let saved;
    const ui = setup(async (path, options) => {if (options) saved = {path, body: JSON.parse(options.body)}; return response('Saved A', 1);});
    ui.note.value = 'a'; await ui.open.onclick(); ui.text.value = 'Edited A';
    ui.note.value = 'b'; await ui.save.onclick();
    assert.equal(saved.path, '/drafts/b'); assert.equal(saved.body.text, 'Edited A');
    console.log('REPRODUCED: editing destination field to B sends A text to /drafts/b.');
  }
  {
    let finish;
    const ui = setup(async (path, options) => options ? new Promise(resolve => {finish = resolve;}) : response('Saved A', 1));
    ui.note.value = 'a'; await ui.open.onclick(); ui.text.value = 'First edit';
    const saving = ui.save.onclick(); ui.text.value = 'Newer unsaved edit';
    finish(response('First edit', 2)); await saving;
    assert.equal(ui.status.textContent, 'Saved'); assert.equal(ui.text.value, 'Newer unsaved edit');
    console.log('REPRODUCED: response for earlier text displays Saved while newer text remains unsaved.');
  }
  console.log('Checks exercised the unchanged inline script with a stub DOM and mocked fetch; no browser or live storage was used.');
})().catch(error => { console.error(error); process.exitCode = 1; });
