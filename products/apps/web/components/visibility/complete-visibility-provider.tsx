/**
 * Complete Visibility Provider
 * 
 * Pattern: VISIBILITY × PROVIDER × COMPLETE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Provides complete visibility system to all pages.
 */

'use client'

import { useEffect } from 'react'
import { completeVisibilitySystem } from '@/lib/visibility/complete-visibility-system'
import { LocationIndicator } from '../context/location-indicator'

export function CompleteVisibilityProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize complete visibility system
    completeVisibilitySystem.initialize()
  }, [])

  return (
    <>
      <LocationIndicator />
      {children}
    </>
  )
}

