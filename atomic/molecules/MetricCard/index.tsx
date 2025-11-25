/**
 * AbëONE Atomic Design System - MetricCard
 * 
 * Pattern: MOLECULE × METRICCARD × COMPOSITION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../Card'
import { Text } from '../../atoms/Text'
import { Icon, type IconProps } from '../../atoms/Icon'
import { cn } from '../../lib/utils'

export interface MetricCardProps {
  title: string
  value: string | number
  description?: string
  icon?: React.ReactNode
  trend?: {
    value: string | number
    direction: 'up' | 'down' | 'neutral'
  }
  variant?: 'default' | 'developer' | 'creative' | 'enterprise'
  className?: string
}

const MetricCard = React.forwardRef<HTMLDivElement, MetricCardProps>(
  ({ title, value, description, icon, trend, variant = 'default', className }, ref) => {
    const trendColors = {
      up: 'text-success-600',
      down: 'text-accent-600',
      neutral: 'text-muted-foreground',
    }
    
    return (
      <Card variant={variant} ref={ref} className={cn('', className)}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          {icon && <div className="h-4 w-4 text-muted-foreground">{icon}</div>}
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value}</div>
          {description && (
            <Text variant="muted" size="xs" className="mt-1">
              {description}
            </Text>
          )}
          {trend && (
            <div className={cn('flex items-center text-xs mt-1', trendColors[trend.direction])}>
              <span>{trend.direction === 'up' ? '↑' : trend.direction === 'down' ? '↓' : '→'}</span>
              <span className="ml-1">{trend.value}</span>
            </div>
          )}
        </CardContent>
      </Card>
    )
  }
)
MetricCard.displayName = 'MetricCard'

export { MetricCard }

