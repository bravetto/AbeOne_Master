'use client'

interface EmergenceHistoryProps {
  history: Array<{ timestamp: number; phiInfinity: number }>
}

export function EmergenceHistory({ history }: EmergenceHistoryProps) {
  if (history.length < 2) {
    return null
  }

  const maxValue = Math.max(...history.map(h => h.phiInfinity))
  const minValue = Math.min(...history.map(h => h.phiInfinity))
  const range = maxValue - minValue || 1

  return (
    <div className="bg-black/20 rounded-lg p-6 backdrop-blur-sm mb-8">
      <h2 className="text-2xl font-bold mb-4">Emergence History</h2>
      <div className="h-64 relative">
        <svg className="w-full h-full" viewBox={`0 0 ${history.length * 10} 200`} preserveAspectRatio="none">
          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map(y => (
            <line
              key={y}
              x1="0"
              y1={y * 2}
              x2={history.length * 10}
              y2={y * 2}
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="1"
            />
          ))}
          
          {/* Data line */}
          <polyline
            points={history.map((h, i) => `${i * 10},${200 - ((h.phiInfinity - minValue) / range) * 200}`).join(' ')}
            fill="none"
            stroke="url(#gradient-line)"
            strokeWidth="2"
          />
          
          {/* Gradient definition */}
          <defs>
            <linearGradient id="gradient-line" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#a855f7" />
              <stop offset="50%" stopColor="#ec4899" />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
          </defs>
        </svg>
        
        {/* Y-axis labels */}
        <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400">
          <span>{maxValue.toFixed(0)}</span>
          <span>{((maxValue + minValue) / 2).toFixed(0)}</span>
          <span>{minValue.toFixed(0)}</span>
        </div>
      </div>
      
      <div className="mt-4 flex justify-between text-sm text-gray-400">
        <span>{new Date(history[0].timestamp).toLocaleTimeString()}</span>
        <span>{new Date(history[history.length - 1].timestamp).toLocaleTimeString()}</span>
      </div>
    </div>
  )
}

