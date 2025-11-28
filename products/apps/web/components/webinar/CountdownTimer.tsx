'use client'

/**
 * Countdown Timer Component
 * 20-40% conversion increase - Creates urgency/scarcity
 * 
 * Pattern: Urgency × Scarcity × Deadline Pressure × ONE
 * Guardians: AEYON (999 Hz) × Lux (530 Hz)
 */

import { useState, useEffect } from 'react'
import { Icon } from '@/components/icons/Icon'

interface CountdownTimerProps {
  targetDate: string // ISO date string
  targetTime: string // Time string (e.g., "2:00 PM EST")
  onExpired?: () => void
}

export function CountdownTimer({ targetDate, targetTime, onExpired }: CountdownTimerProps) {
  const [timeRemaining, setTimeRemaining] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    expired: false
  })

  useEffect(() => {
    // Parse target date and time
    const [datePart] = targetDate.split('T')
    const [hours, minutes] = targetTime.includes('PM') 
      ? targetTime.replace(' PM EST', '').split(':').map((v, i) => i === 0 ? parseInt(v) + 12 : parseInt(v))
      : targetTime.replace(' AM EST', '').split(':').map(v => parseInt(v))
    
    const webinarDate = new Date(`${datePart}T${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:00-05:00`)

    const interval = setInterval(() => {
      const now = new Date()
      const diff = webinarDate.getTime() - now.getTime()

      if (diff <= 0) {
        setTimeRemaining({ days: 0, hours: 0, minutes: 0, seconds: 0, expired: true })
        clearInterval(interval)
        if (onExpired) onExpired()
        return
      }

      setTimeRemaining({
        days: Math.floor(diff / (1000 * 60 * 60 * 24)),
        hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((diff % (1000 * 60)) / 1000),
        expired: false
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [targetDate, targetTime, onExpired])

  if (timeRemaining.expired) {
    return (
      <div className="bg-warm-500/20 border-2 border-warm-500 rounded-xl p-6 mb-6">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Icon name="rocket" size={24} className="text-warm-600" />
          <p className="text-center text-warm-700 font-bold text-lg">
            Webinar is live! Join now →
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-br from-warm-50 to-warm-100 border-2 border-warm-500 rounded-xl p-6 mb-6 shadow-lg">
      <div className="flex items-center justify-center gap-2 mb-4">
        <Icon name="calendar" size={20} className="text-warm-600" />
        <p className="text-center text-warm-700 font-semibold text-lg">
          Webinar starts in:
        </p>
      </div>
      <div className="flex justify-center gap-3 md:gap-6 mb-4">
        <div className="text-center bg-white rounded-lg p-3 min-w-[60px] shadow-md">
          <div className="text-2xl md:text-4xl font-bold text-warm-600">{timeRemaining.days}</div>
          <div className="text-xs text-warm-600 font-medium">Days</div>
        </div>
        <div className="text-warm-600 text-2xl md:text-3xl font-bold self-center">:</div>
        <div className="text-center bg-white rounded-lg p-3 min-w-[60px] shadow-md">
          <div className="text-2xl md:text-4xl font-bold text-warm-600">{String(timeRemaining.hours).padStart(2, '0')}</div>
          <div className="text-xs text-warm-600 font-medium">Hours</div>
        </div>
        <div className="text-warm-600 text-2xl md:text-3xl font-bold self-center">:</div>
        <div className="text-center bg-white rounded-lg p-3 min-w-[60px] shadow-md">
          <div className="text-2xl md:text-4xl font-bold text-warm-600">{String(timeRemaining.minutes).padStart(2, '0')}</div>
          <div className="text-xs text-warm-600 font-medium">Minutes</div>
        </div>
        <div className="text-warm-600 text-2xl md:text-3xl font-bold self-center">:</div>
        <div className="text-center bg-white rounded-lg p-3 min-w-[60px] shadow-md">
          <div className="text-2xl md:text-4xl font-bold text-warm-600">{String(timeRemaining.seconds).padStart(2, '0')}</div>
          <div className="text-xs text-warm-600 font-medium">Seconds</div>
        </div>
      </div>
      <p className="text-center text-sm text-warm-700 font-medium">
        Limited to Founding 100 members
      </p>
    </div>
  )
}

