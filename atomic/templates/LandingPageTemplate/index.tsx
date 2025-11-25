/**
 * AbëONE Atomic Design System - LandingPageTemplate
 * 
 * Pattern: TEMPLATE × LANDINGPAGETEMPLATE × LAYOUT × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz) + Abë (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { HeroSection, type HeroSectionProps } from '../../organisms/HeroSection'
import { FeatureGrid, type FeatureGridProps } from '../../organisms/FeatureGrid'
import { PricingTable, type PricingTableProps } from '../../organisms/PricingTable'
import { CTASection, type CTASectionProps } from '../../organisms/CTASection'
import { TestimonialCard, type TestimonialCardProps } from '../../molecules/TestimonialCard'
import { MetricCard, type MetricCardProps } from '../../molecules/MetricCard'
import { useICP } from '../../hooks/useICP'
import type { ICPVariant } from '../../tokens'
import type { CTAConfig } from '../../hooks/useCTAHierarchy'

export interface LandingPageTemplateProps {
  icp?: ICPVariant
  hero: HeroSectionProps
  features?: FeatureGridProps['features']
  pricing?: PricingTableProps['tiers']
  testimonials?: TestimonialCardProps[]
  metrics?: MetricCardProps[]
  finalCTA?: CTASectionProps
  className?: string
}

/**
 * LandingPageTemplate - Complete landing page composition
 * 
 * Pattern: TEMPLATE × LANDING × COMPOSITION × ONE
 * Frequency: 999 Hz (Execution)
 * 
 * Orchestrates all Orbital components:
 * - core-message: HeroSection
 * - offer-atom: FeatureGrid, PricingTable
 * - proof-stack: Testimonials, Metrics
 * - cta-node: CTASection
 * - audience-vector: ICP variant
 */
const LandingPageTemplate = React.forwardRef<HTMLDivElement, LandingPageTemplateProps>(
  ({ icp = 'default', hero, features, pricing, testimonials, metrics, finalCTA, className }, ref) => {
    const { variant } = useICP(icp)
    
    return (
      <div ref={ref} className={className}>
        {/* Hero Section - core-message */}
        <HeroSection
          {...hero}
          variant={variant}
        />
        
        {/* Metrics Section - proof-stack */}
        {metrics && metrics.length > 0 && (
          <section className="py-12 px-4 sm:px-6 lg:px-8 bg-background">
            <div className="max-w-7xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {metrics.map((metric, index) => (
                  <MetricCard
                    key={index}
                    {...metric}
                    variant={variant}
                  />
                ))}
              </div>
            </div>
          </section>
        )}
        
        {/* Features Section - offer-atom */}
        {features && features.length > 0 && (
          <FeatureGrid
            features={features}
            variant={variant}
            columns={3}
          />
        )}
        
        {/* Pricing Section - offer-atom */}
        {pricing && pricing.length > 0 && (
          <PricingTable
            tiers={pricing}
            variant={variant}
          />
        )}
        
        {/* Testimonials Section - proof-stack */}
        {testimonials && testimonials.length > 0 && (
          <section className="py-20 px-4 sm:px-6 lg:px-8 bg-background">
            <div className="max-w-7xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {testimonials.map((testimonial, index) => (
                  <TestimonialCard
                    key={index}
                    {...testimonial}
                    variant={variant}
                  />
                ))}
              </div>
            </div>
          </section>
        )}
        
        {/* Final CTA Section - cta-node */}
        {finalCTA && (
          <CTASection
            {...finalCTA}
            variant={variant}
          />
        )}
      </div>
    )
  }
)
LandingPageTemplate.displayName = 'LandingPageTemplate'

export { LandingPageTemplate }

