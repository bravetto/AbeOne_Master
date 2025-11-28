/**
 * AbëONE Atomic Design System - TestimonialCard
 * 
 * Pattern: MOLECULE × TESTIMONIALCARD × COMPOSITION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Card, CardContent, CardHeader } from '../Card'
import { Text } from '../../atoms/Text'
import { Image } from '../../atoms/Image'
import { cn } from '../../lib/utils'

export interface TestimonialCardProps {
  quote: string
  author: {
    name: string
    role?: string
    company?: string
    avatar?: string
  }
  rating?: number
  variant?: 'default' | 'developer' | 'creative' | 'enterprise'
  className?: string
}

const TestimonialCard = React.forwardRef<HTMLDivElement, TestimonialCardProps>(
  ({ quote, author, rating, variant = 'default', className }, ref) => {
    return (
      <Card variant={variant} ref={ref} className={cn('', className)}>
        <CardContent className="pt-6">
          {rating && (
            <div className="flex mb-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <span
                  key={i}
                  className={cn(
                    'text-lg',
                    i < rating ? 'text-secondary-500' : 'text-muted-foreground'
                  )}
                >
                  
                </span>
              ))}
            </div>
          )}
          <Text
            as="blockquote"
            size="base"
            className="mb-4 italic"
          >
            "{quote}"
          </Text>
          <div className="flex items-center gap-3">
            {author.avatar && (
              <Image
                src={author.avatar}
                alt={author.name}
                size="sm"
                rounded="full"
                className="flex-shrink-0"
              />
            )}
            <div>
              <Text weight="semibold" size="sm">
                {author.name}
              </Text>
              {(author.role || author.company) && (
                <Text variant="muted" size="xs">
                  {author.role}
                  {author.role && author.company && ', '}
                  {author.company}
                </Text>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)
TestimonialCard.displayName = 'TestimonialCard'

export { TestimonialCard }

