import { Suspense, useState } from 'react';
import { Await, Link, useLoaderData, useLocation, useNavigate } from 'react-router-dom';
import { Alert, Drawer, IconButton, LoadingSpinner } from '@centml/ui';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';
import centmlLogo from '@assets/centml/logo.svg';
import centmlInverted from '@assets/centml/logo_inverted.svg';
import { appKeys, getAssets } from '@api/app/app';
import ChatSessions from './Sessions';
import { useQuery } from '@tanstack/react-query';

const LOGO_STYLE = 'mx-auto my-2 w-[120px] ';

const MobileSidebar = () => {
	const [isOpen, setIsOpen] = useState(false);

	const { documents } = useLoaderData() as { documents: Promise<{ filenames: string[] }> };
	const navigate = useNavigate();
	const { pathname } = useLocation();

	const { data: assets, isLoading } = useQuery({ queryKey: appKeys.assets(), queryFn: () => getAssets() });

	const isViewingSettings = pathname.includes(ROUTES.SETTINGS);

	return (
		<>
			<div className="mb-2 block flex items-center justify-between pr-2 sm:hidden">
				<IconButton label={isOpen ? 'hide navigation' : 'show navigation'} icon="bars-3" onPress={() => setIsOpen(!isOpen)} />

				{isViewingSettings ? (
					<IconButton label="home" icon="home" onPress={() => navigate(ROUTES.DASHBOARD)} />
				) : (
					<IconButton label="settings" icon="cog-6-tooth" onPress={() => navigate(ROUTES.SETTINGS + '/' + SETTINGS_ROUTES.DOCUMENTS)} />
				)}
			</div>

			<Drawer title="navigation" hideTitle position="left" size="sm" isOpen={isOpen} onOpenChange={() => setIsOpen(false)}>
				<Link to={ROUTES.DASHBOARD}>
					{!isLoading && (
						<>
							<img
								src={assets?.paths.logo_inverted ? assets.paths.logo_inverted : centmlInverted}
								alt="logo"
								className={LOGO_STYLE + 'hidden dark:block'}
								onError={(e) => {
									e.currentTarget.onerror = null;
									e.currentTarget.src = centmlInverted;
								}}
							/>
							<img
								src={assets?.paths.logo ? assets?.paths.logo : centmlLogo}
								alt="logo"
								className={LOGO_STYLE + 'dark:hidden'}
								onError={(e) => {
									e.currentTarget.onerror = null;
									e.currentTarget.src = centmlLogo;
								}}
							/>
						</>
					)}
				</Link>

				<ChatSessions isMobile />

				<ul>
					<Suspense fallback={<LoadingSpinner />}>
						<Await
							resolve={documents}
							errorElement={
								<li>
									<Alert variant="error" showIcon>
										<p>Could not get documents</p>
									</Alert>
								</li>
							}
						>
							{(documents) => {
								return (
									documents.length === 0 && (
										<li>
											<Alert variant="warning" showIcon>
												<p>No connected documents</p>
											</Alert>
										</li>
									)
								);
							}}
						</Await>
					</Suspense>
				</ul>
			</Drawer>
		</>
	);
};

export default MobileSidebar;
