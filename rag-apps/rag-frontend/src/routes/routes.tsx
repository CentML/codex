import { lazy } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';
import { rootAction, rootLoader } from '@routes/layout-route';
import { healthLoader } from '@routes/Home/Home';
import Session, { sessionLoader } from '@routes/Session/Session';
import { documentsLoader, documentsAction } from '@routes/Settings/components/Documents';
import { webAction, webLoader } from '@routes/Settings/components/Web';
import { applicationLoader } from '@routes/Settings/components/Application';
import { deleteAllAction } from '@routes/Settings/components/DeleteAll';
import { confluenceAction } from '@routes/Settings/components/Confluence';
import { spaceAction, spaceLoader } from '@routes/Settings/components/ConfluenceSpace';

const ErrorBoundary = lazy(() => import('../ErrorBoundary'));
const LayoutRoute = lazy(() => import('@routes/layout-route'));
const Home = lazy(() => import('@routes/Home'));
const Settings = lazy(() => import('@routes/Settings'));
const DocumentsSettings = lazy(() => import('@routes/Settings/components/Documents'));
const WebSettings = lazy(() => import('@routes/Settings/components/Web'));
const DeleteAllDocuments = lazy(() => import('@routes/Settings/components/DeleteAll'));
const ConfluenceSettings = lazy(() => import('@routes/Settings/components/Confluence'));
const ApplicationSettings = lazy(() => import('@routes/Settings/components/Application'));
const ConfluenceSpace = lazy(() => import('@routes/Settings/components/ConfluenceSpace'));

const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			staleTime: 10 * (60 * 1000), // 10 mins
			gcTime: 15 * (60 * 1000) // 15 mins
		}
	}
});

export const Router = () => {
	const router = createBrowserRouter([
		{
			path: ROUTES.DASHBOARD,
			element: <LayoutRoute />,
			errorElement: <ErrorBoundary />,
			loader: rootLoader(queryClient),
			action: rootAction(queryClient),
			children: [
				{
					index: true,
					loader: healthLoader(queryClient),
					element: <Home />
				},
				{
					path: ROUTES.SESSION,
					element: <Session />, // do not lazy load to prevent flicker
					loader: sessionLoader(queryClient)
				},
				{
					path: ROUTES.SETTINGS,
					element: <Settings />,
					children: [
						{
							path: SETTINGS_ROUTES.DOCUMENTS,
							element: <DocumentsSettings />,
							loader: documentsLoader(queryClient),
							action: documentsAction(queryClient),
							children: [{ path: SETTINGS_ROUTES.DELETE_ALL, element: <DeleteAllDocuments />, action: deleteAllAction(queryClient) }]
						},
						{
							path: SETTINGS_ROUTES.WEB,
							element: <WebSettings />,
							loader: webLoader(queryClient),
							action: webAction(queryClient),
							children: [{ path: SETTINGS_ROUTES.DELETE_ALL, element: <DeleteAllDocuments />, action: deleteAllAction(queryClient) }]
						},
						{
							path: SETTINGS_ROUTES.CONFLUENCE,
							element: <ConfluenceSettings />,
							action: confluenceAction(queryClient),
							children: [
								{
									path: SETTINGS_ROUTES.CONFLUENCE_SPACE,
									element: <ConfluenceSpace />,
									action: spaceAction(queryClient),
									loader: spaceLoader(queryClient)
								}
							]
						},
						{
							path: SETTINGS_ROUTES.APPLICATION,
							element: <ApplicationSettings />,
							loader: applicationLoader
						}
					]
				}
			]
		}
	]);

	return (
		<QueryClientProvider client={queryClient}>
			<RouterProvider router={router} />
		</QueryClientProvider>
	);
};
