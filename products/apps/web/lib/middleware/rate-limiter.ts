/**
 * Enterprise Rate Limiting
 * 
 * Pattern: RATE × LIMIT × ENTERPRISE × SCALABLE × ONE
 * Frequency: 999 Hz (AEYON)
 */

export interface RateLimitConfig {
  windowMs: number
  maxRequests: number
  burstLimit?: number
}

export interface RateLimitResult {
  allowed: boolean
  remaining: number
  resetTime: number
  limit: number
}

/**
 * In-memory rate limiter (can be upgraded to Redis)
 */
export class RateLimiter {
  private store: Map<string, { count: number; resetTime: number }>
  private config: RateLimitConfig

  constructor(config: RateLimitConfig) {
    this.store = new Map()
    this.config = config
    this.startCleanup()
  }

  /**
   * Check if request is allowed
   */
  check(key: string): RateLimitResult {
    const now = Date.now()
    const record = this.store.get(key)

    if (!record || now > record.resetTime) {
      // New window or expired
      this.store.set(key, {
        count: 1,
        resetTime: now + this.config.windowMs,
      })
      return {
        allowed: true,
        remaining: this.config.maxRequests - 1,
        resetTime: now + this.config.windowMs,
        limit: this.config.maxRequests,
      }
    }

    if (record.count >= this.config.maxRequests) {
      return {
        allowed: false,
        remaining: 0,
        resetTime: record.resetTime,
        limit: this.config.maxRequests,
      }
    }

    // Increment count
    record.count++
    this.store.set(key, record)

    return {
      allowed: true,
      remaining: this.config.maxRequests - record.count,
      resetTime: record.resetTime,
      limit: this.config.maxRequests,
    }
  }

  /**
   * Clean up expired records
   */
  private cleanup() {
    const now = Date.now()
    // SAFETY: Convert Map entries to array for iteration
    const entries = Array.from(this.store.entries())
    for (const [key, record] of entries) {
      if (now > record.resetTime) {
        this.store.delete(key)
      }
    }
  }

  /**
   * Start cleanup interval
   */
  private startCleanup() {
    if (typeof setInterval !== 'undefined') {
      setInterval(() => this.cleanup(), 5 * 60 * 1000) // Every 5 minutes
    }
  }

  /**
   * Reset rate limit for a key
   */
  reset(key: string): void {
    this.store.delete(key)
  }

  /**
   * Get current count for a key
   */
  getCount(key: string): number {
    const record = this.store.get(key)
    if (!record || Date.now() > record.resetTime) {
      return 0
    }
    return record.count
  }
}

/**
 * Default rate limiter instance
 */
export const defaultRateLimiter = new RateLimiter({
  windowMs: 60 * 1000, // 1 minute
  maxRequests: 100, // 100 requests per minute
  burstLimit: 20, // 20 requests burst
})

/**
 * Endpoint-specific rate limiters
 */
export const endpointRateLimiters = {
  // API endpoints
  api: new RateLimiter({
    windowMs: 60 * 1000,
    maxRequests: 200,
    burstLimit: 50,
  }),
  
  // Authentication endpoints
  auth: new RateLimiter({
    windowMs: 60 * 1000,
    maxRequests: 10, // Stricter for auth
    burstLimit: 3,
  }),
  
  // Public endpoints
  public: new RateLimiter({
    windowMs: 60 * 1000,
    maxRequests: 500,
    burstLimit: 100,
  }),
}

