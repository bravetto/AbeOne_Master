/**
 * BiasGuard Simple Validator - Streamlined Context Engineering
 * Based on BiasGuard's own analysis: Remove complexity, focus on essentials
 */

export interface SimpleValidation {
	valid: boolean;
	issues: string[];
	score: number;
}

export class SimpleValidator {
	// Authentic JAHmere Webb facts (never change these)
	private static readonly FACTS = {
		courtDate: '2025-08-25',
		crisisAmount: '$26,500',
		revenuePercent: '15%',
		crisisTime: '2:42:56 AM',
		crisisDate: 'July 14, 2025'
	};

	// Framework patterns to reject
	private static readonly BAD_PATTERNS = [
		'useState', 'useEffect', 'className', // React
		'v-if', 'v-for', '{{', '}}', // Vue
		'width:', 'height:', 'top:', 'left:' // Bad animations
	];

	// Good Svelte 5 patterns
	private static readonly GOOD_PATTERNS = [
		'$state', '$derived', '$effect', '$props'
	];

	/**
	 * Quick validation - essential checks only
	 */
	static validate(code: string): SimpleValidation {
		const issues: string[] = [];
		let score = 100;

		// Check for bad patterns
		SimpleValidator.BAD_PATTERNS.forEach(pattern => {
			if (code.includes(pattern)) {
				issues.push(`Avoid: ${pattern}`);
				score -= 15;
			}
		});

		// Check for good Svelte patterns
		const hasGoodPatterns = SimpleValidator.GOOD_PATTERNS.some(pattern => 
			code.includes(pattern)
		);
		if (!hasGoodPatterns && code.includes('<script')) {
			issues.push('Use Svelte 5 runes: $state, $derived, $effect');
			score -= 20;
		}

		// Check JAHmere Webb facts
		if (code.includes('July 28') || code.includes('$25,000')) {
			issues.push('Wrong JAHmere Webb facts - use authentic details');
			score -= 30;
		}

		return {
			valid: issues.length === 0,
			issues,
			score: Math.max(0, score)
		};
	}

	/**
	 * Quick console validation
	 */
	static check(code: string): void {
		const result = SimpleValidator.validate(code);
		
		if (result.valid) {
			console.log(' BiasGuard validation passed');
		} else {
			console.warn(' BiasGuard issues:');
			result.issues.forEach(issue => console.warn(`  - ${issue}`));
			console.info(`Score: ${result.score}/100`);
		}
	}
}

// Export for easy use
export const validateCode = SimpleValidator.validate;
export const checkCode = SimpleValidator.check;
