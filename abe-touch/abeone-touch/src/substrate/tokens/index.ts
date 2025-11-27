/**
 * AbëONE Design Tokens
 * 
 * The DNA of the interface. Every color, shadow, and animation
 * derives from these foundational values.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

// =============================================================================
// COLOR TOKENS
// =============================================================================

export const colors = {
  // Brand
  primary: {
    50: '#ecfeff',
    100: '#cffafe',
    200: '#a5f3fc',
    300: '#67e8f9',
    400: '#22d3ee',
    500: '#06b6d4', // Main
    600: '#0891b2',
    700: '#0e7490',
    800: '#155e75',
    900: '#164e63',
  },
  accent: {
    50: '#faf5ff',
    100: '#f3e8ff',
    200: '#e9d5ff',
    300: '#d8b4fe',
    400: '#c084fc',
    500: '#a855f7', // Main
    600: '#9333ea',
    700: '#7c3aed',
    800: '#6b21a8',
    900: '#581c87',
  },
  
  // Semantic
  success: '#22c55e',
  warning: '#eab308',
  error: '#ef4444',
  
  // Neutrals - Dark Theme
  dark: {
    surface: '#1a1a2e',
    background: '#0f0f1a',
    elevated: '#252540',
    border: 'rgba(255, 255, 255, 0.1)',
    text: {
      primary: '#ffffff',
      secondary: '#a0a0b0',
      muted: '#606070',
    },
  },
  
  // Neutrals - Light Theme
  light: {
    surface: '#e0e5ec',
    background: '#d1d9e6',
    elevated: '#f0f5fc',
    border: 'rgba(0, 0, 0, 0.1)',
    text: {
      primary: '#1a1a2e',
      secondary: '#4a4a5a',
      muted: '#8a8a9a',
    },
  },
} as const;

// =============================================================================
// NEUROMORPHIC SHADOWS
// =============================================================================

export const neuShadows = {
  dark: {
    light: 'rgba(255, 255, 255, 0.05)',
    dark: 'rgba(0, 0, 0, 0.5)',
  },
  light: {
    light: 'rgba(255, 255, 255, 0.8)',
    dark: 'rgba(0, 0, 0, 0.15)',
  },
} as const;

// =============================================================================
// SPACING
// =============================================================================

export const spacing = {
  0: '0',
  1: '0.25rem',
  2: '0.5rem',
  3: '0.75rem',
  4: '1rem',
  5: '1.25rem',
  6: '1.5rem',
  8: '2rem',
  10: '2.5rem',
  12: '3rem',
  16: '4rem',
  20: '5rem',
  24: '6rem',
} as const;

// =============================================================================
// TYPOGRAPHY
// =============================================================================

export const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, -apple-system, sans-serif',
    mono: 'JetBrains Mono, Fira Code, monospace',
  },
  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
    '5xl': ['3rem', { lineHeight: '1' }],
    '6xl': ['3.75rem', { lineHeight: '1' }],
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
} as const;

// =============================================================================
// ANIMATION
// =============================================================================

export const animation = {
  duration: {
    fast: '150ms',
    normal: '300ms',
    slow: '500ms',
    slower: '1000ms',
  },
  easing: {
    default: 'cubic-bezier(0.4, 0, 0.2, 1)',
    in: 'cubic-bezier(0.4, 0, 1, 1)',
    out: 'cubic-bezier(0, 0, 0.2, 1)',
    inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

// =============================================================================
// CSS VARIABLES GENERATOR
// =============================================================================

export const getCSSVariables = (theme: 'dark' | 'light') => {
  const c = theme === 'dark' ? colors.dark : colors.light;
  const s = theme === 'dark' ? neuShadows.dark : neuShadows.light;
  
  return `
    --abe-surface: ${c.surface};
    --abe-background: ${c.background};
    --abe-elevated: ${c.elevated};
    --abe-border: ${c.border};
    --abe-primary: ${colors.primary[500]};
    --abe-accent: ${colors.accent[500]};
    --abe-success: ${colors.success};
    --abe-warning: ${colors.warning};
    --abe-error: ${colors.error};
    --abe-text-primary: ${c.text.primary};
    --abe-text-secondary: ${c.text.secondary};
    --abe-text-muted: ${c.text.muted};
    --neu-shadow-light: ${s.light};
    --neu-shadow-dark: ${s.dark};
  `;
};

// =============================================================================
// EXPORTS
// =============================================================================

export const tokens = {
  colors,
  neuShadows,
  spacing,
  typography,
  animation,
  getCSSVariables,
};

export default tokens;
