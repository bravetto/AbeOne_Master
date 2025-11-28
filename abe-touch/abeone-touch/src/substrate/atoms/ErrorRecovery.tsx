/**
 * AbëONE Atom: ErrorRecovery
 * 
 * Error recovery UI and retry logic.
 * 
 * Pattern: ERROR × RECOVERY × ATOM × UX × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz) + ALRAX (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import * as React from 'react';
import { NeuromorphicButton } from './NeuromorphicButton';
import { cn } from '@/lib/utils';

/**
 * Error Recovery Options
 */
export interface ErrorRecoveryProps {
  /** Error message */
  error: string | Error | null;
  /** On retry callback */
  onRetry?: () => void;
  /** On dismiss callback */
  onDismiss?: () => void;
  /** Show retry button */
  showRetry?: boolean;
  /** Custom retry label */
  retryLabel?: string;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Custom class name */
  className?: string;
}

/**
 * ErrorRecovery Component
 */
export const ErrorRecovery: React.FC<ErrorRecoveryProps> = ({
  error,
  onRetry,
  onDismiss,
  showRetry = true,
  retryLabel = 'Retry',
  size = 'md',
  className,
}) => {
  if (!error) return null;

  const errorMessage = error instanceof Error ? error.message : error;
  
  const sizeClasses = {
    sm: 'text-xs p-2',
    md: 'text-sm p-3',
    lg: 'text-base p-4',
  };

  return (
    <div className={cn(
      'flex flex-col items-center gap-3 p-4 rounded-xl',
      'bg-[var(--abe-error)]/10 border border-[var(--abe-error)]/20',
      sizeClasses[size],
      className
    )}>
      <div className="flex items-center gap-2 text-[var(--abe-error)]">
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" x2="12" y1="8" y2="12"/>
          <line x1="12" x2="12.01" y1="16" y2="16"/>
        </svg>
        <span className="font-medium">Error</span>
      </div>
      
      <p className="text-[var(--abe-text-secondary)] text-center">
        {errorMessage}
      </p>
      
      {showRetry && onRetry && (
        <div className="flex gap-2">
          <NeuromorphicButton
            variant="raised"
            size="sm"
            onClick={onRetry}
          >
            {retryLabel}
          </NeuromorphicButton>
          
          {onDismiss && (
            <NeuromorphicButton
              variant="flat"
              size="sm"
              onClick={onDismiss}
            >
              Dismiss
            </NeuromorphicButton>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * useErrorRecovery Hook
 */
export interface UseErrorRecoveryOptions {
  /** Maximum retry attempts */
  maxRetries?: number;
  /** Retry delay in milliseconds */
  retryDelay?: number;
  /** Exponential backoff */
  exponentialBackoff?: boolean;
  /** On retry callback */
  onRetry?: (attempt: number) => void | Promise<void>;
}

export function useErrorRecovery(options: UseErrorRecoveryOptions = {}) {
  const {
    maxRetries = 3,
    retryDelay = 1000,
    exponentialBackoff = true,
    onRetry,
  } = options;

  const [error, setError] = React.useState<Error | null>(null);
  const [retryCount, setRetryCount] = React.useState(0);
  const [isRetrying, setIsRetrying] = React.useState(false);

  /**
   * Set error
   */
  const setErrorState = React.useCallback((err: Error | null) => {
    setError(err);
    if (!err) {
      setRetryCount(0);
    }
  }, []);

  /**
   * Retry operation
   */
  const retry = React.useCallback(async () => {
    if (retryCount >= maxRetries) {
      setError(new Error(`Maximum retries (${maxRetries}) exceeded`));
      return;
    }

    setIsRetrying(true);
    setError(null);

    try {
      const delay = exponentialBackoff 
        ? retryDelay * Math.pow(2, retryCount)
        : retryDelay;

      await new Promise(resolve => setTimeout(resolve, delay));
      
      await onRetry?.(retryCount + 1);
      
      setRetryCount(prev => prev + 1);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Retry failed'));
    } finally {
      setIsRetrying(false);
    }
  }, [retryCount, maxRetries, retryDelay, exponentialBackoff, onRetry]);

  /**
   * Reset error recovery
   */
  const reset = React.useCallback(() => {
    setError(null);
    setRetryCount(0);
    setIsRetrying(false);
  }, []);

  return {
    error,
    setError: setErrorState,
    retry,
    reset,
    retryCount,
    isRetrying,
    canRetry: retryCount < maxRetries,
  };
}

