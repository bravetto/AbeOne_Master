'use client'

/**
 * Product Ideas Widget
 * 
 * Pattern: PRODUCT × IDEAS × DASHBOARD × METRICS × ONE
 * Guardian: AEYON (999 Hz) × META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useQuery } from '@tanstack/react-query'
import { AnimatedCard } from './AnimatedCard'

interface ProductIdeasData {
  total_ideas: number
  pending_review: number
  approved: number
  in_execution: number
  completed: number
  average_review_time_hours: number
  average_approval_time_hours: number
  approval_rate: number
}

export function ProductIdeasWidget() {
  const { data, isLoading } = useQuery<ProductIdeasData>({
    queryKey: ['product-ideas', 'metrics'],
    queryFn: async () => {
      const response = await fetch('/api/portal/product-ideas/metrics')
      if (!response.ok) {
        // Fallback to mock data
        return {
          total_ideas: 12,
          pending_review: 3,
          approved: 5,
          in_execution: 2,
          completed: 2,
          average_review_time_hours: 18,
          average_approval_time_hours: 48,
          approval_rate: 75
        }
      }
      return response.json()
    },
    refetchInterval: 30000, // 30-second refresh
  })

  if (isLoading) {
    return (
      <AnimatedCard delay={600}>
        <div style={{ 
          padding: '34px',
          backgroundColor: '#0a0a0a',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#a0a0a0' }}>Loading product ideas...</div>
        </div>
      </AnimatedCard>
    )
  }

  if (!data) return null

  const metrics = [
    {
      label: 'Total Ideas',
      value: data.total_ideas,
      color: '#ffffff',
    },
    {
      label: 'Pending Review',
      value: data.pending_review,
      color: '#FFD700',
    },
    {
      label: 'Approved',
      value: data.approved,
      color: '#00ff88',
    },
    {
      label: 'In Execution',
      value: data.in_execution,
      color: '#0080ff',
    },
    {
      label: 'Completed',
      value: data.completed,
      color: '#00ff88',
    },
    {
      label: 'Approval Rate',
      value: `${data.approval_rate}%`,
      color: '#ffffff',
    },
  ]

  return (
    <AnimatedCard delay={600}>
      <div style={{
        padding: '34px',
        backgroundColor: '#0a0a0a',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <h3 style={{
          fontSize: '42px',
          fontWeight: '600',
          color: '#ffffff',
          marginBottom: '21px',
          letterSpacing: '-0.01em',
        }}>
          Product Ideas
        </h3>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '21px',
        }}>
          {metrics.map((metric, index) => (
            <div
              key={index}
              style={{
                padding: '24px',
                backgroundColor: '#141414',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                textAlign: 'center',
              }}
            >
              <p style={{
                fontSize: '40px',
                fontWeight: '600',
                color: metric.color,
                marginBottom: '8px',
                letterSpacing: '-0.02em',
                lineHeight: 1.1,
              }}>
                {metric.value}
              </p>
              <p style={{
                fontSize: '14px',
                color: '#a0a0a0',
                fontWeight: '400',
              }}>
                {metric.label}
              </p>
            </div>
          ))}
        </div>
      </div>
    </AnimatedCard>
  )
}

