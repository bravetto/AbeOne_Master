'use client'

/**
 * Pulse Glow Component
 * 
 * Pattern: GLOW × PULSE × JOY × ANIMATION × ONE
 * Guardian: Lux (852 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { ReactNode } from 'react'

interface PulseGlowProps {
  children: ReactNode
  color?: string
  intensity?: 'low' | 'medium' | 'high'
}

export function PulseGlow({ children, color = '#0080ff', intensity = 'medium' }: PulseGlowProps) {
  const intensityMap = {
    low: 0.2,
    medium: 0.4,
    high: 0.6,
  }

  const glowIntensity = intensityMap[intensity]
  const colorHex = color.replace('#', '')
  const alphaHex = Math.round(glowIntensity * 255).toString(16).padStart(2, '0')

  return (
    <>
      <div
        style={{
          position: 'relative',
          animation: `pulseGlow-${colorHex} 2s ease-in-out infinite`,
        }}
      >
        {children}
      </div>
      <style jsx global>{`
        @keyframes pulseGlow-${colorHex} {
          0%, 100% {
            filter: drop-shadow(0 0 8px ${color}${alphaHex});
          }
          50% {
            filter: drop-shadow(0 0 16px ${color}${alphaHex});
          }
        }
      `}</style>
    </>
  )
}

