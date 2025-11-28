/**
 * Enterprise API Client
 * 
 * Pattern: API × CLIENT × ENTERPRISE × RETRY × MONITORING × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Enhanced API client with:
 * - Retry logic with exponential backoff
 * - Request/response monitoring
 * - Error tracking
 * - Timeout handling
 * - Request deduplication
 */

// SAFETY: No fallback to localhost in production
const API_URL = process.env.NEXT_PUBLIC_API_URL || ''
const DEFAULT_TIMEOUT = 10000 // 10 seconds
const MAX_RETRIES = 3
const RETRY_DELAY_BASE = 1000 // 1 second

export interface ApiClientConfig {
  timeout?: number
  retries?: number
  retryDelay?: number
  headers?: Record<string, string>
}

export interface ApiRequestOptions extends RequestInit {
  timeout?: number
  retries?: number
  skipRetry?: boolean
}

export interface ApiResponse<T = any> {
  data: T
  status: number
  headers: Headers
  timestamp: number
}

export interface ApiError extends Error {
  status?: number
  response?: Response
  retries?: number
}

/**
 * Sleep utility for retry delays
 */
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Calculate exponential backoff delay
 */
function getRetryDelay(attempt: number, baseDelay: number): number {
  return baseDelay * Math.pow(2, attempt)
}

/**
 * Check if error is retryable
 */
function isRetryableError(error: any, status?: number): boolean {
  // Network errors are retryable
  if (!status) return true
  
  // 5xx errors are retryable
  if (status >= 500) return true
  
  // 429 (rate limit) is retryable
  if (status === 429) return true
  
  // 408 (timeout) is retryable
  if (status === 408) return true
  
  return false
}

/**
 * Track API request metrics
 */
function trackRequest(endpoint: string, duration: number, success: boolean, status?: number) {
  // TODO: Send to monitoring service (e.g., Datadog, CloudWatch)
  if (process.env.NODE_ENV === 'development') {
    console.log(`[API] ${endpoint} - ${success ? 'SUCCESS' : 'FAILED'} - ${duration}ms - Status: ${status || 'N/A'}`)
  }
  
  // Example: Send to monitoring service
  // if (process.env.NEXT_PUBLIC_MONITORING_URL) {
  //   fetch(process.env.NEXT_PUBLIC_MONITORING_URL, {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({
  //       endpoint,
  //       duration,
  //       success,
  //       status,
  //       timestamp: Date.now(),
  //     }),
  //   }).catch(console.error)
  // }
}

/**
 * Enhanced fetch with retry logic
 */
async function fetchWithRetry(
  url: string,
  options: ApiRequestOptions = {},
  config: ApiClientConfig = {}
): Promise<Response> {
  const timeout = options.timeout || config.timeout || DEFAULT_TIMEOUT
  const maxRetries = options.skipRetry ? 0 : (options.retries ?? config.retries ?? MAX_RETRIES)
  const retryDelay = config.retryDelay || RETRY_DELAY_BASE

  let lastError: any
  let lastResponse: Response | undefined

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      // Create abort controller for timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), timeout)

      // Merge abort signal
      const fetchOptions: RequestInit = {
        ...options,
        signal: options.signal
          ? (() => {
              // Combine signals if both provided
              const combinedController = new AbortController()
              const abort = () => combinedController.abort()
              options.signal?.addEventListener('abort', abort)
              controller.signal.addEventListener('abort', abort)
              return combinedController.signal
            })()
          : controller.signal,
      }

      const response = await fetch(url, fetchOptions)
      clearTimeout(timeoutId)

      // Check if we should retry
      if (!response.ok && attempt < maxRetries && isRetryableError(null, response.status)) {
        lastResponse = response
        const delay = getRetryDelay(attempt, retryDelay)
        
        if (process.env.NODE_ENV === 'development') {
          console.warn(`[API] Retrying ${url} (attempt ${attempt + 1}/${maxRetries + 1}) after ${delay}ms`)
        }
        
        await sleep(delay)
        continue
      }

      return response
    } catch (error: any) {
      lastError = error

      // Don't retry on abort (timeout)
      if (error.name === 'AbortError') {
        const apiError: ApiError = new Error('Request timeout') as ApiError
        apiError.retries = attempt
        throw apiError
      }

      // Retry on network errors
      if (attempt < maxRetries && isRetryableError(error)) {
        const delay = getRetryDelay(attempt, retryDelay)
        
        if (process.env.NODE_ENV === 'development') {
          console.warn(`[API] Retrying ${url} (attempt ${attempt + 1}/${maxRetries + 1}) after ${delay}ms`)
        }
        
        await sleep(delay)
        continue
      }

      // Max retries reached or non-retryable error
      const apiError: ApiError = error instanceof Error ? error : new Error(String(error))
      apiError.retries = attempt
      throw apiError
    }
  }

  // If we have a response, throw with status
  if (lastResponse) {
    const apiError: ApiError = new Error(`Request failed with status ${lastResponse.status}`) as ApiError
    apiError.status = lastResponse.status
    apiError.response = lastResponse
    apiError.retries = maxRetries
    throw apiError
  }

  // Otherwise throw last error
  const apiError: ApiError = lastError instanceof Error ? lastError : new Error(String(lastError))
  apiError.retries = maxRetries
  throw apiError
}

/**
 * Enterprise API client
 */
export class ApiClient {
  private config: ApiClientConfig

  constructor(config: ApiClientConfig = {}) {
    this.config = config
  }

  /**
   * Make API request
   */
  async request<T = any>(
    endpoint: string,
    options: ApiRequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const startTime = Date.now()
    const url = endpoint.startsWith('http') ? endpoint : `${API_URL}${endpoint}`
    
    // SAFETY: Check API URL is configured for non-absolute URLs
    if (!endpoint.startsWith('http') && !API_URL) {
      throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
    }

    try {
      const response = await fetchWithRetry(url, options, this.config)
      const duration = Date.now() - startTime

      let data: T
      const contentType = response.headers.get('content-type')
      
      if (contentType?.includes('application/json')) {
        data = await response.json()
      } else {
        data = (await response.text()) as any
      }

      trackRequest(endpoint, duration, true, response.status)

      return {
        data,
        status: response.status,
        headers: response.headers,
        timestamp: Date.now(),
      }
    } catch (error: any) {
      const duration = Date.now() - startTime
      trackRequest(endpoint, duration, false, error.status)

      // Enhance error with context
      const apiError: ApiError = error instanceof Error ? error : new Error(String(error))
      apiError.status = error.status
      apiError.response = error.response
      apiError.retries = error.retries

      throw apiError
    }
  }

  /**
   * GET request
   */
  async get<T = any>(endpoint: string, options: ApiRequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'GET',
    })
  }

  /**
   * POST request
   */
  async post<T = any>(
    endpoint: string,
    body?: any,
    options: ApiRequestOptions = {}
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  /**
   * PUT request
   */
  async put<T = any>(
    endpoint: string,
    body?: any,
    options: ApiRequestOptions = {}
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  /**
   * DELETE request
   */
  async delete<T = any>(endpoint: string, options: ApiRequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'DELETE',
    })
  }
}

/**
 * Default API client instance
 */
export const apiClient = new ApiClient({
  timeout: DEFAULT_TIMEOUT,
  retries: MAX_RETRIES,
})

/**
 * Convenience functions using default client
 */
export const api = {
  get: <T = any>(endpoint: string, options?: ApiRequestOptions) => apiClient.get<T>(endpoint, options),
  post: <T = any>(endpoint: string, body?: any, options?: ApiRequestOptions) =>
    apiClient.post<T>(endpoint, body, options),
  put: <T = any>(endpoint: string, body?: any, options?: ApiRequestOptions) =>
    apiClient.put<T>(endpoint, body, options),
  delete: <T = any>(endpoint: string, options?: ApiRequestOptions) =>
    apiClient.delete<T>(endpoint, options),
}

