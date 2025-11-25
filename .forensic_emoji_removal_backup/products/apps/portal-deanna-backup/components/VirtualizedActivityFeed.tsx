/**
 * Virtualized Activity Feed Component
 * 
 * Pattern: VIRTUAL × SCROLLING × PERFORMANCE × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { FixedSizeList } from 'react-window'
import { useMemo } from 'react'

interface ActivityItem {
  id: string
  type: 'commit' | 'pr' | 'task' | 'deployment' | 'meeting' | 'creation'
  title: string
  description?: string
  user: string
  project: string
  timestamp: string
  guardian?: string
  icon: string
  color: string
}

interface VirtualizedActivityFeedProps {
  activities: ActivityItem[]
  formatTimeAgo: (timestamp: string) => string
}

const ITEM_HEIGHT = 120
const CONTAINER_HEIGHT = 400 // Max height for mobile

export function VirtualizedActivityFeed({ activities, formatTimeAgo }: VirtualizedActivityFeedProps) {
  const itemData = useMemo(() => activities, [activities])

  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => {
    const activity = itemData[index]
    if (!activity) return null

    return (
      <div style={style} className="px-4 pb-3">
        <div className="flex items-start gap-3 p-3 bg-gradient-to-r from-white to-purple-50/50 dark:from-gray-800 dark:to-purple-900/20 rounded-xl border border-purple-100 dark:border-purple-800 hover:shadow-md transition-all">
          <div className="text-2xl flex-shrink-0">{activity.icon}</div>
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                <p className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">
                  {activity.title}
                </p>
                {activity.description && (
                  <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                    {activity.description}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-2 flex-wrap">
                  <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full">
                    {activity.user}
                  </span>
                  <span className="text-xs px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded-full">
                    {activity.project}
                  </span>
                  {activity.guardian && (
                    <span className="text-xs px-2 py-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 rounded-full">
                      {activity.guardian}
                    </span>
                  )}
                </div>
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
                {formatTimeAgo(activity.timestamp)}
              </span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
        <div className="text-4xl mb-2">🌊</div>
        <p>Watching for activity...</p>
      </div>
    )
  }

  return (
    <FixedSizeList
      height={Math.min(CONTAINER_HEIGHT, activities.length * ITEM_HEIGHT)}
      itemCount={activities.length}
      itemSize={ITEM_HEIGHT}
      width="100%"
      className="scrollbar-thin scrollbar-thumb-purple-300 scrollbar-track-transparent"
    >
      {Row}
    </FixedSizeList>
  )
}

