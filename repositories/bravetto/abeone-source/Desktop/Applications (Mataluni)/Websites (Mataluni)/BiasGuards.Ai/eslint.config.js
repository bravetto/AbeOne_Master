import js from '@eslint/js';
import ts from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import svelte from 'eslint-plugin-svelte';
import svelteParser from 'svelte-eslint-parser';
import prettier from 'eslint-config-prettier';

/**
 * BiasGuards.AI ESLint Configuration
 * Justice-driven code quality standards with zero tolerance for drift
 */
export default [
	// Base JavaScript recommendations
	js.configs.recommended,

	// TypeScript configuration
	{
		files: ['**/*.ts', '**/*.tsx'],
		languageOptions: {
			parser: tsParser,
			parserOptions: {
				ecmaVersion: 2022,
				sourceType: 'module',
				project: './tsconfig.json'
			}
		},
		plugins: {
			'@typescript-eslint': ts
		},
		rules: {
			// TypeScript strict rules for BiasGuards quality
			'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
			'@typescript-eslint/no-explicit-any': 'error',
			'@typescript-eslint/no-non-null-assertion': 'error',
			'@typescript-eslint/prefer-nullish-coalescing': 'error',
			'@typescript-eslint/prefer-optional-chain': 'error',
			'@typescript-eslint/no-unnecessary-type-assertion': 'error',
			'@typescript-eslint/no-floating-promises': 'error',
			'@typescript-eslint/await-thenable': 'error',
			'@typescript-eslint/no-misused-promises': 'error',
			'@typescript-eslint/require-await': 'error',
			'@typescript-eslint/no-unsafe-assignment': 'error',
			'@typescript-eslint/no-unsafe-call': 'error',
			'@typescript-eslint/no-unsafe-member-access': 'error',
			'@typescript-eslint/no-unsafe-return': 'error'
		}
	},

	// Svelte configuration
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				parser: tsParser,
				extraFileExtensions: ['.svelte']
			}
		},
		plugins: {
			svelte
		},
		rules: {
			// Svelte 5 + Runes specific rules
			'svelte/no-deprecated-dollar-labeled-statements': 'error',
			'svelte/no-reactive-functions': 'error',
			'svelte/no-reactive-literals': 'error',
			'svelte/prefer-destructuring-props': 'error',
			'svelte/no-useless-mustaches': 'error',
			'svelte/no-unused-svelte-ignore': 'error',
			'svelte/valid-compile': 'error',
			'svelte/no-at-debug-tags': 'warn',
			'svelte/no-at-html-tags': 'error',

			// BiasGuards anti-drift rules - NO React patterns
			'svelte/no-react-specific-props': 'error',
			'svelte/button-has-type': 'error',
			'svelte/no-target-blank': 'error',

			// Accessibility (WCAG 2.1 AA compliance)
			'svelte/a11y-alt-text': 'error',
			'svelte/a11y-aria-attributes': 'error',
			'svelte/a11y-click-events-have-key-events': 'error',
			'svelte/a11y-role-has-required-aria-props': 'error',
			'svelte/a11y-tabindex-no-positive': 'error'
		}
	},

	// Global rules for all files
	{
		files: ['**/*.js', '**/*.ts', '**/*.svelte'],
		rules: {
			// Code quality standards
			'no-console': 'warn',
			'no-debugger': 'error',
			'no-alert': 'error',
			'no-eval': 'error',
			'no-implied-eval': 'error',
			'no-new-func': 'error',
			'no-script-url': 'error',

			// Performance rules
			'no-async-promise-executor': 'error',
			'no-await-in-loop': 'warn',
			'no-promise-executor-return': 'error',

			// BiasGuards naming conventions
			camelcase: [
				'error',
				{
					properties: 'never',
					ignoreDestructuring: true,
					allow: ['^VITE_', '^__[A-Z_]+__$'] // Allow env vars and build constants
				}
			],

			// Import/export rules
			'no-duplicate-imports': 'error',
			'sort-imports': [
				'error',
				{
					ignoreCase: true,
					ignoreDeclarationSort: true
				}
			]
		}
	},

	// Configuration files
	{
		files: ['*.config.{js,ts}', '*.setup.{js,ts}'],
		rules: {
			'no-console': 'off'
		}
	},

	// Test files
	{
		files: ['**/*.test.{js,ts}', '**/*.spec.{js,ts}', 'tests/**/*'],
		rules: {
			'no-console': 'off',
			'@typescript-eslint/no-explicit-any': 'off'
		}
	},

	// Prettier integration (must be last)
	prettier,

	// Ignore patterns
	{
		ignores: [
			'dist/**',
			'build/**',
			'.svelte-kit/**',
			'node_modules/**',
			'coverage/**',
			'test-results/**',
			'playwright-report/**',
			'.env*',
			'*.log'
		]
	}
];
