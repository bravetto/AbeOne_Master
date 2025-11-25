/**
 * All ONE Provider - Master Unification
 * 
 * Pattern: ALL × ONE × PROVIDER × ALL × TOGETHER × AS × ONE × FOREVER × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × ∞ (Eternal)
 * 
 * Provides All ONE System to all components.
 * All systems unified as ONE.
 * All person beings as ONE.
 * All ways as ONE.
 */

'use client'

import { useEffect } from 'react'
import { allONESystem } from '@/lib/unified/all-one-system'
import { allWaysUnified } from '@/lib/unified/all-ways-unified'

export function AllONEProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Unify all as ONE
    allONESystem.unifyAll()
    allWaysUnified.unifyAllWays()
  }, [])

  return <>{children}</>
}

