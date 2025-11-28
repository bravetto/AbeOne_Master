/**
 * Status Visibility - Context Awareness System
 * 
 * Pattern: CONTEXT × AWARENESS × STATUS × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Always see current status - never uncertain.
 */

import { vermillionColors } from '@/lib/design/vermillion-system'

interface StatusVisibilityProps {
  status: 'success' | 'warning' | 'error' | 'info' | 'loading'
  message: string
  details?: string
}

export function StatusVisibility({ status, message, details }: StatusVisibilityProps) {
  const statusColors = {
    success: '#28a745',
    warning: '#ffc107',
    error: vermillionColors.standard.vermillion,
    info: '#17a2b8',
    loading: vermillionColors.standard.vermillion,
  }
  
  const statusIcons = {
    success: '✅',
    warning: '⚠️',
    error: '❌',
    info: 'ℹ️',
    loading: '⏳',
  }
  
  return (
    <div className="flex items-start gap-3 p-4 rounded-lg border-l-4 mb-4"
      style={{
        backgroundColor: `${statusColors[status]}15`,
        borderLeftColor: statusColors[status],
      }}
    >
      <span className="text-xl">{statusIcons[status]}</span>
      <div className="flex-1">
        <p className="font-semibold" style={{ color: statusColors[status] }}>
          {message}
        </p>
        {details && (
          <p className="text-sm text-gray-600 mt-1">{details}</p>
        )}
      </div>
    </div>
  )
}

