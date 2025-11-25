/**
 * AbëBEATs Checkout Component
 * 
 * Pattern: ABEBEATS × CHECKOUT × REVENUE × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Revenue Potential: $5K-$50K/week
 * 
 * Latest Best Practices:
 * - Clear pricing display
 * - Value proposition
 * - Secure checkout flow
 * - Mobile-responsive
 */

'use client'

import { CheckoutButton } from './CheckoutButton'
import { Card } from '@/components/ui/card'

interface AbebeatsCheckoutProps {
  priceId: string
  variant?: 'truice' | 'standard'
}

/**
 * AbëBEATs Checkout Component
 * 
 * Ready for immediate revenue generation
 */
export function AbebeatsCheckout({ 
  priceId, 
  variant = 'standard' 
}: AbebeatsCheckoutProps) {
  const productInfo = {
    truice: {
      name: 'AbëBEATsTRU Music Video',
      description: 'Professional music video generation with TRUICE variant',
      price: '$500-$5,000',
      features: [
        'High-quality video generation',
        'TRUICE variant included',
        'VEO31 integration',
        'Professional output',
      ],
    },
    standard: {
      name: 'AbëBEATs Music Video',
      description: 'Professional music video generation',
      price: '$500-$5,000',
      features: [
        'High-quality video generation',
        'Custom styling',
        'Professional output',
        'Fast turnaround',
      ],
    },
  }

  const info = productInfo[variant]

  return (
    <Card className="p-8 space-y-6">
      <div className="space-y-4">
        <h2 className="text-3xl font-bold">{info.name}</h2>
        <p className="text-lg text-gray-600">{info.description}</p>
        
        <div className="space-y-2">
          <p className="text-2xl font-semibold text-lux-600">
            {info.price}
          </p>
          <p className="text-sm text-gray-500">
            Value: $500-$5,000 | Cost: $9-$15
          </p>
        </div>

        <ul className="space-y-2">
          {info.features.map((feature, index) => (
            <li key={index} className="flex items-start">
              <span className="text-green-600 mr-2">✓</span>
              <span>{feature}</span>
            </li>
          ))}
        </ul>
      </div>

      <CheckoutButton
        priceId={priceId}
        successUrl={`${window.location.origin}/products/abebeats/success?session_id={CHECKOUT_SESSION_ID}`}
        cancelUrl={`${window.location.origin}/products/abebeats`}
        metadata={{
          product: 'abebeats',
          variant: variant,
        }}
        className="w-full"
      >
        Generate Music Video
      </CheckoutButton>
    </Card>
  )
}

