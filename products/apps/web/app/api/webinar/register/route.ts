/**
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
 * Webinar Registration API Route (Updated with Database)
 * 
 * Pattern: API × WEBINAR × REGISTRATION × DATABASE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (ALRAX)
 * 
 * Registers attendees for webinars with database persistence.
 * Enterprise-grade: validated, error-handled, database-integrated, rate-limited.
 */

import { NextRequest, NextResponse } from 'next/server'
import { withPublicApi } from '@/lib/middleware/api-wrapper'
import { checkRateLimit } from '@/lib/rate-limit/upstash'
import { createRegistration } from '@/lib/db/webinar'
import { webinarEmailQueue } from '@/lib/queue/bull'

/**
 * POST /api/webinar/register
 * 
 * Registers an attendee for a webinar.
 * 
 * Body: {
 *   webinarId: string (required)
 *   email: string (required, valid email)
 *   name: string (required)
 *   firstName?: string (optional)
 *   lastName?: string (optional)
 *   company?: string (optional)
 *   github?: string (optional)
 *   icp?: "developer" | "creative" (optional)
 *   headlineVariant?: number (optional, 0-4)
 *   source?: string (optional)
 * }
 */
export const POST = withPublicApi(async (request: NextRequest) => {
  try {
    // Rate limiting (spam protection)
    const clientIP = request.headers.get('x-forwarded-for')?.split(',')[0] || 
                     request.headers.get('x-real-ip') || 
                     'unknown'
    const rateLimitResult = await checkRateLimit(`${clientIP}:register`, 'registration')
    
    if (!rateLimitResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: 'Too many registration attempts. Please try again later.',
          retryAfter: Math.ceil((rateLimitResult.reset - Date.now()) / 1000),
        },
        {
          status: 429,
          headers: {
            'Retry-After': String(Math.ceil((rateLimitResult.reset - Date.now()) / 1000)),
            'X-RateLimit-Limit': String(rateLimitResult.limit),
            'X-RateLimit-Remaining': String(rateLimitResult.remaining),
            'X-RateLimit-Reset': String(Math.ceil(rateLimitResult.reset / 1000)),
          },
        }
      )
    }

    // Parse and validate request body
    const body = await request.json()
    
    const {
      webinarId,
      email,
      name,
      firstName,
      lastName,
      company,
      github,
      icp,
      headlineVariant,
      source,
    } = body

    // VALIDATION: Required fields
    if (!webinarId || !email || !name) {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required fields: webinarId, email, name',
        },
        { status: 400 }
      )
    }

    // VALIDATION: Email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid email format',
        },
        { status: 400 }
      )
    }

    // VALIDATION: ICP value
    if (icp && !['developer', 'creative'].includes(icp)) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid ICP value. Must be "developer" or "creative"',
        },
        { status: 400 }
      )
    }

    // Create registration in database
    let registration
    try {
      registration = await createRegistration({
        webinarId,
        email,
        firstName: firstName || name.split(' ')[0],
        lastName: lastName || name.split(' ').slice(1).join(' ') || undefined,
        company,
        github,
        icp: icp as 'developer' | 'creative' | undefined,
        headlineVariant: headlineVariant !== undefined ? Number(headlineVariant) : undefined,
        source: source || 'web',
      })
    } catch (error: any) {
      console.error('Registration database error:', error)
      
      // Check if it's a duplicate registration
      if (error.code === 'P2002') {
        return NextResponse.json(
          {
            success: false,
            error: 'You are already registered for this webinar',
          },
          { status: 409 }
        )
      }

      return NextResponse.json(
        {
          success: false,
          error: 'Registration failed. Please try again.',
        },
        { status: 500 }
      )
    }

    // Schedule email jobs
    try {
      // Confirmation email (immediate)
      await webinarEmailQueue.add(
        'send-confirmation',
        {
          registrationId: registration.id,
          email: registration.email,
          firstName: registration.firstName,
          webinarId: registration.webinar.webinarId,
          webinarTopic: registration.webinar.topic,
          registrationIdHuman: registration.registrationId,
        },
        {
          priority: 1,
          delay: 0,
        }
      )

      // Reminder emails (if webinar is scheduled)
      if (registration.webinar.scheduledAt) {
        const scheduledAt = new Date(registration.webinar.scheduledAt)
        const now = new Date()

        // 24h reminder
        const reminder24h = scheduledAt.getTime() - (24 * 60 * 60 * 1000)
        if (reminder24h > now.getTime()) {
          await webinarEmailQueue.add(
            'send-reminder-24h',
            {
              registrationId: registration.id,
              email: registration.email,
              firstName: registration.firstName,
              webinarId: registration.webinar.webinarId,
              webinarTopic: registration.webinar.topic,
              scheduledAt: scheduledAt.toISOString(),
            },
            {
              priority: 2,
              delay: reminder24h - now.getTime(),
            }
          )
        }

        // 3h reminder
        const reminder3h = scheduledAt.getTime() - (3 * 60 * 60 * 1000)
        if (reminder3h > now.getTime()) {
          await webinarEmailQueue.add(
            'send-reminder-3h',
            {
              registrationId: registration.id,
              email: registration.email,
              firstName: registration.firstName,
              webinarId: registration.webinar.webinarId,
              webinarTopic: registration.webinar.topic,
              scheduledAt: scheduledAt.toISOString(),
            },
            {
              priority: 2,
              delay: reminder3h - now.getTime(),
            }
          )
        }

        // 15m reminder
        const reminder15m = scheduledAt.getTime() - (15 * 60 * 1000)
        if (reminder15m > now.getTime()) {
          await webinarEmailQueue.add(
            'send-reminder-15m',
            {
              registrationId: registration.id,
              email: registration.email,
              firstName: registration.firstName,
              webinarId: registration.webinar.webinarId,
              webinarTopic: registration.webinar.topic,
              scheduledAt: scheduledAt.toISOString(),
            },
            {
              priority: 3,
              delay: reminder15m - now.getTime(),
            }
          )
        }
      }
    } catch (error: any) {
      console.error('Failed to schedule email jobs:', error)
      // Don't fail registration if email scheduling fails
      // Emails can be sent manually or retried later
    }

    // SUCCESS: Return registration confirmation
    return NextResponse.json(
      {
        success: true,
        message: 'Successfully registered for webinar',
        registrationId: registration.registrationId,
        webinarId: registration.webinar.webinarId,
        email: registration.email,
        name: `${registration.firstName} ${registration.lastName || ''}`.trim(),
        timestamp: new Date().toISOString(),
      },
      {
        status: 201,
        headers: {
          'Cache-Control': 'no-store, must-revalidate',
          'X-RateLimit-Limit': String(rateLimitResult.limit),
          'X-RateLimit-Remaining': String(rateLimitResult.remaining),
          'X-RateLimit-Reset': String(Math.ceil(rateLimitResult.reset / 1000)),
        },
      }
    )
  } catch (error: any) {
    // VERIFY: Error handling
    console.error('Webinar registration error:', error)

    // Handle JSON parse errors
    if (error instanceof SyntaxError || error.message?.includes('JSON')) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid JSON in request body',
        },
        { status: 400 }
      )
    }

    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Internal server error during registration',
      },
      { status: 500 }
    )
  }
})

/**
 * GET /api/webinar/register
 * 
 * Health check endpoint.
 */
export const GET = withPublicApi(async () => {
  return NextResponse.json(
    {
      success: true,
      message: 'Webinar registration API is operational',
      endpoints: {
        POST: '/api/webinar/register - Register attendee',
        GET: '/api/webinar/register - Health check',
      },
      features: {
        database: 'PostgreSQL with Prisma',
        rateLimiting: 'Upstash Redis',
        emailQueue: 'BullMQ',
        reminders: 'Automated (24h, 3h, 15m)',
      },
    },
    {
      headers: {
        'Cache-Control': 'no-store, must-revalidate',
      },
    }
  )
})
