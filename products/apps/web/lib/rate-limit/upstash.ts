/**
 * Upstash Redis Rate Limiting
 * Pattern: RATE_LIMIT × UPSTASH × REDIS × ONE
 */

import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const redis =
  process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN
    ? new Redis({
        url: process.env.UPSTASH_REDIS_REST_URL,
        token: process.env.UPSTASH_REDIS_REST_TOKEN,
      })
    : null

export const rateLimiters = {
  public: redis
    ? new Ratelimit({
        redis,
        limiter: Ratelimit.slidingWindow(100, '1 m'),
        analytics: true,
      })
    : null,
  api: redis
    ? new Ratelimit({
        redis,
        limiter: Ratelimit.slidingWindow(50, '1 m'),
        analytics: true,
      })
    : null,
  auth: redis
    ? new Ratelimit({
        redis,
        limiter: Ratelimit.slidingWindow(10, '1 m'),
        analytics: true,
      })
    : null,
  registration: redis
    ? new Ratelimit({
        redis,
        limiter: Ratelimit.slidingWindow(5, '5 m'),
        analytics: true,
      })
    : null,
}

class InMemoryRateLimiter {
  private limits: Map<string, { count: number; resetAt: number }> = new Map()

  async limit(key: string, max: number, window: number) {
    const now = Date.now()
    const record = this.limits.get(key)

    if (!record || now > record.resetAt) {
      this.limits.set(key, { count: 1, resetAt: now + window })
      return {
        success: true,
        limit: max,
        remaining: max - 1,
        reset: record?.resetAt || now + window,
      }
    }

    if (record.count >= max) {
      return { success: false, limit: max, remaining: 0, reset: record.resetAt }
    }

    record.count++
    return {
      success: true,
      limit: max,
      remaining: max - record.count,
      reset: record.resetAt,
    }
  }
}

const fallbackLimiter = new InMemoryRateLimiter()

export async function checkRateLimit(
  identifier: string,
  type: 'public' | 'api' | 'auth' | 'registration' = 'public'
) {
  const limiter = rateLimiters[type]

  if (!limiter) {
    const window = type === 'registration' ? 5 * 60 * 1000 : 60 * 1000
    const max =
      type === 'registration' ? 5 : type === 'auth' ? 10 : type === 'api' ? 50 : 100
    return fallbackLimiter.limit(identifier, max, window)
  }

  const result = await limiter.limit(identifier)
  return {
    success: result.success,
    limit: result.limit,
    remaining: result.remaining,
    reset: result.reset,
  }
}
