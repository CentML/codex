import {
	Await,
	defer,
	Form as RouterForm,
	LoaderFunctionArgs,
	redirect,
	useLoaderData,
	useNavigate,
	useParams,
	ActionFunctionArgs,
	useSearchParams,
	useNavigation,
	useActionData
} from 'react-router-dom';
import { Alert, Button, Drawer, Link, toast } from '@centml/ui';
import { QueryClient } from '@tanstack/react-query';
import { confluenceKeys, deleteSpaceDocument, getSpaceDocuments } from '@api/confluence/confluence';
import { deleteDocument } from '@api/documents/documents';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';
import { Suspense, useEffect, useState } from 'react';
import { createColumnHelper } from '@tanstack/react-table';
import { SpaceDocument } from '@api/confluence/types';
import Table from '@components/Table';

export const spaceAction =
	(queryClient: QueryClient) =>
	async ({ request, params }: ActionFunctionArgs) => {
		const { space } = params;
		const { intent } = Object.fromEntries(await request.formData());

		if (!space || !intent) return null;

		try {
			if (intent === 'delete-all') {
				await deleteDocument(space);
				await queryClient.invalidateQueries({ queryKey: confluenceKeys.all });
				return redirect(ROUTES.SETTINGS + '/' + SETTINGS_ROUTES.CONFLUENCE);
			} else {
				await deleteSpaceDocument(space, intent as string);
				await queryClient.invalidateQueries({ queryKey: confluenceKeys.connectedSpaceDocuments(space) });
				return { result: 'success' };
			}
		} catch (error) {
			console.error(error);
			toast('Could not delete document', { type: 'error' });
			return null;
		}
	};

export const spaceLoader =
	(queryClient: QueryClient) =>
	({ params }: LoaderFunctionArgs) => {
		const { space } = params;

		if (!space) return redirect(ROUTES.SETTINGS + '/' + SETTINGS_ROUTES.CONFLUENCE);

		const documents = queryClient.fetchQuery({ queryKey: confluenceKeys.connectedSpaceDocuments(space), queryFn: () => getSpaceDocuments(space) });

		return defer({ documents });
	};

const columnHelper = createColumnHelper<SpaceDocument>();
const columns = [
	columnHelper.accessor('title', { id: 'title', header: 'Title ', enableSorting: true }),
	columnHelper.accessor('count', {
		id: 'count',
		header: () => <div className="w-full text-center">Embeddings</div>,
		cell: (cell) => <p className="text-center">{cell.getValue()}</p>
	}),
	columnHelper.display({
		id: 'delete',
		cell: ({ row }) => {
			return <DeleteHelper spaceKey={row.original.title} />;
		}
	})
];

const DeleteHelper = ({ spaceKey }: { spaceKey: string }) => {
	const [showConfirmation, setShowConfirmation] = useState(false);
	const navigation = useNavigation();
	const actionData = useActionData() as undefined | { result: string };

	useEffect(() => {
		if (actionData?.result === 'success' && showConfirmation) setShowConfirmation(false);
	}, [actionData?.result]);

	if (showConfirmation) {
		return (
			<RouterForm method="post" className="flex items-center justify-end gap-3">
				<Button variant="secondary" outlined onPress={() => setShowConfirmation(false)} isDisabled={navigation.state === 'submitting'}>
					Cancel
				</Button>
				<Button variant="destructive" type="submit" name="intent" value={spaceKey} loading={navigation.state === 'submitting'}>
					Delete Permanently
				</Button>
			</RouterForm>
		);
	}

	return (
		<div className="flex justify-end">
			<Button className="border-none" variant="destructive" outlined onPress={() => setShowConfirmation(true)}>
				Delete
			</Button>
		</div>
	);
};

const ConfluenceSpace = () => {
	const [showConfirmation, setShowConfirmation] = useState(false);

	const { documents } = useLoaderData() as { documents: ReturnType<typeof spaceLoader> };
	const navigate = useNavigate();
	const navigation = useNavigation();
	const { space } = useParams();
	const [searchParams] = useSearchParams();

	return (
		<Drawer isOpen size="full" position="bottom" title="confluence space" hideTitle onOpenChange={() => navigate(-1)}>
			<div className="container mx-auto">
				<h2 className="my-4 text-2xl">
					{space} - {searchParams.get('name')}
				</h2>
				<hr />
				<div className="flex flex-col gap-2 py-4">
					<Suspense fallback={<Table isLoading columns={columns} />}>
						<Await resolve={documents}>
							{(documents) => {
								return <Table background="white" columns={columns} data={documents} isSortable />;
							}}
						</Await>
					</Suspense>

					{showConfirmation ? (
						<Alert showIcon variant="error" size="auto">
							<p>
								Are you sure you want to disconnect this space? All embedded documents will be removed, this action is permanent and cannot be undone.
							</p>
							<div className="mt-2 flex items-center gap-3">
								<Button variant="secondary" onPress={() => setShowConfirmation(false)} isDisabled={navigation.state === 'submitting'}>
									Cancel
								</Button>
								<RouterForm method="post">
									<Button variant="destructive" type="submit" name="intent" value="delete-all" loading={navigation.state === 'submitting'}>
										Confirm
									</Button>
								</RouterForm>
							</div>
						</Alert>
					) : (
						<div className="flex w-full items-center justify-between">
							<Link onPress={() => navigate(-1)} outlined variant="secondary">
								Back
							</Link>

							<Button variant="destructive" onPress={() => setShowConfirmation(true)}>
								Disconnect
							</Button>
						</div>
					)}
				</div>
			</div>
		</Drawer>
	);
};

export default ConfluenceSpace;
