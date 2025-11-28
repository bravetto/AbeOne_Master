/**
 * Stripe Checkout Button Component
 * 
 * Pattern: STRIPE × CHECKOUT × CLIENT × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Latest Best Practices:
 * - Uses Stripe Checkout (hosted page - most secure)
 * - Loading states
 * - Error handling
 * - Type-safe props
 * - Accessible button
 */

'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { createCheckoutSession } from '@/lib/stripe'

interface CheckoutButtonProps {
  priceId: string
  successUrl: string
  cancelUrl: string
  children: React.ReactNode
  metadata?: Record<string, string>
  className?: string
  disabled?: boolean
}

/**
 * CheckoutButton Component
 * 
 * Best Practice: Uses Stripe Checkout (hosted page)
 * This is the most secure approach - payment details never touch our server
 */
export function CheckoutButton({
  priceId,
  successUrl,
  cancelUrl,
  children,
  metadata,
  className,
  disabled = false,
}: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCheckout = async () => {
    setLoading(true)
    setError(null)

    try {
      // Best Practice: Create session server-side, redirect to Stripe Checkout
      const checkoutUrl = await createCheckoutSession({
        priceId,
        successUrl,
        cancelUrl,
        metadata,
      })

      // Redirect to Stripe Checkout (hosted payment page)
      window.location.href = checkoutUrl

    } catch (err: any) {
      console.error('[CHECKOUT] Failed:', err)
      setError(err.message || 'Failed to start checkout. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="space-y-2">
      <Button
        onClick={handleCheckout}
        disabled={disabled || loading}
        className={className}
        aria-label="Proceed to checkout"
      >
        {loading ? 'Processing...' : children}
      </Button>
      
      {error && (
        <p className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

