/**
 * Stripe Client Utilities
 * 
 * Pattern: STRIPE × CLIENT × UTILITIES × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Latest Best Practices:
 * - Lazy load Stripe.js (only load when needed)
 * - Client-side only (uses publishable key)
 * - Type-safe Stripe instance
 * - Error handling
 */

'use client'

import { loadStripe, Stripe } from '@stripe/stripe-js'

// CRITICAL: ABEKEYS VAULT ONLY - NEVER use .env.local
// Publishable key must be passed from server-side (from ABEKEYS vault)
// This is set via getServerSideProps or Server Components
let stripePublishableKey: string | undefined = undefined

// This will be set by server-side code that reads from ABEKEYS vault
export function setStripePublishableKey(key: string) {
  stripePublishableKey = key
}

if (typeof window !== 'undefined' && !stripePublishableKey) {
  console.warn('[STRIPE] Publishable key not set. Must be loaded from ABEKEYS vault server-side.')
}

// Best Practice: Lazy load Stripe.js
let stripePromise: Promise<Stripe | null> | null = null

/**
 * Get Stripe instance (lazy loaded)
 * 
 * Best Practice: Only load Stripe.js when needed
 * This improves initial page load performance
 * 
 * CRITICAL: Must load publishable key from ABEKEYS vault first
 */
export async function getStripe(): Promise<Stripe | null> {
  // Load publishable key from ABEKEYS vault if not already set
  if (!stripePublishableKey) {
    try {
      const response = await fetch('/api/stripe-config')
      if (response.ok) {
        const data = await response.json()
        stripePublishableKey = data.publishableKey
      } else {
        console.error('[STRIPE] Failed to load publishable key from ABEKEYS vault')
        return Promise.resolve(null)
      }
    } catch (error) {
      console.error('[STRIPE] Error loading publishable key:', error)
      return Promise.resolve(null)
    }
  }

  if (!stripePublishableKey) {
    return Promise.resolve(null)
  }

  if (!stripePromise) {
    stripePromise = loadStripe(stripePublishableKey, {
      // Best Practice: Use latest API version
      apiVersion: '2024-11-20.acacia',
    })
  }

  return stripePromise
}

/**
 * Create checkout session and redirect
 * 
 * Best Practice: Server-side session creation, client-side redirect
 */
export async function createCheckoutSession(params: {
  priceId: string
  successUrl: string
  cancelUrl: string
  metadata?: Record<string, string>
}): Promise<string> {
  try {
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || error.error || 'Failed to create checkout session')
    }

    const data = await response.json()
    
    if (!data.url) {
      throw new Error('No checkout URL returned')
    }

    return data.url

  } catch (error: any) {
    console.error('[STRIPE] Checkout session creation failed:', error)
    throw error
  }
}

/**
 * Check session status
 */
export async function getSessionStatus(sessionId: string) {
  try {
    const response = await fetch(`/api/checkout?sessionId=${sessionId}`)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || error.error || 'Failed to retrieve session')
    }

    return await response.json()

  } catch (error: any) {
    console.error('[STRIPE] Session status check failed:', error)
    throw error
  }
}

