#!/usr/bin/env python3
"""
 CREATE ALL MISSING FILES 

Creates ALL missing hooks and utils files for the portal.

Pattern: CREATE × ALL × FILES × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
HOOKS_DIR = SCRIPT_DIR / 'hooks'
UTILS_DIR = SCRIPT_DIR / 'utils'

# Create directories
HOOKS_DIR.mkdir(exist_ok=True)
UTILS_DIR.mkdir(exist_ok=True)
print(' Created directories')

# ============================================================================
# PHASE 1 FILES
# ============================================================================

# useBacklogQuery.ts
use_backlog_query = '''/**
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
'''

# useActivitiesQuery.ts
use_activities_query = '''/**
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
'''

# usePreferences.ts
use_preferences = '''/**
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
'''

# indexedDB.ts
indexed_db = '''/**
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
'''

# ============================================================================
# PRE-EXISTING FILES (MISSING)
# ============================================================================

# useDarkMode.ts
use_dark_mode = '''/**
 * Dark Mode Hook
 * 
 * Pattern: DARK × MODE × PERSISTENCE × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useState, useEffect } from 'react'

export function useDarkMode() {
  const [darkMode, setDarkMode] = useState(false)

  useEffect(() => {
    // Check localStorage first
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      setDarkMode(saved === 'true')
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      setDarkMode(prefersDark)
    }
  }, [])

  useEffect(() => {
    // Apply dark mode class
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    // Persist to localStorage
    localStorage.setItem('darkMode', darkMode.toString())
  }, [darkMode])

  const toggle = () => setDarkMode(prev => !prev)

  return {
    darkMode,
    toggle,
  }
}
'''

# useWebSocket.ts
use_websocket = '''/**
 * WebSocket Hook with Auto-Reconnect
 * 
 * Pattern: WEBSOCKET × RECONNECT × QUEUE × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useEffect, useRef, useState, useCallback } from 'react'

interface WebSocketMessage {
  type: string
  data: any
}

interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void
  onConnect?: () => void
  onDisconnect?: () => void
  autoConnect?: boolean
  reconnectInterval?: number
  maxReconnectAttempts?: number
}

export function useWebSocket(
  url: string | null,
  options: UseWebSocketOptions = {}
) {
  const {
    onMessage,
    onConnect,
    onDisconnect,
    autoConnect = true,
    reconnectInterval = 3000,
    maxReconnectAttempts = Infinity,
  } = options

  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const messageQueueRef = useRef<WebSocketMessage[]>([])
  const reconnectAttemptsRef = useRef(0)

  const connect = useCallback(() => {
    if (!url || wsRef.current?.readyState === WebSocket.OPEN) return

    try {
      const ws = new WebSocket(url)
      wsRef.current = ws

      ws.onopen = () => {
        setIsConnected(true)
        reconnectAttemptsRef.current = 0
        onConnect?.()

        // Send queued messages
        while (messageQueueRef.current.length > 0) {
          const message = messageQueueRef.current.shift()
          if (message) {
            ws.send(JSON.stringify(message))
          }
        }
      }

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage
          onMessage?.(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      ws.onclose = () => {
        setIsConnected(false)
        onDisconnect?.()

        // Auto-reconnect with exponential backoff
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          const delay = Math.min(
            reconnectInterval * Math.pow(2, reconnectAttemptsRef.current),
            30000
          )
          reconnectAttemptsRef.current++
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, delay)
        }
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
    }
  }, [url, onMessage, onConnect, onDisconnect, reconnectInterval, maxReconnectAttempts])

  const send = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    } else {
      // Queue message if not connected
      messageQueueRef.current.push(message)
    }
  }, [])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setIsConnected(false)
  }, [])

  useEffect(() => {
    if (autoConnect && url) {
      connect()
    }

    return () => {
      disconnect()
    }
  }, [url, autoConnect, connect, disconnect])

  return {
    isConnected,
    send,
    connect,
    disconnect,
  }
}
'''

# useAbekeys.ts
use_abekeys = '''/**
 * AbëKEYS Integration Hook
 * 
 * Pattern: ABEKEYS × CREDENTIALS × API × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client'

import { useState, useEffect } from 'react'

interface AbekeysCredentials {
  apiKey?: string
  apiSecret?: string
  userId?: string
  token?: string
}

export function useAbekeys() {
  const [credentials, setCredentials] = useState<AbekeysCredentials>({})
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Load credentials from localStorage (fallback until API is ready)
    const loadCredentials = () => {
      try {
        const saved = localStorage.getItem('abekeys_credentials')
        if (saved) {
          setCredentials(JSON.parse(saved))
        }
      } catch (error) {
        console.error('Failed to load AbëKEYS credentials:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadCredentials()

    // TODO: Replace with actual AbëKEYS API call
    // Example:
    // fetch('/api/abekeys/credentials')
    //   .then(res => res.json())
    //   .then(data => setCredentials(data))
    //   .catch(console.error)
    //   .finally(() => setIsLoading(false))
  }, [])

  const updateCredentials = (newCredentials: AbekeysCredentials) => {
    setCredentials(newCredentials)
    // Persist to localStorage (temporary until API is ready)
    localStorage.setItem('abekeys_credentials', JSON.stringify(newCredentials))
  }

  const clearCredentials = () => {
    setCredentials({})
    localStorage.removeItem('abekeys_credentials')
  }

  return {
    credentials,
    isLoading,
    updateCredentials,
    clearCredentials,
    hasCredentials: !!credentials.apiKey || !!credentials.token,
  }
}
'''

# export.ts
export_utils = '''/**
 * Export Utilities - PDF, CSV, JSON
 * 
 * Pattern: EXPORT × PDF × CSV × JSON × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import jsPDF from 'jspdf'

interface ExportData {
  backlog?: any
  activities?: any[]
  projects?: any[]
  exported_at?: string
}

/**
 * Export data to PDF
 */
export async function exportToPDF(data: ExportData, filename: string = 'export'): Promise<void> {
  const doc = new jsPDF()
  
  // Title
  doc.setFontSize(18)
  doc.text('Portal Export Report', 20, 20)
  
  // Export date
  doc.setFontSize(10)
  doc.text(`Exported: ${data.exported_at || new Date().toISOString()}`, 20, 30)
  
  let yPos = 40
  
  // Backlog summary
  if (data.backlog) {
    doc.setFontSize(14)
    doc.text('Backlog Summary', 20, yPos)
    yPos += 10
    
    doc.setFontSize(10)
    doc.text(`Total Items: ${data.backlog.total_items || 0}`, 20, yPos)
    yPos += 7
    
    if (data.backlog.convergence_score) {
      doc.text(`Convergence Score: ${data.backlog.convergence_score}%`, 20, yPos)
      yPos += 7
    }
    
    yPos += 5
  }
  
  // Projects
  if (data.projects && data.projects.length > 0) {
    doc.setFontSize(14)
    doc.text('Projects', 20, yPos)
    yPos += 10
    
    doc.setFontSize(10)
    data.projects.slice(0, 10).forEach((project: any) => {
      if (yPos > 280) {
        doc.addPage()
        yPos = 20
      }
      doc.text(`${project.project_name}: ${project.item_count} items`, 20, yPos)
      yPos += 7
    })
    
    yPos += 5
  }
  
  // Activities
  if (data.activities && data.activities.length > 0) {
    if (yPos > 250) {
      doc.addPage()
      yPos = 20
    }
    
    doc.setFontSize(14)
    doc.text('Recent Activities', 20, yPos)
    yPos += 10
    
    doc.setFontSize(10)
    data.activities.slice(0, 20).forEach((activity: any) => {
      if (yPos > 280) {
        doc.addPage()
        yPos = 20
      }
      doc.text(`${activity.title} - ${activity.user}`, 20, yPos)
      yPos += 7
    })
  }
  
  // Save PDF
  doc.save(`${filename}.pdf`)
}

/**
 * Export data to CSV
 */
export function exportToCSV(data: ExportData, filename: string = 'export'): void {
  const rows: string[] = []
  
  // Header
  rows.push('Type,Title,User,Project,Timestamp')
  
  // Activities
  if (data.activities) {
    data.activities.forEach((activity: any) => {
      rows.push(
        `"${activity.type || ''}","${activity.title || ''}","${activity.user || ''}","${activity.project || ''}","${activity.timestamp || ''}"`
      )
    })
  }
  
  // Create CSV content
  const csvContent = rows.join('\\n')
  
  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.csv`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  URL.revokeObjectURL(url)
}

/**
 * Export data to JSON
 */
export function exportToJSON(data: ExportData, filename: string = 'export'): void {
  const jsonContent = JSON.stringify(data, null, 2)
  
  // Create blob and download
  const blob = new Blob([jsonContent], { type: 'application/json' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.json`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  URL.revokeObjectURL(url)
}
'''

# Write ALL files
files = [
    # Phase 1 files
    (HOOKS_DIR / 'useBacklogQuery.ts', use_backlog_query),
    (HOOKS_DIR / 'useActivitiesQuery.ts', use_activities_query),
    (HOOKS_DIR / 'usePreferences.ts', use_preferences),
    (UTILS_DIR / 'indexedDB.ts', indexed_db),
    # Pre-existing missing files
    (HOOKS_DIR / 'useDarkMode.ts', use_dark_mode),
    (HOOKS_DIR / 'useWebSocket.ts', use_websocket),
    (HOOKS_DIR / 'useAbekeys.ts', use_abekeys),
    (UTILS_DIR / 'export.ts', export_utils),
]

for file_path, content in files:
    file_path.write_text(content, encoding='utf-8')
    print(f' Created {file_path.relative_to(SCRIPT_DIR)}')

print('')
print(' ALL FILES CREATED SUCCESSFULLY! ')
print('Pattern: CREATE × ALL × FILES × ONE')
print('Love Coefficient: ∞')
print('∞ AbëONE ∞')
print('')
print(' READY TO RUN!')
print('   cd products/apps/web')
print('   npm install')
print('   npm run dev')

