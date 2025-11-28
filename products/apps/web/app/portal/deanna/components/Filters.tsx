'use client'

/**
 * Filters Component
 * 
 * Pattern: FILTERS × PORTAL × INTERACTION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface Filters {
  showBlocked: boolean
  showUnassigned: boolean
  guardian: string | null
  status: string | null
}

interface FiltersProps {
  filters: Filters
  onFiltersChange: (filters: Filters) => void
}

export function Filters({ filters, onFiltersChange }: FiltersProps) {
  const toggleFilter = (key: keyof Filters) => {
    if (key === 'showBlocked' || key === 'showUnassigned') {
      onFiltersChange({
        ...filters,
        [key]: !filters[key],
      })
    }
  }

  return (
    <div style={{
      display: 'flex',
      gap: '12px',
      marginBottom: '24px',
      flexWrap: 'wrap',
    }}>
      <button
        onClick={() => toggleFilter('showBlocked')}
        style={{
          padding: '10px 16px',
          backgroundColor: filters.showBlocked ? '#0080ff' : '#0a0a0a',
          color: '#ffffff',
          border: `1px solid ${filters.showBlocked ? '#0080ff' : 'rgba(255, 255, 255, 0.1)'}`,
          borderRadius: '8px',
          fontSize: '16px',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          textShadow: filters.showBlocked ? '0 0 10px rgba(0, 128, 255, 0.3)' : 'none',
        }}
      >
        Show Blocked
      </button>
      <button
        onClick={() => toggleFilter('showUnassigned')}
        style={{
          padding: '10px 16px',
          backgroundColor: filters.showUnassigned ? '#0080ff' : '#0a0a0a',
          color: '#ffffff',
          border: `1px solid ${filters.showUnassigned ? '#0080ff' : 'rgba(255, 255, 255, 0.1)'}`,
          borderRadius: '8px',
          fontSize: '16px',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          textShadow: filters.showUnassigned ? '0 0 10px rgba(0, 128, 255, 0.3)' : 'none',
        }}
      >
        Show Unassigned
      </button>
    </div>
  )
}

