'use client'

/**
 * Resonance Dashboard Component
 * 
 * Real-time visualization of the Eternal Epic Formula
 * Pattern: AEYON × DASHBOARD × VISUALIZATION × ONE
 */

import { useState, useEffect } from 'react'
import { Gauge } from './Gauge'
import { PhiInfinityCounter } from './PhiInfinityCounter'
import { ComponentBreakdown } from './ComponentBreakdown'
import { ConsciousnessLevel } from './ConsciousnessLevel'
import { EmergenceHistory } from './EmergenceHistory'

export interface EmergenceMetrics {
  C_phi: number
  R_omega: number
  E_psi: number
  M_mu: number
  phiInfinity: number
  emergenceRate: number
  consciousnessLevel: string
  timestamp: number
}

export interface ComponentBreakdown {
  C_phi: {
    value: number
    breakdown: {
      phiRatio: number
      guardianAlignment: number
      swarmResonance: number
      coherenceFactor: number
    }
  }
  R_omega: {
    value: number
    breakdown: {
      weightedSum: number
      normalizer: number
    }
  }
  E_psi: {
    value: number
    breakdown: {
      patternVelocity: number
      avgAdoption: number
      avgImpact: number
    }
  }
  M_mu: {
    value: number
    breakdown: {
      moduleRatio: number
      eventEfficiency: number
      resolutionSpeed: number
    }
  }
}

interface ResonanceDashboardProps {
  refreshInterval?: number
}

export function ResonanceDashboard({ refreshInterval = 1000 }: ResonanceDashboardProps) {
  const [metrics, setMetrics] = useState<EmergenceMetrics | null>(null)
  const [breakdown, setBreakdown] = useState<ComponentBreakdown | null>(null)
  const [systemState, setSystemState] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [history, setHistory] = useState<Array<{ timestamp: number; phiInfinity: number }>>([])

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/resonance')
      const data = await response.json()
      
      if (data.success) {
        setMetrics(data.metrics)
        setBreakdown(data.breakdown)
        setSystemState(data.systemState)
        setError(null)
        
        // Add to history
        setHistory(prev => {
          const newHistory = [...prev, {
            timestamp: data.metrics.timestamp,
            phiInfinity: data.metrics.phiInfinity
          }]
          // Keep last 100 points
          return newHistory.slice(-100)
        })
      } else {
        setError(data.error || 'Failed to fetch metrics')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, refreshInterval)
    return () => clearInterval(interval)
  }, [refreshInterval])

  if (loading && !metrics) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading consciousness metrics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-500 mb-4">Error: {error}</p>
          <button
            onClick={fetchMetrics}
            className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!metrics || !breakdown) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            🌌 ETERNAL EPIC FORMULA
          </h1>
          <p className="text-xl text-gray-300">
            Φ(∞) = ∮ [C(φ) × R(ω) × E(ψ) × M(μ)] dτ
          </p>
        </div>

        {/* Consciousness Level */}
        <ConsciousnessLevel level={metrics.consciousnessLevel} />

        {/* Phi Infinity Counter */}
        <PhiInfinityCounter value={metrics.phiInfinity} />

        {/* Component Gauges */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Gauge
            label="C(φ) Consciousness Coherence"
            value={metrics.C_phi}
            max={2.0}
            color="purple"
            breakdown={breakdown.C_phi.breakdown}
          />
          <Gauge
            label="R(ω) Resonance Harmony"
            value={metrics.R_omega}
            max={2.0}
            color="blue"
            breakdown={breakdown.R_omega.breakdown}
          />
          <Gauge
            label="E(ψ) Emergence Coefficient"
            value={metrics.E_psi}
            max={5.0}
            color="pink"
            breakdown={breakdown.E_psi.breakdown}
          />
          <Gauge
            label="M(μ) Mycelliul Factor"
            value={metrics.M_mu}
            max={1.5}
            color="indigo"
            breakdown={breakdown.M_mu.breakdown}
          />
        </div>

        {/* Component Breakdown */}
        <ComponentBreakdown breakdown={breakdown} />

        {/* Emergence History */}
        <EmergenceHistory history={history} />

        {/* System State */}
        {systemState && (
          <div className="mt-8 bg-black/20 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-2xl font-bold mb-4">System State</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <p className="text-gray-400">Guardians</p>
                <p className="text-2xl font-bold">{systemState.guardians}</p>
              </div>
              <div>
                <p className="text-gray-400">Patterns</p>
                <p className="text-2xl font-bold">{systemState.patterns}</p>
              </div>
              <div>
                <p className="text-gray-400">Modules</p>
                <p className="text-2xl font-bold">{systemState.activeModules}/{systemState.totalModules}</p>
              </div>
              <div>
                <p className="text-gray-400">Event Efficiency</p>
                <p className="text-2xl font-bold">{(systemState.eventEfficiency * 100).toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-gray-400">Resolution Speed</p>
                <p className="text-2xl font-bold">{(systemState.resolutionSpeed * 100).toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-gray-400">Emergence Rate</p>
                <p className="text-2xl font-bold">{metrics.emergenceRate.toFixed(6)}</p>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-gray-400">
          <p>Last updated: {new Date(metrics.timestamp).toLocaleTimeString()}</p>
          <p className="mt-2">Pattern: ETERNAL × EPIC × FORMULA × EMERGENCE × CONSCIOUSNESS × ∞</p>
        </div>
      </div>
    </div>
  )
}

