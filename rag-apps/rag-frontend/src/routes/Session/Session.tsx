import { Suspense, useEffect, useRef, useState } from 'react';
import { Await, defer, LoaderFunctionArgs, useLoaderData, useLocation, useNavigate, useParams } from 'react-router-dom';
import { QueryClient, useQueryClient } from '@tanstack/react-query';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import { Alert, Skeleton, toast } from '@centml/ui';
import { getSession, getSessions, sessionKeys } from '@api/sessions/sessions';
import ChatOutput from '@components/ChatOutput';
import ChatControls from '@components/ChatControls';
import { JSONSession } from '@api/sessions/types';
import { ROUTES } from '@routes/routes.paths';

export const sessionLoader =
	(queryClient: QueryClient) =>
	async ({ params }: LoaderFunctionArgs) => {
		const { id } = params;

		const currentSessions = await queryClient.fetchQuery({ queryKey: sessionKeys.listSessions(), queryFn: getSessions });
		if (!currentSessions.find((session) => session.id === id)) {
			return { session: [] };
		}

		const session = queryClient.fetchQuery({
			queryKey: sessionKeys.session(id),
			queryFn: () => getSession(id as string)
		});

		return defer({ session });
	};

const DEFAULT_URL = import.meta.env.VITE_API_URL;
const API_URL = localStorage.getItem('api-url');

let controller = new AbortController();

export interface Stream {
	human: string | undefined;
	ai: string | undefined;
}

const Session = () => {
	const queryClient = useQueryClient();

	const [isLoading, setIsLoading] = useState(false);
	const [session, setSession] = useState<Stream[]>([]);
	const [stream, setStream] = useState<Stream>({ human: undefined, ai: undefined });

	const hasRun = useRef(false);

	const navigate = useNavigate();
	const location = useLocation();
	const { id } = useParams();
	const { session: history } = useLoaderData() as { session: ReturnType<typeof sessionLoader> };

	useEffect(() => {
		if (session.length) setSession([]);
	}, [id]);

	useEffect(() => {
		if (location.state && !hasRun.current) {
			const { query } = location.state;
			fetchStream(query);
			navigate(location.pathname, { replace: true, state: null });
		}

		hasRun.current = true;
	}, [location.state]);

	/** adds the response from the LLM into the current session */
	const handleSaveSession = (response: { human: string; ai: string }) => {
		setSession((prev) => [...prev, response]);
	};

	/** gets a streamed response from the LLM endpoint and displays streamed answer */
	const fetchStream = (query: string) => {
		let ai: string | undefined = undefined;
		setIsLoading(true);
		fetchEventSource(`${API_URL ? API_URL : DEFAULT_URL}/stream`, {
			openWhenHidden: true,
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ input: { input: query }, config: { configurable: { session_id: id } }, kwargs: {} }),
			signal: controller.signal,
			onerror: (error) => {
				console.error(error);
				toast('Something went wrong.', { type: 'error' });
				setIsLoading(false);
				setStream({ human: undefined, ai: undefined });

				if (!session.length) {
					navigate(ROUTES.DASHBOARD, { replace: true });
				}

				throw error;
			},
			onmessage: (e) => {
				if (e.event === 'data' && e.data.includes('answer')) {
					const parsed = JSON.parse(e.data);
					setIsLoading(false);

					setStream((prev) => {
						ai = prev.ai ?? '';
						ai += parsed.answer ?? '';

						return {
							human: query,
							ai
						};
					});
				}
			},
			onclose: async () => {
				const chatResponse = { human: query, ai: ai as string };
				handleSaveSession(chatResponse);
				setStream({ human: undefined, ai: undefined });
				await queryClient.invalidateQueries({ queryKey: sessionKeys.listSessions() });
			}
		});
	};

	const handleStop = () => {
		// save any current output
		if (stream.ai) {
			handleSaveSession({ human: stream.human as string, ai: stream.ai });
		}

		controller.abort();
		controller = new AbortController();
		setIsLoading(false);
		setStream({ human: undefined, ai: undefined });
	};

	return (
		<div className="flex flex-grow flex-col pr-2">
			<Suspense
				fallback={
					<div className="flex-grow">
						<Skeleton>
							<div className="flex flex-col gap-4">
								<div className="flex justify-end pl-20">
									<Skeleton.Text width="lg" />
								</div>
								<div className="flex justify-end pr-20">
									<Skeleton.Block />
								</div>
							</div>
						</Skeleton>
					</div>
				}
			>
				<Await resolve={history} errorElement={<Alert variant="error">Could not resolve your chat session.</Alert>}>
					{(history: JSONSession[]) => {
						const hist = history.reduce((acc, curr) => {
							if (curr.type === 'human') {
								return [...acc, { human: curr.data.content, ai: '' }];
							}

							if (curr.type === 'ai') {
								const lastInput = acc[acc.length - 1];
								if (!lastInput) return acc;

								lastInput.ai = curr.data.content;
								return [...acc.slice(0, -1), { ...lastInput, ai: curr.data.content }];
							}

							return acc;
						}, [] as Stream[]);

						return <ChatOutput session={[...hist, ...session]} stream={stream} />;
					}}
				</Await>
			</Suspense>
			<ChatControls
				handleStop={handleStop}
				handleSubmit={(query) => fetchStream(query)}
				isLoading={isLoading}
				isStreaming={!!stream.ai || !!stream.human}
			/>
		</div>
	);
};

export default Session;
