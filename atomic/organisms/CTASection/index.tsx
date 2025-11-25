/**
 * AbëONE Atomic Design System - CTASection
 * 
 * Pattern: ORGANISM × CTASECTION × SECTION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { CTAButton } from '../../molecules/CTAButton'
import { Text } from '../../atoms/Text'
import { cn } from '../../lib/utils'
import type { ICPVariant } from '../../tokens'
import type { CTAConfig } from '../../hooks/useCTAHierarchy'

export interface CTASectionProps {
  headline: string
  subheadline?: string
  primaryCTA: CTAConfig
  secondaryCTA?: CTAConfig
  variant?: ICPVariant
  className?: string
}

const CTASection = React.forwardRef<HTMLElement, CTASectionProps>(
  ({ headline, subheadline, primaryCTA, secondaryCTA, variant = 'default', className }, ref) => {
    return (
      <section
        ref={ref as any}
        className={cn(
          'py-20 px-4 sm:px-6 lg:px-8',
          variant === 'developer' && 'bg-aeMidnight-800',
          variant === 'creative' && 'bg-gradient-to-r from-primary-500 to-secondary-500',
          variant === 'enterprise' && 'bg-aeMidnight-700',
          variant === 'default' && 'bg-primary-600',
          className
        )}
      >
        <div className="max-w-4xl mx-auto text-center">
          <Text
            as="h2"
            variant={variant === 'creative' ? 'default' : variant === 'developer' ? 'developer' : 'default'}
            size="4xl"
            weight="bold"
            className={cn(
              'mb-4',
              (variant === 'creative' || variant === 'default') && 'text-white',
              variant === 'developer' && 'text-aeBlue-50',
              variant === 'enterprise' && 'text-white'
            )}
          >
            {headline}
          </Text>
          
          {subheadline && (
            <Text
              variant={variant === 'creative' ? 'default' : variant === 'developer' ? 'developer' : 'default'}
              size="lg"
              className={cn(
                'mb-8 max-w-2xl mx-auto',
                (variant === 'creative' || variant === 'default') && 'text-white/90',
                variant === 'developer' && 'text-aeBlue-100',
                variant === 'enterprise' && 'text-white/90'
              )}
            >
              {subheadline}
            </Text>
          )}
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <CTAButton
              variant={variant === 'default' ? undefined : variant}
              size="xl"
              label={primaryCTA.label}
              href={primaryCTA.href}
              onClick={primaryCTA.onClick}
              icon={primaryCTA.icon}
              className={cn(
                variant === 'creative' && 'bg-white text-primary-600 hover:bg-gray-100',
                variant === 'developer' && 'bg-aeBlue-500 text-white hover:bg-aeBlue-600',
                variant === 'enterprise' && 'bg-white text-aeMidnight-700 hover:bg-gray-100'
              )}
            />
            {secondaryCTA && (
              <CTAButton
                variant="outline"
                size="xl"
                label={secondaryCTA.label}
                href={secondaryCTA.href}
                onClick={secondaryCTA.onClick}
                icon={secondaryCTA.icon}
                className={cn(
                  variant === 'creative' && 'border-white text-white hover:bg-white/10',
                  variant === 'developer' && 'border-aeBlue-400 text-aeBlue-50 hover:bg-aeBlue-500/20',
                  variant === 'enterprise' && 'border-white text-white hover:bg-white/10'
                )}
              />
            )}
          </div>
        </div>
      </section>
    )
  }
)
CTASection.displayName = 'CTASection'

export { CTASection }

