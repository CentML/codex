import axiosInstance from '@api/axiosInstance';
import { Space, SpaceDocument } from './types';

export const confluenceKeys = {
	all: ['confluence'] as const,
	list: () => [...confluenceKeys.all, 'list'] as const,
	connectedSpaceDocuments: (space: string) => [...confluenceKeys.list(), space]
};

export const getConfluenceSpaces = async (variables: { base_url: string; username: string; api_key: string }) => {
	const { base_url, username, api_key } = variables;
	const params = new URLSearchParams({ base_url, username, api_key });

	return axiosInstance
		.get<{ spaces: Space[] }>('/confluence', { params })
		.then((res) => res.data.spaces.slice().sort((a, b) => a.key.localeCompare(b.key)));
};

export const connectConfluenceSpaces = (variables: { base_url: string; username: string; api_key: string; space_keys: string[] }) => {
	const { base_url, username, api_key, space_keys } = variables;

	return axiosInstance.post('/confluence', { base_url, username, api_key, space_keys }).then((res) => res.data);
};

export const getSpaceDocuments = (space: string) => {
	return axiosInstance.get<{ documents: SpaceDocument[] }>(`/confluence/${space}`).then((res) => res.data.documents);
};

export const deleteSpaceDocument = (space: string, doc_title: string) => {
	const params = new URLSearchParams({ doc_title });

	return axiosInstance.delete(`/confluence/${space}`, { params });
};
