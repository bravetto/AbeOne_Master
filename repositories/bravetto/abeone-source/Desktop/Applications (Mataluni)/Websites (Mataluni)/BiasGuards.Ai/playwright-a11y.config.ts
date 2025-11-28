import { defineConfig, devices } from '@playwright/test';

/**
 * BiasGuards.AI Accessibility Testing Configuration
 * WCAG 2.1 AA compliance testing with axe-core
 */
export default defineConfig({
	// Test directory for accessibility tests
	testDir: './tests/accessibility',

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
		['html', { outputFolder: 'test-results/accessibility-report' }],
		['json', { outputFile: 'test-results/accessibility-results.json' }],
		['junit', { outputFile: 'test-results/accessibility-results.xml' }]
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

		// BiasGuards accessibility requirements
		actionTimeout: 10000,
		navigationTimeout: 30000
	},

	// Configure projects for accessibility testing
	projects: [
		{
			name: 'accessibility-desktop',
			use: { ...devices['Desktop Chrome'] }
		},

		{
			name: 'accessibility-mobile',
			use: { ...devices['Pixel 5'] }
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
	outputDir: './test-results/accessibility/',

	// Artifacts
	fullyParallel: true,

	// Maximum failures before stopping
	maxFailures: process.env.CI ? 5 : undefined
});
