import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import ChatOutput from './ChatOutput';

const stream = {
	human: undefined,
	ai: undefined
};

describe('Chat output', () => {
	const scrollIntoViewMock = vi.fn();
	window.HTMLElement.prototype.scrollIntoView = scrollIntoViewMock;

	it('renders', () => {
		render(<ChatOutput session={undefined} stream={stream} />);

		expect(screen.getByText(/hello/i)).toBeDefined();
	});

	it('displays messages', () => {
		render(
			<ChatOutput
				session={{
					id: '123',
					chat: [
						{ human: 'what is love?', ai: 'baby dont hurt me' },
						{ human: 'whats love got to do with it?', ai: 'second hand emotion' }
					]
				}}
				stream={stream}
			/>
		);

		expect(screen.getAllByRole('listitem')).toHaveLength(2);
		expect(screen.getByText('what is love?')).toBeDefined();
		expect(screen.getByText('whats love got to do with it?')).toBeDefined();
	});

	it('displays stream answer', () => {
		render(<ChatOutput session={undefined} stream={{ human: 'sweet dreams', ai: 'are made of this' }} />);

		expect(screen.getByText('sweet dreams')).toBeDefined();
		expect(screen.getByText('are made of this')).toBeDefined();
	});
});
