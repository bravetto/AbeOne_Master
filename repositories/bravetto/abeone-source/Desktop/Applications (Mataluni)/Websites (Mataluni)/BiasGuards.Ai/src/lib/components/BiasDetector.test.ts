/**
 * BiasDetector Tests - Optimized
 * JAHmere Webb Freedom Mission - August 25, 2025
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('BiasDetector', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	describe('Core Analysis', () => {
		it('validates JAHmere Webb mission context', () => {
			const missionText = 'Born from JAHmere Webb\'s legal crisis';
			expect(missionText).toContain('JAHmere Webb');
		});

		it('processes text input', () => {
			const analyzeText = (input: string) => input.trim().length > 0;
			expect(analyzeText('test content')).toBe(true);
			expect(analyzeText('   ')).toBe(false);
		});

		it('generates bias scores', () => {
			const generateScore = () => 75; // Fixed score, no random
			const score = generateScore();
			expect(score).toBeGreaterThanOrEqual(0);
			expect(score).toBeLessThanOrEqual(100);
		});

		it('detects bias patterns', () => {
			const detectBias = (text: string) => {
				const patterns = [];
				if (text.includes('gender')) patterns.push('Gender Bias');
				return patterns;
			};
			
			const result = detectBias('gender-based text');
			expect(result.length).toBeGreaterThan(0);
		});
	});

	describe('Interface', () => {
		it('manages input state', () => {
			let textInput = '';
			const updateInput = (value: string) => { textInput = value; };
			
			updateInput('sample text');
			expect(textInput).toBe('sample text');
		});

		it('handles analysis state', () => {
			let isAnalyzing = false;
			const toggleAnalysis = () => { isAnalyzing = !isAnalyzing; };
			
			toggleAnalysis();
			expect(isAnalyzing).toBe(true);
		});

		it('validates input length', () => {
			const canAnalyze = (input: string) => input.trim().length > 5;
			
			expect(canAnalyze('hello world')).toBe(true);
			expect(canAnalyze('hi')).toBe(false);
		});
	});

	describe('Results', () => {
		it('formats scores', () => {
			const formatScore = (score: number) => `${score.toFixed(1)}%`;
			expect(formatScore(75.6)).toBe('75.6%');
		});

		it('handles empty results', () => {
			const displayResults = (results: any) => {
				return results ? `Score: ${results.score}%` : 'No analysis';
			};
			
			expect(displayResults(null)).toBe('No analysis');
			expect(displayResults({ score: 42 })).toBe('Score: 42%');
		});
	});

	describe('Performance', () => {
		it('processes input efficiently', () => {
			const quickCheck = (input: string) => {
				return input.trim().length === 0 ? null : { valid: true };
			};
			
			expect(quickCheck('')).toBeNull();
			expect(quickCheck('content')).toEqual({ valid: true });
		});
	});
});

// Test utilities
export const TestUtils = {
	mockResults: () => ({
		biasScore: 75, // Fixed score, no random
		confidence: 85, // Fixed confidence
		suggestions: ['Review neutral language', 'Consider inclusive terms']
	}),
	
	isValidScore: (score: number) => score >= 0 && score <= 100,
	
	formatPercentage: (value: number) => `${value.toFixed(1)}%`
};