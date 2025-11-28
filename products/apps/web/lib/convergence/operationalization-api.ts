/**
 * Convergence Operationalization API
 * 
 * Pattern: AEYON × ARLAX × OPERATIONALIZATION × SCALE × API × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (ARLAX) × ∞ (Scale)
 * 
 * RESTful API for operationalizing convergence systems.
 */

import { recursiveOperationalizer } from './recursive-operationalizer'
import {
  OperationalizationConfig,
  OperationalizationResult,
} from './arlax-operationalizer'
import { RecursiveOperationalizationPlan } from './recursive-operationalizer'

export interface OperationalizationRequest {
  target: 'self' | 'convergence' | 'all'
  config: OperationalizationConfig
  depth?: number
}

export interface OperationalizationResponse {
  success: boolean
  results: OperationalizationResult[]
  tree: {
    systems: string[]
    depth: number
    dependencies: Map<string, string[]>
  }
  timestamp: number
}

/**
 * Operationalization API
 * 
 * Provides RESTful interface for operationalization.
 */
export class OperationalizationAPI {
  /**
   * Operationalize convergence system
   */
  async operationalize(
    request: OperationalizationRequest
  ): Promise<OperationalizationResponse> {
    const plan: RecursiveOperationalizationPlan = {
      depth: request.depth || 0,
      target: request.target,
      config: request.config,
      dependencies: [],
    }

    const results = await recursiveOperationalizer.operationalizeRecursively(
      plan
    )

    const tree = recursiveOperationalizer.getOperationalizationTree()

    return {
      success: results.every((r) => r.success),
      results,
      tree,
      timestamp: Date.now(),
    }
  }

  /**
   * Operationalize self (meta-operationalization)
   */
  async operationalizeSelf(
    config: OperationalizationConfig
  ): Promise<OperationalizationResult> {
    return await recursiveOperationalizer.operationalizeSelf(config)
  }

  /**
   * Get operationalization status
   */
  getStatus(): {
    operationalized: boolean
    systems: string[]
    depth: number
  } {
    const tree = recursiveOperationalizer.getOperationalizationTree()
    return {
      operationalized: tree.systems.length > 0,
      systems: tree.systems,
      depth: tree.depth,
    }
  }
}

// Export singleton instance
export const operationalizationAPI = new OperationalizationAPI()

