import axiosInstance from '@api/axiosInstance';
import { Assets } from './types';

export const appKeys = {
	all: ['app'] as const,
	health: () => [...appKeys.all, 'health'] as const,
	assets: () => [...appKeys.all, 'assets'] as const
};

export const healthCheck = (signal: AbortSignal) => {
	return axiosInstance.get<{ status: string }>('/health_check', { signal }).then((res) => res.data);
};

export const getAssets = () => {
	return axiosInstance.get<Assets | null>('/assets').then((res) => res.data);
};
