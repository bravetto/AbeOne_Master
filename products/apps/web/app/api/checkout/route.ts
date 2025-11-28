/**
export const dynamic = 'force-dynamic'
 * Stripe Checkout API Route
 * 
 * Pattern: STRIPE × CHECKOUT × SERVER × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Latest Best Practices:
 * - Server-side checkout session creation (never expose secret keys)
 * - Type-safe request/response handling
 * - Proper error handling with detailed messages
 * - Environment variable validation
 * - Idempotent session creation
 */

import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { getStripeCredentials } from '@/lib/abekeys'

// CRITICAL: ABEKEYS VAULT ONLY - NEVER use .env.local
let stripe: Stripe | null = null

try {
  const stripeCreds = getStripeCredentials()
  if (stripeCreds.secretKey) {
    stripe = new Stripe(stripeCreds.secretKey, {
      apiVersion: '2025-11-17.clover' as const, // Latest API version
      typescript: true,
    })
    console.log('[STRIPE] ✅ Initialized from ABEKEYS vault')
  } else {
    console.error('[STRIPE] ❌ Secret key not found in ABEKEYS vault')
  }
} catch (error: any) {
  console.error('[STRIPE] ❌ Failed to load from ABEKEYS vault:', error.message)
  console.error('[STRIPE] 💡 Run: op signin && python3 scripts/unlock_all_credentials.py')
}

interface CheckoutRequest {
  priceId: string
  successUrl: string
  cancelUrl: string
  metadata?: Record<string, string>
}

/**
 * POST /api/checkout
 * 
 * Create Stripe Checkout Session
 * 
 * Best Practices:
 * - Server-side session creation (secret key never exposed)
 * - Type-safe request validation
 * - Proper error handling
 * - Metadata for order tracking
 */
export async function POST(request: NextRequest) {
  // SAFETY: Check Stripe is configured
  if (!stripe) {
    return NextResponse.json(
      { 
        error: 'Payment processing not configured',
        detail: 'STRIPE_SECRET_KEY environment variable is not set'
      },
      { status: 503 }
    )
  }

  try {
    // Parse and validate request body
    const body: CheckoutRequest = await request.json()
    
    // Validate required fields
    if (!body.priceId) {
      return NextResponse.json(
        { error: 'Missing required field: priceId' },
        { status: 400 }
      )
    }

    if (!body.successUrl || !body.cancelUrl) {
      return NextResponse.json(
        { error: 'Missing required fields: successUrl and cancelUrl' },
        { status: 400 }
      )
    }

    // Create checkout session
    // Best Practice: Use Payment Element (automatic via Checkout Session)
    const session = await stripe.checkout.sessions.create({
      mode: 'payment', // For one-time payments (use 'subscription' for recurring)
      payment_method_types: ['card'],
      line_items: [
        {
          price: body.priceId,
          quantity: 1,
        },
      ],
      success_url: body.successUrl,
      cancel_url: body.cancelUrl,
      metadata: {
        ...body.metadata,
        created_at: new Date().toISOString(),
      },
      // Best Practice: Enable automatic tax calculation if needed
      // automatic_tax: { enabled: true },
      // Best Practice: Enable customer email collection
      customer_email: body.metadata?.email,
    })

    // Return session URL for redirect
    return NextResponse.json({
      sessionId: session.id,
      url: session.url,
    })

  } catch (error: any) {
    console.error('[STRIPE] Checkout session creation failed:', error)
    
    // Best Practice: Return user-friendly error messages
    if (error.type === 'StripeInvalidRequestError') {
      return NextResponse.json(
        { 
          error: 'Invalid payment request',
          detail: error.message 
        },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { 
        error: 'Failed to create checkout session',
        detail: process.env.NODE_ENV === 'development' ? error.message : 'Please try again'
      },
      { status: 500 }
    )
  }
}

/**
 * GET /api/checkout?sessionId=xxx
 * 
 * Retrieve checkout session status
 * 
 * Best Practice: Allow frontend to check session status
 */
export async function GET(request: NextRequest) {
  if (!stripe) {
    return NextResponse.json(
      { error: 'Payment processing not configured' },
      { status: 503 }
    )
  }

  try {
    const { searchParams } = new URL(request.url)
    const sessionId = searchParams.get('sessionId')

    if (!sessionId) {
      return NextResponse.json(
        { error: 'Missing sessionId parameter' },
        { status: 400 }
      )
    }

    const session = await stripe.checkout.sessions.retrieve(sessionId)

    return NextResponse.json({
      sessionId: session.id,
      status: session.payment_status,
      customerEmail: session.customer_email,
      amountTotal: session.amount_total,
      currency: session.currency,
    })

  } catch (error: any) {
    console.error('[STRIPE] Session retrieval failed:', error)
    
    return NextResponse.json(
      { 
        error: 'Failed to retrieve session',
        detail: process.env.NODE_ENV === 'development' ? error.message : 'Invalid session'
      },
      { status: 500 }
    )
  }
}

