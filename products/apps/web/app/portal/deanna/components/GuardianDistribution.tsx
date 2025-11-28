'use client'

/**
 * Guardian Distribution Component
 * 
 * Pattern: GUARDIAN × DISTRIBUTION × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface GuardianDistributionProps {
  itemsByGuardian: Record<string, number>
}

export function GuardianDistribution({ itemsByGuardian }: GuardianDistributionProps) {
  const total = Object.values(itemsByGuardian).reduce((sum, count) => sum + count, 0)
  const sorted = Object.entries(itemsByGuardian)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 8) // Top 8 guardians

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
        Guardian Distribution
      </h2>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}>
        {sorted.map(([guardian, count]) => {
          const percentage = total > 0 ? (count / total) * 100 : 0
          const displayName = guardian.replace('Guardian ', '')
          
          return (
            <div key={guardian}>
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
                  {displayName}
                </span>
                <span style={{
                  fontSize: '16px',
                  color: '#0080ff',
                  textShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
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
                  backgroundColor: '#0080ff',
                  transition: 'width 0.5s ease',
                  boxShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
                }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

