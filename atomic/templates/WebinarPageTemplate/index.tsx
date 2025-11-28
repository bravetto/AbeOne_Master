/**
 * AbëONE Atomic Design System - WebinarPageTemplate
 * 
 * Pattern: TEMPLATE × WEBINARPAGETEMPLATE × LAYOUT × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz) + Abë (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { HeroSection, type HeroSectionProps } from '../../organisms/HeroSection'
import { FeatureGrid, type FeatureGridProps } from '../../organisms/FeatureGrid'
import { CTASection, type CTASectionProps } from '../../organisms/CTASection'
import { FormField } from '../../molecules/FormField'
import { Input } from '../../atoms/Input'
import { Button } from '../../atoms/Button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../molecules/Card'
import { useICP } from '../../hooks/useICP'
import type { ICPVariant } from '../../tokens'

export interface WebinarPageTemplateProps {
  icp?: ICPVariant
  hero: HeroSectionProps & {
    date?: string
    time?: string
    duration?: string
    speaker?: {
      name: string
      title: string
      avatar?: string
    }
  }
  features?: FeatureGridProps['features']
  registrationForm?: {
    onSubmit: (data: { name: string; email: string; company?: string }) => void
  }
  finalCTA?: CTASectionProps
  className?: string
}

/**
 * WebinarPageTemplate - Webinar registration page composition
 * 
 * Pattern: TEMPLATE × WEBINAR × COMPOSITION × ONE
 * Frequency: 999 Hz (Execution)
 * 
 * Orchestrates Orbital components for webinar pages:
 * - core-message: HeroSection with date/time/speaker
 * - offer-atom: Features, Registration form
 * - proof-stack: Speaker credentials
 * - cta-node: CTASection
 * - audience-vector: ICP variant
 */
const WebinarPageTemplate = React.forwardRef<HTMLDivElement, WebinarPageTemplateProps>(
  ({ icp = 'default', hero, features, registrationForm, finalCTA, className }, ref) => {
    const { variant } = useICP(icp)
    const [formData, setFormData] = React.useState({
      name: '',
      email: '',
      company: '',
    })
    
    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault()
      if (registrationForm?.onSubmit) {
        registrationForm.onSubmit(formData)
      }
    }
    
    return (
      <div ref={ref} className={className}>
        {/* Hero Section - core-message */}
        <HeroSection
          headline={hero.headline}
          subheadline={hero.subheadline}
          primaryCTA={hero.primaryCTA}
          secondaryCTA={hero.secondaryCTA}
          image={hero.image}
          socialProof={hero.socialProof}
          variant={variant}
        />
        
        {/* Webinar Details Card */}
        {(hero.date || hero.time || hero.duration || hero.speaker) && (
          <section className="py-12 px-4 sm:px-6 lg:px-8 bg-background">
            <div className="max-w-4xl mx-auto">
              <Card variant={variant}>
                <CardHeader>
                  <CardTitle>Webinar Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {hero.date && (
                    <div>
                      <strong>Date:</strong> {hero.date}
                    </div>
                  )}
                  {hero.time && (
                    <div>
                      <strong>Time:</strong> {hero.time}
                    </div>
                  )}
                  {hero.duration && (
                    <div>
                      <strong>Duration:</strong> {hero.duration}
                    </div>
                  )}
                  {hero.speaker && (
                    <div className="pt-4 border-t">
                      <strong>Speaker:</strong> {hero.speaker.name}
                      {hero.speaker.title && (
                        <div className="text-sm text-muted-foreground">
                          {hero.speaker.title}
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
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
        
        {/* Registration Form - offer-atom */}
        {registrationForm && (
          <section className="py-20 px-4 sm:px-6 lg:px-8 bg-background">
            <div className="max-w-2xl mx-auto">
              <Card variant={variant}>
                <CardHeader>
                  <CardTitle>Register for Webinar</CardTitle>
                  <CardDescription>
                    Fill out the form below to secure your spot
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <FormField label="Full Name" required>
                      <Input
                        variant={variant}
                        placeholder="John Doe"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        required
                      />
                    </FormField>
                    
                    <FormField label="Email" required>
                      <Input
                        variant={variant}
                        type="email"
                        placeholder="john@example.com"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        required
                      />
                    </FormField>
                    
                    <FormField label="Company (Optional)">
                      <Input
                        variant={variant}
                        placeholder="Acme Inc."
                        value={formData.company}
                        onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                      />
                    </FormField>
                    
                    <Button
                      type="submit"
                      variant={variant === 'default' ? undefined : variant}
                      size="lg"
                      className="w-full"
                    >
                      Register Now
                    </Button>
                  </form>
                </CardContent>
              </Card>
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
WebinarPageTemplate.displayName = 'WebinarPageTemplate'

export { WebinarPageTemplate }

