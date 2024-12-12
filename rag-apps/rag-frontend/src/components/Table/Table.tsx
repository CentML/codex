import {
	useReactTable,
	ColumnDef,
	getCoreRowModel,
	flexRender,
	RowSelectionState,
	Row,
	getSortedRowModel,
	getPaginationRowModel,
	PaginationState,
	OnChangeFn
} from '@tanstack/react-table';
import { useNavigate } from 'react-router-dom';
import { Icon, IconButton, Skeleton } from '@centml/ui';
import clsx from 'clsx';

interface CommonTableProps<T> {
	background?: 'white' | 'gray';
	// eslint-disable-next-line  @typescript-eslint/no-explicit-any
	columns: ColumnDef<T, any>[];
	columnOrder?: string[];
	getRowId?: (originalRow: T, index: number, parent?: Row<T> | undefined) => string;
	isSortable?: boolean;
	isPaginated?: boolean;
	pagination?: PaginationState;
	rowSelection?: RowSelectionState;
	setRowSelection?: OnChangeFn<RowSelectionState>;
}

interface DataTableProps<T> extends CommonTableProps<T> {
	data: T[];
	emptyState?: React.ReactNode;
	isLoading?: never;
}

interface LoadingTableProps<T> extends CommonTableProps<T> {
	data?: T[];
	emptyState?: never;
	isLoading: true;
}

type TableProps<T> = DataTableProps<T> | LoadingTableProps<T>;

const Table = <T,>({
	background = 'gray',
	columns,
	columnOrder,
	data = [],
	emptyState,
	getRowId,
	isSortable,
	isLoading,
	isPaginated,
	pagination,
	rowSelection,
	setRowSelection
}: TableProps<T>) => {
	const tableInstance = useReactTable({
		data,
		columns,
		getCoreRowModel: getCoreRowModel(),
		getPaginationRowModel: isPaginated ? getPaginationRowModel() : undefined,
		getSortedRowModel: isSortable ? getSortedRowModel() : undefined,
		getRowId,
		initialState: {
			columnOrder
		},
		onRowSelectionChange: setRowSelection,
		state: {
			pagination,
			rowSelection
		}
	});
	const isEmpty = data.length === 0;

	return (
		<table className={clsx('w-full', { 'h-full': isEmpty })}>
			<thead>
				{tableInstance.getHeaderGroups().map((headerGroup) => (
					<tr key={headerGroup.id} className="bg-gray-300 text-left text-sm dark:bg-neutral-700">
						{headerGroup.headers.map((header) => (
							<th
								key={header.id}
								onClick={header.column.getToggleSortingHandler()}
								className={clsx(
									'whitespace-nowrap px-3 py-1.5 font-normal first:rounded-l-md first:pl-2 first:pl-4 last:rounded-r-md dark:bg-neutral-700 dark:text-white',
									{ 'cursor-pointer hover:bg-gray-400/10 hover:dark:bg-neutral-800/30': header.column.getCanSort() && isSortable }
								)}
								title={
									header.column.getCanSort() && isSortable
										? header.column.getNextSortingOrder() === 'asc'
											? 'Sort ascending'
											: header.column.getNextSortingOrder() === 'desc'
												? 'Sort descending'
												: 'Clear sort'
										: undefined
								}
							>
								<div className="flex items-center gap-1">
									{header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}{' '}
									{isSortable
										? {
												asc: <Icon icon="chevron-up" className="h-4 w-4" />,
												desc: <Icon icon="chevron-down" className="h-4 w-4" />
											}[header.column.getIsSorted() as string]
										: null}
								</div>
							</th>
						))}
					</tr>
				))}
			</thead>
			<tbody>
				<tr
					aria-hidden
					className={clsx('h-4', {
						'bg-white dark:bg-neutral-800': background === 'white',
						'bg-gray-100 dark:bg-neutral-900': background === 'gray'
					})}
				>
					<td colSpan={columns.length} />
				</tr>
				{isLoading ? (
					<LoadingRows cols={columns.length} rows={3} />
				) : isEmpty ? (
					<tr className="h-full">
						<td className="rounded-[5px] rounded-t-md bg-white p-3 text-center dark:bg-neutral-800" colSpan={columns.length}>
							{emptyState}
						</td>
					</tr>
				) : (
					tableInstance.getRowModel().rows.map((row, i) => (
						<tr
							key={row.id}
							className={clsx(
								"relative bg-white after:absolute after:bottom-0 after:left-1/2 after:w-[99%] after:-translate-x-1/2 after:transform after:border-b after:content-[''] hover:bg-gray-50",
								{
									'[&>td:first-of-type]:rounded-tl-md [&>td:last-of-type]:rounded-tr-md': i === 0,
									'dark:bg-neutral-700 hover:dark:bg-neutral-700/50': background === 'white',
									'dark:bg-neutral-800 hover:dark:bg-neutral-700/50': background === 'gray'
								}
							)}
						>
							{row.getVisibleCells().map((cell) => (
								<td key={cell.id} className="p-3 text-sm first:pl-4 dark:text-white">
									{flexRender(cell.column.columnDef.cell, cell.getContext())}
								</td>
							))}
						</tr>
					))
				)}
				{!isEmpty && (
					<tr
						aria-hidden
						className={clsx('h-11', {
							'bg-white dark:bg-neutral-700': background === 'white',
							'bg-white dark:bg-neutral-800': background === 'gray'
						})}
					>
						<td className="first:rounded-bl-md last:rounded-br-md" colSpan={columns.length} />
					</tr>
				)}
			</tbody>
		</table>
	);
};

const Link = ({ pathname }: { pathname: string }) => {
	const navigate = useNavigate();

	return (
		<div className="flex justify-end">
			<IconButton icon="chevron-right" label="view" squared onPress={() => navigate({ pathname })} />
		</div>
	);
};

const LoadingRows = ({ cols, rows }: { cols: number; rows: number }) => {
	return [...new Array(rows)].map((_, i) => (
		<tr key={i}>
			{[...new Array(cols)].map((_, j) => (
				<td className="bg-gray-100 p-1 dark:bg-neutral-900" key={j}>
					<Skeleton>
						<Skeleton.Text />
					</Skeleton>
				</td>
			))}
		</tr>
	));
};

export default Table;
Table.Link = Link;
