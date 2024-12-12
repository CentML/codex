import { fireEvent, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '@tests/test-util';
import ChatControls from './ChatControls';

describe('Chat controls', () => {
	it('renders', () => {
		renderWithProviders(<ChatControls handleSubmit={vi.fn()} handleStop={vi.fn()} isLoading={false} isStreaming={false} />);

		expect(screen.getByRole('textbox')).toBeDefined();
		expect(screen.getByRole('button', { name: /submit/i })).toBeDefined();
	});

	it('can submit a query', () => {
		const mockSubmit = vi.fn();
		const QUERY = 'tell me a story';

		renderWithProviders(<ChatControls handleSubmit={mockSubmit} handleStop={vi.fn()} isLoading={false} isStreaming={false} />);

		fireEvent.click(screen.getByRole('button', { name: /submit/i }));
		expect(mockSubmit).not.toHaveBeenCalled();

		expect(screen.getByRole('dialog', { name: /validation error/i })).toBeDefined();
		fireEvent.click(screen.getAllByRole('button', { name: /dismiss/i })[0]);

		fireEvent.change(screen.getByRole('textbox'), { target: { value: QUERY } });
		fireEvent.click(screen.getByRole('button', { name: /submit/i }));
		expect(mockSubmit).toHaveBeenCalledWith(QUERY);
	});
});
