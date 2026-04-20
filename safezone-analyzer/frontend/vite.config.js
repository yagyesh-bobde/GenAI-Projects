import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

/** Browser hits same origin (e.g. :5173); only that port needs to be public. */
const apiProxy = {
	'/api': {
		target: 'http://127.0.0.1:8000',
		changeOrigin: true,
		rewrite: (path) => path.replace(/^\/api/, '')
	}
};

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: apiProxy
	},
	preview: {
		proxy: apiProxy
	}
});
