import { Link } from '@centml/ui';
import { isRouteErrorResponse, useRouteError, useNavigate } from 'react-router-dom';
import { ROUTES } from '@routes/routes.paths';
import logo from '@assets/centml/logo.svg';
import invertedLogo from '@assets/centml/logo_inverted.svg';

export const ErrorBoundary = () => {
	const navigate = useNavigate();
	const error = useRouteError();

	if (error instanceof Error) console.error(error);

	return (
		<div className="flex h-screen flex-col items-center justify-center gap-2 bg-gray-100 dark:bg-neutral-900">
			<img src={logo} className="h-[59px] w-[160px] dark:hidden" alt="CentML logo" />
			<img src={invertedLogo} className="hidden h-[59px] w-[160px] dark:block" alt="CentML logo" />
			<div className="my-4 text-center">
				<h2 className="text-3xl font-semibold text-secondary-500 dark:text-secondary-400">Error</h2>
				<p className="text-error-500">
					{isRouteErrorResponse(error)
						? `${error.status} ${error.statusText}`
						: error instanceof Error
							? error.message
								? error.message
								: 'An unknown error has occurred'
							: ''}
				</p>
			</div>

			<Link onPress={() => navigate(ROUTES.DASHBOARD)} variant="primary">
				Home
			</Link>
		</div>
	);
};

export default ErrorBoundary;
