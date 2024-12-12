import { Suspense, useState } from 'react';
import { Await, useLoaderData, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { IconButton, Link, LoadingSpinner, toast, Tooltip } from '@centml/ui';
import centmlLogo from '@assets/centml/logo_inverted.svg';
import centmlCollapsed from '@assets/centml/logo_collapsed.svg';
import { ROUTES, SETTINGS_ROUTES } from '@routes/routes.paths';
import { appKeys, getAssets } from '@api/app/app';
import Sessions from './Sessions';
import MobileSidebar from './MobileSidebar';

const Sidebar = () => {
	const [isCollapsed, setIsCollapsed] = useState(false);
	const { documents } = useLoaderData() as { documents: Promise<{ filenames: string[] }> };

	const navigate = useNavigate();

	const { data: assets, isLoading } = useQuery({ queryKey: appKeys.assets(), queryFn: () => getAssets() });

	return (
		<>
			<aside className={`hidden sm:block ${isCollapsed ? 'w-[80px] transition-all' : 'relative w-[250px] transition-all'}`}>
				<nav className="flex h-full list-none flex-col overflow-y-auto rounded-lg bg-zinc-700 py-2 dark:bg-neutral-800">
					<ul className={`mb-4 flex px-2 ${isCollapsed ? 'flex-col items-center gap-2' : 'flex-row items-center justify-center'}`}>
						{!isLoading && (
							<li>
								<Link href={ROUTES.DASHBOARD}>
									{isCollapsed ? (
										<img
											src={assets?.paths.logo_collapsed ? assets?.paths.logo_collapsed : centmlCollapsed}
											alt="logo"
											onError={(e) => {
												e.currentTarget.onerror = null;
												e.currentTarget.src = centmlCollapsed;
											}}
										/>
									) : (
										<img
											src={assets?.paths.logo_inverted ? assets?.paths.logo_inverted : centmlLogo}
											alt="logo"
											className="w-[120px]"
											onError={(e) => {
												e.currentTarget.onerror = null;
												e.currentTarget.src = centmlLogo;
											}}
										/>
									)}
								</Link>
							</li>
						)}

						<li>
							<IconButton
								className="!bg-transparent text-white"
								icon={isCollapsed ? 'chevron-right' : 'chevron-left'}
								label={isCollapsed ? 'expand sidebar' : 'collapse sidebar'}
								onPress={() => setIsCollapsed((prev) => !prev)}
								squared
							/>
						</li>
					</ul>

					<Sessions isCollapsed={isCollapsed} />

					<div className="flex items-center justify-between px-2">
						{!isCollapsed && (
							<div className="text-center">
								<p className="text-[11px] text-white">
									Powered by <span className="sr-only">CentML</span>
								</p>
								<img src={centmlLogo} alt="centml logo" className="w-[100px]" />
							</div>
						)}
						<ul className={`flex w-full items-center justify-end gap-0.5 ${isCollapsed && 'flex-col'}`}>
							<Suspense fallback={<LoadingSpinner />}>
								<Await
									resolve={documents}
									errorElement={
										<li>
											<Tooltip tip="Could not get documents">
												<IconButton
													className="mx-auto h-8 w-8 !text-error-500"
													icon="exclamation-circle"
													squared
													label="show error"
													onPress={() => toast('Could not get documents', { type: 'error' })}
												/>
											</Tooltip>
										</li>
									}
								>
									{(documents) => {
										return (
											documents.length === 0 && (
												<li>
													<Tooltip tip="No files in database">
														<IconButton
															className="mx-auto h-8 w-8 !text-warning-500"
															icon="exclamation-triangle"
															squared
															label="show warning"
															onPress={() => toast('No files in database', { type: 'warning' })}
														/>
													</Tooltip>
												</li>
											)
										);
									}}
								</Await>
							</Suspense>

							<li>
								<IconButton
									icon="cog-6-tooth"
									label="settings"
									onPress={() => navigate({ pathname: ROUTES.SETTINGS + '/' + SETTINGS_ROUTES.DOCUMENTS })}
									squared
									className="h-8 w-8 text-white"
								/>
							</li>
						</ul>
					</div>
				</nav>
			</aside>

			<MobileSidebar />
		</>
	);
};

export default Sidebar;
