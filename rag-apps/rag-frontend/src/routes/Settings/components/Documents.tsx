import { Suspense, useState } from 'react';
import { ActionFunctionArgs, Await, defer, useLoaderData, useNavigation, useSubmit } from 'react-router-dom';
import { QueryClient } from '@tanstack/react-query';
import { Alert, Button, FileInput, toast } from '@centml/ui';
import { deleteDocument, documentKeys, getCurrentDocuments, uploadFiles } from '@api/documents/documents';
import Connected from './Connected';

export const documentsLoader = (queryClient: QueryClient) => () => {
	const documents = queryClient.fetchQuery({
		queryKey: documentKeys.documentsByType('document'),
		queryFn: () => getCurrentDocuments('document')
	});

	return defer({ documents });
};

export const documentsAction =
	(queryClient: QueryClient) =>
	async ({ request }: ActionFunctionArgs) => {
		const formData = Object.fromEntries(await request.formData());

		try {
			if (request.method === 'DELETE') {
				await deleteDocument(formData.file as string);
			}

			if (request.method === 'POST') {
				const files = Object.keys(formData)
					.filter((k) => k.includes('file'))
					.map((k) => formData[k]);
				await uploadFiles(files as File[]);
			}

			await queryClient.invalidateQueries({ queryKey: documentKeys.currentDocuments() });
		} catch (error) {
			toast('Could not delete document', { type: 'error' });
			console.error(error);
		} finally {
			return null;
		}
	};

const Documents = () => {
	const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
	const { documents } = useLoaderData() as { documents: ReturnType<typeof documentsLoader> };
	const submit = useSubmit();
	const navigation = useNavigation();

	return (
		<div className="py-4">
			<div>
				<form
					method="POST"
					encType="multipart/form-data"
					className="flex flex-col gap-4"
					onSubmit={(e) => {
						e.preventDefault();

						const formData = new FormData();
						selectedFiles.forEach((file, i) => formData.append(`file-${i}`, file));
						submit(formData, { method: 'POST', encType: 'multipart/form-data' });
					}}
				>
					<div className="flex flex-col gap-2">
						<div>
							<p className="text-sm dark:text-white">Upload documents</p>
							<p className="text-xs text-gray-600 dark:text-gray-300">Supported files: PDF (.pdf), markdown (.md), text (.txt)</p>
						</div>
						<FileInput acceptedFileTypes={['.pdf', '.md', '.txt']} allowsMultiple onSelectFile={(files) => setSelectedFiles(files)} />
					</div>
					<div className="flex justify-end">
						<Button type="submit" loading={navigation.state === 'submitting'} isDisabled={!selectedFiles.length}>
							Submit
						</Button>
					</div>
				</form>
			</div>

			<Suspense fallback={<Connected documents={[]} isLoading />}>
				<Await
					resolve={documents}
					errorElement={
						<Alert showIcon className="mt-4" variant="error">
							Could not get documents
						</Alert>
					}
				>
					{(documents) => <Connected documents={documents} />}
				</Await>
			</Suspense>
		</div>
	);
};

export default Documents;
