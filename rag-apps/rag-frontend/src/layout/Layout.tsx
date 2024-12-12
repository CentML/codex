import { PropsWithChildren } from 'react';
import Sidebar from './Sidebar';

const Layout = ({ children }: PropsWithChildren) => {
	return (
		<div className="flex max-h-screen min-h-screen flex-col bg-gray-100 p-2 pr-0 sm:flex-row dark:bg-neutral-900">
			<Sidebar />
			<main className="flex w-full flex-grow flex-col overflow-y-auto">{children}</main>
		</div>
	);
};

export default Layout;
