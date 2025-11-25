import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
// Bundle analyzer will be configured separately

export default defineConfig({
	plugins: [
		sveltekit()
		// Bundle analyzer configured via separate command
	],

	// Performance optimizations
	build: {
		// Target modern browsers for smaller bundles
		target: 'es2022',
		// Enable minification
		minify: 'esbuild',
		// Chunk splitting for better caching
		rollupOptions: {
			output: {
				manualChunks: {
					// Separate GSAP for better caching
					gsap: ['gsap'],
					// Vendor chunk for third-party libraries
					vendor: ['@skeletonlabs/skeleton']
				}
			}
		},
		// Performance budget enforcement (150KB limit)
		chunkSizeWarningLimit: 150,
		// Source maps for debugging
		sourcemap: true
	},

	// Development server configuration
	server: {
		port: 5173,
		host: true,
		// Enable HTTPS for PWA testing
		https: false,
		// Hot module replacement
		hmr: {
			overlay: true
		}
	},

	// Preview server configuration
	preview: {
		port: 4173,
		host: true
	},

	// CSS preprocessing
	css: {
		postcss: './postcss.config.js',
		devSourcemap: true
	},

	// Dependency optimization
	optimizeDeps: {
		include: ['gsap', '@skeletonlabs/skeleton'],
		exclude: ['@sveltejs/kit']
	},

	// Environment variables
	define: {
		// BiasGuards mission context
		__COURT_DATE__: JSON.stringify('August 25, 2025'),
		__MISSION__: JSON.stringify('JAHmere Webb Freedom Mission'),
		__REVENUE_TO_JUSTICE__: JSON.stringify('15%'),
		__BUILD_TIME__: JSON.stringify(new Date().toISOString())
	},

	// Test configuration
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		environment: 'jsdom',
		setupFiles: ['./src/lib/test-setup.ts']
	},

	// Vite 5.4 optimized configuration
	ssr: {
		noExternal: ['@skeletonlabs/skeleton']
	}
});
