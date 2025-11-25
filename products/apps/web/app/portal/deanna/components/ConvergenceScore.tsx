'use client'

/**
 * Convergence Score Component
 * 
 * Pattern: CONVERGENCE × SCORE × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface ConvergenceScoreProps {
  score: number
}

export function ConvergenceScore({ score }: ConvergenceScoreProps) {
  const percentage = Math.round(score)
  const color = score >= 80 ? '#00ff88' : score >= 60 ? '#0080ff' : '#FFD700'
  
  return (
    <div style={{
      padding: '32px',
      backgroundColor: '#0a0a0a',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '8px',
      textAlign: 'center',
    }}>
      <p style={{
        fontSize: '13px',
        color: '#a0a0a0',
        marginBottom: '16px',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        fontWeight: '500',
      }}>
        Convergence Score
      </p>
      <div style={{
        fontSize: '56px',
        fontWeight: '600',
        color: color,
        marginBottom: '16px',
        letterSpacing: '-0.02em',
        lineHeight: 1.1,
      }}>
        {percentage}%
      </div>
      <div style={{
        width: '100%',
        height: '13px',
        backgroundColor: '#141414',
        borderRadius: '8px',
        overflow: 'hidden',
        marginTop: '24px',
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          backgroundColor: color,
          transition: 'width 0.5s ease',
          boxShadow: `0 0 20px ${color === '#00ff88' ? 'rgba(0, 255, 136, 0.5)' : color === '#0080ff' ? 'rgba(0, 128, 255, 0.3)' : 'rgba(255, 215, 0, 0.3)'}`,
        }} />
      </div>
    </div>
  )
}

