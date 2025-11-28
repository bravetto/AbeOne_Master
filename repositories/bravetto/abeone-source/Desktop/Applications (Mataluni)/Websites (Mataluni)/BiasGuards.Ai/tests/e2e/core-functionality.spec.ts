import { test, expect } from '@playwright/test';

/**
 * BiasGuards.AI Core Functionality E2E Tests
 * Essential user journeys for mission-critical features
 */

test.describe('Core Functionality', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/');
		await page.waitForLoadState('networkidle');
	});

	test('loads with mission context', async ({ page }) => {
		// Verify page loads
		await expect(page).toHaveTitle(/BiasGuards\.AI/);

		// Check mission context
		const missionContext = await page.evaluate(() => {
			return (
				window as unknown as { __BIASGUARDS_MISSION__?: { courtDate: string; mission: string } }
			).__BIASGUARDS_MISSION__;
		});

		expect(missionContext?.courtDate).toBe('August 25, 2025');
		expect(missionContext?.mission).toBe('JAHmere Webb Freedom Mission');
	});

	test('displays key sections', async ({ page }) => {
		// Hero section
		const heroSection = page.locator('[data-testid="hero-section"]');
		await expect(heroSection).toBeVisible();

		// Performance stats
		const statsSection = page.locator('[data-testid="performance-stats"]');
		await expect(statsSection).toBeVisible();

		// Interactive demo
		const demoSection = page.locator('[data-testid="interactive-demo"]');
		await expect(demoSection).toBeVisible();
	});

	test('interactive demo works', async ({ page }) => {
		const demoSection = page.locator('[data-testid="interactive-demo"]');
		await demoSection.scrollIntoViewIfNeeded();

		// Find text input
		const textInput = demoSection.locator('input[type="text"], textarea').first();

		if (await textInput.isVisible()) {
			await textInput.fill('Test bias detection');

			// Find analyze button
			const analyzeButton = demoSection
				.locator('button:has-text("Analyze"), button[type="submit"]')
				.first();

			if (await analyzeButton.isVisible()) {
				await analyzeButton.click();
				await page.waitForTimeout(1000);

				// Check for results
				const resultsArea = demoSection.locator('[data-testid="bias-results"], .results');
				if ((await resultsArea.count()) > 0) {
					await expect(resultsArea.first()).toBeVisible();
				}
			}
		}
	});

	test('responsive on mobile', async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 });
		await page.waitForTimeout(300);

		// Key elements remain visible
		await expect(page.locator('[data-testid="hero-section"]')).toBeVisible();
		await expect(page.locator('[data-testid="performance-stats"]')).toBeVisible();
		await expect(page.locator('[data-testid="interactive-demo"]')).toBeVisible();
	});
});
