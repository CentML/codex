import { Suspense } from 'react';
import { v4 as uuid } from 'uuid';
import { Await, defer, useLoaderData, useNavigate } from 'react-router-dom';
import { QueryClient } from '@tanstack/react-query';
import { Alert, Card, Icon, Link } from '@centml/ui';
import { healthCheck, appKeys} from '@api/app/app';
import ChatControls from '@components/ChatControls';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';

export const healthLoader = (queryClient: QueryClient) => async () => {
	const health = queryClient.fetchQuery({
		queryKey: appKeys.health(),
		queryFn: ({ signal }) => healthCheck(signal)
	});

	return defer({ health });
};

function Home() {
	const { health } = useLoaderData() as { health: ReturnType<typeof healthLoader> };
	const navigate = useNavigate();

	const handleSubmit = (query: string) => {
		navigate({ pathname: uuid() }, { state: { query } });
	};

	return (
		<div className="flex flex-grow flex-col pr-2">
			<div className="flex flex-grow flex-col overflow-y-auto">
				<div className="flex flex-grow items-center justify-center">
					<Suspense>
						<Await
							resolve={health}
							errorElement={
								<div className="flex items-center justify-center">
									<Alert variant="error" className="flex justify-center">
										<div className="flex flex-col items-center justify-center gap-2 text-center">
											<p>Could not connect to your API URL. Please check your settings.</p>
											<Link variant="primary" onPress={() => navigate(ROUTES.SETTINGS + '/' + SETTINGS_ROUTES.APPLICATION)}>
												Settings
											</Link>
										</div>
									</Alert>
								</div>
							}
						>
							{({ status }) => {
								if (status !== 'healthy')
									return (
										<div className="flex items-center justify-center">
											<Alert size="md" variant="warning" className="flex justify-center">
												<p className="text-center">Backend API status: {status}</p>
											</Alert>
										</div>
									);
								return (
									<Card>
										<div className="flex flex-col items-center justify-center gap-2">
											<Icon icon="chat-bubble-left" aria-hidden />

											<p className="text-center text-lg">"Hello! What can I help you with? Ask me a question and I'll do my best to answer it."</p>
										</div>
									</Card>
								);
							}}
						</Await>
					</Suspense>
				</div>
			</div>

			<ChatControls handleSubmit={handleSubmit} />
		</div>
	);
}

export default Home;
