/**
export const dynamic = 'force-dynamic'
 * Stripe Config API Route
 * 
 * Pattern: ABEKEYS × CONFIG × SERVER × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * CRITICAL: ABEKEYS VAULT ONLY - NEVER use .env.local
 * 
 * Returns publishable key from ABEKEYS vault (safe to expose to client)
 */

import { NextResponse } from 'next/server'
import { getStripeCredentials } from '@/lib/abekeys'

/**
 * GET /api/stripe-config
 * 
 * Returns Stripe publishable key from ABEKEYS vault
 * Safe to expose to client (publishable keys are public)
 */
export async function GET() {
  try {
    const creds = getStripeCredentials()
    
    // If publishable key not in vault, try to fetch from Stripe API
    if (!creds.publishableKey && creds.secretKey) {
      // Use secret key to retrieve account and get publishable key
      // Note: This requires Stripe API call - for now return error with instructions
      return NextResponse.json(
        { 
          error: 'Stripe publishable key not found in ABEKEYS vault',
          detail: 'Add publishable_key to ~/.abekeys/credentials/stripe.json OR fetch from Stripe Dashboard',
          hint: 'Secret key is available - checkout will work server-side'
        },
        { status: 503 }
      )
    }

    if (!creds.publishableKey) {
      return NextResponse.json(
        { 
          error: 'Stripe publishable key not found in ABEKEYS vault',
          detail: 'Add publishable_key to ~/.abekeys/credentials/stripe.json'
        },
        { status: 503 }
      )
    }

    return NextResponse.json({
      publishableKey: creds.publishableKey,
    })

  } catch (error: any) {
    console.error('[STRIPE-CONFIG] Failed to load from ABEKEYS vault:', error)
    
    return NextResponse.json(
      { 
        error: 'Failed to load Stripe config from ABEKEYS vault',
        detail: error.message || 'ABEKEYS vault not accessible'
      },
      { status: 503 }
    )
  }
}

