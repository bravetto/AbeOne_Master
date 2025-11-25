import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(),

		// BiasGuards.AI specific configuration
		alias: {
			'@': './src',
			'@/components': './src/lib/components',
			'@/utils': './src/lib/utils',
			'@/stores': './src/lib/stores',
			'@/types': './src/lib/types',
			'@/assets': './src/lib/assets'
		},

		// Environment variables
		env: {
			publicPrefix: 'VITE_'
		}
	}
};

export default config;
