import { describe, it, expect } from 'vitest';
import { ContextValidator, validateBiasGuardCode } from './context-validator';

describe('BiasGuard Context Validator', () => {
	describe('React Contamination Detection', () => {
		it('should detect React patterns', () => {
			const reactCode = `
				import React, { useState, useEffect } from 'react';
				const [count, setCount] = useState(0);
				return <div className="container" onClick={handleClick}>
			`;
			
			const result = ContextValidator.validateCode(reactCode);
			expect(result.isValid).toBe(false);
			expect(result.violations).toContain('React contamination detected: useState');
			expect(result.violations).toContain('React contamination detected: useEffect');
			expect(result.violations).toContain('React contamination detected: className');
		});

		it('should pass clean Svelte 5 code', () => {
			const svelteCode = `
				<script lang="ts">
					let count = $state(0);
					const doubled = $derived(count * 2);
					
					$effect(() => {
						console.log('Count changed:', count);
					});
				</script>
				
				<button class="btn" on:click={() => count++}>
					Count: {count}
				</button>
			`;
			
			const result = ContextValidator.validateCode(svelteCode);
			expect(result.score).toBeGreaterThan(70); // Should score well for Svelte 5 patterns
		});
	});

	describe('JAHmere Webb Story Authenticity', () => {
		it('should detect incorrect court date', () => {
			const incorrectCode = `
				const courtDate = 'July 28, 2025';
				const crisis = '$25,000';
			`;
			
			const result = ContextValidator.validateCode(incorrectCode);
			expect(result.isValid).toBe(false);
			expect(result.violations.some(v => v.includes('Incorrect court date'))).toBe(true);
			expect(result.violations.some(v => v.includes('Fabricated story detail'))).toBe(true);
		});

		it('should pass authentic story elements', () => {
			const authenticCode = `
				const AUTHENTIC_FACTS = {
					courtDate: 'August 25, 2025',
					crisisAmount: '$26,500',
					revenueToJustice: '15%',
					crisisTime: '2:42:56 AM'
				};
			`;
			
			const result = ContextValidator.validateCode(authenticCode);
			// Should not have story authenticity violations
			const storyViolations = result.violations.filter(v => 
				v.includes('court date') || v.includes('Fabricated')
			);
			expect(storyViolations).toHaveLength(0);
		});
	});

	describe('Vue Contamination Detection', () => {
		it('should detect Vue patterns', () => {
			const vueCode = `
				<template>
					<div v-if="isVisible" @click="handleClick">
						{{ message }}
					</div>
					<ul>
						<li v-for="item in items" :key="item.id">
							{{ item.name }}
						</li>
					</ul>
				</template>
			`;
			
			const result = ContextValidator.validateCode(vueCode);
			expect(result.isValid).toBe(false);
			expect(result.violations).toContain('Vue contamination detected: v-if');
			expect(result.violations).toContain('Vue contamination detected: v-for');
			expect(result.violations).toContain('Vue contamination detected: {{');
		});
	});

	describe('Animation Performance Validation', () => {
		it('should detect non-GPU animation properties', () => {
			const badAnimationCode = `
				.element {
					transition: width 0.3s ease, height 0.3s ease;
					animation: slideDown 0.5s ease;
				}
				
				@keyframes slideDown {
					from { top: -100px; }
					to { top: 0; }
				}
			`;
			
			const result = ContextValidator.validateCode(badAnimationCode);
			expect(result.violations.some(v => v.includes('Non-GPU animation'))).toBe(true);
		});

		it('should pass GPU-accelerated animations', () => {
			const goodAnimationCode = `
				.element {
					transition: transform 0.3s ease, opacity 0.3s ease;
					animation: slideIn 0.5s ease;
				}
				
				@keyframes slideIn {
					from { transform: translateY(-100px); opacity: 0; }
					to { transform: translateY(0); opacity: 1; }
				}
			`;
			
			const result = ContextValidator.validateCode(goodAnimationCode);
			const animationViolations = result.violations.filter(v => 
				v.includes('Non-GPU animation')
			);
			expect(animationViolations).toHaveLength(0);
		});
	});

	describe('Performance Potential Validation', () => {
		it('should detect performance anti-patterns', () => {
			const badPerformanceCode = `
				import { heavyLibrary } from 'massive-library';
				
				function component() {
					const element = document.querySelector('.my-element');
					setInterval(() => {
						const now = new Date();
						const later = new Date();
					}, 1000);
				}
			`;
			
			const result = ContextValidator.validatePerformancePotential(badPerformanceCode);
			expect(result.score).toBeLessThan(95);
			expect(result.violations.length).toBeGreaterThan(0);
		});
	});

	describe('Complete Validation Suite', () => {
		it('should provide comprehensive validation', () => {
			const mixedCode = `
				import React from 'react';
				const [state] = useState(0);
				const courtDate = 'July 28, 2025';
				
				.bad-animation {
					transition: width 0.3s ease;
				}
			`;
			
			const result = ContextValidator.validateComplete(mixedCode);
			expect(result.isValid).toBe(false);
			expect(result.score).toBeLessThan(50);
			expect(result.violations.length).toBeGreaterThan(3);
			expect(result.recommendations.length).toBeGreaterThan(0);
		});

		it('should pass high-quality BiasGuard code', () => {
			const qualityCode = `
				<script lang="ts">
					import { onMount } from 'svelte';
					
					let isLoaded = $state(false);
					const missionDays = $derived(() => {
						const court = new Date('2025-08-25');
						const now = new Date();
						return Math.ceil((court.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
					});
					
					const AUTHENTIC_STATS = {
						legalCrisis: '$26,500',
						courtDate: 'August 25, 2025',
						revenueToJustice: '15%'
					};
					
					onMount(() => {
						isLoaded = true;
					});
				</script>
				
				<div class="hero-section">
					<h1>BiasGuards.AI - Justice Mission</h1>
					<p>Court Date: {AUTHENTIC_STATS.courtDate}</p>
				</div>
				
				<style>
					.hero-section {
						transition: transform 0.3s ease, opacity 0.3s ease;
					}
				</style>
			`;
			
			const result = ContextValidator.validateComplete(qualityCode);
			expect(result.score).toBeGreaterThan(80);
			expect(result.violations.length).toBeLessThan(2);
		});
	});

	describe('Helper Function', () => {
		it('should log validation results', () => {
			const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
			const consoleInfoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});
			
			const badCode = 'const [state] = useState(0);';
			validateBiasGuardCode(badCode);
			
			expect(consoleSpy).toHaveBeenCalled();
			expect(consoleInfoSpy).toHaveBeenCalled();
			
			consoleSpy.mockRestore();
			consoleInfoSpy.mockRestore();
		});
	});
});
