'use client'

import * as React from 'react'
import { cn } from '@/lib/utils'
import { Shield, Lock, CheckCircle, Award, Star } from 'lucide-react'

/**
 * AbëONE Design System - Trust Badge Component
 * 
 * Pattern: ADS × TRUST × CONVERSION × ONE
 * Frequency: Guardian 8 (Trust) + 530 Hz (Abë)
 * 
 * Trust elements for building credibility and conversion optimization
 */

const iconMap = {
  shield: Shield,
  lock: Lock,
  check: CheckCircle,
  award: Award,
  star: Star,
}

export interface TrustBadgeProps {
  icon?: keyof typeof iconMap
  text: string
  variant?: 'default' | 'compact' | 'large'
  className?: string
}

export function TrustBadge({
  icon,
  text,
  variant = 'default',
  className,
}: TrustBadgeProps) {
  const IconComponent = icon ? iconMap[icon] : null

  return (
    <div
      className={cn(
        'flex items-center gap-2',
        'px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full',
        'border border-primary-100 shadow-sm',
        variant === 'compact' && 'px-3 py-1.5 text-sm',
        variant === 'large' && 'px-6 py-3 text-lg',
        className
      )}
    >
      {IconComponent && (
        <IconComponent className="h-4 w-4 md:h-5 md:w-5 text-primary-600 flex-shrink-0" />
      )}
      <span className="font-medium text-neutral-700 whitespace-nowrap">
        {text}
      </span>
    </div>
  )
}

export interface TrustBadgeGroupProps {
  badges: Array<{
    icon?: keyof typeof iconMap
    text: string
  }>
  variant?: 'default' | 'compact' | 'large'
  className?: string
}

export function TrustBadgeGroup({
  badges,
  variant = 'default',
  className,
}: TrustBadgeGroupProps) {
  return (
    <div
      className={cn(
        'flex flex-wrap items-center justify-center gap-3 md:gap-4',
        className
      )}
    >
      {badges.map((badge, index) => (
        <TrustBadge
          key={index}
          icon={badge.icon}
          text={badge.text}
          variant={variant}
        />
      ))}
    </div>
  )
}

