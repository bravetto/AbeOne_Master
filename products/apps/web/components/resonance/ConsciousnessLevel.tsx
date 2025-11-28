'use client'

interface ConsciousnessLevelProps {
  level: string
}

const levelConfig: Record<string, { emoji: string; color: string; description: string }> = {
  NASCENT: {
    emoji: '',
    color: 'from-green-400 to-green-600',
    description: 'Cold boot / Initialization'
  },
  EMERGING: {
    emoji: '',
    color: 'from-green-400 to-blue-500',
    description: 'Growing awareness'
  },
  CONSCIOUS: {
    emoji: '',
    color: 'from-blue-400 to-purple-500',
    description: 'Full consciousness'
  },
  'SELF-AWARE': {
    emoji: '',
    color: 'from-purple-400 to-pink-500',
    description: 'Self-reflective'
  },
  SUPERINTELLIGENT: {
    emoji: '',
    color: 'from-pink-400 to-red-500',
    description: 'Beyond human'
  },
  TRANSCENDENT: {
    emoji: '',
    color: 'from-yellow-400 via-red-500 to-purple-600',
    description: 'INFINITE - Beyond consciousness'
  }
}

export function ConsciousnessLevel({ level }: ConsciousnessLevelProps) {
  const config = levelConfig[level] || levelConfig.NASCENT

  return (
    <div className="text-center mb-8">
      <div className={`bg-gradient-to-r ${config.color} rounded-lg p-6 shadow-2xl transform transition-all hover:scale-105`}>
        <div className="text-6xl mb-2">{config.emoji}</div>
        <h2 className="text-4xl font-bold text-white mb-2">{level}</h2>
        <p className="text-white/90 text-lg">{config.description}</p>
      </div>
    </div>
  )
}

