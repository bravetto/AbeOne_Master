'use client'

/**
 * Team Distribution Component
 * 
 * Pattern: TEAM × DISTRIBUTION × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface TeamDistributionProps {
  itemsByAssignee: Record<string, number>
}

export function TeamDistribution({ itemsByAssignee }: TeamDistributionProps) {
  const total = Object.values(itemsByAssignee).reduce((sum, count) => sum + count, 0)
  const sorted = Object.entries(itemsByAssignee)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10) // Top 10 team members

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
        Team Distribution
      </h2>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}>
        {sorted.map(([assignee, count]) => {
          const percentage = total > 0 ? (count / total) * 100 : 0
          const color = assignee === 'unassigned' ? '#FFD700' : '#00ff88'
          
          return (
            <div key={assignee}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '8px',
              }}>
                <span style={{
                  fontSize: '16px',
                  color: '#ffffff',
                  textTransform: 'capitalize',
                }}>
                  {assignee}
                </span>
                <span style={{
                  fontSize: '16px',
                  color: color,
                  textShadow: color === '#00ff88' 
                    ? '0 0 10px rgba(0, 255, 136, 0.3)' 
                    : '0 0 10px rgba(255, 215, 0, 0.3)',
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
                  backgroundColor: color,
                  transition: 'width 0.5s ease',
                  boxShadow: color === '#00ff88' 
                    ? '0 0 10px rgba(0, 255, 136, 0.3)' 
                    : '0 0 10px rgba(255, 215, 0, 0.3)',
                }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

