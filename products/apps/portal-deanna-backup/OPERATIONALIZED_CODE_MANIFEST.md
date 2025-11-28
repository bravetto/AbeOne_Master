# OPERATIONALIZED CODE MANIFEST

**Pattern**: OPERATIONALIZE × CONVERGE × MANIFEST × ONE  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

---

## FILE: hooks/useBacklogQuery.ts

```typescript
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
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const response = await fetch(`${apiUrl}/api/portal/backlog/aggregated`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch backlog: ${response.statusText}`)
  }
  
  const data = await response.json()
  await cacheBacklog(data)
  return data
}

export function useBacklogQuery() {
  return useQuery<AggregatedBacklog, Error>({
    queryKey: ['backlog', 'aggregated'],
    queryFn: fetchAggregatedBacklog,
    staleTime: 10000,
    refetchInterval: 30000,
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  })
}
```

---

## FILE: hooks/useActivitiesQuery.ts

```typescript
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
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const response = await fetch(`${apiUrl}/api/portal/activities`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch activities: ${response.statusText}`)
  }
  
  const data = await response.json()
  await cacheActivities(data.activities || data)
  return Array.isArray(data) ? data : (data.activities || [])
}

export function useActivitiesQuery() {
  return useQuery<ActivityItem[], Error>({
    queryKey: ['activities'],
    queryFn: fetchActivities,
    staleTime: 5000,
    refetchInterval: 5000,
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  })
}
```

---

## FILE: hooks/usePreferences.ts

```typescript
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
```

---

## FILE: hooks/useDarkMode.ts

```typescript
/**
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
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      setDarkMode(saved === 'true')
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      setDarkMode(prefersDark)
    }
  }, [])

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('darkMode', darkMode.toString())
  }, [darkMode])

  const toggle = () => setDarkMode(prev => !prev)

  return {
    darkMode,
    toggle,
  }
}
```

---

## FILE: hooks/useWebSocket.ts

```typescript
/**
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
        while (messageQueueRef.current.length > 0) {
          const message = messageQueueRef.current.shift()
          if (message) ws.send(JSON.stringify(message))
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
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          const delay = Math.min(
            reconnectInterval * Math.pow(2, reconnectAttemptsRef.current),
            30000
          )
          reconnectAttemptsRef.current++
          reconnectTimeoutRef.current = setTimeout(() => connect(), delay)
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
    return () => disconnect()
  }, [url, autoConnect, connect, disconnect])

  return {
    isConnected,
    send,
    connect,
    disconnect,
  }
}
```

---

## FILE: hooks/useAbekeys.ts

```typescript
/**
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
  }, [])

  const updateCredentials = (newCredentials: AbekeysCredentials) => {
    setCredentials(newCredentials)
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
```

---

## FILE: utils/indexedDB.ts

```typescript
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

if (typeof window !== 'undefined') {
  dbInstance.init().catch(console.error)
}

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
        resolve(request.result?.data || null)
      }
      request.onerror = () => reject(request.error)
    })
  } catch (error) {
    console.error('Failed to get cached backlog:', error)
    return null
  }
}

export async function cacheActivities(activities: any[]): Promise<void> {
  try {
    await dbInstance.init()
    const store = dbInstance.getStore(STORES.ACTIVITIES, 'readwrite')
    if (!store) throw new Error('Failed to access activities store')
    const clearRequest = store.clear()
    await new Promise<void>((resolve, reject) => {
      clearRequest.onsuccess = () => resolve()
      clearRequest.onerror = () => reject(clearRequest.error)
    })
    const activitiesToStore = activities.slice(0, 100)
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
```

---

## FILE: utils/export.ts

```typescript
/**
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

export async function exportToPDF(data: ExportData, filename: string = 'export'): Promise<void> {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text('Portal Export Report', 20, 20)
  doc.setFontSize(10)
  doc.text(`Exported: ${data.exported_at || new Date().toISOString()}`, 20, 30)
  
  let yPos = 40
  
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
  
  doc.save(`${filename}.pdf`)
}

export function exportToCSV(data: ExportData, filename: string = 'export'): void {
  const rows: string[] = []
  rows.push('Type,Title,User,Project,Timestamp')
  
  if (data.activities) {
    data.activities.forEach((activity: any) => {
      rows.push(
        `"${activity.type || ''}","${activity.title || ''}","${activity.user || ''}","${activity.project || ''}","${activity.timestamp || ''}"`
      )
    })
  }
  
  const csvContent = rows.join('\n')
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

export function exportToJSON(data: ExportData, filename: string = 'export'): void {
  const jsonContent = JSON.stringify(data, null, 2)
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
```

---

**Pattern**: OPERATIONALIZE × CONVERGE × MANIFEST × ONE  
**Status**:  **ALL FILES OPERATIONALIZED**  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

