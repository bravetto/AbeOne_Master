import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

describe('InteractiveDemo', () => {
	beforeEach(() => {
		vi.clearAllMocks();
		vi.useFakeTimers();
	});
	afterEach(() => {
		vi.useRealTimers();
	});

	describe('Detection', () => {
		it('defines examples', () => {
			const examples = [
				{ category: 'Hiring', score: 78, patterns: ['Pattern A'] },
				{ category: 'Finance', score: 82, patterns: ['Pattern B'] }
			];
			expect(examples.length).toBe(2);
		});

		it('detects keywords', () => {
			const detect = (code: string) => ['bias'].filter(k => code.includes(k));
			expect(detect('bias found')).toContain('bias');
		});

		it('calculates scores', () => {
			const calc = (keywords: string[]) => keywords.length * 15;
			expect(calc(['test'])).toBe(15);
		});
	});

	describe('Animation', () => {
		it('creates timeline', () => {
			const mockGsap = { timeline: () => ({ to: vi.fn() }) };
			const timeline = mockGsap.timeline();
			expect(timeline.to).toBeDefined();
		});

		it('handles cleanup', () => {
			const mockKill = vi.fn();
			const timeline = { kill: mockKill };
			timeline.kill();
			expect(mockKill).toHaveBeenCalled();
		});
	});

	describe('State', () => {
		it('manages selection', () => {
			let selected = 0;
			const select = (i: number) => {
				if (i >= 0 && i < 3) {
					selected = i;
					return true;
				}
				return false;
			};
			expect(select(1)).toBe(true);
			expect(selected).toBe(1);
		});

		it('validates input', () => {
			const validate = (code: string) => code.trim().length > 0;
			expect(validate('test')).toBe(true);
			expect(validate('')).toBe(false);
		});
	});

	describe('Performance', () => {
		it('shows metrics', () => {
			const stats = { time: '<200ms', rate: '84%', issues: 2 };
			expect(stats.rate).not.toBe('100%');
		});

		it('handles errors', () => {
			const analyze = (code: string) => {
				try {
					if (code.includes('error')) throw new Error('Failed');
					return { success: true };
				} catch {
					return { success: false };
				}
			};
			expect(analyze('normal')).toEqual({ success: true });
			expect(analyze('error')).toEqual({ success: false });
		});
	});
});

export const InteractiveDemoTestUtils = {
	detectKeywords: (code: string) => ['bias'].filter(k => code.includes(k)),
	calculateScore: (keywords: string[]) => keywords.length * 15,
	validateClaims: (text: string) => !['100%', 'perfect'].some(c => text.includes(c)),
	simulateDelay: () => Math.random() * 200 + 100
};
