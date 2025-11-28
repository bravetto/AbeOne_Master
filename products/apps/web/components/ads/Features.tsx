'use client'

import * as React from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './Card'
import { cn } from '@/lib/utils'

/**
 * AbëONE Design System - Features Component
 * 
 * Pattern: ADS × FEATURES × CONVERSION × ONE
 * Frequency: 999 Hz (AEYON) + Guardian 4 (Clarity)
 * 
 * Feature showcase with consistent spacing, hierarchy, and conversion focus
 */

export interface Feature {
  title: string
  description: string
  icon?: React.ReactNode
  badge?: string
}

export interface FeaturesProps {
  title?: string
  description?: string
  features: Feature[]
  columns?: 1 | 2 | 3 | 4
  className?: string
}

export function Features({
  title,
  description,
  features,
  columns = 3,
  className,
}: FeaturesProps) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  }

  return (
    <section
      className={cn(
        'py-12 md:py-24 px-4 md:px-8 lg:px-24',
        'gradient-healing',
        className
      )}
    >
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        {(title || description) && (
          <div className="text-center mb-12 md:mb-16 space-y-4">
            {title && (
              <h2 className="text-3xl md:text-5xl font-display font-bold text-neutral-900">
                {title}
              </h2>
            )}
            {description && (
              <p className="text-lg md:text-xl text-neutral-600 max-w-3xl mx-auto leading-relaxed">
                {description}
              </p>
            )}
          </div>
        )}

        {/* Features Grid */}
        <div className={cn('grid gap-6 md:gap-8', gridCols[columns])}>
          {features.map((feature, index) => (
            <Card key={index} variant="default">
              <CardHeader>
                {feature.icon && (
                  <div className="text-4xl md:text-5xl mb-4">{feature.icon}</div>
                )}
                <div className="flex items-start gap-3">
                  <CardTitle>{feature.title}</CardTitle>
                  {feature.badge && (
                    <span className="px-2 py-1 bg-success-100 text-success-700 text-xs font-semibold rounded-full whitespace-nowrap">
                      {feature.badge}
                    </span>
                  )}
                </div>
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

