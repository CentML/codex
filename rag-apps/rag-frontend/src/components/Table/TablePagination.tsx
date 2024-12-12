import { IconButton, NumberInput, ToggleButton } from '@centml/ui';

interface TablePaginationProps {
	currentPage: number;
	handlePageChange: (page: number) => void;
	handleRowsChange: (rows: number) => void;
	hideRowControls?: boolean;
	rowCounts?: number[];
	rows: number;
	totalPages: number;
	totalRows: number;
}

const TablePagination = ({
	currentPage,
	handlePageChange,
	handleRowsChange,
	hideRowControls,
	rowCounts,
	rows,
	totalRows,
	totalPages
}: TablePaginationProps) => {
	const rowOptions = rowCounts ? [...rowCounts, 0] : [10, 25, 0];

	return (
		<div className="mt-1 flex flex-col-reverse gap-2 sm:flex-row sm:justify-between">
			{!hideRowControls ? (
				<div className="flex items-center">
					{rowOptions.map((n, i, self) => (
						<ToggleButton
							aria-label={`View ${n === 0 ? 'all' : n} rows `}
							key={n}
							className={`rounded-none border px-2 ${i === 0 && 'rounded-l-md'} ${i === self.length - 1 && 'rounded-r-md'}`}
							isSelected={n === rows}
							onChange={() => {
								if (n === 0) handleRowsChange(totalRows);
								else handleRowsChange(n);
							}}
						>
							{n === 0 ? 'All' : n}
						</ToggleButton>
					))}
					<p className="ml-1 text-sm dark:text-white">
						Showing <strong>{rows ? rows : 10}</strong> of <strong>{totalRows}</strong> Rows
					</p>
				</div>
			) : (
				<div />
			)}

			<div className="flex flex-row items-center sm:justify-start justify-center gap-2">
				<IconButton
					icon="chevron-left"
					label="previous page"
					isDisabled={currentPage === 0}
					squared
					onPress={() => handlePageChange(currentPage - 1)}
				/>

				<p className="text-sm dark:text-white">
					Page: <span className="sr-only">{currentPage}</span>
				</p>

				<NumberInput
					className="w-10"
					label="go to page"
					labelHidden
					minValue={1}
					maxValue={totalPages}
					value={currentPage + 1}
					onChange={(page) => handlePageChange(page - 1)}
				/>

				<p className="text-right text-sm dark:text-white">
					<span className="sr-only">Page {currentPage}</span>
					of <strong>{totalPages}</strong>
				</p>

				<IconButton
					icon="chevron-right"
					label="next page"
					isDisabled={currentPage + 1 === totalPages}
					squared
					onPress={() => handlePageChange(currentPage + 1)}
				/>
			</div>
		</div>
	);
};

export default TablePagination;
