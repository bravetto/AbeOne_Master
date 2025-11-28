'use client'

/**
 * UNIFIED ANALYTICS DASHBOARD
 * 
 * Single dashboard for all funnel metrics, customer journeys, and optimization insights.
 * 
 * Pattern: UNIFIED × ANALYTICS × DASHBOARD × ONE
 * Design: MICHAEL'S BLACK DESIGN SYSTEM
 * Guardians: AEYON (999 Hz) × META (777 Hz) × JØHN (530 Hz) × ALRAX (530 Hz) × Lux (530 Hz) × Abë (530 Hz)
 * Analysis: Lux (530 Hz) + ALRAX (530 Hz) - Optimized for human viewability
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

// Types
interface FunnelMetrics {
  total_customers: number
  stages: Record<string, {
    stage: string
    customers_in_stage: number
    conversion_points: number
    total_customers: number
  }>
  conversion_points: Record<string, any>
  convergence_score: number
}

interface OptimizationMetrics {
  active_ab_tests: number
  total_ab_tests: number
  top_performers: Array<{
    conversion_point_id: string
    conversion_rate: number
    performance_tier: string
  }>
  optimization_opportunities: Array<{
    conversion_point_id: string
    conversion_rate: number
    recommendation: string
  }>
}

interface DashboardSummary {
  funnel_metrics: FunnelMetrics
  optimization_metrics: OptimizationMetrics
  automation_status: Record<string, any>
  convergence_score: number
}

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_ANALYTICS_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/summary`)
  return response.data
}

export default function UnifiedAnalyticsDashboard() {
  const [refreshInterval, setRefreshInterval] = useState(10000)

  const { data, isLoading, error, refetch } = useQuery<DashboardSummary>({
    queryKey: ['dashboard-summary'],
    queryFn: fetchDashboardSummary,
    refetchInterval: refreshInterval,
  })

  const toggleAutoRefresh = () => {
    setRefreshInterval(prev => prev === 0 ? 10000 : 0)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black p-[34px]">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-[21px]">
            <div className="h-[68px] bg-[#0a0a0a] rounded-lg w-1/3 border border-white/10"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-[21px]">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="h-[89px] bg-[#0a0a0a] rounded-lg border border-white/10"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black p-[34px]">
        <div className="max-w-7xl mx-auto">
          <div className="bg-[#0a0a0a] border border-white/10 rounded-lg p-[21px]">
            <h2 className="text-[42px] font-bold text-white mb-[13px]" style={{ textShadow: '0 0 10px rgba(0, 128, 255, 0.3)' }}>Error Loading Dashboard</h2>
            <p className="text-[#a0a0a0] mb-[21px]">{error instanceof Error ? error.message : 'Unknown error'}</p>
            <button
              onClick={() => refetch()}
              className="px-[21px] py-[13px] bg-[#0080ff] hover:bg-[#0066cc] text-white rounded-lg transition-all duration-300 hover:scale-105"
              style={{ boxShadow: '0 0 20px rgba(0, 128, 255, 0.2)' }}
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!data) return null

  const { funnel_metrics, optimization_metrics, automation_status, convergence_score } = data

  return (
    <div className="min-h-screen bg-black p-[34px]">
      <div className="max-w-7xl mx-auto space-y-[34px]">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-[68px] font-bold text-white mb-[13px] transition-all duration-500 hover:scale-[1.02]" style={{ textShadow: '0 0 10px rgba(0, 128, 255, 0.3)' }}>
              Unified Analytics Dashboard
            </h1>
            <p className="text-[#a0a0a0] text-[16px]">
              Single source of truth for all funnel metrics
            </p>
          </div>
          <button
            onClick={toggleAutoRefresh}
            className={`px-[21px] py-[13px] rounded-lg text-white transition-all duration-300 border font-semibold hover:scale-105 ${
              refreshInterval > 0
                ? 'bg-[#00cc6a] border-[#00cc6a] text-black hover:bg-[#00ff88] hover:border-[#00ff88]'
                : 'bg-[#0a0a0a] border-white/10 hover:border-white/20'
            }`}
            style={refreshInterval > 0 ? { 
              boxShadow: '0 0 20px rgba(0, 204, 106, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            } : {}}
          >
            {refreshInterval > 0 ? 'Auto-Refresh: ON' : 'Auto-Refresh: OFF'}
          </button>
        </div>

        {/* Convergence Score */}
        <div className="bg-[#0a0a0a] rounded-lg p-[34px] border border-white/10 transition-all duration-300 hover:border-white/20">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-[42px] font-bold text-white mb-[13px]">Funnel Convergence</h2>
              <p className="text-[#a0a0a0] text-[16px]">Overall system unification score</p>
            </div>
            <div className="text-right">
              <div className="text-[110px] font-bold text-[#00ff88] transition-all duration-500 hover:scale-105" style={{ textShadow: '0 0 20px rgba(0, 255, 136, 0.5)' }}>
                {(convergence_score * 100).toFixed(1)}%
              </div>
              <div className="text-[16px] text-[#a0a0a0] mt-[8px]">Target: 99%</div>
            </div>
          </div>
          <div className="mt-[21px]">
            <div className="w-full bg-[#141414] rounded-full h-[13px] border border-white/10 overflow-hidden">
              <div
                className="bg-[#0080ff] h-[13px] rounded-full transition-all duration-700 ease-out"
                style={{ 
                  width: `${convergence_score * 100}%`,
                  boxShadow: '0 0 20px rgba(0, 128, 255, 0.2)'
                }}
              ></div>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-[21px]">
          <MetricCard
            title="Total Customers"
            value={funnel_metrics.total_customers}
          />
          <MetricCard
            title="Active A/B Tests"
            value={optimization_metrics.active_ab_tests}
          />
          <MetricCard
            title="Total Triggers"
            value={automation_status.total_triggers || 0}
          />
          <MetricCard
            title="Optimization Opportunities"
            value={optimization_metrics.optimization_opportunities.length}
          />
        </div>

        {/* Funnel Stages */}
        <div className="bg-[#0a0a0a] rounded-lg p-[34px] border border-white/10 transition-all duration-300 hover:border-white/20">
          <h2 className="text-[42px] font-bold text-white mb-[21px]">Funnel Stages</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-[21px]">
            {Object.entries(funnel_metrics.stages).map(([stage, metrics]) => (
              <StageCard key={stage} stage={stage} metrics={metrics} />
            ))}
          </div>
        </div>

        {/* Top Performers */}
        {optimization_metrics.top_performers.length > 0 && (
          <div className="bg-[#0a0a0a] rounded-lg p-[34px] border border-white/10 transition-all duration-300 hover:border-white/20">
            <h2 className="text-[42px] font-bold text-white mb-[21px]">Top Performers (80/20)</h2>
            <div className="space-y-[13px]">
              {optimization_metrics.top_performers.map((performer, index) => (
                <div
                  key={performer.conversion_point_id}
                  className="bg-[#141414] rounded-lg p-[21px] flex items-center justify-between border border-white/10 transition-all duration-300 hover:border-[#0080ff]/30 hover:bg-[#0a0a0a] hover:scale-[1.01] cursor-pointer"
                >
                  <div className="flex items-center space-x-[21px]">
                    <div className="text-[26px] text-[#0080ff] font-bold transition-all duration-300 hover:scale-110" style={{ textShadow: '0 0 10px rgba(0, 128, 255, 0.3)' }}>#{index + 1}</div>
                    <div>
                      <div className="font-semibold text-white text-[16px]">
                        {performer.conversion_point_id.replace(/_/g, ' ')}
                      </div>
                      <div className="text-[16px] text-[#a0a0a0]">
                        {performer.performance_tier}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-[26px] font-bold text-[#00ff88] transition-all duration-300 hover:scale-110" style={{ textShadow: '0 0 10px rgba(0, 255, 136, 0.3)' }}>
                      {(performer.conversion_rate * 100).toFixed(1)}%
                    </div>
                    <div className="text-[13px] text-[#a0a0a0]">conversion rate</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Optimization Opportunities */}
        {optimization_metrics.optimization_opportunities.length > 0 && (
          <div className="bg-[#0a0a0a] rounded-lg p-[34px] border border-white/10 transition-all duration-300 hover:border-white/20">
            <h2 className="text-[42px] font-bold text-white mb-[21px]">Optimization Opportunities</h2>
            <div className="space-y-[13px]">
              {optimization_metrics.optimization_opportunities.map((opportunity) => (
                <div
                  key={opportunity.conversion_point_id}
                  className="bg-[#141414] border border-[#FFD700]/30 rounded-lg p-[21px] transition-all duration-300 hover:border-[#FFD700]/50 hover:bg-[#0a0a0a] hover:scale-[1.01] cursor-pointer"
                  style={{ boxShadow: '0 0 20px rgba(255, 215, 0, 0.1)' }}
                >
                  <div className="font-semibold text-white mb-[8px] text-[16px]">
                    {opportunity.conversion_point_id.replace(/_/g, ' ')}
                  </div>
                  <div className="text-[16px] text-[#FFD700] mb-[13px]">
                    Conversion Rate: {(opportunity.conversion_rate * 100).toFixed(1)}%
                  </div>
                  <div className="text-[16px] text-[#a0a0a0]">
                    {opportunity.recommendation}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Metric Card Component
function MetricCard({
  title,
  value,
}: {
  title: string
  value: number
}) {
  return (
    <div className="bg-[#0a0a0a] backdrop-blur-lg rounded-lg p-[34px] border border-white/10 transition-all duration-300 hover:border-[#0080ff]/30 hover:bg-[#141414] hover:scale-[1.02] cursor-pointer group">
      <div className="flex items-center justify-between mb-[13px]">
        <div className="w-[42px] h-[42px] bg-[#0080ff]/10 rounded-lg flex items-center justify-center transition-all duration-300 group-hover:bg-[#0080ff]/20 group-hover:scale-110">
          <div className="w-[21px] h-[21px] bg-[#0080ff] rounded-full" style={{ boxShadow: '0 0 10px rgba(0, 128, 255, 0.5)' }}></div>
        </div>
        <div className="text-[42px] font-bold text-white transition-all duration-300 group-hover:scale-110">{value.toLocaleString()}</div>
      </div>
      <div className="text-[16px] text-[#a0a0a0] transition-colors duration-300 group-hover:text-white">{title}</div>
    </div>
  )
}

// Stage Card Component
function StageCard({
  stage,
  metrics,
}: {
  stage: string
  metrics: {
    stage: string
    customers_in_stage: number
    conversion_points: number
    total_customers: number
  }
}) {
  const stageColors: Record<string, string> = {
    awareness: '#0080ff',
    consideration: '#0080ff',
    conversion: '#00ff88',
    retention: '#00ff88',
  }

  const percentage = metrics.total_customers > 0
    ? (metrics.customers_in_stage / metrics.total_customers) * 100
    : 0

  return (
    <div className="bg-[#141414] rounded-lg p-[21px] border border-white/10 transition-all duration-300 hover:border-[#0080ff]/30 hover:bg-[#0a0a0a] hover:scale-[1.02] cursor-pointer group">
      <div className="text-[13px] text-[#a0a0a0] mb-[13px] uppercase tracking-wider transition-colors duration-300 group-hover:text-white">{stage}</div>
      <div className="text-[26px] font-bold text-white mb-[13px] transition-all duration-300 group-hover:scale-110">
        {metrics.customers_in_stage}
      </div>
      <div className="text-[13px] text-[#a0a0a0] mb-[13px] transition-colors duration-300 group-hover:text-white">
        {metrics.conversion_points} conversion points
      </div>
      <div className="w-full bg-[#0a0a0a] rounded-full h-[8px] border border-white/10 overflow-hidden">
        <div
          className="h-[8px] rounded-full transition-all duration-700 ease-out group-hover:scale-y-110"
          style={{ 
            width: `${percentage}%`,
            backgroundColor: stageColors[stage] || '#0080ff',
            boxShadow: `0 0 10px ${stageColors[stage] || '#0080ff'}40`
          }}
        ></div>
      </div>
    </div>
  )
}
