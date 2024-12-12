import { useState } from 'react';
import { Form as RouterForm, Outlet, useNavigate } from 'react-router-dom';
import { Button, Link } from '@centml/ui';
import { SETTINGS_ROUTES } from '@routes/routes.paths';
import { createColumnHelper } from '@tanstack/react-table';
import Table from '@components/Table';
import TablePagination from '@components/Table/TablePagination';

// deleting  single item isn't liked for urls due to the url being part of the route - should change to a param or on the request body
const columnHelper = createColumnHelper<string[]>();
const columns = [
	columnHelper.accessor((row) => row, { id: 'filename', header: 'Filename' }),
	columnHelper.display({
		id: 'delete',
		cell: ({ row }) => {
			return (
				<RouterForm className="flex justify-end" method="delete">
					<Button type="submit" className="border-none" outlined variant="destructive" name="file" value={row.original.toString()}>
						Delete
					</Button>
				</RouterForm>
			);
		}
	})
];

interface ConnectedProps {
	documents: string[];
	isLoading?: boolean;
	variant?: 'document' | 'url';
}

const Connected = ({ documents, isLoading, variant = 'document' }: ConnectedProps) => {
	const [page, setPage] = useState(0);
	const [rows, setRows] = useState(10);
	const navigate = useNavigate();

	if (isLoading) {
		return (
			<div className="my-4">
				<Table columns={columns} isLoading data={[]} />
			</div>
		);
	}

	return (
		<>
			<div className="my-4">
				<Table
					columns={columns}
					data={documents}
					isSortable
					emptyState={<p className="text-sm dark:text-white">No {variant === 'document' ? 'documents uploaded' : 'web resources scraped'}</p>}
				/>
				<TablePagination
					currentPage={page}
					handlePageChange={(page) => setPage(page)}
					handleRowsChange={(rows) => setRows(rows)}
					hideRowControls
					rows={rows}
					totalPages={Math.ceil(documents.length / rows)}
					totalRows={documents.length}
				/>
			</div>

			<div className="flex justify-end">
				<Link variant="destructive" onPress={() => navigate(`${SETTINGS_ROUTES.DELETE_ALL}?type=${variant}`)}>
					Delete all
				</Link>
			</div>

			<Outlet />
		</>
	);
};

export default Connected;
