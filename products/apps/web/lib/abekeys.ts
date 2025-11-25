/**
 * ABEKEYS Vault Integration
 * 
 * Pattern: ABEKEYS × VAULT × SECURE × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (ZERO)
 * 
 * CRITICAL: NEVER use .env.local - ABEKEYS vault ONLY
 * 
 * Latest Best Practices:
 * - Server-side only (never expose to client)
 * - Read from ~/.abekeys/credentials/
 * - Type-safe credential access
 * - Fail fast if vault not available
 */

import { readFileSync } from 'fs'
import { join } from 'path'
import { homedir } from 'os'

const ABEKEYS_VAULT_PATH = join(homedir(), '.abekeys', 'credentials')

interface CredentialData {
  service?: string
  api_key?: string
  secret_key?: string
  publishable_key?: string
  webhook_secret?: string
  [key: string]: any
}

/**
 * Get credential from ABEKEYS vault
 * 
 * SAFETY: Server-side only - never call from client components
 * 
 * @param service Service name (e.g., 'stripe', 'clerk')
 * @returns Credential data or null if not found
 */
export function getAbekeysCredential(service: string): CredentialData | null {
  // SAFETY: Only works server-side
  if (typeof window !== 'undefined') {
    throw new Error('ABEKEYS vault access is server-side only')
  }

  try {
    const credPath = join(ABEKEYS_VAULT_PATH, `${service}.json`)
    const credData = readFileSync(credPath, 'utf-8')
    return JSON.parse(credData) as CredentialData
  } catch (error: any) {
    if (error.code === 'ENOENT') {
      console.warn(`[ABEKEYS] Credential not found: ${service}`)
      return null
    }
    console.error(`[ABEKEYS] Error reading credential ${service}:`, error)
    return null
  }
}

/**
 * Get API key from ABEKEYS vault
 * 
 * @param service Service name
 * @returns API key or null
 */
export function getAbekeysApiKey(service: string): string | null {
  const cred = getAbekeysCredential(service)
  if (!cred) return null
  
  // Try common field names
  return cred.api_key || cred.secret_key || cred.token || null
}

/**
 * Get Stripe credentials from ABEKEYS vault
 * 
 * @returns Stripe credentials object
 */
export function getStripeCredentials() {
  const cred = getAbekeysCredential('stripe')
  if (!cred) {
    throw new Error('Stripe credentials not found in ABEKEYS vault. Run: op signin && python3 scripts/unlock_all_credentials.py')
  }

  // ABEKEYS vault structure: { service, api_key, ... }
  // Stripe credential uses 'api_key' field for secret key
  const secretKey = cred.secret_key || cred.api_key || null
  
  if (!secretKey) {
    throw new Error('Stripe secret key not found in ABEKEYS vault. Check ~/.abekeys/credentials/stripe.json')
  }

  return {
    secretKey,
    publishableKey: cred.publishable_key || cred.publishableKey || null,
    webhookSecret: cred.webhook_secret || cred.webhookSecret || null,
  }
}

/**
 * Get Clerk credentials from ABEKEYS vault
 * 
 * @returns Clerk credentials object
 */
export function getClerkCredentials() {
  // Try main clerk first, then fallback to others
  const cred = getAbekeysCredential('clerk') 
    || getAbekeysCredential('bill_clerk')
    || getAbekeysCredential('clerk__poly__production_owner')
  
  if (!cred) {
    throw new Error('Clerk credentials not found in ABEKEYS vault. Run: op signin && python3 scripts/unlock_all_credentials.py')
  }

  return {
    secretKey: cred.secret_key || cred.api_key || null,
    publishableKey: cred.publishable_key || null,
  }
}

/**
 * Validate ABEKEYS vault is accessible
 * 
 * @returns True if vault is accessible
 */
export function validateAbekeysVault(): boolean {
  try {
    const testCred = getAbekeysCredential('stripe')
    return testCred !== null
  } catch {
    return false
  }
}


/**
 * Get Database credentials from ABEKEYS vault
 */
export function getDatabaseCredentials(): string | null {
  const cred = getAbekeysCredential('database') 
    || getAbekeysCredential('postgres')
    || getAbekeysCredential('postgresql')
    || getAbekeysCredential('neon')
    || getAbekeysCredential('supabase')
  
  if (!cred) return null
  
  return cred.connection_string || cred.database_url || cred.url || cred.api_key || null
}

/**
 * Get Redis credentials from ABEKEYS vault
 */
export function getRedisCredentials(): {
  url?: string
  upstashUrl?: string
  upstashToken?: string
} | null {
  const cred = getAbekeysCredential('redis')
    || getAbekeysCredential('upstash')
    || getAbekeysCredential('upstash_redis')
  
  if (!cred) return null
  
  return {
    url: cred.url || cred.redis_url || null,
    upstashUrl: cred.upstash_url || cred.rest_url || cred.upstash_rest_url || null,
    upstashToken: cred.upstash_token || cred.rest_token || cred.token || cred.api_key || null,
  }
}

/**
 * Get SendGrid credentials from ABEKEYS vault
 */
export function getSendGridCredentials(): {
  apiKey: string
  fromEmail?: string
  fromName?: string
} | null {
  const cred = getAbekeysCredential('sendgrid')
    || getAbekeysCredential('send_grid')
  
  if (!cred) return null
  
  const apiKey = cred.api_key || cred.secret_key || cred.token || null
  if (!apiKey) return null
  
  return {
    apiKey,
    fromEmail: cred.from_email || cred.fromEmail || cred.email || 'noreply@aiguardian.ai',
    fromName: cred.from_name || cred.fromName || cred.name || 'AiGuardian Team',
  }
}
