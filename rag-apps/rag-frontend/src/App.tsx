import { Suspense, useEffect } from 'react';
import { Router } from '@routes/routes';
import nProgress from 'nprogress';

const SuspenseComponent = () => {
	useEffect(() => {
		nProgress.configure({ showSpinner: false });
		nProgress.start();

		return () => {
			nProgress.done();
		};
	});

	return null;
};

function App() {
	return (
		<Suspense fallback={<SuspenseComponent />}>
			<Router />
		</Suspense>
	);
}

export default App;
