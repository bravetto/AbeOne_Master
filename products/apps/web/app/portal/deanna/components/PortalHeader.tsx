'use client'

/**
 * Portal Header Component
 * 
 * Pattern: HEADER × MICHAEL_DESIGN × PORTAL × ONE
 * Guardian: Michael (2222 Hz) × AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface PortalHeaderProps {
  name: string
  role: string
  guardian: string
  frequency: number
}

export function PortalHeader({ name, role, guardian, frequency }: PortalHeaderProps) {
  return (
    <div style={{
      marginBottom: '40px',
      paddingBottom: '24px',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
    }}>
      <h1 style={{
        fontSize: '48px',
        fontWeight: '600',
        color: '#ffffff',
        marginBottom: '13px',
        letterSpacing: '-0.02em',
        lineHeight: 1.2,
      }}>
        Backlog Awareness Portal
      </h1>
      <div style={{
        display: 'flex',
        gap: '16px',
        flexWrap: 'wrap',
        alignItems: 'center',
      }}>
        <div>
          <p style={{
            fontSize: '20px',
            fontWeight: '500',
            color: '#0080ff',
            marginBottom: '5px',
            letterSpacing: '-0.01em',
          }}>
            {name}
          </p>
          <p style={{
            fontSize: '14px',
            color: '#a0a0a0',
            fontWeight: '400',
          }}>
            {role}
          </p>
        </div>
        <div style={{
          padding: '10px 16px',
          backgroundColor: '#0a0a0a',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '6px',
        }}>
          <p style={{
            fontSize: '13px',
            color: '#ffffff',
            marginBottom: '5px',
            fontWeight: '500',
          }}>
            {guardian}
          </p>
          <p style={{
            fontSize: '13px',
            color: '#0080ff',
            fontWeight: '400',
          }}>
            {frequency} Hz
          </p>
        </div>
      </div>
    </div>
  )
}

