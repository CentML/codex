import { useEffect, useMemo, useState } from 'react';
import { ActionFunctionArgs, Outlet, redirect, Form as RouterForm, useNavigate, useNavigation } from 'react-router-dom';
import { Alert, Button, Link, LoadingSpinner, PasswordInput, SearchInput, TextInput, toast } from '@centml/ui';
import { QueryClient, useQuery } from '@tanstack/react-query';
import { createColumnHelper } from '@tanstack/react-table';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';
import { confluenceKeys, connectConfluenceSpaces, getConfluenceSpaces } from '@api/confluence/confluence';
import { Space } from '@api/confluence/types';
import Table from '@components/Table';
import TablePagination from '@components/Table/TablePagination';

const ATLASSIAN_KEY = 'atlassian-storage';
const CONFLUENCE_CREDENTIALS = localStorage.getItem(ATLASSIAN_KEY);

export const confluenceAction =
	(queryClient: QueryClient) =>
	async ({ request }: ActionFunctionArgs) => {
		const { base_url, username, api_key, intent, space } = Object.fromEntries(await request.formData());

		if (intent === 'add-credentials') {
			localStorage.setItem(ATLASSIAN_KEY, JSON.stringify({ base_url: (base_url as string).replace(/\/+$/, ''), username, api_key }));

			await queryClient.invalidateQueries({ queryKey: confluenceKeys.list() });
			return redirect(`${ROUTES.SETTINGS}/${SETTINGS_ROUTES.CONFLUENCE}`);
		}

		toast('Connecting space. This may take some time.', { type: 'info' });

		try {
			await connectConfluenceSpaces({
				base_url: base_url as string,
				username: username as string,
				api_key: api_key as string,
				space_keys: [space] as string[]
			});

			toast(`Connected to space: ${space}`, { type: 'success' });

			await queryClient.invalidateQueries({ queryKey: confluenceKeys.list() });
		} catch (error) {
			console.error(error);
			toast(`Could not connect to space: ${space}`, { type: 'error' });
		} finally {
			return null;
		}
	};

const columnHelper = createColumnHelper<Space>();
const columns = [
	columnHelper.accessor('key', { id: 'key', header: 'Space key', enableSorting: true }),
	columnHelper.accessor('name', { id: 'name', header: 'Space name', enableSorting: true }),
	columnHelper.display({
		id: 'connect',
		cell: ({ row }) => {
			const { base_url, username, api_key } = JSON.parse(CONFLUENCE_CREDENTIALS ?? '{}');

			if (row.original.isConnected) {
				return <TableLink spaceKey={row.original.key} name={row.original.name} />;
			}

			return (
				<RouterForm className="flex justify-end" method="post">
					<input type="hidden" name="base_url" value={base_url} />
					<input type="hidden" name="username" value={username} />
					<input type="hidden" name="api_key" value={api_key} />
					<Button
						type="submit"
						className="border-none"
						name="space"
						outlined={!row.original.isConnected}
						isDisabled={row.original.isConnected}
						value={row.original.key}
					>
						{row.original.isConnected ? 'Connected' : 'Connect'}
					</Button>
				</RouterForm>
			);
		}
	})
];

const TableLink = ({ spaceKey, name }: { spaceKey: string; name: string }) => {
	const navigate = useNavigate();

	return (
		<div className="flex justify-end">
			<Link onPress={() => navigate(`${spaceKey}?name=${encodeURI(name)}`)} variant="primary" className="inline border-none">
				View Space
			</Link>
		</div>
	);
};

// in order to provide a stable reference for the table data a loader function cannot be used
const Confluence = () => {
	const [page, setPage] = useState(0);
	const [rows, setRows] = useState(10);
	const [search, setSearch] = useState('');

	const navigation = useNavigation();

	const { base_url, username, api_key } = JSON.parse(CONFLUENCE_CREDENTIALS ?? '{}');

	const { data, isLoading, error } = useQuery({
		queryKey: confluenceKeys.list(),
		queryFn: () => getConfluenceSpaces({ base_url, username, api_key })
	});

	if (error) console.error(error);

	const tableData = useMemo(
		() => data?.filter(({ key, name }) => `${key} ${name}`.toLowerCase().includes(search.toLowerCase())) ?? [],
		[data, search]
	);

	return (
		<>
			<div className="flex flex-col gap-4 py-4">
				<p className="dark:text-white">Connect to your Confluence account by providing your URL, username, and API key</p>
				<Credentials />

				{isLoading && <Table isLoading columns={columns} />}

				{error && (
					<Alert variant="error" showIcon>
						Could not connect to your Confluence spaces
					</Alert>
				)}

				{data && (
					<div className="flex flex-col gap-1">
						<div className="flex items-center justify-between">
							<SearchInput label="search spaces by key" labelHidden placeholder="Search spaces" onChange={(s) => setSearch(s)} value={search} />
							{navigation.state === 'submitting' && <LoadingSpinner />}
						</div>

						<Table
							columns={columns}
							data={tableData}
							isPaginated
							isSortable
							pagination={{
								pageIndex: page,
								pageSize: rows
							}}
							emptyState={<p className="my-2 text-sm">No spaces available.</p>}
						/>
						<TablePagination
							currentPage={page}
							handlePageChange={(page) => setPage(page)}
							handleRowsChange={(rows) => setRows(rows)}
							rows={rows}
							totalPages={Math.ceil(tableData.length / rows)}
							totalRows={tableData.length}
						/>
					</div>
				)}
			</div>
			<Outlet />
		</>
	);
};

export default Confluence;

interface Credentials {
	base_url: string;
	username: string;
	api_key: string;
}

const Credentials = () => {
	const [credentials, setCredentials] = useState<Credentials>({ base_url: '', username: '', api_key: '' });

	useEffect(() => {
		if (CONFLUENCE_CREDENTIALS) {
			const parsedCredentials = JSON.parse(CONFLUENCE_CREDENTIALS);
			setCredentials(parsedCredentials);
		}
	}, []);

	return (
		<RouterForm className="flex flex-col gap-2" method="post">
			<div className="grid grid-cols-3 gap-3">
				<TextInput
					label="URL"
					name="base_url"
					onChange={(base_url) => setCredentials((prev) => ({ ...prev, base_url }))}
					value={credentials.base_url}
					type="url"
					isRequired
				/>
				<TextInput
					label="Username"
					name="username"
					onChange={(username) => setCredentials((prev) => ({ ...prev, username }))}
					value={credentials.username}
					isRequired
				/>
				<PasswordInput
					label="API Key"
					name="api_key"
					onChange={(api_key) => setCredentials((prev) => ({ ...prev, api_key }))}
					value={credentials.api_key}
					isRequired
				/>
			</div>

			<div className="flex justify-end">
				<Button type="submit" name="intent" value="add-credentials">
					Save
				</Button>
			</div>
		</RouterForm>
	);
};
