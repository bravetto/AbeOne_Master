/**
 * AbëONE Atomic Design System - CTAButton
 * 
 * Pattern: MOLECULE × CTABUTTON × COMPOSITION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Button, type ButtonProps } from '../../atoms/Button'
import { Icon, type IconProps } from '../../atoms/Icon'
import { Loader2 } from 'lucide-react'
import { cn } from '../../lib/utils'

export interface CTAButtonProps extends ButtonProps {
  label: string
  icon?: React.ReactNode
  loading?: boolean
  loadingText?: string
  iconPosition?: 'left' | 'right'
}

const CTAButton = React.forwardRef<HTMLButtonElement, CTAButtonProps>(
  ({ label, icon, loading = false, loadingText, iconPosition = 'left', className, children, ...props }, ref) => {
    const content = loading ? (loadingText || 'Loading...') : label
    
    return (
      <Button
        ref={ref}
        disabled={loading || props.disabled}
        className={cn('relative', className)}
        {...props}
      >
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin mr-2" />
        ) : icon && iconPosition === 'left' ? (
          <span className="mr-2">{icon}</span>
        ) : null}
        {content}
        {!loading && icon && iconPosition === 'right' && (
          <span className="ml-2">{icon}</span>
        )}
        {children}
      </Button>
    )
  }
)
CTAButton.displayName = 'CTAButton'

export { CTAButton }

