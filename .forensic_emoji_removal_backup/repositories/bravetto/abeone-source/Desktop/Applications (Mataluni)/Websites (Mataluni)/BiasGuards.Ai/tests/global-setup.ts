/**
 * BiasGuards.AI Global Test Setup
 * Playwright global setup for E2E testing
 */

import { chromium, type FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
	console.log('🛡️ BiasGuards.AI E2E Test Setup Starting...');

	// Launch browser for setup
	const browser = await chromium.launch();
	const context = await browser.newContext();
	const page = await context.newPage();

	try {
		// Verify the application is running
		console.log('📡 Checking application availability...');
		await page.goto('http://localhost:4173', {
			waitUntil: 'networkidle',
			timeout: 30000
		});

		// Verify BiasGuards mission context is loaded
		const missionContext = await page.evaluate(() => {
			return (window as any).__BIASGUARDS_MISSION__;
		});

		if (!missionContext) {
			throw new Error('BiasGuards mission context not found');
		}

		console.log('⚖️ Mission context verified:', {
			courtDate: missionContext.courtDate,
			mission: missionContext.mission,
			revenueToJustice: missionContext.revenueToJustice
		});

		// Verify critical performance metrics
		console.log('⚡ Running performance checks...');
		const performanceMetrics = await page.evaluate(() => {
			return new Promise(resolve => {
				// Wait for performance entries
				setTimeout(() => {
					const navigation = performance.getEntriesByType(
						'navigation'
					)[0] as PerformanceNavigationTiming;
					const paint = performance.getEntriesByType('paint');

					const fcp = paint.find(entry => entry.name === 'first-contentful-paint')?.startTime || 0;
					const domContentLoaded = navigation.domContentLoadedEventEnd - navigation.navigationStart;

					resolve({
						fcp: fcp / 1000, // Convert to seconds
						domContentLoaded: domContentLoaded / 1000,
						loadComplete: navigation.loadEventEnd - navigation.navigationStart
					});
				}, 2000);
			});
		});

		console.log('📊 Performance metrics:', performanceMetrics);

		// Verify BiasGuards components are present
		console.log('🔍 Verifying core components...');

		const heroSection = await page.locator('section').first();
		await heroSection.waitFor({ state: 'visible', timeout: 10000 });

		const biasDetectorPresent = await page.locator('text=AI Bias Detection Engine').isVisible();
		const missionStatementPresent = await page.locator('text=Born from Crisis').isVisible();

		if (!biasDetectorPresent || !missionStatementPresent) {
			throw new Error('Core BiasGuards components not found');
		}

		console.log('✅ All core components verified');
		console.log('🚀 BiasGuards.AI E2E Test Setup Complete');
	} catch (error) {
		console.error('❌ Global setup failed:', error);
		throw error;
	} finally {
		await context.close();
		await browser.close();
	}
}

export default globalSetup;
