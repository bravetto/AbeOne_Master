'use client'

/**
 * Metrics Grid Component
 * 
 * Pattern: METRICS × GRID × MICHAEL_DESIGN × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface AggregatedBacklog {
  total_items: number
  items_by_status: Record<string, number>
  items_by_guardian: Record<string, number>
  items_by_assignee: Record<string, number>
  projects: Array<{
    project_id: string
    project_name: string
    project_type: string
    item_count: number
  }>
  aggregated_at: string
  convergence_score: number
}

interface MetricsGridProps {
  backlog: AggregatedBacklog
}

export function MetricsGrid({ backlog }: MetricsGridProps) {
  const metrics = [
    {
      label: 'Total Items',
      value: backlog.total_items,
      color: '#ffffff',
    },
    {
      label: 'In Progress',
      value: backlog.items_by_status.in_progress || 0,
      color: '#0080ff',
    },
    {
      label: 'Blocked',
      value: backlog.items_by_status.blocked || 0,
      color: '#FFD700',
    },
    {
      label: 'Done',
      value: backlog.items_by_status.done || 0,
      color: '#00ff88',
    },
  ]

  return (
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
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
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
  )
}

