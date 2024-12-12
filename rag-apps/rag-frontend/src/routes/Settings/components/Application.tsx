import { FormEvent, useState } from 'react';
import { useLoaderData } from 'react-router-dom';
import { Button, Switch, TextInput, toast } from '@centml/ui';
import centmlLogoDark from '@assets/centml/logo_inverted.svg';
import centmlLogo from '@assets/centml/logo.svg';
import { useQuery } from '@tanstack/react-query';
import { healthCheck, appKeys } from '@api/app/app';

export const applicationLoader = () => {
	const localStorageTheme = localStorage.getItem('theme');
	const localStorageAPiUrl = localStorage.getItem('api-url');

	let isDarkMode;
	if (localStorageTheme === 'dark') isDarkMode = true;
	if (localStorageTheme === 'light') isDarkMode = false;

	return {
		isDarkMode,
		localStorageAPiUrl
	};
};

interface LoaderData {
	isDarkMode: boolean;
	localStorageAPiUrl: string | null;
}

const Application = () => {
	const { isDarkMode: localStorageDarkMode, localStorageAPiUrl } = useLoaderData() as LoaderData;
	const [isDarkMode, setIsDarkMode] = useState(localStorageDarkMode);
	const [apiUrl, setApiUrl] = useState(localStorageAPiUrl ?? '');

	const { data, isLoading, error } = useQuery({
		queryKey: appKeys.health(),
		queryFn: ({ signal }) => healthCheck(signal)
	});

	if (error) console.error(error);

	const handleTheme = (isSelected: boolean) => {
		if (isSelected) {
			document.documentElement.classList.add('dark');
			localStorage.setItem('theme', 'dark');
			setIsDarkMode(true);
		} else {
			document.documentElement.classList.remove('dark');
			localStorage.setItem('theme', 'light');
			setIsDarkMode(false);
		}
	};

	const handleApiSubmit = (e: FormEvent) => {
		e.preventDefault();

		if (apiUrl === '') localStorage.removeItem('api-url');
		else localStorage.setItem('api-url', apiUrl);

		toast('URL updated', { type: 'success' });
		window.location.reload();
	};

	return (
		<div className="flex flex-grow flex-col gap-4 py-4">
			<p className="dark:text-white">Specify the location of the backend API URL</p>
			<form onSubmit={handleApiSubmit} className="flex flex-col">
				<div className="flex flex-col gap-1">
					<TextInput label="API URL" onChange={(url) => setApiUrl(url)} value={apiUrl} placeholder="http://localhost:8001" />
					<p className="text-sm dark:text-white">
						Status:{' '}
						{isLoading ? (
							<span className="text-xs italic">checking...</span>
						) : data?.status === 'healthy' ? (
							<span className="text-success-500">Healthy</span>
						) : (
							<span className="text-error-500">Not connected</span>
						)}
					</p>
				</div>

				<div className="flex justify-end">
					<Button type="submit">Submit</Button>
				</div>
			</form>

			<hr />
			<div className="flex">
				<Switch label="Dark mode" isSelected={isDarkMode} onChange={handleTheme} />
			</div>

			<hr />

			<div className="mt-auto flex flex-grow flex-col items-end justify-end">
				<p className="text-[11px] text-black dark:text-white">
					Powered by <span className="sr-only">CentML</span>
				</p>
				<img src={centmlLogo} alt="centml logo" className="w-[75px] dark:hidden" />
				<img src={centmlLogoDark} alt="centml logo" className="hidden w-[75px] dark:block" />
			</div>
		</div>
	);
};

export default Application;
