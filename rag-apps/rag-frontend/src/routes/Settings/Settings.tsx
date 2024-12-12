import { useEffect } from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { TabGroup } from '@centml/ui';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';

const SETTINGS_KEYS = [SETTINGS_ROUTES.DOCUMENTS, SETTINGS_ROUTES.WEB, SETTINGS_ROUTES.CONFLUENCE, SETTINGS_ROUTES.APPLICATION] as const;

const Settings = () => {
	const navigate = useNavigate();
	const { pathname } = useLocation();

	useEffect(() => {
		if (pathname === ROUTES.SETTINGS) {
			navigate(SETTINGS_ROUTES.DOCUMENTS, { replace: true });
		}
	}, [location]);

	return (
		<div className="container flex flex-grow flex-col px-4">
			<h4 className="my-6 text-3xl capitalize dark:text-white">Settings</h4>

			<TabGroup
				items={[
					{
						id: SETTINGS_ROUTES.DOCUMENTS,
						triggerElement: 'Documents'
					},
					{
						id: SETTINGS_ROUTES.WEB,
						triggerElement: 'Web'
					},
					{
						id: SETTINGS_ROUTES.CONFLUENCE,
						triggerElement: 'Confluence'
					},
					{
						id: SETTINGS_ROUTES.APPLICATION,
						triggerElement: 'Application'
					}
				]}
				label="Settings menu"
				orientation="horizontal"
				selectedKey={SETTINGS_KEYS.find((key) => pathname.includes(key))}
				onSelectionChange={(key) => navigate({ pathname: key as string })}
			/>

			<Outlet />
		</div>
	);
};

export default Settings;
