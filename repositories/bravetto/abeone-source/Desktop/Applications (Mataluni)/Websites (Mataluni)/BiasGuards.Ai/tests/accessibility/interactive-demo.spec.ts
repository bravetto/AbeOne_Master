import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * BiasGuards.AI Interactive Demo Accessibility Tests
 * WCAG 2.1 AA compliance testing for the bias detection demo
 */

test.describe('Interactive Demo Accessibility', () => {
	test.beforeEach(async ({ page }) => {
		// Navigate to homepage where demo is located
		await page.goto('/');

		// Wait for the page to be fully loaded
		await page.waitForLoadState('networkidle');

		// Wait for the interactive demo component to be present
		await page.waitForSelector('[data-testid="interactive-demo"]', { timeout: 10000 });
	});

	test('demo form should be fully accessible', async ({ page }) => {
		// Focus on the demo section
		await page.locator('[data-testid="interactive-demo"]').scrollIntoViewIfNeeded();

		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('form inputs should have proper labels and descriptions', async ({ page }) => {
		const demoSection = page.locator('[data-testid="interactive-demo"]');

		// Check that all form inputs have associated labels
		const inputs = demoSection.locator('input, textarea, select');
		const inputCount = await inputs.count();

		for (let i = 0; i < inputCount; i++) {
			const input = inputs.nth(i);
			const inputId = await input.getAttribute('id');
			const ariaLabel = await input.getAttribute('aria-label');
			const ariaLabelledBy = await input.getAttribute('aria-labelledby');

			// Each input should have either an id with corresponding label, aria-label, or aria-labelledby
			if (inputId) {
				const label = page.locator(`label[for="${inputId}"]`);
				await expect(label).toBeVisible();
			} else {
				expect(ariaLabel || ariaLabelledBy).toBeTruthy();
			}
		}

		// Run axe test for form labels
		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withRules(['label', 'label-title-only'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('demo results should be announced to screen readers', async ({ page }) => {
		const demoSection = page.locator('[data-testid="interactive-demo"]');

		// Find and fill the demo form
		const textInput = demoSection.locator('input[type="text"], textarea').first();

		if (await textInput.isVisible()) {
			await textInput.fill('This is a test case for bias detection');

			// Submit the form or trigger analysis
			const submitButton = demoSection
				.locator('button[type="submit"], button:has-text("Analyze")')
				.first();

			if (await submitButton.isVisible()) {
				await submitButton.click();

				// Wait for results to appear
				await page.waitForTimeout(2000);

				// Check that results have proper ARIA live region for announcements
				const resultsSection = demoSection.locator('[data-testid="bias-results"], [aria-live]');

				if ((await resultsSection.count()) > 0) {
					const ariaLive = await resultsSection.first().getAttribute('aria-live');
					expect(['polite', 'assertive']).toContain(ariaLive);
				}
			}
		}

		// Run axe test for live regions
		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withRules(['aria-valid-attr-value', 'aria-live-region-atomic'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('keyboard navigation should work throughout demo', async ({ page }) => {
		const demoSection = page.locator('[data-testid="interactive-demo"]');
		await demoSection.scrollIntoViewIfNeeded();

		// Start keyboard navigation from the demo section
		await demoSection.focus();

		// Tab through all interactive elements
		const interactiveElements = demoSection.locator('button, input, textarea, select, a[href]');
		const elementCount = await interactiveElements.count();

		for (let i = 0; i < elementCount; i++) {
			await page.keyboard.press('Tab');

			// Verify that focus is visible and within the demo section
			const focusedElement = page.locator(':focus');
			await expect(focusedElement).toBeVisible();

			// Verify focused element is within demo section
			const isWithinDemo = (await demoSection.locator(':focus').count()) > 0;
			if (i < elementCount - 1) {
				// Allow last element to potentially be outside
				expect(isWithinDemo).toBe(true);
			}
		}

		// Run axe test for keyboard accessibility
		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withRules(['focusable-content', 'tabindex'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('demo should handle errors accessibly', async ({ page }) => {
		const demoSection = page.locator('[data-testid="interactive-demo"]');

		// Try to submit empty form or trigger error state
		const submitButton = demoSection
			.locator('button[type="submit"], button:has-text("Analyze")')
			.first();

		if (await submitButton.isVisible()) {
			await submitButton.click();

			// Wait for potential error messages
			await page.waitForTimeout(1000);

			// Check for error messages with proper ARIA attributes
			const errorMessages = demoSection.locator(
				'[role="alert"], [aria-invalid="true"] + *, .error'
			);

			if ((await errorMessages.count()) > 0) {
				// Verify error messages are properly associated with form fields
				const invalidInputs = demoSection.locator('[aria-invalid="true"]');
				const invalidCount = await invalidInputs.count();

				for (let i = 0; i < invalidCount; i++) {
					const input = invalidInputs.nth(i);
					const ariaDescribedBy = await input.getAttribute('aria-describedby');

					if (ariaDescribedBy) {
						const errorElement = page.locator(`#${ariaDescribedBy}`);
						await expect(errorElement).toBeVisible();
					}
				}
			}
		}

		// Run axe test for error handling
		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withRules(['aria-valid-attr-value', 'aria-describedby-references'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('demo should work with high contrast mode', async ({ page }) => {
		// Simulate high contrast mode by adding CSS
		await page.addStyleTag({
			content: `
				@media (prefers-contrast: high) {
					* {
						background-color: white !important;
						color: black !important;
						border-color: black !important;
					}
					button, input, textarea, select {
						border: 2px solid black !important;
					}
				}
			`
		});

		const demoSection = page.locator('[data-testid="interactive-demo"]');
		await demoSection.scrollIntoViewIfNeeded();

		// Verify all interactive elements are still visible and functional
		const buttons = demoSection.locator('button');
		const buttonCount = await buttons.count();

		for (let i = 0; i < buttonCount; i++) {
			const button = buttons.nth(i);
			await expect(button).toBeVisible();

			// Check that button has sufficient contrast (this is a basic check)
			const computedStyle = await button.evaluate(el => {
				const style = getComputedStyle(el);
				return {
					backgroundColor: style.backgroundColor,
					color: style.color,
					borderColor: style.borderColor
				};
			});

			// In high contrast mode, these should be high contrast colors
			expect(computedStyle.color).toBeTruthy();
			expect(computedStyle.backgroundColor).toBeTruthy();
		}

		// Run axe test for color contrast
		const accessibilityScanResults = await new AxeBuilder({ page })
			.include('[data-testid="interactive-demo"]')
			.withRules(['color-contrast'])
			.analyze();

		expect(accessibilityScanResults.violations).toEqual([]);
	});
});
