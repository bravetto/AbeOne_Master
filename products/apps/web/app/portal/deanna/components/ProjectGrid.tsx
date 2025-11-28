'use client'

/**
 * Project Grid Component
 * 
 * Pattern: PROJECTS × GRID × VISUALIZATION × ONE
 * Guardian: AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

interface Project {
  project_id: string
  project_name: string
  project_type: string
  item_count: number
  last_sync?: string
}

interface Filters {
  showBlocked: boolean
  showUnassigned: boolean
  guardian: string | null
  status: string | null
}

interface ProjectGridProps {
  projects: Project[]
  filters: Filters
}

export function ProjectGrid({ projects, filters }: ProjectGridProps) {
  const typeColors: Record<string, string> = {
    orbital: '#0080ff',
    satellite: '#00ff88',
    product: '#FFD700',
  }

  return (
    <div style={{
      padding: '24px',
      backgroundColor: '#0a0a0a',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '8px',
    }}>
      <h2 style={{
        fontSize: '24px',
        fontWeight: '600',
        color: '#ffffff',
        marginBottom: '24px',
        letterSpacing: '-0.01em',
      }}>
        Projects
      </h2>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: '16px',
      }}>
        {projects.map((project) => {
          const typeColor = typeColors[project.project_type] || '#a0a0a0'
          
          return (
            <div
              key={project.project_id}
              style={{
                padding: '16px',
                backgroundColor: '#141414',
                border: `1px solid ${typeColor}40`,
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = typeColor
                e.currentTarget.style.backgroundColor = '#0a0a0a'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = `${typeColor}40`
                e.currentTarget.style.backgroundColor = '#141414'
              }}
            >
              <p style={{
                fontSize: '18px',
                fontWeight: '500',
                color: '#ffffff',
                marginBottom: '8px',
                letterSpacing: '-0.01em',
              }}>
                {project.project_name}
              </p>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '13px',
              }}>
                <span style={{
                  fontSize: '16px',
                  color: typeColor,
                  textShadow: `0 0 10px ${typeColor === '#0080ff' ? 'rgba(0, 128, 255, 0.3)' : typeColor === '#00ff88' ? 'rgba(0, 255, 136, 0.3)' : 'rgba(255, 215, 0, 0.3)'}`,
                }}>
                  {project.item_count} items
                </span>
                <span style={{
                  fontSize: '13px',
                  color: '#666666',
                  textTransform: 'uppercase',
                }}>
                  {project.project_type}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

