#!/bin/bash
#  Phase 1 File Creation Script 
# 
# Pattern: CREATE × FILES × PHASE1 × ONE
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create directories
mkdir -p hooks utils

# Create useBacklogQuery.ts
cat > hooks/useBacklogQuery.ts << 'EOF'
/**
 * React Query Hook for Backlog Data
 * 
 * Pattern: QUERY × BACKLOG × CACHING × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useQuery } from '@tanstack/react-query'
import { cacheBacklog } from '../utils/indexedDB'

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

const fetchAggregatedBacklog = async (): Promise<AggregatedBacklog> => {
  // TODO: Replace with actual API endpoint
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const response = await fetch(`${apiUrl}/api/portal/backlog/aggregated`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch backlog: ${response.statusText}`)
  }
  
  const data = await response.json()
  
  // Cache for offline access
  await cacheBacklog(data)
  
  return data
}

export function useBacklogQuery() {
  return useQuery<AggregatedBacklog, Error>({
    queryKey: ['backlog', 'aggregated'],
    queryFn: fetchAggregatedBacklog,
    staleTime: 10000, // 10 seconds
    refetchInterval: 30000, // Poll every 30 seconds
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  })
}
EOF

# Create useActivitiesQuery.ts
cat > hooks/useActivitiesQuery.ts << 'EOF'
/**
 * React Query Hook for Activities Feed
 * 
 * Pattern: QUERY × ACTIVITIES × REAL-TIME × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useQuery } from '@tanstack/react-query'
import { cacheActivities } from '../utils/indexedDB'

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

const fetchActivities = async (): Promise<ActivityItem[]> => {
  // TODO: Replace with actual API endpoint
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const response = await fetch(`${apiUrl}/api/portal/activities`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch activities: ${response.statusText}`)
  }
  
  const data = await response.json()
  
  // Cache for offline access
  await cacheActivities(data.activities || data)
  
  return Array.isArray(data) ? data : (data.activities || [])
}

export function useActivitiesQuery() {
  return useQuery<ActivityItem[], Error>({
    queryKey: ['activities'],
    queryFn: fetchActivities,
    staleTime: 5000, // 5 seconds - activities are more time-sensitive
    refetchInterval: 5000, // Poll every 5 seconds for real-time feel
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  })
}
EOF

# Create usePreferences.ts
cat > hooks/usePreferences.ts << 'EOF'
/**
 * Preferences Hook with IndexedDB Persistence
 * 
 * Pattern: PREFERENCES × PERSISTENCE × PERSONALIZATION × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useState, useEffect, useCallback } from 'react'
import { getPreferences, savePreferences } from '../utils/indexedDB'

interface UserPreferences {
  favorites: string[]
  showBlocked: boolean
  showUnassigned: boolean
  darkMode?: boolean
  notifications?: boolean
  defaultView?: 'list' | 'grid'
}

const DEFAULT_PREFERENCES: UserPreferences = {
  favorites: ['abeflows', 'aiguards-backend', 'emergent-os'],
  showBlocked: true,
  showUnassigned: true,
  darkMode: false,
  notifications: true,
  defaultView: 'list',
}

export function usePreferences() {
  const [preferences, setPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES)
  const [isLoading, setIsLoading] = useState(true)

  // Load preferences from IndexedDB on mount
  useEffect(() => {
    const loadPreferences = async () => {
      try {
        const saved = await getPreferences()
        if (saved) {
          setPreferences({ ...DEFAULT_PREFERENCES, ...saved })
        }
      } catch (error) {
        console.error('Failed to load preferences:', error)
      } finally {
        setIsLoading(false)
      }
    }
    
    loadPreferences()
  }, [])

  // Save preferences to IndexedDB whenever they change
  useEffect(() => {
    if (!isLoading) {
      savePreferences(preferences).catch(console.error)
    }
  }, [preferences, isLoading])

  const toggleFavorite = useCallback((projectId: string) => {
    setPreferences(prev => {
      const favorites = prev.favorites.includes(projectId)
        ? prev.favorites.filter(id => id !== projectId)
        : [...prev.favorites, projectId]
      return { ...prev, favorites }
    })
  }, [])

  const updatePreference = useCallback(<K extends keyof UserPreferences>(
    key: K,
    value: UserPreferences[K]
  ) => {
    setPreferences(prev => ({ ...prev, [key]: value }))
  }, [])

  return {
    preferences,
    isLoading,
    toggleFavorite,
    updatePreference,
  }
}
EOF

# Create indexedDB.ts
cat > utils/indexedDB.ts << 'EOF'
/**
 * IndexedDB Utilities for Offline Caching
 * 
 * Pattern: STORAGE × OFFLINE × PERSISTENCE × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

const DB_NAME = 'PortalDB'
const DB_VERSION = 1

const STORES = {
  BACKLOG: 'backlog',
  ACTIVITIES: 'activities',
  PREFERENCES: 'preferences',
} as const

interface DB {
  db: IDBDatabase | null
  init: () => Promise<void>
  getStore: (storeName: string, mode?: IDBTransactionMode) => IDBObjectStore | null
}

let dbInstance: DB = {
  db: null,
  init: async () => {
    return new Promise((resolve, reject) => {
      if (!('indexedDB' in window)) {
        reject(new Error('IndexedDB not supported'))
        return
      }

      const request = indexedDB.open(DB_NAME, DB_VERSION)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        dbInstance.db = request.result
        resolve()
      }

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result

        // Create object stores if they don't exist
        if (!db.objectStoreNames.contains(STORES.BACKLOG)) {
          db.createObjectStore(STORES.BACKLOG, { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains(STORES.ACTIVITIES)) {
          const activitiesStore = db.createObjectStore(STORES.ACTIVITIES, { keyPath: 'id' })
          activitiesStore.createIndex('timestamp', 'timestamp', { unique: false })
        }
        if (!db.objectStoreNames.contains(STORES.PREFERENCES)) {
          db.createObjectStore(STORES.PREFERENCES, { keyPath: 'id' })
        }
      }
    })
  },
  getStore: (storeName: string, mode: IDBTransactionMode = 'readonly') => {
    if (!dbInstance.db) return null
    const transaction = dbInstance.db.transaction([storeName], mode)
    return transaction.objectStore(storeName)
  },
}

// Initialize DB on first import
if (typeof window !== 'undefined') {
  dbInstance.init().catch(console.error)
}

// Backlog caching
export async function cacheBacklog(backlog: any): Promise<void> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.BACKLOG, 'readwrite')
    if (!store) throw new Error('Failed to access backlog store')

    await new Promise<void>((resolve, reject) => {
      const request = store.put({ id: 'current', data: backlog, timestamp: Date.now() })
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to cache backlog:', error)
  }
}

export async function getCachedBacklog(): Promise<any | null> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.BACKLOG)
    if (!store) return null

    return new Promise((resolve, reject) => {
      const request = store.get('current')
      request.onsuccess = () => {
        const result = request.result
        resolve(result?.data || null)
      }
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to get cached backlog:', error)
    return null
  }
}

// Activities caching
export async function cacheActivities(activities: any[]): Promise<void> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.ACTIVITIES, 'readwrite')
    if (!store) throw new Error('Failed to access activities store')

    // Clear old activities (keep last 100)
    const clearRequest = store.clear()
    await new Promise<void>((resolve, reject) => {
      clearRequest.onsuccess = () => resolve()
      clearRequest.onerror = () => reject(clearRequest.error)
    })

    // Add new activities
    const activitiesToStore = activities.slice(0, 100) // Limit to 100 most recent
    for (const activity of activitiesToStore) {
      await new Promise<void>((resolve, reject) => {
        const request = store.add(activity)
        request.onsuccess = () => resolve()
        request.onerror = () => reject(request.error)
      })
    }
  } catch (error) {
    console.error('Failed to cache activities:', error)
  }
}

export async function getCachedActivities(): Promise<any[]> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.ACTIVITIES)
    if (!store) return []

    return new Promise((resolve, reject) => {
      const request = store.getAll()
      request.onsuccess = () => {
        const activities = request.result || []
        // Sort by timestamp descending
        activities.sort((a, b) => 
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        )
        resolve(activities)
      }
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to get cached activities:', error)
    return []
  }
}

// Preferences persistence
export async function savePreferences(preferences: any): Promise<void> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.PREFERENCES, 'readwrite')
    if (!store) throw new Error('Failed to access preferences store')

    await new Promise<void>((resolve, reject) => {
      const request = store.put({ id: 'user', ...preferences, timestamp: Date.now() })
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to save preferences:', error)
  }
}

export async function getPreferences(): Promise<any | null> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.PREFERENCES)
    if (!store) return null

    return new Promise((resolve, reject) => {
      const request = store.get('user')
      request.onsuccess = () => {
        const result = request.result
        if (result) {
          // Remove id and timestamp from preferences
          const { id, timestamp, ...preferences } = result
          resolve(preferences)
        } else {
          resolve(null)
        }
      }
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to get preferences:', error)
    return null
  }
}
EOF

echo " Phase 1 files created successfully!"
echo ""
echo "Created files:"
echo "  - hooks/useBacklogQuery.ts"
echo "  - hooks/useActivitiesQuery.ts"
echo "  - hooks/usePreferences.ts"
echo "  - utils/indexedDB.ts"
echo ""
echo " Phase 1 implementation complete! "
echo "Pattern: CREATE × FILES × PHASE1 × ONE"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"

