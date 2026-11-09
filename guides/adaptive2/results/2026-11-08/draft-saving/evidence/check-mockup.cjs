const {chromium} = require('/usr/local/lib/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const root = process.argv[2];
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/shai/.cache/ms-playwright/chromium-1228/chrome-linux/chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[], external=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
 await page.goto(pathToFileURL(path.join(root,'mockup.html')).href);
 assert.equal(await page.title(),'Notebook — proposed autosave and recovery');
 const original=await page.locator('#editor').inputValue();
 await page.screenshot({path:path.join(root,'evidence/mockup-saved.png'),fullPage:true});
 for(const [value,label] of Object.entries({saved:'Saved',pending:'Unsaved changes',saving:'Saving…',slow:'Still saving…',failed:"Couldn't save",uncertain:"Couldn't confirm save",conflict:'Conflict',near:'Unsaved changes',large:'Too large to save',loadfail:'Saved'})){
   await page.selectOption('#scenario',value);assert.equal(await page.locator('#badge').innerText(),label);
 }
 console.log('PASS: all 10 selectable scenario states render their expected labels.');
 await page.selectOption('#scenario','pending');
 await page.locator('#editor').fill('Draft A to preserve');
 await page.locator('#destination').fill('note-b');
 assert.equal(await page.locator('#active-id').innerText(),'field-notes');
 await page.click('#open');await page.locator('#switch-dialog').waitFor({state:'visible'});
 assert.equal(await page.locator('#editor').inputValue(),'Draft A to preserve');
 assert.equal(await page.locator('#stay').evaluate(el=>el===document.activeElement),true);
 for(let i=0;i<6;i++){await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.closest('dialog')!==null),true);}
 await page.keyboard.press('Escape');assert.equal(await page.locator('#switch-dialog').isVisible(),false);
 assert.equal(await page.locator('#open').evaluate(el=>el===document.activeElement),true);
 console.log('PASS: changing the navigation target retains active identity; dialog preserves text, traps keyboard focus, supports Escape and returns focus.');
 await page.click('#save');await page.locator('#editor').fill('Newer text while saving');
 await page.waitForFunction(()=>document.querySelector('#badge').textContent==='Unsaved changes');
 assert.equal(await page.locator('#editor').inputValue(),'Newer text while saving');
 console.log('PASS: simulated acknowledgement of earlier text does not label newer edits Saved or replace them.');
 await page.click('#open');await page.click('#save-open');await page.click('#stay');
 await page.waitForFunction(()=>document.querySelector('#badge').textContent==='Saved');
 assert.equal(await page.locator('#active-id').innerText(),'field-notes');
 console.log('PASS: canceling a switch prevents navigation after the simulated save finishes.');
 await page.locator('#editor').fill('Next revision');await page.click('#open');await page.click('#save-open');
 await page.waitForFunction(()=>document.querySelector('#active-id').textContent==='note-b');
 console.log('PASS: Save & open waits for simulated confirmation before changing the active note.');
 for(const value of ['failed','uncertain']){
  await page.selectOption('#scenario',value);const before=await page.locator('#editor').inputValue();
  await page.locator('#notice-actions button').first().click();
  await page.waitForFunction(()=>document.querySelector('#badge').textContent==='Saved');
  assert.equal(await page.locator('#editor').inputValue(),before);
 }
 console.log('PASS: failed/uncertain recovery simulations preserve current text.');
 await page.selectOption('#scenario','large');
 assert.equal(await page.locator('#save').isDisabled(),true);
 assert.equal(await page.locator('#editor').evaluate(el=>new TextEncoder().encode(el.value).length),65537);
 assert.match(await page.locator('#counter').innerText(),/1 over the limit/);
 const downloadEvent=page.waitForEvent('download');await page.click('#download');const download=await downloadEvent;
 const downloaded=fs.readFileSync(await download.path(),'utf8');assert.equal(Buffer.byteLength(downloaded),65537);
 assert.equal(downloaded,await page.locator('#editor').inputValue());
 assert.equal(await page.locator('#badge').innerText(),'Too large to save');
 await page.click('#open');assert.equal(await page.locator('#save-open').isDisabled(),true);await page.click('#stay');
 console.log('PASS: exact 65,537-byte draft is preserved; Save/switch are blocked; complete download does not mark Saved.');
 await page.selectOption('#scenario','conflict');
 const local=await page.locator('#editor').inputValue();
 await page.getByRole('button',{name:'Review differences',exact:true}).click();
 assert.equal(await page.locator('#local-copy').inputValue(),local);
 await page.click('#start-stored');
 assert.equal(await page.locator('#editor').inputValue(),local);assert.equal(await page.locator('#local-copy').inputValue(),local);
 assert.equal(await page.locator('#reviewed').inputValue(),await page.locator('#stored-copy').inputValue());
 const reviewed=await page.locator('#reviewed').inputValue();
 await page.click('#back');await page.getByRole('button',{name:'Review differences',exact:true}).click();
 assert.equal(await page.locator('#reviewed').inputValue(),reviewed);
 assert.equal(await page.locator('#local-copy').inputValue(),local);
 await page.screenshot({path:path.join(root,'evidence/mockup-conflict.png'),fullPage:true});
 await page.click('#save-reviewed');assert.equal(await page.locator('#badge').innerText(),'Saved');
 assert.equal(await page.locator('#local-copy').inputValue(),local);
 console.log('PASS: comparison uses a separate draft; choosing stored text leaves the original untouched; reopening comparison retains the reviewed draft; explicit reviewed-save simulation retains original for recovery.');
 await page.selectOption('#scenario','loadfail');assert.equal(await page.locator('#editor').inputValue(),original);assert.equal(await page.locator('#active-id').innerText(),'field-notes');
 console.log('PASS: target-load failure scenario retains the current editor.');
 const semantics=await page.evaluate(()=>({
   duplicateIds:[...document.querySelectorAll('[id]')].map(el=>el.id).filter((id,i,all)=>all.indexOf(id)!==i),
   unlabeled:[...document.querySelectorAll('input,textarea,select')].filter(el=>!el.labels?.length&&!el.getAttribute('aria-label')).map(el=>el.id),
   status:document.querySelector('#save-status').getAttribute('role'),
   externalAssets:[...document.querySelectorAll('[src],link[href]')].map(el=>el.getAttribute('src')||el.getAttribute('href'))
 }));
 assert.deepEqual(semantics.duplicateIds,[]);assert.deepEqual(semantics.unlabeled,[]);assert.equal(semantics.status,'status');assert.deepEqual(semantics.externalAssets,[]);
 await page.setViewportSize({width:390,height:844});await page.selectOption('#scenario','uncertain');
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
 await page.screenshot({path:path.join(root,'evidence/mockup-mobile.png'),fullPage:true});
 await page.selectOption('#scenario','conflict');await page.getByRole('button',{name:'Review differences',exact:true}).click();
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
 console.log('PASS: labeled inputs, unique IDs, live status, and narrow-screen layout checks; comparison stacks without horizontal page overflow at 390 px.');
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
 assert.equal(await page.evaluate(()=>localStorage.length+sessionStorage.length),0);
 console.log('PASS: no browser script errors, HTTP requests, external assets, or local/session storage writes.');
 console.log('LIMIT: this checks a scripted proposal, not autosave implementation, a real API, all browsers, or screen-reader conformance.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
