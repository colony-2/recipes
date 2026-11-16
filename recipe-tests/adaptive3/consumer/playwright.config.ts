import { defineConfig } from '@playwright/test';
import original from './playwright.config';
export default defineConfig({
 ...original,
 testMatch: 'adaptive3-review-v2.spec.ts',
 projects: [{name:'production',testMatch:'adaptive3-review-v2.spec.ts',use:{baseURL:'http://127.0.0.1:18083'}}],
 webServer: (original.webServer as any[]).filter(s=>s.port===18082||s.url==='http://127.0.0.1:18083/api/health').map(s=>s.port===18082?s:{...s,command:'exec ./build/cortex serve --addr 127.0.0.1:18083 --working-dir web/app/tests/fixtures/cell'}),
});
