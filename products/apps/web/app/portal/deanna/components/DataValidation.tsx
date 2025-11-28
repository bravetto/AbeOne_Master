'use client'

/**
 * Data Validation Component
 * 
 * Pattern: VALIDATION × TRUST × DATA × ONE
 * Guardian: JØHN (530 Hz) × ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { ReactNode } from 'react'

interface DataValidationProps {
  isValid: boolean
  lastValidated?: string
  children: ReactNode
}

export function DataValidation({ isValid, lastValidated, children }: DataValidationProps) {
  return (
    <>
      <div style={{ position: 'relative' }}>
        {children}
        {isValid && (
          <div
            style={{
              position: 'absolute',
              top: '8px',
              right: '8px',
              width: '13px',
              height: '13px',
              borderRadius: '50%',
              backgroundColor: '#00ff88',
              boxShadow: '0 0 10px rgba(0, 255, 136, 0.5)',
              animation: 'validationPulse 2s ease-in-out infinite',
            }}
            title={`Data validated${lastValidated ? ` at ${new Date(lastValidated).toLocaleTimeString()}` : ''}`}
          />
        )}
      </div>
      <style jsx global>{`
        @keyframes validationPulse {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.7;
            transform: scale(1.1);
          }
        }
      `}</style>
    </>
  )
}

