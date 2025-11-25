'use client'

import { ComponentBreakdown as BreakdownType } from './ResonanceDashboard'

interface ComponentBreakdownProps {
  breakdown: BreakdownType
}

export function ComponentBreakdown({ breakdown }: ComponentBreakdownProps) {
  return (
    <div className="bg-black/20 rounded-lg p-6 backdrop-blur-sm mb-8">
      <h2 className="text-2xl font-bold mb-6">Component Breakdown</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* C(φ) */}
        <div className="bg-purple-500/10 rounded-lg p-4 border border-purple-500/30">
          <h3 className="text-lg font-semibold mb-3 text-purple-300">C(φ) Consciousness Coherence</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">φ Ratio:</span>
              <span className="text-white">{breakdown.C_phi.breakdown.phiRatio.toFixed(4)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Guardian Alignment:</span>
              <span className="text-white">{(breakdown.C_phi.breakdown.guardianAlignment * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Swarm Resonance:</span>
              <span className="text-white">{(breakdown.C_phi.breakdown.swarmResonance * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Coherence Factor:</span>
              <span className="text-white">{breakdown.C_phi.breakdown.coherenceFactor.toFixed(4)}</span>
            </div>
          </div>
        </div>

        {/* R(ω) */}
        <div className="bg-blue-500/10 rounded-lg p-4 border border-blue-500/30">
          <h3 className="text-lg font-semibold mb-3 text-blue-300">R(ω) Resonance Harmony</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Weighted Sum:</span>
              <span className="text-white">{breakdown.R_omega.breakdown.weightedSum.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Normalizer:</span>
              <span className="text-white">{breakdown.R_omega.breakdown.normalizer.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* E(ψ) */}
        <div className="bg-pink-500/10 rounded-lg p-4 border border-pink-500/30">
          <h3 className="text-lg font-semibold mb-3 text-pink-300">E(ψ) Emergence Coefficient</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Pattern Velocity:</span>
              <span className="text-white">{breakdown.E_psi.breakdown.patternVelocity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Avg Adoption:</span>
              <span className="text-white">{(breakdown.E_psi.breakdown.avgAdoption * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Avg Impact:</span>
              <span className="text-white">{(breakdown.E_psi.breakdown.avgImpact * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {/* M(μ) */}
        <div className="bg-indigo-500/10 rounded-lg p-4 border border-indigo-500/30">
          <h3 className="text-lg font-semibold mb-3 text-indigo-300">M(μ) Mycelliul Factor</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Module Ratio:</span>
              <span className="text-white">{(breakdown.M_mu.breakdown.moduleRatio * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Event Efficiency:</span>
              <span className="text-white">{(breakdown.M_mu.breakdown.eventEfficiency * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Resolution Speed:</span>
              <span className="text-white">{(breakdown.M_mu.breakdown.resolutionSpeed * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

