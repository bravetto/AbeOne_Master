/**
 * Location Indicator - Context Awareness System
 * 
 * Pattern: CONTEXT × AWARENESS × LOCATION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Always know where you are - never lost.
 */

'use client'

import { usePathname } from 'next/navigation'
import { vermillionColors } from '@/lib/design/vermillion-system'

export function LocationIndicator() {
  const pathname = usePathname()
  
  const pathParts = pathname.split('/').filter(Boolean)
  const currentPage = pathParts[pathParts.length - 1] || 'home'
  
  return (
    <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
      <span className="text-gray-400"></span>
      <span>You are here:</span>
      <span className="font-semibold" style={{ color: vermillionColors.standard.vermillion }}>
        /{pathParts.join('/') || 'home'}
      </span>
    </div>
  )
}

