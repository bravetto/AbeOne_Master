'use client'

/**
 * Product Ideas Activity Feed
 * 
 * Pattern: PRODUCT × IDEAS × ACTIVITY × FEED × ONE
 * Guardian: AEYON (999 Hz) × Lux (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useQuery } from '@tanstack/react-query'
import { AnimatedCard } from './AnimatedCard'

interface ProductIdeaActivity {
  id: string
  type: 'submitted' | 'reviewed' | 'approved' | 'rejected' | 'execution_started' | 'completed'
  idea_id: string
  idea_name: string
  author: string
  timestamp: string
  status: 'pending' | 'approved' | 'rejected' | 'in_execution' | 'completed'
}

export function ProductIdeasActivityFeed() {
  const { data, isLoading } = useQuery<ProductIdeaActivity[]>({
    queryKey: ['product-ideas', 'activities'],
    queryFn: async () => {
      const response = await fetch('/api/portal/product-ideas/activities')
      if (!response.ok) {
        // Fallback to mock data
        return [
          {
            id: '1',
            type: 'submitted',
            idea_id: 'idea-1',
            idea_name: 'Real-Time Collaboration in AbëDESKs',
            author: 'Michael',
            timestamp: new Date(Date.now() - 3600000).toISOString(),
            status: 'pending'
          },
          {
            id: '2',
            type: 'approved',
            idea_id: 'idea-2',
            idea_name: 'Mobile App for AbëBEATs',
            author: 'Team',
            timestamp: new Date(Date.now() - 7200000).toISOString(),
            status: 'approved'
          }
        ]
      }
      return response.json()
    },
    refetchInterval: 15000, // 15-second refresh
  })

  if (isLoading) {
    return (
      <AnimatedCard delay={900}>
        <div style={{ 
          padding: '34px',
          backgroundColor: '#0a0a0a',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#a0a0a0' }}>Loading activities...</div>
        </div>
      </AnimatedCard>
    )
  }

  if (!data || data.length === 0) {
    return (
      <AnimatedCard delay={900}>
        <div style={{
          padding: '34px',
          backgroundColor: '#0a0a0a',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '24px',
            fontWeight: '600',
            color: '#ffffff',
            marginBottom: '24px',
            letterSpacing: '-0.01em',
          }}>
            Product Ideas Activity
          </h2>
          <div style={{ color: '#a0a0a0' }}>No recent activity</div>
        </div>
      </AnimatedCard>
    )
  }

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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return '#00ff88'
      case 'rejected': return '#ff4444'
      case 'in_execution': return '#0080ff'
      case 'completed': return '#00ff88'
      default: return '#FFD700'
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'submitted': return 'submitted'
      case 'reviewed': return 'reviewed'
      case 'approved': return 'approved'
      case 'rejected': return 'rejected'
      case 'execution_started': return 'execution started'
      case 'completed': return 'completed'
      default: return type
    }
  }

  const getIcon = (type: string) => {
    switch (type) {
      case 'submitted': return '📝'
      case 'reviewed': return '👀'
      case 'approved': return '✅'
      case 'rejected': return '❌'
      case 'execution_started': return '🚀'
      case 'completed': return '🎉'
      default: return '📋'
    }
  }

  return (
    <AnimatedCard delay={900}>
      <div style={{
        padding: '24px',
        backgroundColor: '#0a0a0a',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <h2 style={{
          fontSize: '24px',
          fontWeight: '600',
          color: '#ffffff',
          marginBottom: '24px',
          letterSpacing: '-0.01em',
        }}>
          Product Ideas Activity
        </h2>
        
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '21px',
          maxHeight: '400px',
          overflowY: 'auto',
        }}>
          {data.map((activity) => (
            <div
              key={activity.id}
              style={{
                padding: '16px',
                backgroundColor: '#141414',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                display: 'flex',
                gap: '16px',
                alignItems: 'flex-start',
              }}
            >
              {/* Status Indicator */}
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: `${getStatusColor(activity.status)}20`,
                border: `1px solid ${getStatusColor(activity.status)}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                flexShrink: 0,
              }}>
                {getIcon(activity.type)}
              </div>

              {/* Activity Content */}
              <div style={{ flex: 1 }}>
                <p style={{
                  fontSize: '15px',
                  fontWeight: '500',
                  color: '#ffffff',
                  marginBottom: '6px',
                  lineHeight: 1.4,
                }}>
                  <strong>{activity.author}</strong> {getTypeLabel(activity.type)} <strong>{activity.idea_name}</strong>
                </p>
                <div style={{
                  display: 'flex',
                  gap: '13px',
                  alignItems: 'center',
                  fontSize: '13px',
                  color: '#666666',
                }}>
                  <span style={{ textTransform: 'capitalize' }}>{activity.status}</span>
                  <span>•</span>
                  <span>{formatTime(activity.timestamp)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AnimatedCard>
  )
}

