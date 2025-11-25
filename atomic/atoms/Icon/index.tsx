/**
 * AbëONE Atomic Design System - Icon
 * 
 * Pattern: ATOM × ICON × DESIGN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { LucideIcon } from 'lucide-react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const iconVariants = cva('', {
  variants: {
    variant: {
      default: 'text-foreground',
      developer: 'text-aeBlue-400',
      creative: 'text-primary-500',
      enterprise: 'text-aeMidnight-600',
      muted: 'text-muted-foreground',
      accent: 'text-accent-600',
      success: 'text-success-600',
    },
    size: {
      xs: 'h-3 w-3',
      sm: 'h-4 w-4',
      md: 'h-5 w-5',
      lg: 'h-6 w-6',
      xl: 'h-8 w-8',
      '2xl': 'h-10 w-10',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'md',
  },
})

export interface IconProps
  extends React.SVGProps<SVGSVGElement>,
    VariantProps<typeof iconVariants> {
  icon: LucideIcon
}

const Icon = React.forwardRef<SVGSVGElement, IconProps>(
  ({ className, variant, size, icon: IconComponent, ...props }, ref) => {
    return (
      <IconComponent
        className={cn(iconVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Icon.displayName = 'Icon'

export { Icon, iconVariants }

