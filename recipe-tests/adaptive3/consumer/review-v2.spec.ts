// Recipes-owned integration using unchanged published Cortex fixture infrastructure.
import { registerCell } from './helpers/cells';
import { fixtureGitTransport } from './helpers/gitTransport';
import { expect, type Page } from '@playwright/test';
import { test as base } from './helpers/nativeZoom';
import { spawn, execFileSync, type ChildProcess } from 'node:child_process';
import { mkdtempSync, mkdirSync, copyFileSync, cpSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { randomUUID } from 'node:crypto';
const reviewGoalPrompt='Keep saved drafts after a restart.';
const test = base.extend<{
  recipeFixture: string;
  recipeRun: {
    tenant: string;
    jobID: string;
    observer: Page;
    startWorker: (jobID?: string) => void;
    stopWorker: () => Promise<void>;
  };
}>({
  recipeFixture: ['browser-review-v2', { option: true }],
  recipeRun: async ({ page, context, request, recipeFixture }, use, testInfo) => {
    const review = recipeFixture !== 'browser-legacy-review';
    if (review) {
      // Match browsers serving Cortex over HTTP outside localhost.
      await context.addInitScript(() => Object.defineProperty(globalThis.crypto, 'randomUUID', { value: undefined }));
    }
    const tenant = `input-${randomUUID()}`;
    await registerCell(request, tenant);
    const jobID = `recipe-${randomUUID()}`;
    const repo = mkdtempSync(join(tmpdir(), 'cortex-input-'));
    const workerPath = resolve('../../build/c2j-test-worker');
    let worker: ChildProcess | undefined;
    let workerTimer: ReturnType<typeof setTimeout> | undefined;
    let workerStopped = true;
    let workerLog = '';
    let fixtureFailed = false;
    const errors: string[] = [];
    context.on('page', browserPage => browserPage.on('pageerror', error => errors.push(error.message)));
    page.on('pageerror', error => errors.push(error.message));

    const workerEnv = fixtureGitTransport(repo);
    const startWorker = (targetJobID = jobID) => {
      workerStopped = false;
      const launch = () => {
        worker = spawn(workerPath, [
          'run', 'one', '--job-id', targetJobID, '--input-mode', 'ops',
          '--poll-interval', '100ms', '--jobdb', `http://127.0.0.1:18082/${tenant}`,
        ], {
          cwd: repo,
          env: workerEnv,
          stdio: ['ignore', 'pipe', 'pipe'],
        });
        worker.stdout!.on('data', data => { workerLog += data.toString(); });
        worker.stderr!.on('data', data => { workerLog += data.toString(); });
        worker.on('error', error => { workerLog += error.stack; });
        worker.on('close', code => {
          workerLog += `\n[fixture] worker closed with ${code} (stopped=${workerStopped})\n`;
          // run one exits with 3 while awaiting external input. Continue polling
          // so browser answers and input deadlines resume the same job.
          if (!workerStopped && code === 3) workerTimer = setTimeout(launch, 500);
        });
      };
      launch();
    };
    const stopWorker = async () => {
      workerStopped = true;
      clearTimeout(workerTimer);
      if (!worker?.pid || worker.exitCode !== null || worker.signalCode !== null) return;
      const stopped = new Promise<void>(done => worker!.once('close', () => done()));
      worker.kill('SIGTERM');
      const timeout = setTimeout(() => worker?.kill('SIGKILL'), 5_000);
      await stopped;
      clearTimeout(timeout);
    };

    try {
      mkdirSync(join(repo, '.c2/recipes'), { recursive: true });
      copyFileSync(recipeFixture==='browser-legacy-review' ? resolve('tests/fixtures/recipes/browser-review.yaml') : recipeFixture==='browser-backstop' ? resolve(process.env.ADAPTIVE3_BROWSER_SOURCE!,'browser-backstop.yaml') : recipeFixture==='browser-review-workflow' ? resolve(process.env.ADAPTIVE3_BROWSER_SOURCE!,'browser-review-workflow.yaml') : resolve(process.env.ADAPTIVE3_BROWSER_FIXTURE!), join(repo, '.c2/recipes/browser-input.yaml'));
      copyFileSync(resolve(process.env.ADAPTIVE3_FORM_HELPER!), join(repo, '.c2/recipes/review-v2.yaml'));
      mkdirSync(join(repo,'recipes/review-v2'),{recursive:true});
      copyFileSync(resolve(process.env.ADAPTIVE3_REVIEW_SOURCE!,'review-v2/op.yaml'),join(repo,'recipes/review-v2/op.yaml'));
      copyFileSync(resolve(process.env.ADAPTIVE3_REVIEW_SOURCE!,'review-v2.py'),join(repo,'recipes/review-v2.py'));
      cpSync(resolve(process.env.ADAPTIVE3_REVIEW_SOURCE!,'adaptive3'),join(repo,'.c2/recipes/adaptive3'),{recursive:true});
      copyFileSync(resolve(process.env.ADAPTIVE3_BROWSER_SOURCE!,recipeFixture==='browser-backstop'?'scripted-backstop-agent.yaml':'scripted-agent.yaml'),join(repo,'.c2/recipes/adaptive3/agent.yaml'));
      copyFileSync(resolve('tests/fixtures/recipes/browser-document-producer.yaml'), join(repo, '.c2/recipes/producer.yaml'));
      const git = (...args: string[]) => execFileSync('git', ['-C', repo, ...args], { stdio: 'pipe' });
      git('init', '-b', 'main');
      git('add', '.c2', 'recipes');
      git('-c', 'user.name=Cortex Browser Test', '-c', 'user.email=browser@example.com', '-c', 'commit.gpgsign=false', 'commit', '-m', 'Input recipe fixture');
      const recipe = `git+${pathToFileURL(repo).href}//.c2/recipes/browser-input.yaml@main`;

      await page.goto(`/?tenantId=${tenant}`);
      await page.getByPlaceholder('Email address').fill('browser@example.com');
      await page.getByRole('button', { name: 'Continue', exact: true }).click();
      await expect(page.getByRole('heading', { name: 'Goals', exact: true })).toBeVisible();

      // This second tab must update through SSE, without refresh or navigation.
      const observer = await context.newPage();
      await observer.goto(`/project/${tenant}/reviews`);
      await expect(observer.getByText('No pending reviews')).toBeVisible();

      let externalDocument: unknown;
      {
        const producerID = `producer-${randomUUID()}`;
        const producer = await request.post(`/api/projects/${tenant}/jobs`, { data: { job_id: producerID, recipe: `git+${pathToFileURL(repo).href}//.c2/recipes/producer.yaml@main`, cell: 'platform', repo: 'github.com/cortex-test/platform' } });
        expect(producer.status(), await producer.text()).toBe(201);
        startWorker(producerID);
        await expect.poll(async () => {
          const result = await request.get(`/api/projects/${tenant}/jobs/${producerID}/outcome`);
          if (result.status() !== 200) return false;
          const body = await result.json(); externalDocument = body.output?.document; return !!externalDocument;
        }, { timeout: 90000 }).toBe(true);
        await stopWorker();

      }
      const submitted = await request.post(`/api/projects/${tenant}/jobs`, {
        data: { job_id: jobID, recipe, cell: 'platform', repo: 'github.com/cortex-test/platform', ...(review ? { inputs: { prompt: reviewGoalPrompt, external_document: externalDocument } } : {}) },
      });
      expect(submitted.status(), await submitted.text()).toBe(201);
      startWorker();

      // Check the backend separately so a broken persisted form reports its
      // HTTP error instead of looking like a browser/SSE visibility timeout.
      let pendingReadFailure: { status: number; body: unknown } | undefined;
      await expect.poll(async () => {
        if (pendingReadFailure) return pendingReadFailure;
        const response = await request.get(`/api/projects/${tenant}/user-inputs/pending`);
        const result = { status: response.status(), body: await response.json() };
        if (response.status() >= 500) {
          pendingReadFailure = result;
          await testInfo.attach('pending-input-error.json', {
            body: JSON.stringify(result, null, 2), contentType: 'application/json',
          });
        }
        return result;
      }, { timeout: 90_000, message: 'The worker must publish a readable pending input' }).toMatchObject({
        status: 200,
        body: expect.arrayContaining([expect.objectContaining({ id: jobID })]),
      });
      await expect(observer.getByText(`Job ID: ${jobID}`, { exact: true })).toBeVisible({ timeout: 90_000 });
      const otherTenant = await request.get(`/api/projects/other-${tenant}/user-inputs/pending`);
      expect(await otherTenant.json()).toEqual([]);

      await page.getByRole('button', { name: 'Refresh', exact: true }).click();
      await expect(page.getByRole('link', { name: new RegExp(`^Job ${jobID}:`) })).toBeVisible();
      await use({ tenant, jobID, observer, startWorker, stopWorker });
      expect(errors).toEqual([]);
    } catch (error) {
      fixtureFailed = true;
      throw error;
    } finally {
      await stopWorker();
      try {
        writeFileSync(testInfo.outputPath('c2j-worker.log'),workerLog);
        await testInfo.attach('c2j-worker.log', { body: workerLog, contentType: 'text/plain' });
        const outcome = await request.get(`/api/projects/${tenant}/jobs/${jobID}/outcome`);
        const outcomeBytes=await outcome.body();writeFileSync(testInfo.outputPath('recipe-outcome.json'),outcomeBytes);
        await testInfo.attach('recipe-outcome.json', { body: outcomeBytes, contentType: 'application/json' });
        if (fixtureFailed || testInfo.status !== testInfo.expectedStatus) {
          for (const [name, path] of [
            ['pending-inputs', 'user-inputs/pending'],
            ['input-details', `user-inputs/${jobID}`],
            ['job-metadata', `jobs/${jobID}`],
          ]) {
            try {
              const response = await request.get(`/api/projects/${tenant}/${path}`);
              await testInfo.attach(`${name}.json`, {
                body: JSON.stringify({ status: response.status(), body: await response.text() }, null, 2),
                contentType: 'application/json',
              });
            } catch (error) {
              // Diagnostics must preserve the original failure, including
              // when an expired input is gone or a server has stopped.
              await testInfo.attach(`${name}-error.txt`, {
                body: String(error), contentType: 'text/plain',
              });
            }
          }
        }
      } finally {
        rmSync(repo, { recursive: true, force: true });
      }
    }
  },
});


test.beforeEach(() => test.setTimeout(300_000));

test('generated forms preserve discussion, originals, uploads and native receipts through worker restarts', async ({page,request,recipeRun},info) => {
 const {tenant,jobID,stopWorker,startWorker}=recipeRun;
 await stopWorker();
 const base=`/api/projects/${tenant}`;
 await page.goto(`/project/${tenant}/reviews/${jobID}`);
 await expect(page.getByRole('radio',{name:/Approve direction/})).toBeVisible();
 const original=await (await request.get(`${base}/user-inputs/${jobID}`)).json();
 const originalForm=original.form;
 expect(originalForm.presentation.type).toBe('review/v2');
 expect(originalForm.kind).toBeUndefined();expect(originalForm.fields).toBeUndefined();
 expect(originalForm.request.documents['review/external.md'].stored.key.jobId).not.toBe(jobID);
 const post=async(response:any,extra:any={})=>page.request.post(`${base}/reviews/${jobID}/respond`,{multipart:{submission:JSON.stringify({request_id:originalForm.request_id,submission_id:randomUUID(),response,...extra})}});
 for(const extra of [{actor:{id:'forged'}},{receipt:{}},{conversation:[]}]) {
  const result=await post({direction:'question',feedback:'Why?',attachments:[],settings:{}},extra);expect(result.status()).toBe(400);
 }
 const forged=await post({direction:'question',feedback:'Why?',attachments:[{kind:'stored',stored:{key:{jobId:jobID,taskOrdinal:0,name:'forged.md',sizeBytes:1}}}],settings:{}});
 expect(forged.status()).toBe(400);
 for(const feedback of [' ', '\ufeff', 'approval with notes']) {
  const result=await post({direction:'accept',feedback,attachments:[],settings:{}});expect(result.status()).toBe(400);
 }
 const emptyFile=await page.request.post(`${base}/reviews/${jobID}/respond`,{multipart:{submission:JSON.stringify({request_id:originalForm.request_id,submission_id:randomUUID(),response:{direction:'accept',feedback:'',attachments:[],settings:{}}}),attachments:{name:'empty.md',mimeType:'text/markdown',buffer:Buffer.alloc(0)}}});
 expect(emptyFile.status()).toBe(400);
 await page.getByRole('radio',{name:/Ask a question/}).check();
 const exact='  What survives a restart?\n';
 await page.getByLabel('Question or requested change (required)',{exact:true}).fill(exact);
 await page.getByLabel('Attach notes',{exact:true}).setInputFiles([{name:'notes.md',mimeType:'text/markdown',buffer:Buffer.from('first note')}]);
 // Switching to approval retains drafts and blocks submission.
 await page.getByRole('radio',{name:/Approve direction/}).check();
 await expect(page.getByText(/This direction does not allow feedback/)).toBeVisible();
 await page.getByRole('radio',{name:/Ask a question/}).check();
 await expect(page.getByLabel('Question or requested change (required)',{exact:true})).toHaveValue(exact);
 const mutations:string[]=[];
 page.on('request',r=>{if(r.method()==='POST'&&r.url().endsWith(`/reviews/${jobID}/respond`))mutations.push(r.postData()??'');});
 await page.getByRole('button',{name:'Review settings',exact:true}).click();
 await page.getByRole('dialog').getByLabel('Fixture phrase',{exact:true}).fill('');
 await page.getByRole('dialog').getByRole('button',{name:'Done',exact:true}).click();
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await expect(page.getByRole('region',{name:'Confirm response'})).toHaveCount(0);
 expect(mutations).toHaveLength(0);
 // Invalid inapplicable edits stay local and do not block another direction.
 await page.getByRole('radio',{name:/Request changes/}).check();
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await expect(page.getByRole('region',{name:'Confirm response'})).toBeVisible();
 await page.getByRole('button',{name:'Back',exact:true}).click();
 await page.getByRole('radio',{name:/Ask a question/}).check();
 await page.getByRole('button',{name:'Review settings',exact:true}).click();
 await page.getByRole('dialog').getByLabel('Fixture phrase',{exact:true}).fill('changed by recipe');
 await expect(page.getByRole('dialog')).toHaveCSS('transform','none');
 await page.screenshot({path:info.outputPath('adaptive3-settings.png')});
 await page.getByRole('dialog').getByRole('button',{name:'Done',exact:true}).click();
 expect(mutations).toHaveLength(0);
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 const accepted=page.waitForResponse(r=>r.url().endsWith(`/reviews/${jobID}/respond`)&&r.request().method()==='POST');
 await page.getByRole('button',{name:'Confirm Ask a question',exact:true}).click();
 const first=await (await accepted).json();
 expect(first.response.feedback).toBe(exact);expect(first.receipt.request_id).toBe(originalForm.request_id);
 expect(first.response.settings).toEqual({fixture_phrase:'changed by recipe'});
 await expect(page.getByText('Waiting for the next turn',{exact:true})).toBeVisible();
 await page.reload();
 await expect(page.getByText('Waiting for the next turn',{exact:true})).toBeVisible();
 await expect(page.getByRole('region',{name:'Discussion'}).getByText(exact,{exact:true})).toHaveCount(1);
 await page.screenshot({path:info.outputPath('adaptive3-gap.png'),fullPage:true});
 startWorker();
 await expect(page.getByText('Saved drafts return when you reopen the app.',{exact:true})).toBeVisible({timeout:90000});
 await stopWorker();
 const next=await (await request.get(`${base}/user-inputs/${jobID}`)).json();
 expect(next.form.request.review_id).toBe(originalForm.request.review_id);
 expect(next.form.request_id).not.toBe(originalForm.request_id);
 expect(next.form.request.documents).toEqual(originalForm.request.documents);
 // A stale native occurrence cannot submit to its successor.
 expect((await post({direction:'accept',feedback:'',attachments:[],settings:{}})).status()).toBe(409);
 await page.getByRole('radio',{name:/Ask a question/}).check();
 await page.getByLabel('Question or requested change (required)',{exact:true}).fill('Do earlier notes survive?');
 await page.getByLabel('Attach notes',{exact:true}).setInputFiles([{name:'notes.md',mimeType:'text/markdown',buffer:Buffer.from('second note')}]);
 // Lose the success response deliberately. Reconciliation must not repost.
 const bodies:string[]=[];
 await page.route(`**${base}/reviews/${jobID}/respond`,async route=>{
  bodies.push(route.request().postData()??'');const result=await route.fetch();expect(result.status()).toBe(200);await route.abort('failed');
 });
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await page.getByRole('button',{name:'Confirm Ask a question',exact:true}).click();
 await expect(page.getByText('Waiting for the next turn',{exact:true})).toBeVisible();
 expect(bodies).toHaveLength(1);
 await page.unroute(`**${base}/reviews/${jobID}/respond`);
 startWorker();
 await expect(page.getByText('Earlier notes keep their original producer references.',{exact:true})).toBeVisible({timeout:90000});
 await stopWorker();
 await page.reload();
 const discussion=page.getByRole('region',{name:'Discussion'});
 await expect(discussion.getByRole('article')).toHaveCount(4);
 await expect(discussion.getByText(exact,{exact:true})).toHaveCount(1);
 await expect(discussion.getByText('Do earlier notes survive?',{exact:true})).toHaveCount(1);
 const downloads=discussion.getByRole('link',{name:'Download notes.md',exact:true});
 await expect(downloads).toHaveCount(2);
 expect(await (await request.get((await downloads.nth(0).getAttribute('href'))!)).text()).toBe('first note');
 expect(await (await request.get((await downloads.nth(1).getAttribute('href'))!)).text()).toBe('second note');
 await expect(page.getByRole('radio',{name:/Approve direction/})).toBeVisible();
 await page.screenshot({path:info.outputPath('adaptive3-discussion-desktop.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:info.outputPath('adaptive3-discussion-phone.png'),fullPage:true});
 await page.getByRole('radio',{name:/Approve direction/}).check();
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await page.getByRole('button',{name:'Confirm Approve direction',exact:true}).click();
 await expect(page.getByText('Response sent',{exact:true})).toBeVisible();
 startWorker();
 let outcome:any;
 await expect.poll(async()=>{const result=await request.get(`${base}/jobs/${jobID}/outcome`);if(result.status()!==200)return false;outcome=(await result.json()).output;return !!outcome?.final;},{timeout:90000}).toBe(true);
 expect(outcome.report).toBe('changed by recipe');
 expect(outcome.first.receipt).toEqual(first.receipt);
 expect(outcome.final.response.direction).toBe('accept');
 expect(outcome.second.response.attachments[0].stored.key).not.toEqual(outcome.first.response.attachments[0].stored.key);
 await info.attach('generated-outcome.json',{body:JSON.stringify(outcome,null,2),contentType:'application/json'});
});

test.describe.serial('unchanged adaptive3 discussion and correction routing',()=>{
 test.use({recipeFixture:'browser-review-workflow'});
 const controls:any[]=[];
 for(const restart of [false,true]) test(restart?'recorded restart matches uninterrupted control':'uninterrupted discussion control',async({page,request,recipeRun},info)=>{
  const {tenant,jobID,startWorker,stopWorker}=recipeRun;
  const api=`/api/projects/${tenant}`;
  const details=async()=>{const response=await request.get(`${api}/user-inputs/${jobID}`);return response.status()===200?(await response.json()).form:null;};
  await page.goto(`/project/${tenant}/reviews/${jobID}`);
  const approve = page.getByRole('button',{name:'Review before Complete',exact:true});
  const discussion = page.getByRole('region',{name:'Discussion'});
  const download = page.getByRole('region',{name:'Selected document'}).getByRole('link',{name:'Download',exact:true});
  await expect(approve).toBeVisible();
  await expect(download).toBeVisible();
  const originalDocument = new URL((await download.getAttribute('href'))!,page.url());
  // Reopen this retained occurrence against the latest job history.
  originalDocument.searchParams.delete('snapshot_token');
  const first=await details();const receipts:any[]=[];const points:any[]=[];
  expect(first.request.revision).toBe(1);
  await expect(page.getByRole('button',{name:'Revise',exact:true})).toHaveCount(1);
  expect(first.request.directions.map((d:any)=>d.label)).toEqual(['Revise','Review before Complete','Take to Completion']);
  await expect(page.getByRole('button',{name:'Take to Completion',exact:true})).toBeVisible();
  expect(Object.keys(first.request.document_metadata).sort()).toEqual(Object.keys(first.request.documents).sort());
  expect(first.request.overview_document_id).toBe('review/design.md');
  await page.getByRole('button',{name:'Show documents',exact:true}).click();
  const documentList=page.getByRole('navigation',{name:'Review documents'});
  await expect(documentList.getByText('Saved draft behavior',{exact:true})).toBeVisible();
  await expect(documentList.getByText('Read the original proposal before choosing a direction.',{exact:true})).toBeVisible();
  await expect(documentList.getByText('Independent draft evidence',{exact:true})).toBeVisible();
  await expect(documentList.locator('.review-document-entry').first()).toContainText('Saved draft behavior');
  if(!restart){
   await page.screenshot({path:info.outputPath('adaptive3-document-details-desktop.png'),fullPage:true});
   await page.setViewportSize({width:390,height:844});
   await expect(documentList.getByRole('button',{name:'Read Saved draft behavior',exact:true})).toBeVisible();
   await page.screenshot({path:info.outputPath('adaptive3-document-details-phone.png'),fullPage:true});
   await page.setViewportSize({width:1280,height:900});
  }
  const submit=async(form:any,direction:string,feedback:string,settings:any={},file?:string)=>{
   const response=await page.request.post(`${api}/reviews/${jobID}/respond`,{multipart:{submission:JSON.stringify({request_id:form.request_id,submission_id:randomUUID(),response:{direction,feedback,attachments:[],settings}}),...(file?{attachments:{name:'notes.md',mimeType:'text/markdown',buffer:Buffer.from(file)}}:{})}});
   expect(response.status(),await response.text()).toBe(200);const native=await response.json();receipts.push(native.receipt);return native;
  };
  let current=first;
  for(const [index,text] of ['First question?','Second question?'].entries()){
   if(restart)await stopWorker();
   const saved=await submit(current,'reply',text,{},index===0?'first note':'second note');
   expect(saved.response.attachments).toHaveLength(1);
   if(restart){await expect(discussion.getByText(text,{exact:true})).toBeVisible();await page.reload();await expect(discussion.getByText(text,{exact:true})).toHaveCount(1);startWorker();}
   let successor:any;
   await expect.poll(async()=>{successor=await details();return successor?.request_id!==current.request_id&&successor?.request?.conversation?.length===(index+1)*2;},{timeout:90000}).toBe(true);
   current=successor;
   expect(current.request.review_id).toBe(first.request.review_id);expect(current.request.documents).toEqual(first.request.documents);
   expect(current.request.revision).toBe(1);
   expect(current.request.document_metadata).toEqual(first.request.document_metadata);
   expect(current.request.overview_document_id).toBe(first.request.overview_document_id);
   expect(current.request.conversation[index*2].receipt).toEqual(saved.receipt);
   expect(current.request.conversation[index*2+1].text).toBe(index===0?'Actual first answer.':'Actual second answer.');
   if(restart){await stopWorker();await page.reload();await expect(page.getByText(current.request.conversation[index*2+1].text,{exact:true})).toBeVisible();startWorker();}
   points.push({turns:current.request.conversation.map((t:any)=>({role:t.role,text:t.text,direction:t.direction,files:t.attachments.map((f:any)=>f.stored.key.sizeBytes)})),originals:Object.keys(current.request.documents).sort()});
  }
  await page.reload();await expect(discussion.getByText('Actual second answer.',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Revise',exact:true}).click();
  const editRequest='Please clarify restoration in the direction document.';
  let correction:any;
  if(restart){
   await page.getByLabel('Comment (required)',{exact:true}).fill('UNSENT PREVIOUS REVIEW');
   await page.getByLabel('Attach notes',{exact:true}).setInputFiles([{name:'unsent.md',mimeType:'text/markdown',buffer:Buffer.from('unsent draft')}]);
   await stopWorker();
   // A contribution from another tab refreshes this saved draft while history is down.
   await page.route(`**${api}/jobs/${jobID}/conversation?*`,route=>route.fulfill({status:503,body:JSON.stringify({error:'History temporarily unavailable'})}));
   correction=await submit(current,'reply','',{},editRequest);
   await expect(page.getByText('Review state unavailable',{exact:true})).toBeVisible();
   await expect(page.getByText('Actual second answer.',{exact:true})).toBeVisible();
   await expect(approve).toBeHidden();
   await page.unroute(`**${api}/jobs/${jobID}/conversation?*`);
   await page.getByRole('button',{name:'Refresh',exact:true}).click();
   startWorker();
  }else{
   await expect(page.getByLabel('Comment (required)',{exact:true})).toHaveValue('');
   await page.getByLabel('Attach notes',{exact:true}).setInputFiles([{name:'notes.md',mimeType:'text/markdown',buffer:Buffer.from(editRequest)}]);
   const sent=page.waitForResponse(r=>r.url().endsWith(`/reviews/${jobID}/respond`)&&r.request().method()==='POST');
   await page.getByRole('button',{name:'Send · Revise',exact:true}).click();
   const response=await sent;
   expect(response.status()).toBe(200);
   correction=await response.json();
  }
  let revised:any;
  await expect.poll(async()=>{revised=await details();return revised?.request?.revision;},{timeout:90000}).toBe(2);
  expect(revised.request_id).not.toBe(current.request_id);
  expect(revised.request.review_id).toBe(first.request.review_id);
  expect(revised.request.documents['review/design.md'].stored.key).not.toEqual(first.request.documents['review/design.md'].stored.key);
  const stale=await page.request.post(`${api}/reviews/${jobID}/respond`,{multipart:{submission:JSON.stringify({request_id:current.request_id,submission_id:randomUUID(),response:{direction:'accept',feedback:'',attachments:[],settings:{}}})}});
  expect(stale.status()).toBe(409);
  await page.goto(`/project/${tenant}/reviews/${jobID}`);
  await expect(approve).toBeVisible();
  await expect(page.getByRole('heading',{name:'Revised saved drafts · v2',exact:true})).toBeVisible();
  for(const turn of revised.request.conversation.filter((t:any)=>t.text)) await expect(discussion.getByText(turn.text,{exact:true})).toHaveCount(1);
  await expect(page.getByText('Revised original after explicit correction.',{exact:true})).toBeVisible();
  expect(await (await page.request.get(originalDocument.href)).text()).toContain('Original bytes 日本語.');
  expect(await (await page.request.get((await download.getAttribute('href'))!)).text()).toContain('Revised original after explicit correction.');
  expect(revised.request.settings[0].value).toBe('auto');
  expect(revised.request.conversation.slice(0,4)).toEqual(current.request.conversation);
  expect(revised.request.conversation[4]).toMatchObject({revision:1,text:'',receipt:correction.receipt});
  expect(revised.request.conversation[4].attachments).toHaveLength(1);
  expect(revised.request.conversation.some((turn:any)=>turn.text==='UNSENT PREVIOUS REVIEW')).toBe(false);
  await expect(page.getByText('unsent.md (12 bytes)',{exact:true})).toHaveCount(0);
  await submit(revised,'reply','Do the original notes still apply?');
  await expect(discussion.getByText('Both original notes are available with the revised plan.',{exact:true})).toBeVisible({timeout:90000});
  const afterQuestion=await details();
  expect(afterQuestion.request.review_id).toBe(first.request.review_id);
  expect(afterQuestion.request.revision).toBe(2);
  expect(afterQuestion.request.conversation.slice(-2).map((turn:any)=>turn.revision)).toEqual([2,2]);
  expect(afterQuestion.request.documents).toEqual(revised.request.documents);
  await approve.click();
  const approvalComment = restart ? 'The revised plan covers the restart case.' : '';
  const comment = page.getByLabel('Comment (optional)',{exact:true});
  await expect(comment).toHaveValue('');
  if (approvalComment) await comment.fill(approvalComment);
  const accepted = page.waitForResponse(r=>r.url().endsWith(`/reviews/${jobID}/respond`)&&r.request().method()==='POST');
  await page.getByRole('button',{name:'Send · Review before Complete',exact:true}).click();
  const final = await (await accepted).json();
  expect(final.receipt.request_id).toBe(afterQuestion.request_id);
  let outcome:any;
  await expect.poll(async()=>{const result=await request.get(`${api}/jobs/${jobID}/outcome`);if(result.status()!==200)return false;outcome=(await result.json()).output;return !!outcome?.revised;},{timeout:90000}).toBe(true);
  expect(outcome.original.human.receipt).toEqual(correction.receipt);expect(outcome.revised.receipt).toEqual(final.receipt);
  expect(outcome.revised.reviewed_documents).toEqual(revised.request.documents);
  expect(outcome.revised.conversation.at(-1)).toMatchObject({direction:'accept',text:approvalComment,revision:2,receipt:final.receipt});
  expect(outcome.original.conversation.filter((t:any)=>t.direction==='reply')).toHaveLength(3);
  expect(outcome.original.conversation.some((t:any)=>t.direction==='accept')).toBe(false);
  const normalized={points,correction:outcome.original.stage,approved:outcome.revised.status,uploads:outcome.original.conversation.flatMap((t:any)=>t.attachments.map((f:any)=>f.stored.key.sizeBytes))};
  if(restart)expect(normalized).toEqual(controls[0]);else controls.push(normalized);
  writeFileSync(info.outputPath('restart-comparison.json'),JSON.stringify({restart,normalized,receipts,outcome},null,2));
  await info.attach('restart-comparison.json',{body:JSON.stringify({restart,normalized,receipts,outcome},null,2),contentType:'application/json'});
  await page.reload();await expect(page.getByText('Waiting for the next turn',{exact:true})).toHaveCount(0);
 });
});


test.describe('frozen legacy review control',()=>{
 test.use({recipeFixture:'browser-legacy-review'});
 test('saved original remains readable after reload',async({page,recipeRun},info)=>{
  await page.goto(`/project/${recipeRun.tenant}/reviews/${recipeRun.jobID}`);
  await expect(page.getByText('Immutable original',{exact:true})).toBeVisible();
  await page.reload();
  await expect(page.getByText('Immutable original',{exact:true})).toBeVisible();
  await page.screenshot({path:info.outputPath('adaptive3-legacy.png'),fullPage:true});
 });
});


test.describe('Backstop recovery', () => {
 test.use({recipeFixture:'browser-backstop'});
 test('native report and instructions keep the correction in this job', async ({page,request,recipeRun},info) => {
  const {tenant,jobID}=recipeRun;
  await page.goto(`/project/${tenant}/reviews/${jobID}`);
  await expect(page.getByRole('button',{name:'Revise',exact:true})).toBeVisible();
  await expect(page.getByRole('heading',{name:'What needs your decision',exact:true})).toBeVisible();
  const report=page.getByRole('article',{name:'Rendered document'});
  await expect(report.locator('blockquote, pre')).toHaveCount(0);
  await expect(report.locator('ol > li')).toHaveCount(3);
  await expect(report.locator('ol > li').first()).toContainText('Then rerun phone validation.');
  const initial=await (await request.get(`/api/projects/${tenant}/user-inputs/${jobID}`)).json();
  expect(initial.form.request.documents['review/backstop-report.md'].kind).toBe('stored');
  expect(initial.form.request.overview_document_id).toBe('review/backstop-report.md');
  await page.setViewportSize({width:1280,height:2000});
  await page.screenshot({path:info.outputPath('backstop-report.png'),fullPage:true});
  await page.setViewportSize({width:1280,height:900});
  await page.getByRole('button',{name:'Revise',exact:true}).click();
  await page.getByLabel('Comment (required)',{exact:true}).fill('Remove only the phone acceptance criterion. Keep browser validation.');
  await page.getByRole('button',{name:'Review settings',exact:true}).click();
  const dialog=page.getByRole('dialog');
  await expect(dialog.getByLabel('Return to',{exact:true})).toBeVisible();
  await expect(dialog.getByLabel('Return to',{exact:true}).locator('option')).toHaveText(['Choose a value','Auto','configure','direction','preparation','implementation']);
  await dialog.getByLabel('Return to',{exact:true}).selectOption({label:'direction'});
  await page.screenshot({path:info.outputPath('backstop-return-settings.png')});
  await dialog.getByRole('button',{name:'Done',exact:true}).click();
  await page.getByRole('button',{name:'Send · Revise',exact:true}).click();
  await expect.poll(async()=>{
   const r=await request.get(`/api/projects/${tenant}/jobs/${jobID}/outcome`);
   return r.status()===200?(await r.json()).output?.result?.stage:null;
  },{timeout:90000}).toBe('direction');
  const outcome=await (await request.get(`/api/projects/${tenant}/jobs/${jobID}/outcome`)).json();
  expect(outcome.output.result.amendment.human.receipt.submission_id).toBeTruthy();
  expect(outcome.output.result.amendment.human.response.feedback).toBe('Remove only the phone acceptance criterion. Keep browser validation.');
 });
});
