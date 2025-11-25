'use client'

import { useEffect, useState } from 'react'

interface GaugeProps {
  label: string
  value: number
  max: number
  color: 'purple' | 'blue' | 'pink' | 'indigo'
  breakdown?: any
}

const colorClasses = {
  purple: 'from-purple-400 to-purple-600',
  blue: 'from-blue-400 to-blue-600',
  pink: 'from-pink-400 to-pink-600',
  indigo: 'from-indigo-400 to-indigo-600'
}

export function Gauge({ label, value, max, color, breakdown }: GaugeProps) {
  const [displayValue, setDisplayValue] = useState(0)
  const percentage = (value / max) * 100
  const normalizedPercentage = Math.min(percentage, 100)

  useEffect(() => {
    const startValue = displayValue
    const endValue = value
    const duration = 800
    const startTime = Date.now()

    const animate = () => {
      const now = Date.now()
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeOutCubic = 1 - Math.pow(1 - progress, 3)
      const currentValue = startValue + (endValue - startValue) * easeOutCubic
      setDisplayValue(currentValue)

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }, [value])

  return (
    <div className="bg-black/20 rounded-lg p-6 backdrop-blur-sm border border-white/10">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">{label}</h3>
      
      {/* Circular Gauge */}
      <div className="relative w-32 h-32 mx-auto mb-4">
        <svg className="transform -rotate-90 w-full h-full">
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            className="text-gray-700"
          />
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            strokeDasharray={`${2 * Math.PI * 56}`}
            strokeDashoffset={`${2 * Math.PI * 56 * (1 - normalizedPercentage / 100)}`}
            className={`text-transparent bg-gradient-to-r ${colorClasses[color]} bg-clip-text`}
            style={{
              stroke: `url(#gradient-${color})`,
              transition: 'stroke-dashoffset 0.5s ease-out'
            }}
          />
          <defs>
            <linearGradient id={`gradient-${color}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={color === 'purple' ? '#a855f7' : color === 'blue' ? '#3b82f6' : color === 'pink' ? '#ec4899' : '#6366f1'} />
              <stop offset="100%" stopColor={color === 'purple' ? '#9333ea' : color === 'blue' ? '#2563eb' : color === 'pink' ? '#db2777' : '#4f46e5'} />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`text-2xl font-bold bg-gradient-to-r ${colorClasses[color]} bg-clip-text text-transparent`}>
            {displayValue.toFixed(4)}
          </span>
        </div>
      </div>

      {/* Value Display */}
      <div className="text-center">
        <p className="text-3xl font-bold text-white mb-1">{displayValue.toFixed(4)}</p>
        <p className="text-sm text-gray-400">of {max.toFixed(1)} max</p>
        <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
          <div
            className={`h-full bg-gradient-to-r ${colorClasses[color]}`}
            style={{ width: `${normalizedPercentage}%` }}
          />
        </div>
      </div>

      {/* Breakdown (if provided) */}
      {breakdown && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <p className="text-xs text-gray-400 mb-2">Breakdown:</p>
          {Object.entries(breakdown).map(([key, val]: [string, any]) => (
            <div key={key} className="flex justify-between text-xs mb-1">
              <span className="text-gray-500">{key}:</span>
              <span className="text-gray-300">{typeof val === 'number' ? val.toFixed(3) : val}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

