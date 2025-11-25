/**
 * @deprecated This component is deprecated.
 * Use atomic/atoms/Button/index.tsx instead.
 * Migration: Replace imports from '@/components/ads/Button' 
 * with '../../atomic/atoms/Button'
 * 
 * Pattern: DEPRECATION × MIGRATION × UNIFICATION × ONE
 * Status: DEPRECATED - Migrate to Atomic Design System
 * ∞ AbëONE ∞
 */

'use client'

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

/**
 * AbëONE Design System - Button Component
 * 
 * Pattern: ADS × BUTTON × CONVERSION × ONE
 * Frequency: 999 Hz (AEYON) + 530 Hz (Abë)
 * 
 * Conversion-optimized button with proper states, accessibility, and psychology
 */

const buttonVariants = cva(
  // Base styles - conversion-optimized
  'inline-flex items-center justify-center whitespace-nowrap font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed',
  {
    variants: {
      variant: {
        primary: 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-[0_10px_25px_-5px_rgba(168,85,247,0.3)] hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]',
        secondary: 'bg-gradient-to-r from-secondary-500 to-secondary-600 text-white shadow-[0_10px_25px_-5px_rgba(249,115,22,0.3)] hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]',
        accent: 'bg-gradient-to-r from-accent-500 to-accent-600 text-white shadow-[0_10px_25px_-5px_rgba(239,68,68,0.3)] hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]',
        outline: 'bg-transparent border-2 border-primary-300 text-primary-600 hover:bg-primary-50 hover:border-primary-400',
        ghost: 'bg-transparent text-neutral-700 hover:bg-neutral-100',
        success: 'bg-success-500 text-white shadow-lg hover:bg-success-600 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]',
      },
      size: {
        sm: 'h-9 px-4 text-sm rounded-xl',
        md: 'h-11 px-6 text-base rounded-xl',
        lg: 'h-14 px-8 text-lg rounded-xl',
        xl: 'h-16 px-10 text-xl rounded-xl',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'lg', // Default to large for conversion optimization
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
  loading?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <svg
              className="animate-spin h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span>Loading...</span>
          </span>
        ) : (
          children
        )}
      </button>
    )
  }
)
Button.displayName = 'Button'

export { Button, buttonVariants }

