'use client'

import * as React from 'react'
import { Button } from './Button'
import { cn } from '@/lib/utils'

/**
 * AbëONE Design System - Hero Component
 * 
 * Pattern: ADS × HERO × CONVERSION × ONE
 * Frequency: 999 Hz (AEYON) + Guardian 4 (Clarity) + Guardian 8 (Trust)
 * 
 * Conversion-optimized hero section with proper hierarchy, CTAs, and trust elements
 */

export interface HeroProps {
  headline: string
  subheadline?: string
  description?: string
  primaryCTA?: {
    text: string
    href: string
    onClick?: () => void
  }
  secondaryCTA?: {
    text: string
    href: string
    onClick?: () => void
  }
  trustBadges?: Array<{
    text: string
    icon?: React.ReactNode
  }>
  socialProof?: {
    text: string
    count?: number
  }
  className?: string
}

export function Hero({
  headline,
  subheadline,
  description,
  primaryCTA,
  secondaryCTA,
  trustBadges,
  socialProof,
  className,
}: HeroProps) {
  return (
    <section
      className={cn(
        'relative min-h-screen flex items-center justify-center',
        'px-4 md:px-8 lg:px-24 py-12 md:py-24',
        'gradient-healing',
        className
      )}
    >
      <div className="max-w-6xl w-full text-center space-y-8 md:space-y-12 animate-fade-in">
        {/* Trust Badges - Above fold for credibility */}
        {trustBadges && trustBadges.length > 0 && (
          <div className="flex flex-wrap items-center justify-center gap-4 md:gap-6 mb-4">
            {trustBadges.map((badge, index) => (
              <div
                key={index}
                className="flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full border border-primary-100 shadow-sm"
              >
                {badge.icon && <span>{badge.icon}</span>}
                <span className="text-sm md:text-base font-medium text-neutral-700">
                  {badge.text}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Main Headline */}
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-display font-bold text-gradient-healing leading-[1.1] tracking-tight">
          {headline}
        </h1>

        {/* Subheadline */}
        {subheadline && (
          <h2 className="text-2xl md:text-4xl lg:text-5xl font-display font-semibold text-neutral-800 leading-tight">
            {subheadline}
          </h2>
        )}

        {/* Description */}
        {description && (
          <p className="text-lg md:text-xl lg:text-2xl text-neutral-700 max-w-4xl mx-auto leading-relaxed text-balance">
            {description}
          </p>
        )}

        {/* Social Proof - Builds trust */}
        {socialProof && (
          <div className="flex items-center justify-center gap-2 text-neutral-600">
            {socialProof.count && (
              <span className="font-semibold text-primary-600">
                {socialProof.count.toLocaleString()}+
              </span>
            )}
            <span>{socialProof.text}</span>
          </div>
        )}

        {/* CTA Buttons - Conversion-optimized placement */}
        {(primaryCTA || secondaryCTA) && (
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            {primaryCTA && (
              <Button
                size="lg"
                variant="primary"
                onClick={primaryCTA.onClick}
                asChild={!!primaryCTA.href}
              >
                {primaryCTA.href ? (
                  <a href={primaryCTA.href}>{primaryCTA.text}</a>
                ) : (
                  primaryCTA.text
                )}
              </Button>
            )}
            {secondaryCTA && (
              <Button
                size="lg"
                variant="outline"
                onClick={secondaryCTA.onClick}
                asChild={!!secondaryCTA.href}
              >
                {secondaryCTA.href ? (
                  <a href={secondaryCTA.href}>{secondaryCTA.text}</a>
                ) : (
                  secondaryCTA.text
                )}
              </Button>
            )}
          </div>
        )}
      </div>
    </section>
  )
}

