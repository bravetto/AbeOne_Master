'use client'

import { useBackendHealth } from '@/hooks/useBackendHealth'

interface TopbarProps {
  kernelStatus: any
}

export default function Topbar({ kernelStatus }: TopbarProps) {
  const { health, isHealthy, isChecking } = useBackendHealth()
  const hasError = kernelStatus?.error
  const isInitialized = kernelStatus?.initialized === true
  
  // Determine status display based on backend health and kernel status
  const getStatusDisplay = () => {
    if (isChecking) {
      return { text: 'Checking connection...', color: 'bg-warm-400', textColor: 'text-warm-600' }
    }
    
    if (health.status === 'not-configured') {
      return { text: 'Backend not configured', color: 'bg-heart-500', textColor: 'text-heart-600' }
    }
    
    if (health.status === 'unavailable' || health.status === 'unhealthy') {
      return { 
        text: health.error || 'Backend unavailable', 
        color: 'bg-heart-500', 
        textColor: 'text-heart-600' 
      }
    }
    
    if (isHealthy && isInitialized) {
      return { text: 'Ready for you', color: 'bg-peace-500', textColor: 'text-peace-600' }
    }
    
    if (isHealthy && !isInitialized) {
      return { text: 'Backend connected', color: 'bg-peace-500', textColor: 'text-peace-600' }
    }
    
    if (hasError) {
      return { text: 'Connection needed', color: 'bg-heart-500', textColor: 'text-heart-600' }
    }
    
    return { text: 'Preparing...', color: 'bg-warm-400', textColor: 'text-warm-600' }
  }
  
  const status = getStatusDisplay()
  
  return (
    <header className="bg-white/90 backdrop-blur-sm shadow-sm border-b border-lux-100">
      <div className="px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-display font-semibold text-gray-800">
          Your Space
        </h1>
        <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 px-4 py-2 bg-gray-50 rounded-lg border border-gray-200">
              <div
              className={`w-3 h-3 rounded-full ${isChecking ? 'animate-pulse' : ''} ${status.color}`}
              />
            <span className={`text-sm font-medium ${status.textColor}`}>
              {status.text}
              </span>
            </div>
        </div>
      </div>
    </header>
  )
}

