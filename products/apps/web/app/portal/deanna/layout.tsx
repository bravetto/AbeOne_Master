'use client'

/**
 * Portal Layout - QueryClient Provider
 * 
 * Pattern: LAYOUT × PORTAL × QUERY_CLIENT × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export default function PortalLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            refetchOnWindowFocus: false,
            retry: 2,
            staleTime: 10000,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

