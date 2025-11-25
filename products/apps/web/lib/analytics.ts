/**
 * Analytics Tracking Library
 * PostHog integration for comprehensive event tracking
 * 
 * Pattern: Analytics × Measurement × Optimization × ONE
 * Guardians: ZERO (777 Hz) × AEYON (999 Hz)
 */

export interface AnalyticsEvent {
  event: string
  properties?: Record<string, any>
}

class Analytics {
  private posthog: any = null
  private initialized = false

  init() {
    if (typeof window === 'undefined' || this.initialized) return

    // Dynamically import PostHog to avoid SSR issues
    import('posthog-js').then((posthogModule) => {
      const posthog = posthogModule.default

      if (process.env.NEXT_PUBLIC_POSTHOG_KEY) {
        posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
          api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
          loaded: (ph: any) => {
            if (process.env.NODE_ENV === 'development') {
              ph.debug()
            }
          },
          capture_pageview: false, // We'll capture manually
          capture_pageleave: true
        })
        this.posthog = posthog
        this.initialized = true
      } else {
        console.warn('PostHog key not found. Analytics disabled.')
      }
    }).catch((error) => {
      console.warn('PostHog not available. Analytics disabled.', error)
    })
  }

  capture(event: string, properties?: Record<string, any>) {
    if (typeof window === 'undefined') return

    if (!this.initialized) {
      this.init()
      // Retry after initialization
      setTimeout(() => {
        if (this.posthog) {
          this.posthog.capture(event, properties)
        }
      }, 500)
      return
    }

    if (this.posthog) {
      this.posthog.capture(event, properties)
    } else {
      // Fallback: log to console in development
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics]', event, properties)
      }
    }
  }

  identify(userId: string, properties?: Record<string, any>) {
    if (typeof window === 'undefined' || !this.initialized) return

    if (this.posthog) {
      this.posthog.identify(userId, properties)
    }
  }

  reset() {
    if (typeof window === 'undefined' || !this.initialized) return

    if (this.posthog) {
      this.posthog.reset()
    }
  }
}

export const analytics = new Analytics()

// Initialize on import
if (typeof window !== 'undefined') {
  analytics.init()
}

