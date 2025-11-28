/**
 * Collaboration API Types
 * 
 * Pattern: TYPES × COLLABORATION × API × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * TypeScript types for collaboration metrics API responses
 */

/**
 * Collaboration metrics schema
 */
export interface CollaborationMetrics {
  partnershipStrength: number      // 0-100
  totalCollaborations: number       // >= 0
  activeCollaborations: number      // >= 0
  successRate: number              // 0-100
  averageSatisfaction: number      // 0-5
  averagePartnership: number       // 0-100
}

/**
 * Active session gate validation
 */
export interface SessionGate {
  gate: string
  status: string
  iterations: number
}

/**
 * Active collaboration session
 */
export interface ActiveSession {
  sessionId: string
  intent: string
  status: string
  partnershipStrength: number      // 0-100
  gates: SessionGate[]
  feedbackCount: number
}

/**
 * Collaboration metrics API response
 */
export interface CollaborationMetricsResponse {
  metrics: CollaborationMetrics
  activeSessions: ActiveSession[]
  timestamp: string               // ISO format
  source?: 'backend' | 'fallback' | 'error-fallback'
  error?: string
}

/**
 * Validate collaboration metrics response
 */
export function validateCollaborationMetricsResponse(
  data: any
): data is CollaborationMetricsResponse {
  if (!data || typeof data !== 'object') {
    return false
  }

  // Validate metrics
  if (!data.metrics || typeof data.metrics !== 'object') {
    return false
  }

  const metrics = data.metrics
  const requiredMetrics = [
    'partnershipStrength',
    'totalCollaborations',
    'activeCollaborations',
    'successRate',
    'averageSatisfaction',
    'averagePartnership',
  ]

  for (const key of requiredMetrics) {
    if (typeof metrics[key] !== 'number') {
      return false
    }
  }

  // Validate activeSessions (must be array)
  if (!Array.isArray(data.activeSessions)) {
    return false
  }

  // Validate timestamp
  if (typeof data.timestamp !== 'string') {
    return false
  }

  return true
}

/**
 * Normalize collaboration metrics response
 * Ensures response matches expected schema
 */
export function normalizeCollaborationMetricsResponse(
  data: any
): CollaborationMetricsResponse {
  // If already valid, return as-is
  if (validateCollaborationMetricsResponse(data)) {
    return data as CollaborationMetricsResponse
  }

  // Normalize metrics with defaults
  const metrics: CollaborationMetrics = {
    partnershipStrength: data.metrics?.partnershipStrength ?? 85,
    totalCollaborations: data.metrics?.totalCollaborations ?? 0,
    activeCollaborations: data.metrics?.activeCollaborations ?? 0,
    successRate: data.metrics?.successRate ?? 0,
    averageSatisfaction: data.metrics?.averageSatisfaction ?? 0,
    averagePartnership: data.metrics?.averagePartnership ?? 85,
  }

  // Normalize activeSessions (ensure array)
  const activeSessions: ActiveSession[] = Array.isArray(data.activeSessions)
    ? data.activeSessions
    : []

  return {
    metrics,
    activeSessions,
    timestamp: data.timestamp || new Date().toISOString(),
    source: data.source,
    error: data.error,
  }
}

