/**
 * AbëONE Atomic Design System - FeatureGrid
 * 
 * Pattern: ORGANISM × FEATUREGRID × SECTION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../molecules/Card'
import { Icon } from '../../atoms/Icon'
import { Text } from '../../atoms/Text'
import { cn } from '../../lib/utils'
import type { ICPVariant } from '../../tokens'
import { LucideIcon } from 'lucide-react'

export interface Feature {
  title: string
  description: string
  icon?: LucideIcon
  image?: string
}

export interface FeatureGridProps {
  features: Feature[]
  variant?: ICPVariant
  columns?: 2 | 3 | 4
  className?: string
}

const FeatureGrid = React.forwardRef<HTMLElement, FeatureGridProps>(
  ({ features, variant = 'default', columns = 3, className }, ref) => {
    const gridCols = {
      2: 'grid-cols-1 md:grid-cols-2',
      3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
      4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
    }
    
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
          <div className={cn('grid gap-8', gridCols[columns])}>
            {features.map((feature, index) => (
              <Card key={index} variant={variant}>
                <CardHeader>
                  {feature.icon && (
                    <div className="mb-4">
                      <Icon
                        icon={feature.icon}
                        variant={variant}
                        size="xl"
                      />
                    </div>
                  )}
                  {feature.image && (
                    <div className="mb-4">
                      <img
                        src={feature.image}
                        alt={feature.title}
                        className="w-12 h-12 object-contain"
                      />
                    </div>
                  )}
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    )
  }
)
FeatureGrid.displayName = 'FeatureGrid'

export { FeatureGrid }

