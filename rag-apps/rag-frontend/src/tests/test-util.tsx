import { PropsWithChildren } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render } from '@testing-library/react';
import type { RenderOptions } from '@testing-library/react';

const queryClient = new QueryClient();

export function renderWithProviders(ui: React.ReactElement, renderOptions?: RenderOptions) {
	const Wrapper = ({ children }: PropsWithChildren) => {
		return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
	};

	return render(ui, { wrapper: Wrapper, ...renderOptions });
}
