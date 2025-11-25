/**
 * Loading States - Visual Continuity System
 * 
 * Pattern: VISUAL × CONTINUITY × LOADING × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Never show blank screen - always show loading state.
 */

import { vermillionColors } from '@/lib/design/vermillion-system'

export function PageLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center"
      style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      }}
    >
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"
          style={{ borderTopColor: vermillionColors.standard.vermillion }}
        />
        <p className="text-white text-lg">Loading...</p>
      </div>
    </div>
  )
}

export function SectionLoading() {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-8 h-8 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin"
        style={{ borderTopColor: vermillionColors.standard.vermillion }}
      />
    </div>
  )
}

export function InlineLoading() {
  return (
    <span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
  )
}

