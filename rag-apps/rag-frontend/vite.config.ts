import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'url';

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		host: true,
		port: 3000
	},
	plugins: [react()],
	resolve: {
		alias: [
			{ find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) },
			{ find: '@api', replacement: fileURLToPath(new URL('./src/api', import.meta.url)) },
			{ find: '@assets', replacement: fileURLToPath(new URL('./src/assets', import.meta.url)) },
			{ find: '@components', replacement: fileURLToPath(new URL('./src/components', import.meta.url)) },
			{ find: '@layout', replacement: fileURLToPath(new URL('./src/layout', import.meta.url)) },
			{ find: '@routes', replacement: fileURLToPath(new URL('./src/routes', import.meta.url)) },
			{ find: '@tests', replacement: fileURLToPath(new URL('./src/tests', import.meta.url)) }
		]
	}
});
