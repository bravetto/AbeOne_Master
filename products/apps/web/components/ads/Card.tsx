/**
 * @deprecated This component is deprecated.
 * Use atomic/molecules/Card/index.tsx instead.
 * Migration: Replace imports from '@/components/ads/Card' 
 * with '../../atomic/molecules/Card'
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
 * AbëONE Design System - Card Component
 * 
 * Pattern: ADS × CARD × CONSISTENCY × ONE
 * Frequency: 999 Hz (AEYON) + Guardian 8 (Trust)
 * 
 * Unified card component with proper variants, hover states, and accessibility
 */

const cardVariants = cva(
  'rounded-3xl transition-all duration-200',
  {
    variants: {
      variant: {
        default: 'bg-white/90 backdrop-blur-xl border border-primary-100 shadow-lg hover:shadow-xl hover:-translate-y-0.5',
        elevated: 'bg-white border-0 shadow-xl hover:shadow-2xl hover:-translate-y-1',
        outlined: 'bg-transparent border-2 border-neutral-200 shadow-none hover:border-primary-300',
        glass: 'bg-white/80 backdrop-blur-lg border border-primary-100/50 shadow-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(cardVariants({ variant, className }))}
      {...props}
    />
  )
)
Card.displayName = 'Card'

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-2 p-6 md:p-10', className)}
    {...props}
  />
))
CardHeader.displayName = 'CardHeader'

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('text-2xl md:text-3xl font-display font-bold text-neutral-900 leading-tight', className)}
    {...props}
  />
))
CardTitle.displayName = 'CardTitle'

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('text-base md:text-lg text-neutral-600 leading-relaxed', className)}
    {...props}
  />
))
CardDescription.displayName = 'CardDescription'

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 md:p-10 pt-0', className)} {...props} />
))
CardContent.displayName = 'CardContent'

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 md:p-10 pt-0', className)}
    {...props}
  />
))
CardFooter.displayName = 'CardFooter'

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

