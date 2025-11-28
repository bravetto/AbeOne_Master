import { defineConfig, devices } from '@playwright/test';

/**
 * BiasGuards.AI E2E Testing Configuration
 * Performance-focused testing aligned with mission-critical requirements
 */
export default defineConfig({
	// Test directory
	testDir: './tests',

	// Global test timeout
	timeout: 30 * 1000,

	// Expect timeout for assertions
	expect: {
		timeout: 5000
	},

	// Fail the build on CI if you accidentally left test.only in the source code
	forbidOnly: !!process.env.CI,

	// Retry on CI only
	retries: process.env.CI ? 2 : 0,

	// Opt out of parallel tests on CI
	workers: process.env.CI ? 1 : undefined,

	// Reporter configuration
	reporter: [
		['html'],
		['json', { outputFile: 'test-results/results.json' }],
		['junit', { outputFile: 'test-results/results.xml' }]
	],

	// Shared settings for all the projects below
	use: {
		// Base URL for tests
		baseURL: 'http://localhost:4173',

		// Collect trace when retrying the failed test
		trace: 'on-first-retry',

		// Screenshot on failure
		screenshot: 'only-on-failure',

		// Video recording
		video: 'retain-on-failure',

		// BiasGuards performance requirements
		// Target <1.2s FCP (First Contentful Paint)
		actionTimeout: 10000,
		navigationTimeout: 30000
	},

	// Configure projects for major browsers
	projects: [
		{
			name: 'chromium',
			use: { ...devices['Desktop Chrome'] }
		},

		{
			name: 'firefox',
			use: { ...devices['Desktop Firefox'] }
		},

		{
			name: 'webkit',
			use: { ...devices['Desktop Safari'] }
		},

		// Mobile testing (mobile-first approach)
		{
			name: 'Mobile Chrome',
			use: { ...devices['Pixel 5'] }
		},

		{
			name: 'Mobile Safari',
			use: { ...devices['iPhone 12'] }
		}
	],

	// Web server configuration
	webServer: {
		command: 'npm run build && npm run preview',
		port: 4173,
		reuseExistingServer: !process.env.CI,

		// BiasGuards performance targets
		// Ensure server starts within reasonable time
		timeout: 120 * 1000
	},

	// Global setup and teardown
	globalSetup: require.resolve('./tests/global-setup.ts'),
	globalTeardown: require.resolve('./tests/global-teardown.ts'),

	// Test output directory
	outputDir: './test-results/',

	// Artifacts
	fullyParallel: true,

	// Maximum failures before stopping
	maxFailures: process.env.CI ? 10 : undefined
});
