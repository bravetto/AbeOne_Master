/**
 * Vermillion Design System
 * 
 * Pattern: COLOR × DESIGN × SYSTEM × ETERNAL × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × ∞ (Eternal)
 * 
 * Eternal design system with vermillion colors.
 * Forever design consistency.
 */

/**
 * Vermillion color tokens
 */
export const vermillionColors = {
  // Standard sRGB
  standard: {
    vermillion: '#E73121',
    vermillionDark: '#B82618',
    vermillionLight: '#FF4A3A',
  },
  
  // P3 wide-gamut (vibrant)
  vibrant: {
    vermillion: 'color(display-p3 0.98 0.22 0.12)',
    vermillionDark: 'color(display-p3 0.75 0.18 0.10)',
    vermillionLight: 'color(display-p3 1.0 0.30 0.20)',
  },
  
  // Pure (maximum saturation)
  pure: {
    vermillion: 'color(display-p3 0.98 0.22 0.12)',
    vermillionDark: 'color(display-p3 0.75 0.18 0.10)',
    vermillionLight: 'color(display-p3 1.0 0.30 0.20)',
  },
} as const

/**
 * Design tokens
 */
export const designTokens = {
  colors: {
    vermillion: vermillionColors,
    background: {
      landing: 'var(--background-landing)',
      dashboard: 'var(--background-dashboard)',
    },
  },
  gradients: {
    healing: 'linear-gradient(135deg, var(--vermillion-pop) 0%, var(--vermillion-vibrant) 100%)',
  },
  typography: {
    heading: {
      fontFamily: 'var(--font-heading)',
      gradient: 'text-gradient-healing',
    },
  },
} as const

/**
 * Get vermillion color with fallback
 */
export function getVermillionColor(variant: 'standard' | 'vibrant' | 'pure' = 'vibrant'): string {
  // SAFETY: Return vermillion color with P3 fallback
  const color = vermillionColors[variant].vermillion
  
  if (variant === 'vibrant' || variant === 'pure') {
    // P3 with sRGB fallback
    return `${vermillionColors.standard.vermillion}; ${color}`
  }
  
  return color
}

/**
 * Design system configuration
 */
export const designSystem = {
  colors: designTokens.colors,
  gradients: designTokens.gradients,
  typography: designTokens.typography,
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '1rem',
  },
} as const

