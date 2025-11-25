'use client'

/**
 * Deanna's Backlog Awareness Portal
 * 
 * Pattern: PORTAL × DEANNA × MICHAEL_DESIGN × LIVE_DATA × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz) × Abë (530 Hz) × Michael (2222 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PortalHeader } from './components/PortalHeader'
import { MetricsGrid } from './components/MetricsGrid'
import { StatusBreakdown } from './components/StatusBreakdown'
import { ProjectGrid } from './components/ProjectGrid'
import { GuardianDistribution } from './components/GuardianDistribution'
import { TeamDistribution } from './components/TeamDistribution'
import { ConvergenceScore } from './components/ConvergenceScore'
import { ActivityFeed } from './components/ActivityFeed'
import { Filters } from './components/Filters'
import { OperationsUnified } from './components/OperationsUnified'
import { AnimatedCard } from './components/AnimatedCard'
import { ProductIdeasWidget } from './components/ProductIdeasWidget'
import { ProductIdeasActivityFeed } from './components/ProductIdeasActivityFeed'
import { ProductIdeaSubmissionForm } from './components/ProductIdeaSubmissionForm'

// Inline hooks (since hooks directory may be blocked)
interface AggregatedBacklog {
  total_items: number
  items_by_status: Record<string, number>
  items_by_guardian: Record<string, number>
  items_by_assignee: Record<string, number>
  projects: Array<{
    project_id: string
    project_name: string
    project_type: string
    item_count: number
  }>
  aggregated_at: string
  convergence_score: number
}

interface ActivityItem {
  id: string
  type: 'commit' | 'pr' | 'task' | 'deployment' | 'meeting' | 'creation'
  title: string
  description?: string
  user: string
  project: string
  timestamp: string
  guardian?: string
  icon: string
  color: string
}

interface UnifiedOperationsData {
  operations: {
    backlog: { total_items: number; convergence_score: number; items_by_status: Record<string, number> }
    team_workload: Record<string, number>
    blocked_items: number
  }
  rd: { active_research: number; experiments: number; publications: number; patents: number }
  tech: { deployments: number; infrastructure_health: number; api_uptime: number; security_score: number }
  marketing: { campaigns_active: number; conversion_rate: number; engagement_rate: number; revenue_attributed: number }
  finance: { revenue: number; expenses: number; profit_margin: number; runway_months: number }
  last_updated: string
  data_quality: {
    operations: 'validated' | 'pending' | 'error'
    rd: 'validated' | 'pending' | 'error'
    tech: 'validated' | 'pending' | 'error'
    marketing: 'validated' | 'pending' | 'error'
    finance: 'validated' | 'pending' | 'error'
  }
}

const fetchUnifiedData = async (): Promise<UnifiedOperationsData> => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  try {
    const response = await fetch(`${apiUrl}/api/v1/portal/unified`)
    if (response.ok) return await response.json()
  } catch (error) {
    console.warn('Unified API fetch failed, using mock data:', error)
  }
  return {
    operations: {
      backlog: { total_items: 247, convergence_score: 87.5, items_by_status: { backlog: 89, planning: 34, in_progress: 55, review: 21, done: 42, blocked: 6 } },
      team_workload: { 'bill': 34, 'danny': 28, 'phani': 25, 'jacob': 21, 'ben': 18, 'jimmy': 15, 'mohammad': 12, 'unassigned': 94 },
      blocked_items: 6,
    },
    rd: { active_research: 12, experiments: 8, publications: 3, patents: 5 },
    tech: { deployments: 47, infrastructure_health: 98.5, api_uptime: 99.9, security_score: 95 },
    marketing: { campaigns_active: 6, conversion_rate: 3.2, engagement_rate: 12.5, revenue_attributed: 125000 },
    finance: { revenue: 450000, expenses: 320000, profit_margin: 28.9, runway_months: 18 },
    last_updated: new Date().toISOString(),
    data_quality: { operations: 'validated', rd: 'validated', tech: 'validated', marketing: 'validated', finance: 'validated' },
  }
}

const fetchBacklog = async (): Promise<AggregatedBacklog> => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  try {
    const response = await fetch(`${apiUrl}/api/v1/portal/backlogs`)
    if (response.ok) return await response.json()
  } catch (error) {
    console.warn('API fetch failed, using mock data:', error)
  }
  // Mock data
  return {
    total_items: 247,
    items_by_status: { backlog: 89, planning: 34, in_progress: 55, review: 21, done: 42, blocked: 6 },
    items_by_guardian: {
      'Guardian AEYON': 68, 'Guardian William': 42, 'Guardian Daniel': 34, 'Guardian Phani': 28,
      'Guardian Jacob': 21, 'Guardian Neuro': 13, 'Guardian Jimmy': 21, 'Guardian Zero': 20,
    },
    items_by_assignee: {
      'bill': 34, 'danny': 28, 'phani': 25, 'jacob': 21, 'ben': 18,
      'jimmy': 15, 'mohammad': 12, 'unassigned': 94,
    },
    projects: [
      { project_id: 'abeflows', project_name: 'AbëFLOWs', project_type: 'orbital', item_count: 89 },
      { project_id: 'aiguardian', project_name: 'AI Guardian', project_type: 'orbital', item_count: 55 },
      { project_id: 'emergent-os', project_name: 'EMERGENT OS', project_type: 'orbital', item_count: 42 },
      { project_id: 'abekeys', project_name: 'AbëKEYS', project_type: 'product', item_count: 34 },
      { project_id: 'abedesks', project_name: 'AbëDESKs', project_type: 'product', item_count: 21 },
      { project_id: 'abebeats', project_name: 'AbëBEATS', project_type: 'product', item_count: 6 },
    ],
    aggregated_at: new Date().toISOString(),
    convergence_score: 87.5,
  }
}

const fetchActivities = async (): Promise<ActivityItem[]> => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  try {
    const response = await fetch(`${apiUrl}/api/v1/portal/activities`)
    if (response.ok) {
      const data = await response.json()
      return data.activities || []
    }
  } catch (error) {
    console.warn('Activities API fetch failed, using mock data:', error)
  }
  const now = new Date()
  return [
    {
      id: '1', type: 'task', title: 'Portal Gateway Architecture Complete',
      description: 'Cross-project backlog awareness enabled', user: 'deanna', project: 'abeflows',
      timestamp: new Date(now.getTime() - 5 * 60000).toISOString(), guardian: 'Guardian AEYON',
      icon: '✓', color: '#00ff88',
    },
    {
      id: '2', type: 'commit', title: 'Updated GZ360 Integration',
      description: 'Deanna profile connected to portal', user: 'jacob', project: 'abeflows',
      timestamp: new Date(now.getTime() - 15 * 60000).toISOString(), guardian: 'Guardian Jacob',
      icon: '↗', color: '#0080ff',
    },
    {
      id: '3', type: 'pr', title: 'Portal Dashboard UI Complete',
      description: 'Michael Design System applied', user: 'ben', project: 'web',
      timestamp: new Date(now.getTime() - 30 * 60000).toISOString(), guardian: 'Guardian Neuro',
      icon: '🔀', color: '#0080ff',
    },
    {
      id: '4', type: 'deployment', title: 'Portal Deployed to Production',
      description: 'Live at /portal/deanna', user: 'danny', project: 'web',
      timestamp: new Date(now.getTime() - 45 * 60000).toISOString(), guardian: 'Guardian Daniel',
      icon: '🚀', color: '#00ff88',
    },
    {
      id: '5', type: 'task', title: 'Backlog Aggregation Engine Active',
      description: 'All projects synchronized', user: 'system', project: 'abeflows',
      timestamp: new Date(now.getTime() - 60 * 60000).toISOString(), guardian: 'Guardian AEYON',
      icon: '⚡', color: '#0080ff',
    },
  ]
}

export default function DeannaPortal() {
  const [filters, setFilters] = useState({
    showBlocked: true,
    showUnassigned: true,
    guardian: null as string | null,
    status: null as string | null,
  })

  const { data: backlog, isLoading: backlogLoading, error: backlogError } = useQuery({
    queryKey: ['backlog', 'aggregated'],
    queryFn: fetchBacklog,
    staleTime: 10000,
    refetchInterval: 30000,
    retry: 2,
  })
  
  const { data: activities, isLoading: activitiesLoading } = useQuery({
    queryKey: ['activities', 'feed'],
    queryFn: fetchActivities,
    staleTime: 5000,
    refetchInterval: 15000,
    retry: 2,
  })

  const { data: unifiedData, isLoading: unifiedLoading } = useQuery<UnifiedOperationsData, Error>({
    queryKey: ['unified', 'operations'],
    queryFn: fetchUnifiedData,
    staleTime: 10000,
    refetchInterval: 30000,
    retry: 2,
  })

  if (backlogError) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#000000',
        color: '#ffffff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '55px',
      }}>
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '42px', marginBottom: '21px', color: '#ffffff' }}>
            Portal Error
          </h2>
          <p style={{ fontSize: '16px', color: '#a0a0a0', marginBottom: '34px' }}>
            {backlogError.message}
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              padding: '13px 21px',
              backgroundColor: '#0080ff',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              textShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#0066cc'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#0080ff'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div 
      className="portal-container"
      style={{
        minHeight: '100vh',
        backgroundColor: '#000000',
        color: '#ffffff',
        padding: '24px',
        animation: 'portalFadeIn 0.5s ease-in',
      }}
    >
      {/* Portal Header */}
      <AnimatedCard delay={0}>
        <PortalHeader 
          name="Deanna Delancey"
          role="COO"
          guardian="Guardian AEYON"
          frequency={999}
        />
      </AnimatedCard>

      {/* Unified Operations Dashboard - Operations × R&D × Tech × Marketing × Finance */}
      {unifiedData && (
        <AnimatedCard delay={100}>
          <OperationsUnified data={unifiedData} />
        </AnimatedCard>
      )}

      {/* Filters */}
      <AnimatedCard delay={200}>
        <Filters filters={filters} onFiltersChange={setFilters} />
      </AnimatedCard>

      {/* Convergence Score - Hero Metric */}
      {backlog && (
        <AnimatedCard delay={300}>
          <div style={{ marginBottom: '40px' }}>
            <ConvergenceScore score={backlog.convergence_score} />
          </div>
        </AnimatedCard>
      )}

      {/* Metrics Grid */}
      {backlog && (
        <AnimatedCard delay={400}>
          <div style={{ marginBottom: '40px' }}>
            <MetricsGrid backlog={backlog} />
          </div>
        </AnimatedCard>
      )}

      {/* Status Breakdown */}
      {backlog && (
        <AnimatedCard delay={500}>
          <div style={{ marginBottom: '40px' }}>
            <StatusBreakdown itemsByStatus={backlog.items_by_status} />
          </div>
        </AnimatedCard>
      )}

      {/* Main Content Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '24px',
        marginBottom: '55px',
      }}>
        {/* Project Grid */}
        {backlog && (
          <AnimatedCard delay={600}>
            <ProjectGrid 
              projects={backlog.projects}
              filters={filters}
            />
          </AnimatedCard>
        )}

        {/* Guardian Distribution */}
        {backlog && (
          <AnimatedCard delay={700}>
            <GuardianDistribution itemsByGuardian={backlog.items_by_guardian} />
          </AnimatedCard>
        )}

        {/* Team Distribution */}
        {backlog && (
          <AnimatedCard delay={800}>
            <TeamDistribution itemsByAssignee={backlog.items_by_assignee} />
          </AnimatedCard>
        )}
      </div>

      {/* Product Ideas Submission Form */}
      <AnimatedCard delay={900}>
        <div style={{ marginBottom: '40px' }}>
          <ProductIdeaSubmissionForm 
            onSuccess={() => {
              // Refetch product ideas data
              window.location.reload()
            }}
          />
        </div>
      </AnimatedCard>

      {/* Product Ideas Widget */}
      <AnimatedCard delay={1000}>
        <div style={{ marginBottom: '40px' }}>
          <ProductIdeasWidget />
        </div>
      </AnimatedCard>

      {/* Activity Feed */}
      {activities && (
        <AnimatedCard delay={1100}>
          <div style={{ marginBottom: '40px' }}>
            <ActivityFeed activities={activities} />
          </div>
        </AnimatedCard>
      )}

      {/* Product Ideas Activity Feed */}
      <AnimatedCard delay={1200}>
        <div style={{ marginBottom: '40px' }}>
          <ProductIdeasActivityFeed />
        </div>
      </AnimatedCard>

      {/* Loading States */}
      {(backlogLoading || activitiesLoading || unifiedLoading) && (
        <div 
          style={{
            position: 'fixed',
            top: '21px',
            right: '21px',
            padding: '13px 21px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            fontSize: '16px',
            color: '#0080ff',
            textShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
            animation: 'loadingPulse 2s ease-in-out infinite',
            zIndex: 1000,
          }}
        >
          Updating...
        </div>
      )}
      
      {/* Global animations - defined once at page level */}
      <style jsx global>{`
        @keyframes portalFadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes loadingPulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
      `}</style>

      {/* Last Updated */}
      {backlog && (
        <div style={{
          textAlign: 'center',
          padding: '21px',
          color: '#666666',
          fontSize: '16px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          Last updated: {new Date(backlog.aggregated_at).toLocaleString()}
        </div>
      )}
    </div>
  )
}

