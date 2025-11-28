'use client'

/**
 * Operations Unified Dashboard
 * 
 * Pattern: OPERATIONS × UNIFIED × R&D × TECH × MARKETING × FINANCE × ONE
 * Guardian: AEYON (999 Hz) × META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { AnimatedCard } from './AnimatedCard'
import { PulseGlow } from './PulseGlow'
import { DataValidation } from './DataValidation'

interface UnifiedData {
  operations: {
    backlog: { total_items: number; convergence_score: number }
    blocked_items: number
  }
  rd: { active_research: number; patents: number }
  tech: { infrastructure_health: number; api_uptime: number }
  marketing: { campaigns_active: number; revenue_attributed: number }
  finance: { revenue: number; profit_margin: number; runway_months: number }
  data_quality: Record<string, 'validated' | 'pending' | 'error'>
}

interface OperationsUnifiedProps {
  data: UnifiedData
}

export function OperationsUnified({ data }: OperationsUnifiedProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '16px',
      marginBottom: '40px',
    }}>
      {/* Operations */}
      <AnimatedCard delay={0}>
        <DataValidation isValid={data.data_quality.operations === 'validated'}>
          <div style={{
            padding: '24px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            transition: 'all 0.3s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#0080ff'
            e.currentTarget.style.backgroundColor = '#141414'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
            e.currentTarget.style.backgroundColor = '#0a0a0a'
          }}
          >
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
              Operations
            </h3>
            <PulseGlow color="#0080ff" intensity="medium">
              <div style={{ fontSize: '40px', fontWeight: '600', color: '#0080ff', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
                {data.operations.backlog.total_items}
              </div>
            </PulseGlow>
            <p style={{ fontSize: '14px', color: '#a0a0a0', marginBottom: '6px', fontWeight: '400' }}>
              Total Items
            </p>
            <p style={{ fontSize: '14px', color: '#00ff88', fontWeight: '400' }}>
              {data.operations.backlog.convergence_score}% Converged
            </p>
          </div>
        </DataValidation>
      </AnimatedCard>

      {/* R&D */}
      <AnimatedCard delay={100}>
        <DataValidation isValid={data.data_quality.rd === 'validated'}>
          <div style={{
            padding: '24px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            transition: 'all 0.3s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#00ff88'
            e.currentTarget.style.backgroundColor = '#141414'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
            e.currentTarget.style.backgroundColor = '#0a0a0a'
          }}
          >
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
              R&D
            </h3>
            <PulseGlow color="#00ff88" intensity="medium">
              <div style={{ fontSize: '40px', fontWeight: '600', color: '#00ff88', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
                {data.rd.active_research}
              </div>
            </PulseGlow>
            <p style={{ fontSize: '14px', color: '#a0a0a0', marginBottom: '6px', fontWeight: '400' }}>
              Active Research
            </p>
            <p style={{ fontSize: '14px', color: '#00ff88', fontWeight: '400' }}>
              {data.rd.patents} Patents Filed
            </p>
          </div>
        </DataValidation>
      </AnimatedCard>

      {/* Tech */}
      <AnimatedCard delay={200}>
        <DataValidation isValid={data.data_quality.tech === 'validated'}>
          <div style={{
            padding: '24px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            transition: 'all 0.3s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#0080ff'
            e.currentTarget.style.backgroundColor = '#141414'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
            e.currentTarget.style.backgroundColor = '#0a0a0a'
          }}
          >
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
              Tech
            </h3>
            <PulseGlow color="#0080ff" intensity="medium">
              <div style={{ fontSize: '40px', fontWeight: '600', color: '#0080ff', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
                {data.tech.infrastructure_health.toFixed(1)}%
              </div>
            </PulseGlow>
            <p style={{ fontSize: '14px', color: '#a0a0a0', marginBottom: '6px', fontWeight: '400' }}>
              Infrastructure Health
            </p>
            <p style={{ fontSize: '14px', color: '#00ff88', fontWeight: '400' }}>
              {data.tech.api_uptime}% Uptime
            </p>
          </div>
        </DataValidation>
      </AnimatedCard>

      {/* Marketing */}
      <AnimatedCard delay={300}>
        <DataValidation isValid={data.data_quality.marketing === 'validated'}>
          <div style={{
            padding: '24px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            transition: 'all 0.3s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#FFD700'
            e.currentTarget.style.backgroundColor = '#141414'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
            e.currentTarget.style.backgroundColor = '#0a0a0a'
          }}
          >
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
              Marketing
            </h3>
            <PulseGlow color="#FFD700" intensity="medium">
              <div style={{ fontSize: '40px', fontWeight: '600', color: '#FFD700', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
                {data.marketing.campaigns_active}
              </div>
            </PulseGlow>
            <p style={{ fontSize: '14px', color: '#a0a0a0', marginBottom: '6px', fontWeight: '400' }}>
              Active Campaigns
            </p>
            <p style={{ fontSize: '14px', color: '#00ff88', fontWeight: '400' }}>
              {formatCurrency(data.marketing.revenue_attributed)} Attributed
            </p>
          </div>
        </DataValidation>
      </AnimatedCard>

      {/* Finance */}
      <AnimatedCard delay={400}>
        <DataValidation isValid={data.data_quality.finance === 'validated'}>
          <div style={{
            padding: '24px',
            backgroundColor: '#0a0a0a',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            transition: 'all 0.3s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#00ff88'
            e.currentTarget.style.backgroundColor = '#141414'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'
            e.currentTarget.style.backgroundColor = '#0a0a0a'
          }}
          >
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
              Finance
            </h3>
            <PulseGlow color="#00ff88" intensity="medium">
              <div style={{ fontSize: '32px', fontWeight: '600', color: '#00ff88', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
                {formatCurrency(data.finance.revenue)}
              </div>
            </PulseGlow>
            <p style={{ fontSize: '14px', color: '#a0a0a0', marginBottom: '6px', fontWeight: '400' }}>
              Revenue
            </p>
            <p style={{ fontSize: '14px', color: '#00ff88', fontWeight: '400' }}>
              {data.finance.profit_margin}% Margin • {data.finance.runway_months}mo Runway
            </p>
          </div>
        </DataValidation>
      </AnimatedCard>
    </div>
  )
}

