import { describe, it, expect } from 'vitest';
import { SimpleValidator, validateCode } from './simple-validator';

describe('SimpleValidator - Proving it works', () => {
	it('catches React contamination', () => {
		const reactCode = 'const [count, setCount] = useState(0);';
		const result = validateCode(reactCode);
		
		expect(result.valid).toBe(false);
		expect(result.issues).toContain('Avoid: useState');
		expect(result.score).toBeLessThan(100);
	});

	it('catches wrong JAHmere Webb facts', () => {
		const wrongCode = 'const courtDate = "July 28, 2025";';
		const result = validateCode(wrongCode);
		
		expect(result.valid).toBe(false);
		expect(result.issues).toContain('Wrong JAHmere Webb facts - use authentic details');
	});

	it('passes clean Svelte 5 code', () => {
		const goodCode = `
			let count = $state(0);
			const courtDate = 'August 25, 2025';
		`;
		const result = validateCode(goodCode);
		
		expect(result.valid).toBe(true);
		expect(result.score).toBeGreaterThan(80);
	});

	it('detects bad animations', () => {
		const badAnimation = '.element { transition: width 0.3s; }';
		const result = validateCode(badAnimation);
		
		expect(result.valid).toBe(false);
		expect(result.issues).toContain('Avoid: width:');
	});
});
