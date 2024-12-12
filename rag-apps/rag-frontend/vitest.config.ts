import { fileURLToPath, URL } from 'url';
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
	plugins: [react()],
	test: {
		environment: 'jsdom',
		setupFiles: 'src/setupTests.ts',
		globals: true,
		server: {
			deps: {
				inline: [/@centml\/ui.*/]
			}
		}
	},
	resolve: {
		alias: [
			{
				find: '@',
				replacement: fileURLToPath(new URL('./src', import.meta.url))
			},
			{
				find: '@api',
				replacement: fileURLToPath(new URL('./src/api', import.meta.url))
			},
			{
				find: '@assets',
				replacement: fileURLToPath(new URL('./src/assets', import.meta.url))
			},
			{
				find: '@components',
				replacement: fileURLToPath(new URL('./src/components', import.meta.url))
			},
			{ find: '@tests', replacement: fileURLToPath(new URL('./src/tests', import.meta.url)) }
		]
	}
});
