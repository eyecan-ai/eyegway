import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, searchForWorkspaceRoot } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	ssr: {
		noExternal: ['three']
	},
	server: {
		fs: {
			allow: [
				// @ts-ignore
				searchForWorkspaceRoot(process.cwd()),
				'/public/themes',
				'/public/layouts',
			],
		},
	}

});