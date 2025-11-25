/**
 * BiasGuards.AI Lighthouse CI Configuration
 * Performance and quality auditing aligned with mission-critical requirements
 */
module.exports = {
	ci: {
		collect: {
			// URLs to audit
			url: ['http://localhost:4173'],

			// Chrome options for consistent testing
			settings: {
				chromeFlags: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--headless']
			},

			// Number of runs per URL
			numberOfRuns: 3,

			// Wait for page to be ready
			startServerCommand: 'npm run preview',
			startServerReadyPattern: 'Local:',
			startServerReadyTimeout: 30000
		},

		assert: {
			// BiasGuards performance requirements
			assertions: {
				// Performance thresholds (98+ target)
				'categories:performance': ['error', { minScore: 0.98 }],

				// Accessibility compliance (WCAG 2.1 AA)
				'categories:accessibility': ['error', { minScore: 0.95 }],

				// Best practices
				'categories:best-practices': ['error', { minScore: 0.9 }],

				// SEO optimization
				'categories:seo': ['error', { minScore: 0.9 }],

				// Core Web Vitals
				'categories:pwa': ['warn', { minScore: 0.8 }],

				// Specific metrics for BiasGuards mission-critical performance
				'first-contentful-paint': ['error', { maxNumericValue: 1200 }], // <1.2s
				'largest-contentful-paint': ['error', { maxNumericValue: 2500 }], // <2.5s
				'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }], // <0.1
				'total-blocking-time': ['error', { maxNumericValue: 300 }], // <300ms
				'speed-index': ['error', { maxNumericValue: 1300 }], // <1.3s

				// Resource optimization
				'unused-javascript': ['warn', { maxNumericValue: 20000 }], // <20KB unused JS
				'render-blocking-resources': ['warn', { maxNumericValue: 500 }], // <500ms blocking
				'uses-webp-images': 'off', // Allow flexibility in image formats
				'uses-optimized-images': ['warn', { maxNumericValue: 50000 }] // <50KB savings
			}
		},

		upload: {
			// Upload results for CI/CD integration
			target: 'temporary-public-storage',

			// GitHub integration (if available)
			githubAppToken: process.env.LHCI_GITHUB_APP_TOKEN,

			// Custom server upload (optional)
			serverBaseUrl: process.env.LHCI_SERVER_BASE_URL,
			token: process.env.LHCI_SERVER_TOKEN
		},

		server: {
			// Optional: Lighthouse CI server configuration
			port: 9001,
			storage: {
				storageMethod: 'filesystem',
				storagePath: './lighthouse-data'
			}
		}
	}
};
