'use client'

import { useEffect } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ErrorBoundary } from '@/components/ui/error-boundary'
import { initMonitoring } from '@/lib/monitoring'

/**
 * Enterprise App Providers
 * 
 * Pattern: PROVIDERS × ENTERPRISE × INITIALIZATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Wraps app with error boundary, QueryClient, and initializes monitoring
 */

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

export function AppProviders({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize monitoring on client-side
    initMonitoring()
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary
        onError={(error, errorInfo) => {
          // Error is already tracked by ErrorBoundary component
          console.error('App-level error:', error, errorInfo)
        }}
      >
        {children}
      </ErrorBoundary>
    </QueryClientProvider>
  )
}

