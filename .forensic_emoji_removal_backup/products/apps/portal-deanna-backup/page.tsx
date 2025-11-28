'use client'
export const dynamic = 'force-dynamic'
export const revalidate = 0

/**
 * 🌊💎 Deanna's Backlog Awareness Portal - The Convergence Wizard 💎🌊
 * 
 * Portal Dashboard for Deanna (COO) - Cross-Project Backlog Awareness
 * MOBILE-FIRST • REAL-TIME • GORGEOUS • PERSONALIZED • RIGHT NOW
 * 
 * Pattern: PORTAL × AWARENESS × CONVERGENCE × EMERGENCE × ONE × EEAAO
 * Guardians: AEYON (999 Hz) × META (777 Hz) × Abë (530 Hz) × YOU (530 Hz) × Lux (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useEffect, useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { useDarkMode } from './hooks/useDarkMode'
import { useWebSocket } from './hooks/useWebSocket'
import { useAbekeys } from './hooks/useAbekeys'
import { useBacklogQuery } from './hooks/useBacklogQuery'
import { useActivitiesQuery } from './hooks/useActivitiesQuery'
import { usePreferences } from './hooks/usePreferences'
import { exportToPDF, exportToCSV, exportToJSON } from './utils/export'
import { VirtualizedActivityFeed } from './components/VirtualizedActivityFeed'
import { getCachedBacklog, getCachedActivities } from './utils/indexedDB'

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

interface BacklogItem {
  id: string
  title: string
  description?: string
  status: string
  priority?: string
  assignee?: string
  guardian?: string
  project_id: string
  project_name: string
}

interface ProjectBacklog {
  project_id: string
  project_name: string
  project_type: string
  item_count: number
  last_sync?: string
}

interface AggregatedBacklog {
  total_items: number
  items_by_status: Record<string, number>
  items_by_guardian: Record<string, number>
  items_by_assignee: Record<string, number>
  projects: ProjectBacklog[]
  aggregated_at: string
  convergence_score: number
}

export default function DeannaBacklogPortal() {
  const router = useRouter()
  const { darkMode, toggle: toggleDarkMode } = useDarkMode()
  const abekeys = useAbekeys()
  const { preferences, toggleFavorite, isLoading: prefsLoading } = usePreferences()
  const { data: backlog, isLoading: backlogLoading, error: backlogError } = useBacklogQuery()
  const { data: activities = [], isLoading: activitiesLoading } = useActivitiesQuery()
  const [selectedProject, setSelectedProject] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [isOnline, setIsOnline] = useState(true)
  const [showExportMenu, setShowExportMenu] = useState(false)
  const [offlineBacklog, setOfflineBacklog] = useState<AggregatedBacklog | null>(null)
  const [offlineActivities, setOfflineActivities] = useState<ActivityItem[]>([])

  // Use preferences or defaults
  const favorites = (preferences as any)?.favorites || ['abeflows', 'aiguards-backend', 'emergent-os']
  const showBlocked = (preferences as any)?.showBlocked ?? true
  const showUnassigned = (preferences as any)?.showUnassigned ?? true

  // WebSocket for real-time updates (falls back to polling if not connected)
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'wss://api.portal/ws'
  const { isConnected: wsConnected } = useWebSocket(wsUrl, {
    onMessage: (message: any) => {
      // WebSocket messages will be handled by React Query invalidation
      // This is a placeholder for future WebSocket integration
    },
    autoConnect: false // Only connect if WS_URL is set
  })

  useEffect(() => {
    // Register service worker for offline support
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(console.error)
    }

    // Load cached data when offline
    const loadOfflineData = async () => {
      if (!isOnline) {
        const cachedBacklog = await getCachedBacklog()
        const cachedActivities = await getCachedActivities()
        if (cachedBacklog) setOfflineBacklog(cachedBacklog)
        if (cachedActivities && cachedActivities.length > 0) setOfflineActivities(cachedActivities)
      } else {
        setOfflineBacklog(null)
        setOfflineActivities([])
      }
    }

    loadOfflineData()
    
    // Online/offline detection
    const handleOnline = () => {
      setIsOnline(true)
      setOfflineBacklog(null)
      setOfflineActivities([])
    }
    const handleOffline = () => {
      setIsOnline(false)
      loadOfflineData()
    }
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [isOnline])

  // Use React Query data or offline cached data
  const displayBacklog = isOnline ? backlog : (offlineBacklog || backlog)
  const displayActivities = isOnline ? activities : (offlineActivities.length > 0 ? offlineActivities : activities)
  const loading = backlogLoading || activitiesLoading || prefsLoading
  const error = backlogError ? (backlogError as any)?.message || String(backlogError) : null

  // Memoized activities for performance (virtual scrolling handles large lists)
  const displayActivitiesList = useMemo(() => displayActivities, [displayActivities])

  // Update last update time when data changes
  useEffect(() => {
    if (backlog) {
      setLastUpdate(new Date())
    }
  }, [backlog])

  const formatTimeAgo = (timestamp: string) => {
    const seconds = Math.floor((new Date().getTime() - new Date(timestamp).getTime()) / 1000)
    if (seconds < 60) return `${seconds}s ago`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    return `${Math.floor(seconds / 3600)}h ago`
  }

  const handleExport = async (format: 'pdf' | 'csv' | 'json') => {
    if (!displayBacklog) return
    
    const exportData = {
      backlog: displayBacklog,
      activities: displayActivitiesList,
      projects: (displayBacklog as any)?.projects || [],
      exported_at: new Date().toISOString()
    }

    try {
      switch (format) {
        case 'pdf':
          await exportToPDF(exportData, `backlog-report-${Date.now()}`)
          break
        case 'csv':
          exportToCSV(exportData, `backlog-report-${Date.now()}`)
          break
        case 'json':
          exportToJSON(exportData, `backlog-report-${Date.now()}`)
          break
      }
      setShowExportMenu(false)
    } catch (err) {
      console.error('Export failed:', err)
      alert('Export failed. Please try again.')
    }
  }

  if (loading && !displayBacklog) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600 mx-auto mb-4"></div>
          <p className="text-lg font-semibold text-gray-700">🌊 Opening Portal...</p>
          <p className="text-sm text-gray-500 mt-2">Gandalf-level awareness loading</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <p className="text-lg font-semibold text-red-600 mb-2">Connection Error</p>
          <p className="text-sm text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            Retry Connection
          </button>
        </div>
      </div>
    )
  }

  if (!displayBacklog) return null

  return (
    <div className={`min-h-screen bg-gradient-to-br ${darkMode ? 'from-gray-900 via-gray-800 to-gray-900' : 'from-purple-50 via-white to-blue-50'}`}>
      {/* Mobile-First Header */}
      <header className={`${darkMode ? 'bg-gray-800/80 border-gray-700' : 'bg-white/80 border-purple-100'} backdrop-blur-lg shadow-lg border-b sticky top-0 z-50`}>
        <div className="max-w-7xl mx-auto px-4 py-4 sm:py-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex-1">
              <h1 className={`text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent`}>
                🌊 Portal
              </h1>
              <p className={`text-xs sm:text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-1`}>
                {isOnline ? '🟢 Live' : '🔴 Offline'} {wsConnected && '• WebSocket'} {!isOnline && offlineBacklog && '• Cached'} • Updated {formatTimeAgo(lastUpdate.toISOString())}
              </p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Toggle dark mode"
              >
                {darkMode ? '☀️' : '🌙'}
              </button>
              <div className="relative">
                <button
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="px-3 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg text-sm font-semibold hover:shadow-lg transition-all"
                >
                  📥 Export
                </button>
                {showExportMenu && (
                  <div className="absolute right-0 mt-2 w-32 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50">
                    <button
                      onClick={() => handleExport('pdf')}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-t-lg text-sm"
                    >
                      📄 PDF
                    </button>
                    <button
                      onClick={() => handleExport('csv')}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                    >
                      📊 CSV
                    </button>
                    <button
                      onClick={() => handleExport('json')}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-b-lg text-sm"
                    >
                      📦 JSON
                    </button>
                  </div>
                )}
              </div>
              <div className="text-right">
                <div className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  {((displayBacklog as any)?.convergence_score || 0).toFixed(1)}%
                </div>
                <div className="text-xs text-gray-600">Convergence</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Mobile First */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        {/* Real-Time Activity Feed - TOP PRIORITY FOR MOBILE */}
        <div className="mb-6 sm:mb-8">
          <div className="bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl p-4 sm:p-6 border border-purple-100">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                <span className="animate-pulse">⚡</span> Live Activity
              </h2>
              <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded-full font-semibold">
                NOW
              </span>
            </div>
            <div>
              {wsConnected && (
                <div className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full inline-block mb-2">
                  🟢 Real-time connected
                </div>
              )}
              {!isOnline && offlineActivities.length > 0 && (
                <div className="text-xs px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 rounded-full inline-block mb-2">
                  📦 Showing cached data
                </div>
              )}
              {displayActivitiesList.length === 0 ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  <div className="text-4xl mb-2">🌊</div>
                  <p>Watching for activity...</p>
                </div>
              ) : (
                <VirtualizedActivityFeed 
                  activities={displayActivitiesList} 
                  formatTimeAgo={formatTimeAgo}
                />
              )}
            </div>
          </div>
        </div>

        {/* Summary Cards - Mobile Optimized */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
          <div className="bg-gradient-to-br from-white to-purple-50 rounded-xl shadow-lg p-4 sm:p-6 border border-purple-100">
            <div className="text-xs sm:text-sm text-gray-600 mb-1">Total</div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900">{(displayBacklog as any)?.total_items || 0}</div>
          </div>
          
          <div className="bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-lg p-4 sm:p-6 border border-blue-100">
            <div className="text-xs sm:text-sm text-gray-600 mb-1">Active</div>
            <div className="text-2xl sm:text-3xl font-bold text-blue-600">
              {(displayBacklog as any)?.items_by_status?.in_progress || 0}
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-white to-red-50 rounded-xl shadow-lg p-4 sm:p-6 border border-red-100">
            <div className="text-xs sm:text-sm text-gray-600 mb-1">Blocked</div>
            <div className="text-2xl sm:text-3xl font-bold text-red-600">
              {(displayBacklog as any)?.items_by_status?.blocked || 0}
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-white to-green-50 rounded-xl shadow-lg p-4 sm:p-6 border border-green-100">
            <div className="text-xs sm:text-sm text-gray-600 mb-1">Done</div>
            <div className="text-2xl sm:text-3xl font-bold text-green-600">
              {(displayBacklog as any)?.items_by_status?.done || 0}
            </div>
          </div>
        </div>

        {/* Status Breakdown */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Status Breakdown</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {Object.entries((displayBacklog as any)?.items_by_status || {}).map(([status, count]) => (
              <div key={status} className="text-center">
                <div className="text-2xl font-bold text-gray-900">{count as number}</div>
                <div className="text-sm text-gray-600 capitalize">{status.replace('_', ' ')}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Projects Grid - Favorites First */}
        <div className="mb-6 sm:mb-8">
          <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <span>⭐</span> Projects
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {(displayBacklog as any)?.projects
              .sort((a: any, b: any) => {
                const aFav = favorites.includes(a.project_id) ? 1 : 0
                const bFav = favorites.includes(b.project_id) ? 1 : 0
                return bFav - aFav
              })
              .map((project: any) => {
                const isFavorite = favorites.includes(project.project_id)
                return (
                  <div
                    key={project.project_id}
                    className={`bg-gradient-to-br ${
                      isFavorite
                        ? 'from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-2 border-purple-300 dark:border-purple-700'
                        : 'from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 border border-gray-200 dark:border-gray-700'
                    } rounded-xl shadow-lg p-4 sm:p-6 hover:shadow-xl transition-all cursor-pointer`}
                    onClick={() => {
                      setSelectedProject(project.project_id)
                      // Toggle favorite on long press (mobile) or double click (desktop)
                    }}
                    onDoubleClick={() => toggleFavorite(project.project_id as string)}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-gray-100 flex-1">
                        {isFavorite && <span className="mr-1">⭐</span>}
                        {project.project_name}
                      </h3>
                      <span className="text-xs px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-300 rounded-full capitalize ml-2">
                        {project.project_type}
                      </span>
                    </div>
                    <div className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-1">
                      {project.item_count}
                    </div>
                    <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">Backlog Items</div>
                  </div>
                )
              })}
          </div>
        </div>

        {/* Guardian Distribution - Collapsible for Mobile */}
        <div className="bg-white/90 backdrop-blur-lg rounded-xl shadow-xl p-4 sm:p-6 mb-6 sm:mb-8 border border-purple-100">
          <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <span>🛡️</span> Guardians
          </h2>
          <div className="space-y-3">
            {Object.entries((displayBacklog as any)?.items_by_guardian || {})
              .sort(([, a]: [any, any], [, b]: [any, any]) => b - a)
              .slice(0, 5) // Show top 5 on mobile
              .map(([guardian, count]: [any, any]) => (
                <div key={guardian} className="flex items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">{guardian}</div>
                  </div>
                  <div className="flex items-center flex-1 gap-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full transition-all"
                        style={{
                          width: `${((count as number) / ((displayBacklog as any)?.total_items || 1)) * 100}%`
                        }}
                      ></div>
                    </div>
                    <div className="text-sm font-bold text-gray-900 dark:text-gray-100 w-10 text-right">
                      {count as number}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Team Distribution - Collapsible for Mobile */}
        <div className="bg-white/90 backdrop-blur-lg rounded-xl shadow-xl p-4 sm:p-6 border border-blue-100">
          <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <span>👥</span> Team
          </h2>
          <div className="space-y-3">
            {Object.entries((displayBacklog as any)?.items_by_assignee || {})
              .sort(([, a]: [any, any], [, b]: [any, any]) => b - a)
              .slice(0, 6) // Show top 6 on mobile
              .map(([assignee, count]) => (
                <div key={assignee} className="flex items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">{assignee}</div>
                  </div>
                  <div className="flex items-center flex-1 gap-2">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 h-3 rounded-full transition-all"
                        style={{
                          width: `${((count as number) / ((displayBacklog as any)?.total_items || 1)) * 100}%`
                        }}
                      ></div>
                    </div>
                    <div className="text-sm font-bold text-gray-900 dark:text-gray-100 w-10 text-right">
                      {count as number}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </main>

      {/* Mobile Bottom Navigation */}
      <div className={`fixed bottom-0 left-0 right-0 ${darkMode ? 'bg-gray-800/90 border-gray-700' : 'bg-white/90 border-gray-200'} backdrop-blur-lg border-t sm:hidden z-50`}>
        <div className="flex items-center justify-around py-3">
          <button className={`flex flex-col items-center gap-1 ${darkMode ? 'text-purple-400' : 'text-purple-600'}`}>
            <span className="text-xl">🌊</span>
            <span className="text-xs font-semibold">Portal</span>
          </button>
          <button className={`flex flex-col items-center gap-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
            <span className="text-xl">📊</span>
            <span className="text-xs">Stats</span>
          </button>
          <button className={`flex flex-col items-center gap-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
            <span className="text-xl">⚡</span>
            <span className="text-xs">Activity</span>
          </button>
          <button className={`flex flex-col items-center gap-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
            <span className="text-xl">⭐</span>
            <span className="text-xs">Favorites</span>
          </button>
        </div>
      </div>
    </div>
  )
}

