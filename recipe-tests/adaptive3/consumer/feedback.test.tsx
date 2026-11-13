// Copied into a Cortex checkout by run.py; exercises its real adapter and renderer.
import { readFileSync } from 'node:fs';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import InputFormRenderer from './InputFormRenderer';
import { adaptInputFormConfig } from '../utils/formAdapter';

const forms = JSON.parse(readFileSync(process.env.ADAPTIVE3_REVIEW_FORMS!, 'utf8'));
afterEach(cleanup);
describe('Adaptive3 native review forms', () => {
  it.each(forms)('$title supports feedback, attachments and returning to the choice', async config => {
    const form = adaptInputFormConfig(config, 'adaptive3-consumer-test');
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    const { container } = render(<InputFormRenderer form={form} onSubmit={onSubmit} />);
    const action = form.fields.find(f => f.id === 'decision')!;
    const feedback = form.fields.find(f => f.id === 'feedback')!;
    const label = action.optionLabels!.revise;
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
      fields: { decision: 'revise', feedback: 'Keep this local. Explain the remaining change.' },
      attachments: { annotations: file },
    })));
  });
});
