import { Outlet, ScrollRestoration, useNavigate, useHref, defer, ActionFunctionArgs, redirect } from 'react-router-dom';
import { RouterProvider, Toaster } from '@centml/ui';
import { QueryClient } from '@tanstack/react-query';
import { deleteSession, sessionKeys } from '@api/sessions/sessions';
import { documentKeys, getCurrentDocuments } from '@api/documents/documents';
import Layout from '@layout/Layout';
import { ROUTES } from './routes.paths';

export const rootAction =
	(queryClient: QueryClient) =>
	async ({ request, params }: ActionFunctionArgs) => {
		const { id } = Object.fromEntries(await request.formData());

		try {
			await deleteSession(id as string);
			await queryClient.invalidateQueries({ queryKey: sessionKeys.listSessions() });

			if (params.id === id) return redirect(ROUTES.DASHBOARD);
			return null;
		} catch (error) {
			console.error(error);
			return null;
		}
	};

export const rootLoader = (queryClient: QueryClient) => async () => {
	const documents = queryClient.fetchQuery({ queryKey: documentKeys.currentDocuments(), queryFn: () => getCurrentDocuments() });
	return defer({ documents });
};

const LayoutRoute = () => {
	const navigate = useNavigate();

	function useAbsoluteHref(path: string) {
		const relative = useHref(path);
		if (path.startsWith('https://') || path.startsWith('http://') || path.startsWith('mailto:')) {
			return path;
		}

		return relative;
	}

	return (
		<RouterProvider navigate={navigate} useHref={useAbsoluteHref}>
			<Layout>
				<Outlet />
			</Layout>
			<ScrollRestoration />
			<Toaster />
		</RouterProvider>
	);
};

export default LayoutRoute;
