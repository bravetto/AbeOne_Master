'use client'

/**
 * Activity Feed Component
 * 
 * Pattern: ACTIVITIES × FEED × REAL-TIME × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { ActivityItem } from '../hooks/useActivitiesQuery'

interface ActivityFeedProps {
  activities: ActivityItem[]
}

export function ActivityFeed({ activities }: ActivityFeedProps) {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays}d ago`
  }

  return (
    <div style={{
      padding: '24px',
      backgroundColor: '#0a0a0a',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '8px',
    }}>
      <h2 style={{
        fontSize: '24px',
        fontWeight: '600',
        color: '#ffffff',
        marginBottom: '24px',
        letterSpacing: '-0.01em',
      }}>
        Recent Activity
      </h2>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '21px',
      }}>
        {activities.map((activity) => (
          <div
            key={activity.id}
            style={{
              padding: '16px',
              backgroundColor: '#141414',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '8px',
              display: 'flex',
              gap: '16px',
              alignItems: 'flex-start',
            }}
          >
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              backgroundColor: `${activity.color}20`,
              border: `1px solid ${activity.color}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '14px',
              color: activity.color,
              flexShrink: 0,
            }}>
              {activity.icon}
            </div>
            <div style={{ flex: 1 }}>
              <p style={{
                fontSize: '15px',
                fontWeight: '500',
                color: '#ffffff',
                marginBottom: '6px',
                lineHeight: 1.4,
              }}>
                {activity.title}
              </p>
              {activity.description && (
                <p style={{
                  fontSize: '14px',
                  color: '#a0a0a0',
                  marginBottom: '8px',
                  lineHeight: 1.4,
                }}>
                  {activity.description}
                </p>
              )}
              <div style={{
                display: 'flex',
                gap: '13px',
                alignItems: 'center',
                fontSize: '13px',
                color: '#666666',
              }}>
                <span style={{ textTransform: 'capitalize' }}>{activity.user}</span>
                <span>•</span>
                <span style={{ textTransform: 'capitalize' }}>{activity.project}</span>
                {activity.guardian && (
                  <>
                    <span>•</span>
                    <span style={{ color: '#0080ff' }}>{activity.guardian}</span>
                  </>
                )}
                <span>•</span>
                <span>{formatTime(activity.timestamp)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

