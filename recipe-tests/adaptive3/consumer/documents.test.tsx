// Copied into an isolated Cortex checkout. Metadata and document IDs come from native reports.
import { readFileSync } from 'node:fs';
import { transferableAbortController } from 'node:util';
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { inputActivityService } from '@colony2/shared';
import InputDetailPage from './InputDetailPage';

vi.mock('./ReviewJobContext', () => ({ default: () => null }));
vi.mock('./AssistantContext', () => ({ useAssistantSource: () => undefined }));
const forms = JSON.parse(readFileSync(process.env.ADAPTIVE3_REVIEW_FORMS!, 'utf8'));
const documentForms = forms.filter(config => Object.keys(config.documents || {}).length > 0);
const server = setupServer();
beforeAll(() => {
  // jsdom's AbortSignal belongs to a different realm from Node's native fetch.
  vi.stubGlobal('AbortController', transferableAbortController().constructor);
  server.listen({ onUnhandledRequest: 'error' });
});
afterEach(() => { cleanup(); server.resetHandlers(); inputActivityService.clearCaches(); });
afterAll(() => { server.close(); vi.unstubAllGlobals(); });

function requireCompleteDetails(config: any) {
  const ids = Object.keys(config.documents || {}).sort();
  expect(ids.length).toBeGreaterThan(0);
  expect(Object.keys(config.document_metadata || {}).sort()).toEqual(ids);
  for (const id of ids) {
    const detail = config.document_metadata[id];
    expect(detail.title.trim()).not.toBe('');
    expect(detail.description.trim()).not.toBe('');
    expect(['primary', 'supporting', 'diagnostic']).toContain(detail.role);
    expect(Number.isInteger(detail.order)).toBe(true);
  }
  expect(ids.filter(id => config.document_metadata[id].role === 'primary')).toEqual([config.overview_document_id]);
}

function roleOrder(config: any): string[] {
  const roles = { primary: 0, supporting: 1, diagnostic: 2 };
  return Object.keys(config.documents).sort((a, b) =>
    roles[config.document_metadata[a].role] - roles[config.document_metadata[b].role] ||
    config.document_metadata[a].order - config.document_metadata[b].order || Buffer.compare(Buffer.from(a), Buffer.from(b)));
}

describe('Adaptive3 generated document reviews through the actual reader', () => {
  it('has a generated document-bearing form and detects the producer omission independently of legacy fallback', () => {
    expect(documentForms.length).toBeGreaterThan(0);
    for (const config of documentForms) {
      requireCompleteDetails(config);
      const { document_metadata, ...missing } = config;
      expect(() => requireCompleteDetails(missing)).toThrow();
    }
  });

  it.each(documentForms.flatMap(config => [1280, 390].map(width => ({ config, width, title: config.title }))))
  ('$title displays explicit details at $width px and keeps feedback during navigation', async ({ config, width }) => {
    requireCompleteDetails(config);
    window.innerWidth = width;
    const fetched: string[] = [];
    let submissions = 0;
    server.use(
      http.get('http://localhost:8080/api/projects/fixture/user-inputs/producer-job', () => HttpResponse.json({
        jobId: 'producer-job', status: 'pending', startTime: '2026-11-13T08:00:00Z', form: config,
      })),
      http.get('http://localhost:8080/api/projects/fixture/reviews/producer-job/documents', ({ request }) => {
        const id = new URL(request.url).searchParams.get('document_id')!;
        expect(Object.keys(config.documents)).toContain(id);
        fetched.push(id);
        // The native fixture files remain test artifacts. Serve their selected identity through the HTTP reader boundary.
        return HttpResponse.text(`Selected attachment: ${id}`, { headers: { 'Content-Type': 'text/plain' } });
      }),
      http.post('http://localhost:8080/api/projects/fixture/reviews/producer-job/respond', () => {
        submissions++; return HttpResponse.json({});
      }),
    );
    const user = userEvent.setup();
    render(<MemoryRouter initialEntries={['/reviews/producer-job']}><Routes>
      <Route path="/reviews/:jobId" element={<InputDetailPage projectId="fixture" />} />
    </Routes></MemoryRouter>);
    const feedback = config.fields.find(field => field.id === 'feedback');
    const question = config.fields.find(field => field.id === 'decision').options.find(option => option.value === 'question');
    await user.click(await screen.findByRole('button', { name: question.label, exact: true }));
    const textbox = await screen.findByRole('textbox', { name: feedback.question });
    await user.type(textbox, 'Keep the draft while I read the evidence.');
    await user.click(screen.getByRole('button', { name: 'Show documents', exact: true }));
    const navigation = await screen.findByRole('navigation', { name: 'Review documents' });
    const expected = roleOrder(config);
    for (const id of expected) {
      const detail = config.document_metadata[id];
      expect(within(navigation).getByText(detail.title, { exact: true })).toBeVisible();
      expect(within(navigation).getByText(detail.description, { exact: true })).toBeVisible();
      expect(within(navigation).getAllByText(detail.role[0].toUpperCase() + detail.role.slice(1)).length).toBeGreaterThan(0);
    }
    await waitFor(() => expect(fetched[0]).toBe(config.overview_document_id));
    const supporting = expected.find(id => id !== config.overview_document_id);
    if (supporting) {
      const title = config.document_metadata[supporting].title;
      await user.click(within(navigation).getByRole('button', { name: width < 768 ? `Read ${title}` : new RegExp(title) }));
      await screen.findByText(`Selected attachment: ${supporting}`);
    }
    expect(textbox).toHaveValue('Keep the draft while I read the evidence.');
    expect(submissions).toBe(0);
    expect(Array.from(navigation.querySelectorAll('.review-document-entry')).map(el =>
      expected.find(id => el.textContent!.includes(id)))).toEqual(expected);
  });
});
