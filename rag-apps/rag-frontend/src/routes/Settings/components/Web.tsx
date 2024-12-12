import { Suspense, useState } from 'react';
import { ActionFunctionArgs, Await, defer, Form as RouterForm, useLoaderData } from 'react-router-dom';
import { QueryClient } from '@tanstack/react-query';
import { Alert, Button, IconButton, TextInput, toast, Tooltip } from '@centml/ui';
import { documentKeys, getCurrentDocuments, connectUrls, deleteDocument } from '@api/documents/documents';
import Connected from './Connected';

export const webLoader = (queryClient: QueryClient) => () => {
	const connectedUrls = queryClient.fetchQuery({
		queryKey: documentKeys.documentsByType('url'),
		queryFn: () => getCurrentDocuments('url')
	});

	return defer({ connectedUrls });
};

export const webAction =
	(queryClient: QueryClient) =>
	async ({ request }: ActionFunctionArgs) => {
		if (request.method === 'DELETE') {
			const { file } = Object.fromEntries(await request.formData());

			try {
				await deleteDocument(file as string);
				await queryClient.invalidateQueries({ queryKey: documentKeys.currentDocuments() });
			} catch (error) {
				toast('Could not remove web resource.', { type: 'error' });
				console.error(error);
			} finally {
				return null;
			}
		}

		if (request.method === 'POST') {
			const data = Object.fromEntries(await request.formData());

			try {
				await connectUrls(Object.values(data) as string[]);
				await queryClient.invalidateQueries({ queryKey: documentKeys.documentsByType('url') });
			} catch (error) {
				console.error(error);
				toast('Could not connect web resources.', { type: 'error' });
			} finally {
				return null;
			}
		}
	};

const Web = () => {
	const [urls, setUrls] = useState(['']);
	const { connectedUrls } = useLoaderData() as { connectedUrls: ReturnType<typeof webLoader> };

	return (
		<div className="py-4">
			<div>
				<RouterForm className="flex flex-col gap-4" method="post">
					<div>
						<p className="mb-2 dark:text-white">Connect web pages to your database</p>
						<ul className="flex flex-col gap-0.5">
							{urls.map((url, i) => (
								<li className="flex items-center gap-1" key={i}>
									<TextInput
										className="flex-grow"
										label="URL"
										labelHidden={i > 0}
										type="url"
										name={`url-${i}`}
										placeholder="https://www.atlassian.com/"
										value={url}
										onChange={(url) => setUrls((prev) => prev.map((p, j) => (j === i ? url : p)))}
									/>
									{urls.length > 1 && (
										<IconButton
											className={i === 0 ? 'mt-5' : ''}
											icon="x-mark"
											label="remove"
											onPress={() => setUrls((prev) => prev.filter((_, j) => i !== j))}
											squared
										/>
									)}
								</li>
							))}
							<div className="mt-1 flex justify-end">
								<Tooltip tip="Add URL">
									<IconButton icon="plus" label="add url" onPress={() => setUrls((prev) => [...prev, ''])} squared />
								</Tooltip>
							</div>
						</ul>
					</div>

					<div className="flex justify-end">
						<Button type="submit">Submit</Button>
					</div>
				</RouterForm>
			</div>

			<Suspense fallback={<Connected documents={[]} isLoading />}>
				<Await
					resolve={connectedUrls}
					errorElement={
						<Alert showIcon className="mt-4" variant="error">
							Could not get documents
						</Alert>
					}
				>
					{(connectedUrls) => <Connected documents={connectedUrls} variant="url" />}
				</Await>
			</Suspense>
		</div>
	);
};

export default Web;
