/**
 * Convergence Dashboard
 * 
 * Pattern: VISUALIZATION × CONVERGENCE × DASHBOARD × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Real-time convergence visualization and tracking.
 */

import { convergenceExecutor, ConvergenceOpportunity, ConvergenceExecution } from './unified-executor'
import { patternDetector } from './pattern-detector'

export interface DashboardData {
  opportunities: ConvergenceOpportunity[]
  executions: ConvergenceExecution[]
  metrics: {
    totalOpportunities: number
    pendingOpportunities: number
    inProgressOpportunities: number
    completedOpportunities: number
    totalExecutions: number
    successfulExecutions: number
    failedExecutions: number
    patterns: string[]
  }
  recentActivity: {
    type: 'opportunity_registered' | 'execution_started' | 'execution_completed' | 'pattern_detected'
    timestamp: number
    data: any
  }[]
}

/**
 * Convergence Dashboard
 * 
 * Provides real-time convergence visibility.
 */
export class ConvergenceDashboard {
  private activityLog: DashboardData['recentActivity'] = []
  private maxActivityLogSize = 100

  /**
   * Get dashboard data
   */
  getDashboardData(): DashboardData {
    const opportunities = convergenceExecutor.getOpportunities()
    const executions = convergenceExecutor.getExecutions()
    const metrics = convergenceExecutor.getMetrics()

    return {
      opportunities,
      executions,
      metrics,
      recentActivity: this.activityLog.slice(-this.maxActivityLogSize),
    }
  }

  /**
   * Log activity
   */
  logActivity(
    type: DashboardData['recentActivity'][0]['type'],
    data: any
  ): void {
    this.activityLog.push({
      type,
      timestamp: Date.now(),
      data,
    })

    // Trim log if too large
    if (this.activityLog.length > this.maxActivityLogSize) {
      this.activityLog.shift()
    }
  }

  /**
   * Get opportunities by status
   */
  getOpportunitiesByStatus(status: ConvergenceOpportunity['status']): ConvergenceOpportunity[] {
    return convergenceExecutor.getOpportunities().filter(o => o.status === status)
  }

  /**
   * Get opportunities by impact
   */
  getOpportunitiesByImpact(impact: ConvergenceOpportunity['impact']): ConvergenceOpportunity[] {
    return convergenceExecutor.getOpportunities().filter(o => o.impact === impact)
  }

  /**
   * Get convergence trends
   */
  getTrends(): {
    opportunitiesTrend: 'increasing' | 'stable' | 'decreasing'
    executionSuccessRate: number
    averageExecutionTime: number
    topPatterns: { pattern: string; count: number }[]
  } {
    const opportunities = convergenceExecutor.getOpportunities()
    const executions = convergenceExecutor.getExecutions()

    // Calculate trends
    const recentOpportunities = opportunities.filter(
      o => Date.now() - o.timestamp < 7 * 24 * 60 * 60 * 1000 // Last 7 days
    )
    const oldOpportunities = opportunities.filter(
      o => Date.now() - o.timestamp >= 7 * 24 * 60 * 60 * 1000
    )

    const opportunitiesTrend =
      recentOpportunities.length > oldOpportunities.length
        ? 'increasing'
        : recentOpportunities.length === oldOpportunities.length
        ? 'stable'
        : 'decreasing'

    // Calculate success rate
    const completedExecutions = executions.filter(e => e.status === 'complete')
    const executionSuccessRate =
      executions.length > 0 ? completedExecutions.length / executions.length : 0

    // Calculate average execution time
    const completedWithTime = executions.filter(
      e => e.status === 'complete' && e.endTime && e.startTime
    )
    const averageExecutionTime =
      completedWithTime.length > 0
        ? completedWithTime.reduce(
            (sum, e) => sum + ((e.endTime || 0) - e.startTime),
            0
          ) / completedWithTime.length
        : 0

    // Top patterns
    const patternCounts = new Map<string, number>()
    opportunities.forEach(o => {
      patternCounts.set(o.pattern, (patternCounts.get(o.pattern) || 0) + 1)
    })
    const topPatterns = Array.from(patternCounts.entries())
      .map(([pattern, count]) => ({ pattern, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5)

    return {
      opportunitiesTrend,
      executionSuccessRate,
      averageExecutionTime,
      topPatterns,
    }
  }
}

// Export singleton instance
export const convergenceDashboard = new ConvergenceDashboard()

