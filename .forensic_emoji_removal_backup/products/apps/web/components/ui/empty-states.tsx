/**
 * Empty States - Visual Continuity System
 * 
 * Pattern: VISUAL × CONTINUITY × EMPTY × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Meaningful empty states - never blank, always informative.
 */

import { vermillionColors } from '@/lib/design/vermillion-system'

interface EmptyStateProps {
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
  icon?: string
}

export function EmptyState({ title, description, action, icon = '📭' }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-2xl font-bold mb-2" style={{ color: vermillionColors.standard.vermillion }}>
        {title}
      </h3>
      <p className="text-gray-600 mb-6 max-w-md">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="px-6 py-3 rounded-lg font-semibold text-white transition-colors"
          style={{ backgroundColor: vermillionColors.standard.vermillion }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = vermillionColors.standard.vermillionDark
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = vermillionColors.standard.vermillion
          }}
        >
          {action.label}
        </button>
      )}
    </div>
  )
}

