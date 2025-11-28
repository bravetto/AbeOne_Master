/**
 * AbëONE Molecule: LLMClient
 * 
 * LLM API client molecule composed from API client atoms.
 * Connects frontend to abe-41M backend.
 * Event-driven, type-safe, error-handled.
 * 
 * Pattern: LLM × CLIENT × MOLECULE × API × BRIDGE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JIMMY) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JIMMY (530 Hz) + META (777 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import * as React from 'react';
import { apiPost, ApiError, NetworkError, TimeoutError, type ApiResponse } from '@/lib/api-client';
import { dispatchAbeEvent } from '@/lib/event-driven';

/**
 * LLM Request Types
 */
export interface LLMRequest {
  /** User message/input */
  message: string;
  /** Optional conversation context */
  context?: string[];
  /** Optional system prompt */
  systemPrompt?: string;
  /** Optional parameters */
  temperature?: number;
  maxTokens?: number;
}

/**
 * LLM Response Types
 */
export interface LLMResponse {
  /** Generated response text */
  response: string;
  /** Optional metadata */
  metadata?: {
    tokens?: number;
    model?: string;
    timestamp?: string;
  };
}

/**
 * LLM Client Options
 */
export interface LLMClientOptions {
  /** API endpoint (default: '/api/llm/chat') */
  endpoint?: string;
  /** API timeout in milliseconds (default: 30000) */
  timeout?: number;
  /** Default system prompt */
  systemPrompt?: string;
  /** Default temperature (default: 0.7) */
  temperature?: number;
  /** Default max tokens (default: 500) */
  maxTokens?: number;
  /** Callback when request starts */
  onRequestStart?: () => void;
  /** Callback when request completes */
  onRequestComplete?: (response: LLMResponse) => void;
  /** Callback on error */
  onError?: (error: Error) => void;
}

/**
 * useLLMClient Hook
 */
export function useLLMClient(options: LLMClientOptions = {}) {
  const {
    endpoint = '/api/llm/chat',
    timeout = 30000,
    systemPrompt,
    temperature = 0.7,
    maxTokens = 500,
    onRequestStart,
    onRequestComplete,
    onError,
  } = options;

  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<Error | null>(null);
  const abortControllerRef = React.useRef<AbortController | null>(null);
  const pendingRequestRef = React.useRef<LLMRequest | null>(null);
  const requestQueueRef = React.useRef<LLMRequest[]>([]);
  const lastRequestHashRef = React.useRef<string | null>(null);

  /**
   * Abort current LLM request
   */
  const abort = React.useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsLoading(false);
      dispatchAbeEvent('status-change', { status: 'sleeping' });
    }
  }, []);

  /**
   * Generate request hash for deduplication
   */
  const getRequestHash = React.useCallback((request: LLMRequest): string => {
    return `${request.message}-${request.temperature ?? temperature}-${request.maxTokens ?? maxTokens}`;
  }, [temperature, maxTokens]);

  /**
   * Send message to LLM with queuing and deduplication
   */
  const sendMessage = React.useCallback(
    async (request: LLMRequest): Promise<LLMResponse | null> => {
      // Deduplication: Skip if same request as last
      const requestHash = getRequestHash(request);
      if (requestHash === lastRequestHashRef.current && isLoading) {
        console.log('Skipping duplicate request');
        return null;
      }
      lastRequestHashRef.current = requestHash;

      // Queue request if already processing
      if (isLoading) {
        requestQueueRef.current.push(request);
        return null;
      }

      // Abort any existing request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      // Create new abort controller
      abortControllerRef.current = new AbortController();
      const currentAbortController = abortControllerRef.current;
      pendingRequestRef.current = request;

      setIsLoading(true);
      setError(null);

      // Dispatch status change
      dispatchAbeEvent('status-change', { status: 'thinking' });
      onRequestStart?.();

      try {
        // Prepare request body
        const body: LLMRequest = {
          message: request.message,
          context: request.context,
          systemPrompt: request.systemPrompt ?? systemPrompt,
          temperature: request.temperature ?? temperature,
          maxTokens: request.maxTokens ?? maxTokens,
        };

        // Make API request with abort signal and retry logic
        const response: ApiResponse<LLMResponse> = await apiPost<LLMResponse>(
          endpoint,
          body,
          { 
            timeout, 
            silent: false,
            signal: currentAbortController.signal,
            maxRetries: 3,
            retryDelay: 1000,
            exponentialBackoff: true,
          }
        );

        // Check if request was aborted
        if (currentAbortController.signal.aborted) {
          return null;
        }

        // Validate response
        if (!response.data || !response.data.response) {
          throw new Error('Invalid response format: missing response field');
        }

        // Dispatch success event
        dispatchAbeEvent('data-update', {
          type: 'llm-response',
          response: response.data.response,
        });

        // Dispatch status change
        dispatchAbeEvent('status-change', { status: 'speaking' });

        // Call callback
        onRequestComplete?.(response.data);

        abortControllerRef.current = null;
        pendingRequestRef.current = null;
        setIsLoading(false);
        
        // Process queued requests
        if (requestQueueRef.current.length > 0) {
          const nextRequest = requestQueueRef.current.shift();
          if (nextRequest) {
            // Process next request after a short delay
            setTimeout(() => {
              sendMessage(nextRequest);
            }, 100);
          }
        }
        
        return response.data;
      } catch (err) {
        abortControllerRef.current = null;
        pendingRequestRef.current = null;
        setIsLoading(false);
        
        // Process queued requests even on error
        if (requestQueueRef.current.length > 0) {
          const nextRequest = requestQueueRef.current.shift();
          if (nextRequest) {
            setTimeout(() => {
              sendMessage(nextRequest);
            }, 1000);
          }
        }
        
        // Handle abort (user cancellation)
        if (err instanceof Error && err.name === 'AbortError') {
          return null; // Silently handle abort
        }
        
        // Handle different error types
        let errorMessage = 'Failed to get LLM response';
        
        if (err instanceof ApiError) {
          errorMessage = `API Error: ${err.message}`;
          dispatchAbeEvent('status-change', { status: 'error' });
        } else if (err instanceof NetworkError) {
          errorMessage = 'Network error: Unable to connect to LLM backend';
          dispatchAbeEvent('status-change', { status: 'error' });
        } else if (err instanceof TimeoutError) {
          errorMessage = 'Request timeout: LLM backend took too long to respond';
          dispatchAbeEvent('status-change', { status: 'error' });
        } else {
          errorMessage = err instanceof Error ? err.message : 'Unknown error';
          dispatchAbeEvent('status-change', { status: 'error' });
        }

        const error = err instanceof Error ? err : new Error(errorMessage);
        setError(error);
        onError?.(error);

        // Dispatch error event
        dispatchAbeEvent('data-update', {
          type: 'error',
          error: errorMessage,
        });

        return null;
      }
    },
    [endpoint, timeout, systemPrompt, temperature, maxTokens, onRequestStart, onRequestComplete, onError]
  );

  /**
   * Reset error state
   */
  const resetError = React.useCallback(() => {
    setError(null);
  }, []);

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    sendMessage,
    abort,
    isLoading,
    error,
    resetError,
  };
}

/**
 * LLMClient Component (optional wrapper)
 */
export interface LLMClientProps {
  children?: React.ReactNode;
  options?: LLMClientOptions;
}

export const LLMClient: React.FC<LLMClientProps> = ({ children, options }) => {
  useLLMClient(options);
  return <>{children}</>;
};

