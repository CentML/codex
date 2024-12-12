import { ActionFunctionArgs, redirect, useNavigate, useNavigation, useSubmit } from 'react-router-dom';
import { ConfirmationModal, toast } from '@centml/ui';
import { QueryClient } from '@tanstack/react-query';
import { deleteAllDocuments, documentKeys } from '@api/documents/documents';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';

export const deleteAllAction =
	(queryClient: QueryClient) =>
	async ({ request }: ActionFunctionArgs) => {
		const { searchParams } = new URL(request.url);
		const doc_type = searchParams.get('type') ?? undefined;

		try {
			await deleteAllDocuments(doc_type as 'document' | 'url');
			await queryClient.invalidateQueries({ queryKey: documentKeys.all });

			return redirect(ROUTES.SETTINGS + '/' + doc_type === 'document' ? SETTINGS_ROUTES.DOCUMENTS : SETTINGS_ROUTES.WEB);
		} catch (error) {
			console.error(error);
			toast('Could not delete documents', { type: 'error' });
			return null;
		}
	};

const DeleteAll = () => {
	const navigate = useNavigate();
	const navigation = useNavigation();
	const submit = useSubmit();

	return (
		<ConfirmationModal
			title="Delete all documents"
			variant="destructive"
			loading={navigation.state === 'submitting'}
			isOpen
			onOpenChange={() => navigate(-1)}
			onConfirm={() => submit(null, { method: 'POST' })}
		>
			<p> Are you sure you want to delete all uploaded files and connected documents? This action is permanent and cannot be undone.</p>
		</ConfirmationModal>
	);
};

export default DeleteAll;
