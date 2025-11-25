/**
 * Environment Variable Validation
 * 
 * Pattern: ENV × VALIDATION × ENTERPRISE × SAFETY × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Validates required environment variables at startup
 */

/**
 * Validate environment variables
 * 
 * SAFETY: Fail fast if required env vars are missing
 */
export function validateEnv() {
  const errors: string[] = []

  // Required in production
  if (process.env.NODE_ENV === 'production') {
    if (!process.env.NEXT_PUBLIC_API_URL) {
      errors.push('NEXT_PUBLIC_API_URL is required in production')
    }
  }

  // Optional but recommended
  const recommended = [
    'NEXT_PUBLIC_MONITORING_URL',
    'NEXT_PUBLIC_LOGGING_URL',
    'NEXT_PUBLIC_ERROR_TRACKING_URL',
  ]

  if (process.env.NODE_ENV === 'production') {
    recommended.forEach((key) => {
      if (!process.env[key]) {
        console.warn(`[ENV] ${key} is not set. Monitoring features may be limited.`)
      }
    })
  }

  if (errors.length > 0) {
    throw new Error(
      `Environment validation failed:\n${errors.map((e) => `  - ${e}`).join('\n')}`
    )
  }
}

/**
 * Get validated environment variable
 */
export function getEnv(key: string, defaultValue?: string): string {
  const value = process.env[key] || defaultValue

  if (!value) {
    throw new Error(`Environment variable ${key} is not set and no default provided`)
  }

  return value
}

/**
 * Get optional environment variable
 */
export function getOptionalEnv(key: string, defaultValue?: string): string | undefined {
  return process.env[key] || defaultValue
}

/**
 * Environment configuration
 */
export const env = {
  // API
  apiUrl: getOptionalEnv('NEXT_PUBLIC_API_URL', ''),
  backendApiUrl: getOptionalEnv('BACKEND_API_URL', process.env.NEXT_PUBLIC_API_URL || ''),
  
  // Monitoring
  monitoringUrl: getOptionalEnv('NEXT_PUBLIC_MONITORING_URL'),
  loggingUrl: getOptionalEnv('NEXT_PUBLIC_LOGGING_URL'),
  errorTrackingUrl: getOptionalEnv('NEXT_PUBLIC_ERROR_TRACKING_URL'),
  
  // Environment
  nodeEnv: getEnv('NODE_ENV', 'development'),
  isProduction: process.env.NODE_ENV === 'production',
  isDevelopment: process.env.NODE_ENV === 'development',
  
  // JWT (server-side only)
  jwtSecret: getOptionalEnv('JWT_SECRET'),
}

// Validate on import in production
if (typeof window === 'undefined' && process.env.NODE_ENV === 'production') {
  try {
    validateEnv()
  } catch (error) {
    console.error('Environment validation failed:', error)
    // Don't throw in production to allow graceful degradation
    // but log the error for visibility
  }
}

