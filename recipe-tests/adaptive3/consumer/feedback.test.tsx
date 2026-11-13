// Copied into a Cortex checkout by run.py; exercises its real adapter and renderer.
import { readFileSync } from 'node:fs';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import InputFormRenderer from './InputFormRenderer';
import { adaptInputFormConfig } from '../utils/formAdapter';

import { MemoryRouter, Routes, Route } from 'react-router-dom';
import InputDetailPage from './InputDetailPage';
import PendingInputsListPage from './PendingInputsListPage';
const page = vi.hoisted(() => ({ inputs: [] as any[], getDetails: vi.fn() }));
vi.mock('@colony2/shared', async () => {
  const actual = await vi.importActual<any>('@colony2/shared');
  return { ...actual,
    useInputActivity: () => ({ pendingInputs: page.inputs, currentProjectId: 'fixture', refresh: vi.fn(), setCurrentProjectId: vi.fn() }),
    inputActivityService: { ...actual.inputActivityService, getInputDetails: page.getDetails },
  };
});
vi.mock('./ReviewJobContext', () => ({ default: () => null }));
vi.mock('./ReviewDocuments', () => ({ default: ({ response }: any) => response }));
vi.mock('./AssistantContext', () => ({ useAssistantSource: () => undefined }));
const forms = JSON.parse(readFileSync(process.env.ADAPTIVE3_REVIEW_FORMS!, 'utf8'));
afterEach(cleanup);
describe('Adaptive3 native review forms', () => {
  it.each(forms.flatMap(config => ['question', 'revise'].map(choice => ({ config, choice, title: config.title }))))('$title / $choice supports feedback and attachments', async ({ config, choice }) => {
    const form = adaptInputFormConfig(config, 'adaptive3-consumer-test');
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    const { container } = render(<InputFormRenderer form={form} onSubmit={onSubmit} />);
    const action = form.fields.find(f => f.id === 'decision')!;
    const feedback = form.fields.find(f => f.id === 'feedback')!;
    const label = action.optionLabels![choice];
    await user.click(screen.getByRole('button', { name: label, exact: true }));
    const editor = screen.getByLabelText(feedback.label);
    expect(editor).toHaveFocus();
    await user.type(editor, 'Keep this local. Explain the remaining change.');
    const file = new File(['Human notes'], 'scope.md', { type: 'text/markdown' });
    await user.upload(container.querySelector('input[type=file]')!, file);
    await user.click(screen.getByRole('button', { name: 'Back', exact: true }));
    await user.click(screen.getByRole('button', { name: label, exact: true }));
    expect(screen.getByLabelText(feedback.label)).toHaveValue('Keep this local. Explain the remaining change.');
    expect(screen.getByText('scope.md')).toBeVisible();
    await user.click(screen.getByRole('button', { name: 'OK', exact: true }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({
      fields: { decision: choice, feedback: 'Keep this local. Explain the remaining change.' },
      attachments: { annotations: file },
    })));
  });
  it.each(forms)('$title identifies the requester in the queue and detail page', async config => {
    expect(config.title).toMatch(/^(Direction|Outcome review|Implementation|Preparation|Backstop) — /);
    expect(config.title.length).toBeLessThanOrEqual(120);
    page.inputs = [{ id: 'job', title: config.title, cell_name: 'notebook' }];
    const list = render(<MemoryRouter><PendingInputsListPage projectId="fixture" /></MemoryRouter>);
    expect(screen.getByText(config.title, { exact: true })).toBeVisible();
    list.unmount();
    page.getDetails.mockResolvedValue({ jobId: 'job', status: 'pending', startTime: '2026-11-13T08:00:00Z', form: config });
    render(<MemoryRouter initialEntries={['/reviews/job']}><Routes><Route path="/reviews/:jobId" element={<InputDetailPage projectId="fixture" />} /></Routes></MemoryRouter>);
    expect(await screen.findByRole('heading', { name: config.title, exact: true })).toBeVisible();
  });
  it.each(forms.filter(config => config.fields.some(field => field.id === 'model')))
  ('$title accepts model changes without a working agent', async config => {
    const form = adaptInputFormConfig(config, 'adaptive3-model-fallback');
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<InputFormRenderer form={form} onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(form.fields.find(f => f.id === 'model')!.label), 'chosen-model');
    await user.type(screen.getByLabelText(form.fields.find(f => f.id === 'reasoning_effort')!.label), 'high');
    const action = form.fields.find(f => f.id === 'decision')!;
    await user.click(screen.getByRole('button', { name: action.optionLabels!.continue, exact: true }));
    await user.click(screen.getByRole('button', { name: 'OK', exact: true }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({
      fields: { decision: 'continue', model: 'chosen-model', reasoning_effort: 'high' },
    })));
  });

});
