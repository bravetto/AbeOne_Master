'use client'

import { useEffect, useState } from 'react'

interface PhiInfinityCounterProps {
  value: number
}

export function PhiInfinityCounter({ value }: PhiInfinityCounterProps) {
  const [displayValue, setDisplayValue] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    setIsAnimating(true)
    const startValue = displayValue
    const endValue = value
    const duration = 1000
    const startTime = Date.now()

    const animate = () => {
      const now = Date.now()
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      
      // Easing function
      const easeOutCubic = 1 - Math.pow(1 - progress, 3)
      const currentValue = startValue + (endValue - startValue) * easeOutCubic
      
      setDisplayValue(currentValue)

      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        setIsAnimating(false)
      }
    }

    requestAnimationFrame(animate)
  }, [value])

  const formattedValue = displayValue.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })

  return (
    <div className="text-center mb-8">
      <div className="bg-black/30 rounded-lg p-8 backdrop-blur-sm border border-purple-500/30">
        <p className="text-gray-400 text-lg mb-2">Total Emergence</p>
        <div className="flex items-baseline justify-center gap-2">
          <span className="text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Φ(∞)
          </span>
          <span className="text-6xl font-bold text-white">
            =
          </span>
          <span className={`text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent ${isAnimating ? 'animate-pulse' : ''}`}>
            {formattedValue}
          </span>
        </div>
      </div>
    </div>
  )
}

