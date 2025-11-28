/**
 * AbëONE Atomic Design System - Text
 * 
 * Pattern: ATOM × TEXT × DESIGN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const textVariants = cva('', {
  variants: {
    variant: {
      default: 'text-foreground',
      developer: 'text-aeBlue-50 font-mono',
      creative: 'text-primary-900',
      enterprise: 'text-aeMidnight-900',
      muted: 'text-muted-foreground',
      accent: 'text-accent-600',
      success: 'text-success-600',
      destructive: 'text-accent-600',
    },
    size: {
      xs: 'text-xs',
      sm: 'text-sm',
      base: 'text-base',
      lg: 'text-lg',
      xl: 'text-xl',
      '2xl': 'text-2xl',
      '3xl': 'text-3xl',
      '4xl': 'text-4xl',
      '5xl': 'text-5xl',
      '6xl': 'text-6xl',
    },
    weight: {
      light: 'font-light',
      normal: 'font-normal',
      medium: 'font-medium',
      semibold: 'font-semibold',
      bold: 'font-bold',
      extrabold: 'font-extrabold',
    },
    align: {
      left: 'text-left',
      center: 'text-center',
      right: 'text-right',
      justify: 'text-justify',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'base',
    weight: 'normal',
    align: 'left',
  },
})

export interface TextProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6'
}

const Text = React.forwardRef<HTMLElement, TextProps>(
  ({ className, variant, size, weight, align, as = 'p', ...props }, ref) => {
    const Comp = as
    return (
      <Comp
        className={cn(textVariants({ variant, size, weight, align, className }))}
        ref={ref as any}
        {...props}
      />
    )
  }
)
Text.displayName = 'Text'

export { Text, textVariants }

