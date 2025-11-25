'use client'

/**
 * Animated Card Component
 * 
 * Pattern: CARD × ANIMATION × JOY × PROFESSIONALISM × ONE
 * Guardian: Lux (852 Hz) × AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { ReactNode } from 'react'

interface AnimatedCardProps {
  children: ReactNode
  delay?: number
  className?: string
}

export function AnimatedCard({ children, delay = 0, className = '' }: AnimatedCardProps) {
  return (
    <>
      <div
        className={className}
        style={{
          animation: `fadeInUp 0.6s ease-out ${delay}ms both`,
        }}
      >
        {children}
      </div>
      <style jsx global>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(21px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </>
  )
}

