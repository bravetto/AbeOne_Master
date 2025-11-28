import type { Config } from 'tailwindcss';
import typography from '@tailwindcss/typography';

export default {
	// Tailwind 3.4 with optimized configuration
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/@skeletonlabs/skeleton/**/*.{html,js,svelte,ts}'
	],

	// BiasGuards brand color system
	theme: {
		extend: {
			// Justice-driven color palette
			colors: {
				// Primary brand colors
				'justice-blue': {
					50: '#eff6ff',
					100: '#dbeafe',
					200: '#bfdbfe',
					300: '#93c5fd',
					400: '#60a5fa',
					500: '#3b82f6',
					600: '#1e40af', // Primary justice blue
					700: '#1d4ed8',
					800: '#1e3a8a',
					900: '#1e3a8a',
					950: '#172554'
				},
				'alert-red': {
					50: '#fef2f2',
					100: '#fee2e2',
					200: '#fecaca',
					300: '#fca5a5',
					400: '#f87171',
					500: '#ef4444',
					600: '#dc2626', // Alert red
					700: '#b91c1c',
					800: '#991b1b',
					900: '#7f1d1d',
					950: '#450a0a'
				},
				'success-green': {
					50: '#f0fdf4',
					100: '#dcfce7',
					200: '#bbf7d0',
					300: '#86efac',
					400: '#4ade80',
					500: '#22c55e',
					600: '#16a34a', // Success green
					700: '#15803d',
					800: '#166534',
					900: '#14532d',
					950: '#052e16'
				}
			},

			// Typography system - Inter + Source Code Pro
			fontFamily: {
				sans: ['Inter', 'system-ui', 'sans-serif'],
				mono: ['Source Code Pro', 'Menlo', 'Monaco', 'monospace'],
				display: ['Inter', 'system-ui', 'sans-serif']
			},

			// 8px grid system for consistency
			spacing: {
				'0.5': '2px', // 0.25 * 8
				'1': '4px', // 0.5 * 8
				'1.5': '6px', // 0.75 * 8
				'2': '8px', // 1 * 8 (base unit)
				'2.5': '10px', // 1.25 * 8
				'3': '12px', // 1.5 * 8
				'3.5': '14px', // 1.75 * 8
				'4': '16px', // 2 * 8
				'5': '20px', // 2.5 * 8
				'6': '24px', // 3 * 8
				'7': '28px', // 3.5 * 8
				'8': '32px', // 4 * 8
				'9': '36px', // 4.5 * 8
				'10': '40px', // 5 * 8
				'11': '44px', // 5.5 * 8
				'12': '48px', // 6 * 8
				'14': '56px', // 7 * 8
				'16': '64px', // 8 * 8
				'20': '80px', // 10 * 8
				'24': '96px', // 12 * 8
				'28': '112px', // 14 * 8
				'32': '128px', // 16 * 8
				'36': '144px', // 18 * 8
				'40': '160px', // 20 * 8
				'44': '176px', // 22 * 8
				'48': '192px', // 24 * 8
				'52': '208px', // 26 * 8
				'56': '224px', // 28 * 8
				'60': '240px', // 30 * 8
				'64': '256px', // 32 * 8
				'72': '288px', // 36 * 8
				'80': '320px', // 40 * 8
				'96': '384px' // 48 * 8
			},

			// Performance-focused animations (NO layout animations)
			animation: {
				'fade-in': 'fadeIn 0.3s ease-in-out',
				'slide-up': 'slideUp 0.3s ease-out',
				'pulse-subtle': 'pulseSubtle 2s ease-in-out infinite',
				'spin-slow': 'spin 3s linear infinite'
			},

			keyframes: {
				fadeIn: {
					'0%': { opacity: '0' },
					'100%': { opacity: '1' }
				},
				slideUp: {
					'0%': { transform: 'translateY(8px)', opacity: '0' },
					'100%': { transform: 'translateY(0)', opacity: '1' }
				},
				pulseSubtle: {
					'0%, 100%': { opacity: '1' },
					'50%': { opacity: '0.8' }
				}
			},

			// Responsive breakpoints optimized for mobile-first
			screens: {
				xs: '475px',
				sm: '640px',
				md: '768px',
				lg: '1024px',
				xl: '1280px',
				'2xl': '1536px'
			}
		}
	},

	plugins: [
		// Typography plugin for enhanced text styling
		typography
	],

	// Dark mode configuration
	darkMode: 'class'
} satisfies Config;
