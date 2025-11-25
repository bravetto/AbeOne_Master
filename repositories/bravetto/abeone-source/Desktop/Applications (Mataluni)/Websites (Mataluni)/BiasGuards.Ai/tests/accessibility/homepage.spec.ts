import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * BiasGuards.AI Homepage Accessibility Tests
 * WCAG 2.1 AA compliance testing for the main landing page
 */

test.describe('Homepage Accessibility', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to homepage
		await page.goto('/');

		// Wait for the page to be fully loaded
		await page.waitForLoadState('networkidle');

		// Wait for BiasGuards mission context to load
		await page.waitForFunction(() => {
			return (
				(window as unknown as { __BIASGUARDS_MISSION__?: unknown }).__BIASGUARDS_MISSION__ !==
				undefined
			);
		});
	});

	test('should not have any automatically detectable accessibility issues', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper heading hierarchy', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['heading-order'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have sufficient color contrast', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['color-contrast'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper alt text for images', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['image-alt'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper form labels', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page }).withRules(['label']).analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper keyboard navigation', async ({ page }) => {
		// Test tab navigation through interactive elements
		await page.keyboard.press('Tab');

		// Check that focus is visible
		const focusedElement = await page.locator(':focus');
		await expect(focusedElement).toBeVisible();

		// Run axe test for keyboard accessibility
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['focusable-content', 'tabindex'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper ARIA attributes', async ({ page }) => {
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['aria-valid-attr', 'aria-required-attr', 'aria-roles'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should be accessible to screen readers', async ({ page }) => {
		// Test for proper semantic structure
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['landmark-one-main', 'page-has-heading-one', 'region'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should handle focus management properly', async ({ page }) => {
		// Test skip links if they exist
		const skipLinks = page.locator('a[href^="#"]').first();

		if (await skipLinks.isVisible()) {
			await skipLinks.click();
			const targetElement = await page.locator((await skipLinks.getAttribute('href')) || '');
			await expect(targetElement).toBeFocused();
		}

		// Run axe test for focus management
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withRules(['skip-link', 'focus-order-semantics'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should be responsive and accessible on mobile', async ({ page }) => {
		// Set mobile viewport
		await page.setViewportSize({ width: 375, height: 667 });

		// Wait for responsive changes
		await page.waitForTimeout(500);

		// Run accessibility scan on mobile
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);

		// Check that interactive elements are appropriately sized for touch
		const buttons = page.locator('button, a[href], input[type="submit"]');
		const buttonCount = await buttons.count();

		for (let i = 0; i < buttonCount; i++) {
			const button = buttons.nth(i);
			const boundingBox = await button.boundingBox();

			if (boundingBox) {
				// WCAG guidelines recommend minimum 44px touch targets
				expect(boundingBox.width).toBeGreaterThanOrEqual(44);
				expect(boundingBox.height).toBeGreaterThanOrEqual(44);
			}
		}
	});
});
