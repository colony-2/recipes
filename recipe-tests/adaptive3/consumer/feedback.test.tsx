// Placed temporarily in a compatible Cortex checkout by run.py.
import { readFileSync } from 'node:fs';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { parseReviewV2, portablePattern, hasReviewFeedback, changedReviewSettings, reviewV2ContributionError, validateReviewScalar } from '@colony2/shared';
import InputDetailPage from './InputDetailPage';

const fixture = vi.hoisted(() => ({ form: null as any, getDetails: vi.fn() }));
vi.mock('@colony2/shared', async () => {
  const actual = await vi.importActual<any>('@colony2/shared');
  return { ...actual, inputActivityService: { ...actual.inputActivityService, getInputDetails: fixture.getDetails } };
});
vi.mock('../hooks/useReviewV2', () => ({ useReviewV2: () => ({
  view: { request: fixture.form.request, phase: 'actionable', current: { form: fixture.form }, conversation: fixture.form.request.conversation },
  error: '', busy: false, refresh: vi.fn(), sending: vi.fn(), accepted: vi.fn(), failed: vi.fn(),
}) }));
vi.mock('./ReviewDocuments', () => ({ default: ({ response }: any) => <div>Original documents retained by reference{response}</div> }));
vi.mock('./ReviewJobContext', () => ({ default: () => null }));
vi.mock('./AssistantContext', () => ({ useAssistantSource: () => undefined }));
const forms = JSON.parse(readFileSync(process.env.ADAPTIVE3_REVIEW_FORMS!, 'utf8'));
const vectors = JSON.parse(readFileSync(process.env.ADAPTIVE3_REVIEW_VECTORS!, 'utf8'));
afterEach(cleanup);
describe('actual helper-produced forms in published Cortex', () => {
  it.each(forms)('$title dispatches to the real v2 reader', async config => {
    expect(config.presentation).toEqual({ type: 'review/v2' });
    expect(config.kind).toBeUndefined(); expect(config.fields).toBeUndefined();
    const request = parseReviewV2(config.request);
    expect(request).toEqual(config.request); // no reconstructed refs or schemas
    fixture.form = { ...config, request_id: 'consumer-native' };
    fixture.getDetails.mockResolvedValue({ jobId: 'job', status: 'pending', startTime: 'now', form: fixture.form });
    render(<MemoryRouter initialEntries={['/reviews/job']}><Routes><Route path="/reviews/:jobId" element={<InputDetailPage projectId="fixture" />} /></Routes></MemoryRouter>);
    for (const d of request.directions) await waitFor(() => expect(screen.getByRole('radio', { name: new RegExp(d.label) })).toBeVisible());
    expect(screen.getByRole('region', { name: 'Discussion' })).toBeVisible();
    for (const turn of request.conversation.filter(t => t.text)) expect(screen.getByText(turn.text, { exact: true, normalizer: value => value })).toBeVisible();
    expect(screen.queryByRole('button', { name: 'Review settings', exact: true }) !== null).toBe(!!request.settings?.length);
    for (const d of request.directions) {
      if (d.feedback_mode === 'forbidden') {
        expect(reviewV2ContributionError(request, d, ' ', 0)).toBeTruthy();
        expect(reviewV2ContributionError(request, d, '', 1)).toBeTruthy();
        expect(reviewV2ContributionError(request, d, '', 0)).toBeUndefined();
      }
      if (d.feedback_mode === 'required') {
        expect(reviewV2ContributionError(request, d, '\ufeff', 0)).toBeTruthy();
        expect(reviewV2ContributionError(request, d, '日本語', 0)).toBeUndefined();
      }
    }
    expect(changedReviewSettings(request, 'accept', {})).toEqual({});
  });
  it('uses identical portable-pattern and Unicode feedback vectors', () => {
    for (const v of vectors.patterns) {
      if (!v.valid) expect(() => portablePattern(v.pattern), v.pattern).toThrow();
      else {
        const pattern = portablePattern(v.pattern);
        for (const [value, expected] of v.matches ?? []) expect(pattern.test(value)).toBe(expected);
      }
    }
    for (const v of vectors.feedback) expect(hasReviewFeedback(v.text)).toBe(v.meaningful);
    for (const v of vectors.scalars) expect(!validateReviewScalar(v.value, v.schema), JSON.stringify(v)).toBe(v.valid);
    for (const v of vectors.declarations) {
      const declaration = { ...forms[0].request, ...v.patch, ...(v.setting ? { settings: [v.setting] } : {}) };
      if (v.valid) expect(() => parseReviewV2(declaration)).not.toThrow();
      else expect(() => parseReviewV2(declaration), JSON.stringify(v)).toThrow();
    }
  });
});
