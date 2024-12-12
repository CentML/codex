import axiosInstance from '@api/axiosInstance';

export const documentKeys = {
	all: ['documents'] as const,
	currentDocuments: () => [...documentKeys.all, 'current'] as const,
	documentsByType: (type: string) => [...documentKeys.currentDocuments(), type] as const
};

export const getCurrentDocuments = (doc_type?: 'document' | 'url' | 'confluence') => {
	return axiosInstance
		.get<{ filenames: string[] }>('/documents', { params: doc_type ? new URLSearchParams({ doc_type }) : undefined })
		.then((res) => res.data.filenames);
};

export const deleteDocument = (document: string) => {
	return axiosInstance.delete('/documents', {
		params: {
			source: JSON.stringify([document]),
		},
	});
};

export const deleteDocuments = (files: string[]) => {
	return axiosInstance.delete('/documents', {
		params: {
			source: JSON.stringify(files),
		},
	});
};

export const deleteAllDocuments = (doc_type?: 'document' | 'url' | 'confluence') => {
	if (doc_type) {
		const params = new URLSearchParams({ doc_type });
		return axiosInstance.delete('/documents/all', { params });
	}

	return axiosInstance.delete('/documents/all');
};

export const uploadFiles = (files: File[]) => {
	const formData = new FormData();

	files.forEach((file) => formData.append('files', file));
	return axiosInstance.post('/documents/files', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
};

export const connectUrls = (urls: string[]) => {
	return axiosInstance.post('/documents/urls', {
		source: urls,
	});
};
