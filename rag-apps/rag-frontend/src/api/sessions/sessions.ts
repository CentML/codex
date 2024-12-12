import axiosInstance from '@api/axiosInstance';
import { SessionData } from './types';

export const sessionKeys = {
	all: ['sessions'] as const,
	listSessions: () => [...sessionKeys.all, 'list'] as const,
	session: (id: string | undefined) => [...sessionKeys.all, id] as const
};

export const getSessions = () => {
	return axiosInstance.get<SessionData[]>('/sessions').then((res) => res.data);
};

export const getSession = (id: string) => {
	return axiosInstance.get(`/sessions/${id}`).then((res) => res.data);
};

export const deleteSession = (id: string) => {
	return axiosInstance.delete(`/sessions/${id}`).then((res) => res.data);
};
