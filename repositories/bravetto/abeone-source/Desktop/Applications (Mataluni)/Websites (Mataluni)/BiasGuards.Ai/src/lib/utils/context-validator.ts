/**
 * BiasGuard Context Engineering Validation System
 * Prevents AI drift and ensures mission-aligned, high-performance code generation
 */

export interface ValidationResult {
	isValid: boolean;
	violations: string[];
	score: number;
	recommendations: string[];
}

export interface BiasGuardContext {
	framework: 'svelte5';
	mission: 'jahmere-webb-justice';
	performance: 'lighthouse-98plus';
	authenticity: 'verified-story-only';
}

export class ContextValidator {
	private static readonly REACT_PATTERNS = [
		'useState',
		'useEffect',
		'useContext',
		'useReducer',
		'className',
		'onClick',
		'onChange',
		'React.',
		'import React'
	];

	private static readonly VUE_PATTERNS = [
		'v-if',
		'v-for',
		'v-model',
		'v-show',
		'@click',
		'@change',
		'{{',
		'}}',
		'Vue.'
	];

	private static readonly SVELTE5_REQUIRED_PATTERNS = [
		'$state',
		'$derived',
		'$effect',
		'$props'
	];

	private static readonly JAHMERE_WEBB_FACTS = {
		courtDate: '2025-08-25',
		crisisAmount: '$26,500',
		revenueToJustice: '15%',
		crisisTime: '2:42:56 AM',
		crisisDate: 'July 14, 2025'
	};

	private static readonly NON_GPU_ANIMATIONS = [
		'width',
		'height',
		'top',
		'left',
		'margin',
		'padding',
		'font-size'
	];

	/**
	 * Validates code against BiasGuard context architecture
	 */
	static validateCode(code: string): ValidationResult {
		const violations: string[] = [];
		const recommendations: string[] = [];
		let score = 100;

		// Check for React contamination
		const reactViolations = this.detectReactContamination(code);
		if (reactViolations.length > 0) {
			violations.push(...reactViolations);
			score -= 30;
			recommendations.push('Use Svelte 5 + Runes API instead of React patterns');
		}

		// Check for Vue contamination
		const vueViolations = this.detectVueContamination(code);
		if (vueViolations.length > 0) {
			violations.push(...vueViolations);
			score -= 25;
			recommendations.push('Use Svelte syntax instead of Vue patterns');
		}

		// Validate Svelte 5 usage
		const svelte5Score = this.validateSvelte5Usage(code);
		if (svelte5Score < 80) {
			violations.push('Missing Svelte 5 Runes API usage');
			score -= 20;
			recommendations.push('Use $state, $derived, $effect for reactive state management');
		}

		// Check JAHmere Webb story authenticity
		const storyViolations = this.validateStoryAuthenticity(code);
		if (storyViolations.length > 0) {
			violations.push(...storyViolations);
			score -= 40; // Heavy penalty for mission dilution
			recommendations.push('Maintain JAHmere Webb story authenticity - only use verified facts');
		}

		// Validate animation performance
		const animationViolations = this.validateAnimationPerformance(code);
		if (animationViolations.length > 0) {
			violations.push(...animationViolations);
			score -= 15;
			recommendations.push('Use GPU-accelerated properties: transform, opacity, filter');
		}

		return {
			isValid: violations.length === 0,
			violations,
			score: Math.max(0, score),
			recommendations
		};
	}

	/**
	 * Detects React patterns in code
	 */
	private static detectReactContamination(code: string): string[] {
		const violations: string[] = [];
		
		this.REACT_PATTERNS.forEach(pattern => {
			if (code.includes(pattern)) {
				violations.push(`React contamination detected: ${pattern}`);
			}
		});

		return violations;
	}

	/**
	 * Detects Vue patterns in code
	 */
	private static detectVueContamination(code: string): string[] {
		const violations: string[] = [];
		
		this.VUE_PATTERNS.forEach(pattern => {
			if (code.includes(pattern)) {
				violations.push(`Vue contamination detected: ${pattern}`);
			}
		});

		return violations;
	}

	/**
	 * Validates proper Svelte 5 Runes usage
	 */
	private static validateSvelte5Usage(code: string): number {
		let score = 0;
		const totalPatterns = this.SVELTE5_REQUIRED_PATTERNS.length;

		this.SVELTE5_REQUIRED_PATTERNS.forEach(pattern => {
			if (code.includes(pattern)) {
				score += (100 / totalPatterns);
			}
		});

		return score;
	}

	/**
	 * Validates JAHmere Webb story authenticity
	 */
	private static validateStoryAuthenticity(code: string): string[] {
		const violations: string[] = [];

		// Check for incorrect court date
		if (code.includes('July 28') || code.includes('2025-07-28')) {
			violations.push('Incorrect court date - must be August 25, 2025');
		}

		// Check for fabricated details
		const fabricatedPatterns = [
			'July 28', // Wrong court date
			'$25,000', // Wrong crisis amount
			'$27,000', // Wrong crisis amount
			'10%', // Wrong revenue percentage
			'20%', // Wrong revenue percentage
			'3:00 AM', // Wrong crisis time
			'July 15' // Wrong crisis date
		];

		fabricatedPatterns.forEach(pattern => {
			if (code.includes(pattern)) {
				violations.push(`Fabricated story detail detected: ${pattern}`);
			}
		});

		return violations;
	}

	/**
	 * Validates animation performance (GPU-only properties)
	 */
	private static validateAnimationPerformance(code: string): string[] {
		const violations: string[] = [];

		// Check for non-GPU animation properties
		this.NON_GPU_ANIMATIONS.forEach(property => {
			const animationPattern = new RegExp(`(transition|animation).*${property}`, 'i');
			if (animationPattern.test(code)) {
				violations.push(`Non-GPU animation property detected: ${property}`);
			}
		});

		return violations;
	}

	/**
	 * Validates Lighthouse performance potential
	 */
	static validatePerformancePotential(code: string): ValidationResult {
		const violations: string[] = [];
		const recommendations: string[] = [];
		let score = 100;

		// Check for performance anti-patterns
		const performanceIssues = [
			{ pattern: /import.*from ['"](?!.*\.svelte).*['"]/, message: 'Large dependency import detected', penalty: 10 },
			{ pattern: /document\.querySelector/, message: 'DOM query in component - use bind:this', penalty: 5 },
			{ pattern: /setInterval|setTimeout/, message: 'Timer usage - ensure cleanup', penalty: 5 },
			{ pattern: /new Date\(\).*new Date\(\)/, message: 'Multiple Date instantiations', penalty: 3 }
		];

		performanceIssues.forEach(({ pattern, message, penalty }) => {
			if (pattern.test(code)) {
				violations.push(message);
				score -= penalty;
			}
		});

		// Recommendations for 98+ Lighthouse score
		if (score < 95) {
			recommendations.push('Optimize for Core Web Vitals');
			recommendations.push('Use lazy loading for images');
			recommendations.push('Minimize JavaScript bundle size');
			recommendations.push('Implement proper caching strategies');
		}

		return {
			isValid: score >= 95,
			violations,
			score,
			recommendations
		};
	}

	/**
	 * Complete validation suite
	 */
	static validateComplete(code: string): ValidationResult {
		const codeValidation = this.validateCode(code);
		const performanceValidation = this.validatePerformancePotential(code);

		return {
			isValid: codeValidation.isValid && performanceValidation.isValid,
			violations: [...codeValidation.violations, ...performanceValidation.violations],
			score: Math.min(codeValidation.score, performanceValidation.score),
			recommendations: [...codeValidation.recommendations, ...performanceValidation.recommendations]
		};
	}
}

/**
 * Quick validation helper for development
 */
export function validateBiasGuardCode(code: string): void {
	const result = ContextValidator.validateComplete(code);
	
	if (!result.isValid) {
		console.warn(' BiasGuard Context Violations Detected:');
		result.violations.forEach(violation => console.warn(`  - ${violation}`));
		
		if (result.recommendations.length > 0) {
			console.info(' Recommendations:');
			result.recommendations.forEach(rec => console.info(`  - ${rec}`));
		}
		
		console.info(` Context Compliance Score: ${result.score}/100`);
	} else {
		console.log(' BiasGuard Context Validation Passed');
	}
}
