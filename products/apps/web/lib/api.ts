/**
 * API Client
 * 
 * Client for communicating with AbëONE backend API.
 */

// SAFETY: No fallback to localhost in production - must be explicitly configured
const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

interface OutcomeRequest {
  goal: string
  success_criteria: string[]
  end_state: string
  constraints: string[]
  validation: string
}

interface OutcomeResponse {
  status: string
  execution_results: any
  validation_report: any
  metadata: any
}

/**
 * Get kernel status
 */
export async function getKernelStatus() {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  try {
    const response = await fetch(`${API_URL}/api/kernel/status`, {
      signal: AbortSignal.timeout(5000) // 5 second timeout
    })
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`)
    }
    return response.json()
  } catch (error: any) {
    if (error.name === 'AbortError' || error.name === 'TypeError') {
      throw new Error('Backend server is not running or not configured.')
    }
    throw error
  }
}

/**
 * Get all modules
 */
export async function getModules() {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  const response = await fetch(`${API_URL}/api/kernel/modules`)
  if (!response.ok) {
    throw new Error('Failed to fetch modules')
  }
  return response.json()
}

/**
 * Get module information
 */
export async function getModuleInfo(moduleId: string) {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  const response = await fetch(`${API_URL}/api/kernel/modules/${moduleId}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch module ${moduleId}`)
  }
  return response.json()
}

/**
 * Execute outcome through Triadic Execution Harness
 */
export async function executeOutcome(outcome: OutcomeRequest): Promise<OutcomeResponse> {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  console.log('API call to:', `${API_URL}/api/agents/execute-outcome`)
  console.log('Request body:', outcome)
  
  try {
    const response = await fetch(`${API_URL}/api/agents/execute-outcome`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(outcome),
      signal: AbortSignal.timeout(30000) // 30 second timeout for execution
    })

    console.log('Response status:', response.status)
    
    if (!response.ok) {
      let errorData
      try {
        errorData = await response.json()
      } catch {
        errorData = { detail: await response.text() || 'Unknown error' }
      }
      console.error('API error:', errorData)
      throw new Error(errorData.detail || `HTTP ${response.status}: Failed to execute outcome`)
    }

    const data = await response.json()
    console.log('API response:', data)
    return data
  } catch (error: any) {
    console.error('Fetch error:', error)
    if (error.name === 'AbortError' || (error.name === 'TypeError' && error.message.includes('fetch'))) {
      throw new Error('Backend server is not running or not configured.')
    }
    if (error.message) {
      throw error
    }
    throw new Error(`Network error: ${error.toString()}`)
  }
}

/**
 * Get harness status
 */
export async function getHarnessStatus() {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  const response = await fetch(`${API_URL}/api/agents/harness-status`)
  if (!response.ok) {
    throw new Error('Failed to fetch harness status')
  }
  return response.json()
}

/**
 * Get system state metrics
 */
export async function getMetrics() {
  // SAFETY: Check API URL is configured
  if (!API_URL) {
    throw new Error('Backend API URL not configured. Set NEXT_PUBLIC_API_URL environment variable.')
  }
  
  const response = await fetch(`${API_URL}/api/state/metrics`)
  if (!response.ok) {
    throw new Error('Failed to fetch metrics')
  }
  return response.json()
}

/**
 * Get collaboration metrics
 * 
 * @deprecated Use Next.js API route `/api/collaboration` directly from components
 * This function is kept for backward compatibility but is no longer used.
 * The dashboard now calls `/api/collaboration` directly which handles backend/fallback logic.
 * 
 * SIMPLIFY: Removed duplicate logic - API route handles all backend/fallback logic
 */
export async function getCollaborationMetrics() {
  // SIMPLIFY: Just call the Next.js API route (which handles backend/fallback)
  const response = await fetch('/api/collaboration', {
    cache: 'no-store',
    headers: {
      'Cache-Control': 'no-cache',
    },
  })
  
  if (!response.ok) {
    throw new Error('Failed to fetch collaboration metrics')
  }
  
  return response.json()
}

