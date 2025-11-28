/**
 * AbëONE Atomic Design System - PricingTable
 * 
 * Pattern: ORGANISM × PRICINGTABLE × SECTION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../../molecules/Card'
import { Button } from '../../atoms/Button'
import { Badge } from '../../atoms/Badge'
import { Text } from '../../atoms/Text'
import { cn } from '../../lib/utils'
import type { ICPVariant } from '../../tokens'

export interface PricingTier {
  name: string
  price: string
  period?: string
  description?: string
  features: string[]
  cta: {
    label: string
    href?: string
    onClick?: () => void
  }
  popular?: boolean
  badge?: string
}

export interface PricingTableProps {
  tiers: PricingTier[]
  variant?: ICPVariant
  className?: string
}

const PricingTable = React.forwardRef<HTMLElement, PricingTableProps>(
  ({ tiers, variant = 'default', className }, ref) => {
    return (
      <section
        ref={ref as any}
        className={cn(
          'py-20 px-4 sm:px-6 lg:px-8',
          variant === 'developer' && 'bg-aeMidnight-900',
          variant === 'creative' && 'bg-white',
          variant === 'enterprise' && 'bg-gray-50',
          variant === 'default' && 'bg-background',
          className
        )}
      >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <Text as="h2" variant={variant} size="4xl" weight="bold" className="mb-4">
              Pricing
            </Text>
            <Text variant="muted" size="lg" className="max-w-2xl mx-auto">
              Choose the plan that's right for you
            </Text>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {tiers.map((tier, index) => (
              <Card
                key={index}
                variant={variant}
                className={cn(
                  'relative',
                  tier.popular && 'border-2 border-primary-500 shadow-lg scale-105'
                )}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <Badge variant="default">Most Popular</Badge>
                  </div>
                )}
                
                {tier.badge && (
                  <div className="absolute top-4 right-4">
                    <Badge variant="info">{tier.badge}</Badge>
                  </div>
                )}
                
                <CardHeader>
                  <CardTitle>{tier.name}</CardTitle>
                  <div className="mt-4">
                    <span className="text-4xl font-bold">{tier.price}</span>
                    {tier.period && (
                      <Text variant="muted" size="sm" className="inline ml-2">
                        /{tier.period}
                      </Text>
                    )}
                  </div>
                  {tier.description && (
                    <CardDescription className="mt-2">
                      {tier.description}
                    </CardDescription>
                  )}
                </CardHeader>
                
                <CardContent>
                  <ul className="space-y-3">
                    {tier.features.map((feature, i) => (
                      <li key={i} className="flex items-start">
                        <span className="text-success-500 mr-2"></span>
                        <Text size="sm">{feature}</Text>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                
                <CardFooter>
                  <Button
                    variant={tier.popular ? variant === 'default' ? undefined : variant : 'outline'}
                    size="lg"
                    className="w-full"
                    onClick={tier.cta.onClick}
                  >
                    {tier.cta.label}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>
    )
  }
)
PricingTable.displayName = 'PricingTable'

export { PricingTable }

