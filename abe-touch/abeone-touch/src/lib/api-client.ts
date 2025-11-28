/**
 * AbëONE API Client Atom
 * 
 * Base API client utilities for making HTTP requests.
 * Event-driven, error-handled, type-safe.
 * 
 * Pattern: API × CLIENT × ATOM × EVENT × DRIVEN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence) × 98.7 Hz (Efficiency)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz) + ALRAX (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { dispatchAbeEvent } from './event-driven';
import { getApiConfig, type ApiConfig } from './api-config';

/**
 * API Error Types
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class NetworkError extends Error {
  constructor(message: string, public originalError?: Error) {
    super(message);
    this.name = 'NetworkError';
  }
}

export class TimeoutError extends Error {
  constructor(message: string = 'Request timeout') {
    super(message);
    this.name = 'TimeoutError';
  }
}

/**
 * Request options
 */
export interface RequestOptions extends RequestInit {
  /** Custom timeout in milliseconds */
  timeout?: number;
  /** Skip error event dispatch */
  silent?: boolean;
  /** Abort signal for cancellation */
  signal?: AbortSignal;
  /** Maximum retry attempts */
  maxRetries?: number;
  /** Retry delay in milliseconds */
  retryDelay?: number;
  /** Use exponential backoff for retries */
  exponentialBackoff?: boolean;
}

/**
 * Response wrapper
 */
export interface ApiResponse<T = any> {
  data: T;
  status: number;
  headers: Headers;
}

/**
 * Create timeout promise
 */
function createTimeoutPromise(timeout: number): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new TimeoutError(`Request exceeded ${timeout}ms timeout`));
    }, timeout);
  });
}

/**
 * Base fetch wrapper with timeout, error handling, and retry logic
 */
export async function apiFetch<T = any>(
  endpoint: string,
  options: RequestOptions = {},
  config?: Partial<ApiConfig>
): Promise<ApiResponse<T>> {
  const apiConfig = getApiConfig(config);
  const url = endpoint.startsWith('/api/') 
    ? endpoint  // Relative Next.js route
    : `${apiConfig.baseUrl}${endpoint}`;  // External API
  const timeout = options.timeout ?? apiConfig.timeout;
  const maxRetries = options.maxRetries ?? 0;
  const retryDelay = options.retryDelay ?? 1000;
  const exponentialBackoff = options.exponentialBackoff ?? true;

  // Merge headers
  const headers = new Headers({
    ...apiConfig.headers,
    ...options.headers,
  });

  // Create abort controller for timeout (or use provided signal)
  const abortController = options.signal 
    ? { signal: options.signal, abort: () => {} }
    : new AbortController();
  const timeoutId = options.signal 
    ? null 
    : setTimeout(() => abortController.abort(), timeout);

  // Combine signals if both provided
  const combinedSignal = options.signal && abortController.signal
    ? (() => {
        const combined = new AbortController();
        const abort = () => combined.abort();
        options.signal!.addEventListener('abort', abort);
        abortController.signal.addEventListener('abort', abort);
        return combined.signal;
      })()
    : options.signal || abortController.signal;

  // Retry logic wrapper
  let lastError: Error | null = null;
  let attempt = 0;

  while (attempt <= maxRetries) {
    try {
      // Race between fetch and timeout
      const response = await Promise.race([
        fetch(url, {
          ...options,
          headers,
          signal: combinedSignal,
        }),
        createTimeoutPromise(timeout),
      ]);

      if (timeoutId) clearTimeout(timeoutId);

      // Parse response
      let data: T;
      const contentType = response.headers.get('content-type');
      
      if (contentType?.includes('application/json')) {
        data = await response.json();
      } else {
        data = (await response.text()) as T;
      }

      // Handle error status codes
      if (!response.ok) {
        const error = new ApiError(
          `API request failed: ${response.statusText}`,
          response.status,
          data
        );

        // Retry on 5xx errors, not on 4xx errors
        if (response.status >= 500 && attempt < maxRetries) {
          lastError = error;
          attempt++;
          const delay = exponentialBackoff 
            ? retryDelay * Math.pow(2, attempt - 1)
            : retryDelay;
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }

        if (!options.silent) {
          dispatchAbeEvent('data-update', {
            type: 'error',
            error: error.message,
            status: response.status,
          });
        }

        throw error;
      }

      return {
        data,
        status: response.status,
        headers: response.headers,
      };
    } catch (error) {
      lastError = error instanceof Error ? error : new Error('Unknown error');

      // Don't retry on abort
      if (error instanceof Error && error.name === 'AbortError') {
        const timeoutError = new TimeoutError();
        if (!options.silent) {
          dispatchAbeEvent('data-update', {
            type: 'error',
            error: timeoutError.message,
          });
        }
        throw timeoutError;
      }

      // Handle network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        const networkError = new NetworkError(
          'Network request failed',
          error as Error
        );
        
        // Retry on network errors
        if (attempt < maxRetries) {
          lastError = networkError;
          attempt++;
          const delay = exponentialBackoff 
            ? retryDelay * Math.pow(2, attempt - 1)
            : retryDelay;
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }

        if (!options.silent) {
          dispatchAbeEvent('data-update', {
            type: 'error',
            error: networkError.message,
          });
        }
        throw networkError;
      }

      // Handle timeout errors
      if (error instanceof TimeoutError) {
        // Retry on timeout
        if (attempt < maxRetries) {
          lastError = error;
          attempt++;
          const delay = exponentialBackoff 
            ? retryDelay * Math.pow(2, attempt - 1)
            : retryDelay;
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        throw error;
      }

      // Re-throw known errors (no retry)
      if (error instanceof ApiError || error instanceof NetworkError || error instanceof TimeoutError) {
        throw error;
      }

      // Unknown error - retry if we have retries left
      if (attempt < maxRetries) {
        attempt++;
        const delay = exponentialBackoff 
          ? retryDelay * Math.pow(2, attempt - 1)
          : retryDelay;
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      // Unknown error - no more retries
      const unknownError = new Error(
        error instanceof Error ? error.message : 'Unknown API error'
      );
      if (!options.silent) {
        dispatchAbeEvent('data-update', {
          type: 'error',
          error: unknownError.message,
        });
      }
      throw unknownError;
    }
  }

  // If we exhausted retries, throw last error
  if (lastError) {
    throw lastError;
  }
  throw new Error('Request failed after retries');
}

/**
 * GET request
 */
export async function apiGet<T = any>(
  endpoint: string,
  options?: RequestOptions,
  config?: Partial<ApiConfig>
): Promise<ApiResponse<T>> {
  return apiFetch<T>(endpoint, { ...options, method: 'GET' }, config);
}

/**
 * POST request
 */
export async function apiPost<T = any>(
  endpoint: string,
  body?: any,
  options?: RequestOptions,
  config?: Partial<ApiConfig>
): Promise<ApiResponse<T>> {
  return apiFetch<T>(
    endpoint,
    {
      ...options,
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    },
    config
  );
}

/**
 * PUT request
 */
export async function apiPut<T = any>(
  endpoint: string,
  body?: any,
  options?: RequestOptions,
  config?: Partial<ApiConfig>
): Promise<ApiResponse<T>> {
  return apiFetch<T>(
    endpoint,
    {
      ...options,
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    },
    config
  );
}

/**
 * DELETE request
 */
export async function apiDelete<T = any>(
  endpoint: string,
  options?: RequestOptions,
  config?: Partial<ApiConfig>
): Promise<ApiResponse<T>> {
  return apiFetch<T>(endpoint, { ...options, method: 'DELETE' }, config);
}

