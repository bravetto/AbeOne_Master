import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],

	test: {
		// Test environment - happy-dom for better Svelte 5 support
		environment: 'happy-dom',

		// Test file patterns
		include: ['src/**/*.{test,spec}.{js,ts}'],
		exclude: ['node_modules', 'dist', '.svelte-kit'],

		// Setup files
		setupFiles: ['./src/lib/test-setup.ts'],

		// Global test configuration
		globals: true,

		// Coverage configuration
		coverage: {
			provider: 'v8',
			reporter: ['text', 'json', 'html', 'lcov'],
			exclude: [
				'coverage/**',
				'dist/**',
				'packages/*/test{,s}/**',
				'**/*.d.ts',
				'**/*.config.*',
				'**/node_modules/**',
				'.svelte-kit/**'
			],
			// BiasGuards quality standards - 90%+ coverage
			thresholds: {
				global: {
					branches: 90,
					functions: 90,
					lines: 90,
					statements: 90
				}
			}
		},

		// Performance settings
		testTimeout: 10000,
		hookTimeout: 10000,

		// BiasGuards mission context for tests
		env: {
			VITE_COURT_DATE: 'August 25, 2025',
			VITE_MISSION: 'JAHmere Webb Freedom Mission',
			VITE_REVENUE_TO_JUSTICE: '15%'
		},

		// Reporter configuration
		reporter: ['verbose', 'json', 'html'],

		// UI configuration for test debugging
		ui: true,
		open: false
	}
});
