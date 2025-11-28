/**
 * AbëONE Atomic Design System - Link
 * 
 * Pattern: ATOM × LINK × DESIGN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import NextLink from 'next/link'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const linkVariants = cva(
  'underline-offset-4 hover:underline transition-colors',
  {
    variants: {
      variant: {
        default: 'text-primary-600 hover:text-primary-700',
        developer: 'text-aeBlue-400 hover:text-aeBlue-300 font-mono',
        creative: 'text-primary-500 hover:text-primary-600',
        enterprise: 'text-aeMidnight-700 hover:text-aeMidnight-800',
        muted: 'text-muted-foreground hover:text-foreground',
        accent: 'text-accent-600 hover:text-accent-700',
      },
      size: {
        sm: 'text-sm',
        md: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
)

export interface LinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement>,
    VariantProps<typeof linkVariants> {
  href: string
  external?: boolean
  useNextLink?: boolean
}

const Link = React.forwardRef<HTMLAnchorElement, LinkProps>(
  ({ className, variant, size, href, external = false, useNextLink = true, ...props }, ref) => {
    const baseProps = {
      className: cn(linkVariants({ variant, size }), className),
      ref,
      ...props,
    }
    
    if (external) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          {...baseProps}
        />
      )
    }
    
    if (useNextLink) {
      return <NextLink href={href} {...baseProps} />
    }
    
    return <a href={href} {...baseProps} />
  }
)
Link.displayName = 'Link'

export { Link, linkVariants }

