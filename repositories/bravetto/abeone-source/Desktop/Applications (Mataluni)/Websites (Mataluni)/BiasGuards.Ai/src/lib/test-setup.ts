/**
 * BiasGuards.AI Test Setup
 * Global test configuration and utilities
 */

import { vi } from 'vitest';
import { cleanup } from '@testing-library/svelte';
import { afterEach, beforeEach } from 'vitest';

// Mock modules before test setup
vi.mock('gsap', () => ({
	gsap: {
		fromTo: vi.fn(),
		to: vi.fn(),
		from: vi.fn(),
		set: vi.fn(),
		registerPlugin: vi.fn(),
		timeline: vi.fn(() => ({
			from: vi.fn().mockReturnThis(),
			to: vi.fn().mockReturnThis(),
			set: vi.fn().mockReturnThis(),
			play: vi.fn().mockReturnThis(),
			kill: vi.fn().mockReturnThis(),
			progress: vi.fn(() => 0.5)
		}))
	}
}));

vi.mock('$app/environment', () => ({
	browser: true,
	dev: true,
	building: false,
	version: '1.0.0'
}));

vi.mock('$lib/utils/animations', () => ({
	BiasGuardAnimations: vi.fn().mockImplementation(() => ({
		animateHeroEntrance: vi.fn(),
		createParticleBackground: vi.fn(() => []),
		addMouseMagnetism: vi.fn(),
		animateNumber: vi.fn(),
		destroy: vi.fn()
	})),
	NumberAnimations: {
		animatePercentage: vi.fn()
	}
}));

// Global test setup
beforeEach(() => {

	// Mock window globals for BiasGuards mission context
	Object.defineProperty(window, '__BIASGUARDS_MISSION__', {
		value: {
			courtDate: 'August 25, 2025',
			mission: 'JAHmere Webb Freedom Mission',
			revenueToJustice: '15%',
			legalCrisis: '$26,500',
			buildTime: '2025-01-01T00:00:00.000Z'
		},
		writable: true
	});

	// Mock performance observer for performance stats
	global.PerformanceObserver = vi.fn().mockImplementation(callback => ({
		observe: vi.fn(),
		disconnect: vi.fn()
	}));
});

// Cleanup after each test
afterEach(() => {
	cleanup();
	vi.clearAllMocks();
});

// Custom matchers for BiasGuards testing
expect.extend({
	toHaveBiasScore(received: any, expectedScore: number, tolerance = 5) {
		const pass = Math.abs(received.biasScore - expectedScore) <= tolerance;
		return {
			message: () => `expected ${received.biasScore} to be within ${tolerance} of ${expectedScore}`,
			pass
		};
	},

	toMeetPerformanceTarget(received: any, target: number, metric: string) {
		let pass = false;

		switch (metric) {
			case 'lighthouse':
				pass = received >= target;
				break;
			case 'fcp':
			case 'lcp':
			case 'cls':
			case 'fid':
			case 'bundleSize':
				pass = received <= target;
				break;
		}

		return {
			message: () => `expected ${metric} ${received} to meet target ${target}`,
			pass
		};
	}
});

// Global test utilities
export const mockBiasAnalysisResult = {
	biasScore: 45.2,
	biasTypes: ['Gender Bias', 'Age Discrimination'],
	suggestions: ['Consider using gender-neutral language', 'Review for age-inclusive terminology'],
	confidence: 87.5
};

export const mockPerformanceData = {
	lighthouse: 99,
	fcp: 0.8,
	lcp: 1.2,
	cls: 0.05,
	fid: 45,
	bundleSize: 142
};

// Test helpers for mission context
export const MISSION_TEST_DATA = {
	courtDate: 'August 25, 2025',
	mission: 'JAHmere Webb Freedom Mission',
	revenueToJustice: '15%',
	legalCrisis: '$26,500'
} as const;
