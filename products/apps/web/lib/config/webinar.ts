/**
 * Webinar Infrastructure Configuration
 * Pattern: CONFIG × ABEKEYS × WEBINAR × ONE
 * ZERO EFFORT. 100% TRUST. NO .env files EVER.
 */

import {
  getDatabaseCredentials,
  getRedisCredentials,
  getSendGridCredentials,
} from '../abekeys'

export function getDatabaseUrl(): string {
  const vaultUrl = getDatabaseCredentials()
  if (vaultUrl) return vaultUrl

  const envUrl = process.env.DATABASE_URL
  if (envUrl) {
    console.warn('[CONFIG] Using DATABASE_URL from process.env. Consider adding to AbëKEYs vault.')
    return envUrl
  }

  throw new Error(
    'Database URL not found. Add to AbëKEYs vault:\n' +
    '  Run: op signin && python3 scripts/unlock_all_credentials.py\n' +
    '  Or create: ~/.abekeys/credentials/database.json'
  )
}

export function getRedisConfig(): {
  url?: string
  upstashUrl?: string
  upstashToken?: string
} {
  const vaultConfig = getRedisCredentials()
  if (vaultConfig) return vaultConfig

  const upstashUrl = process.env.UPSTASH_REDIS_REST_URL
  const upstashToken = process.env.UPSTASH_REDIS_REST_TOKEN
  const redisUrl = process.env.REDIS_URL

  if (upstashUrl && upstashToken) {
    console.warn('[CONFIG] Using Upstash Redis from process.env. Consider adding to AbëKEYs vault.')
    return { upstashUrl, upstashToken }
  }

  if (redisUrl) {
    console.warn('[CONFIG] Using Redis URL from process.env. Consider adding to AbëKEYs vault.')
    return { url: redisUrl }
  }

  return {}
}

export function getSendGridConfig(): {
  apiKey: string
  fromEmail: string
  fromName: string
} {
  const vaultConfig = getSendGridCredentials()
  if (vaultConfig) {
    return {
      apiKey: vaultConfig.apiKey,
      fromEmail: vaultConfig.fromEmail || 'noreply@aiguardian.ai',
      fromName: vaultConfig.fromName || 'AiGuardian Team',
    }
  }

  const apiKey = process.env.SENDGRID_API_KEY
  if (apiKey) {
    console.warn('[CONFIG] Using SendGrid API key from process.env. Consider adding to AbëKEYs vault.')
    return {
      apiKey,
      fromEmail: process.env.SENDGRID_FROM_EMAIL || 'noreply@aiguardian.ai',
      fromName: process.env.SENDGRID_FROM_NAME || 'AiGuardian Team',
    }
  }

  throw new Error(
    'SendGrid API key not found. Add to AbëKEYs vault:\n' +
    '  Run: op signin && python3 scripts/unlock_all_credentials.py\n' +
    '  Or create: ~/.abekeys/credentials/sendgrid.json'
  )
}
