/**
 * AbëONE Atomic Design System - HeroSection
 * 
 * Pattern: ORGANISM × HEROSECTION × SECTION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Text } from '../../atoms/Text'
import { Button } from '../../atoms/Button'
import { CTAButton } from '../../molecules/CTAButton'
import { Image } from '../../atoms/Image'
import { useCTAHierarchy, type CTAConfig } from '../../hooks/useCTAHierarchy'
import { cn } from '../../lib/utils'
import type { ICPVariant } from '../../tokens'

export interface HeroSectionProps {
  headline: string
  subheadline?: string
  primaryCTA?: CTAConfig
  secondaryCTA?: CTAConfig
  image?: {
    src: string
    alt: string
  }
  socialProof?: {
    text: string
    logos?: string[]
  }
  variant?: ICPVariant
  className?: string
}

const HeroSection = React.forwardRef<HTMLElement, HeroSectionProps>(
  ({ headline, subheadline, primaryCTA, secondaryCTA, image, socialProof, variant = 'default', className }, ref) => {
    const ctas = [primaryCTA, secondaryCTA].filter(Boolean) as CTAConfig[]
    const { primary, secondary, isValid } = useCTAHierarchy(ctas)
    
    if (!isValid) {
      console.warn(' HeroSection: CTA hierarchy validation failed')
    }
    
    return (
      <section
        ref={ref as any}
        className={cn(
          'relative py-20 px-4 sm:px-6 lg:px-8',
          variant === 'developer' && 'bg-aeMidnight-900',
          variant === 'creative' && 'bg-gradient-to-br from-primary-50 to-secondary-50',
          variant === 'enterprise' && 'bg-white',
          variant === 'default' && 'bg-background',
          className
        )}
      >
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <Text
                as="h1"
                variant={variant}
                size="5xl"
                weight="bold"
                className="leading-tight"
              >
                {headline}
              </Text>
              
              {subheadline && (
                <Text
                  as="p"
                  variant={variant === 'default' ? 'muted' : variant}
                  size="xl"
                  className="max-w-2xl"
                >
                  {subheadline}
                </Text>
              )}
              
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                {primary && (
                  <CTAButton
                    variant={variant === 'default' ? undefined : variant}
                    size="lg"
                    label={primary.label}
                    href={primary.href}
                    onClick={primary.onClick}
                    icon={primary.icon}
                  />
                )}
                {secondary && (
                  <Button
                    variant={variant === 'default' ? 'outline' : variant}
                    size="lg"
                    onClick={secondary.onClick}
                  >
                    {secondary.label}
                  </Button>
                )}
              </div>
              
              {socialProof && (
                <div className="pt-8">
                  <Text variant="muted" size="sm" className="mb-4">
                    {socialProof.text}
                  </Text>
                  {socialProof.logos && (
                    <div className="flex items-center gap-6 opacity-60">
                      {socialProof.logos.map((logo, i) => (
                        <Image
                          key={i}
                          src={logo}
                          alt={`Logo ${i + 1}`}
                          size="md"
                          className="grayscale"
                        />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
            
            {image && (
              <div className="relative">
                <Image
                  src={image.src}
                  alt={image.alt}
                  size="full"
                  rounded="xl"
                  variant={variant}
                  className="w-full h-auto"
                />
              </div>
            )}
          </div>
        </div>
      </section>
    )
  }
)
HeroSection.displayName = 'HeroSection'

export { HeroSection }

