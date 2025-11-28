'use client'

/**
 * Status Breakdown Component
 * 
 * Pattern: STATUS × BREAKDOWN × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface StatusBreakdownProps {
  itemsByStatus: Record<string, number>
}

export function StatusBreakdown({ itemsByStatus }: StatusBreakdownProps) {
  const statusConfig: Record<string, { label: string; color: string }> = {
    backlog: { label: 'Backlog', color: '#666666' },
    planning: { label: 'Planning', color: '#0080ff' },
    in_progress: { label: 'In Progress', color: '#0080ff' },
    review: { label: 'Review', color: '#FFD700' },
    done: { label: 'Done', color: '#00ff88' },
    blocked: { label: 'Blocked', color: '#FFD700' },
  }

  const total = Object.values(itemsByStatus).reduce((sum, count) => sum + count, 0)

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
        Status Breakdown
      </h2>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}>
        {Object.entries(itemsByStatus).map(([status, count]) => {
          const config = statusConfig[status] || { label: status, color: '#a0a0a0' }
          const percentage = total > 0 ? (count / total) * 100 : 0
          
          return (
            <div key={status}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '8px',
              }}>
                <span style={{
                  fontSize: '16px',
                  color: '#ffffff',
                }}>
                  {config.label}
                </span>
                <span style={{
                  fontSize: '16px',
                  color: config.color,
                  textShadow: `0 0 10px ${config.color === '#0080ff' ? 'rgba(0, 128, 255, 0.3)' : config.color === '#00ff88' ? 'rgba(0, 255, 136, 0.3)' : 'transparent'}`,
                }}>
                  {count} ({Math.round(percentage)}%)
                </span>
              </div>
              <div style={{
                width: '100%',
                height: '8px',
                backgroundColor: '#141414',
                borderRadius: '4px',
                overflow: 'hidden',
              }}>
                <div style={{
                  width: `${percentage}%`,
                  height: '100%',
                  backgroundColor: config.color,
                  transition: 'width 0.5s ease',
                  boxShadow: config.color === '#0080ff' 
                    ? '0 0 10px rgba(0, 128, 255, 0.3)' 
                    : config.color === '#00ff88' 
                    ? '0 0 10px rgba(0, 255, 136, 0.3)' 
                    : 'none',
                }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

