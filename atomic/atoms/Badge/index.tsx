/**
 * AbëONE Atomic Design System - Badge
 * 
 * Pattern: ATOM × BADGE × DESIGN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary-500 text-white hover:bg-primary-600',
        developer: 'border-transparent bg-aeBlue-600 text-white hover:bg-aeBlue-700 font-mono',
        creative: 'border-transparent bg-gradient-to-r from-primary-400 to-secondary-400 text-white',
        enterprise: 'border-transparent bg-aeMidnight-700 text-white hover:bg-aeMidnight-800',
        success: 'border-transparent bg-success-500 text-white hover:bg-success-600',
        warning: 'border-transparent bg-secondary-500 text-white hover:bg-secondary-600',
        error: 'border-transparent bg-accent-500 text-white hover:bg-accent-600',
        info: 'border-transparent bg-aeBlue-500 text-white hover:bg-aeBlue-600',
        outline: 'text-foreground border-input',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }

