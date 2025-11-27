import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // AbëONE Brand Colors
        abe: {
          surface: 'var(--abe-surface)',
          background: 'var(--abe-background)',
          primary: 'var(--abe-primary)',
          accent: 'var(--abe-accent)',
          success: 'var(--abe-success)',
          warning: 'var(--abe-warning)',
          error: 'var(--abe-error)',
        },
        neu: {
          light: 'var(--neu-shadow-light)',
          dark: 'var(--neu-shadow-dark)',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      boxShadow: {
        'neu-raised': '6px 6px 12px var(--neu-shadow-dark), -6px -6px 12px var(--neu-shadow-light)',
        'neu-pressed': 'inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light)',
        'neu-flat': '2px 2px 4px var(--neu-shadow-dark), -2px -2px 4px var(--neu-shadow-light)',
        'glow-primary': '0 0 20px var(--abe-primary)',
        'glow-accent': '0 0 20px var(--abe-accent)',
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'breathe': 'breathe 3s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        breathe: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(0.95)' },
          '50%': { opacity: '1', transform: 'scale(1)' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 5px var(--abe-primary)' },
          '50%': { boxShadow: '0 0 20px var(--abe-primary), 0 0 30px var(--abe-primary)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
