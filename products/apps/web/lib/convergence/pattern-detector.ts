/**
 * Automated Convergence Pattern Detector
 * 
 * Pattern: PATTERN × DETECTION × AUTOMATION × CONVERGENCE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Automatically detects convergence opportunities across all projects and systems.
 */

import { ConvergenceOpportunity } from './unified-executor'
import { convergenceExecutor } from './unified-executor'

export interface PatternMatch {
  pattern: string
  confidence: number
  projects: string[]
  systems: string[]
  evidence: string[]
}

/**
 * Pattern Detector
 * 
 * Detects convergence patterns automatically.
 */
export class PatternDetector {
  private knownPatterns: Map<string, RegExp> = new Map()

  constructor() {
    this.initializePatterns()
  }

  /**
   * Initialize known patterns
   */
  private initializePatterns(): void {
    // Pattern: CDF × Chrome Extension
    this.knownPatterns.set(
      'CDF × Chrome Extension',
      /cdf|chrome.*extension|export.*cdf/i
    )

    // Pattern: Monitoring × Build Health
    this.knownPatterns.set(
      'Monitoring × Build Health',
      /monitoring|build.*health|metrics/i
    )

    // Pattern: Convergence × Execution
    this.knownPatterns.set(
      'Convergence × Execution',
      /convergence|execute|unified/i
    )

    // Pattern: Guardian × Swarm
    this.knownPatterns.set(
      'Guardian × Swarm',
      /guardian|swarm|orchestrat/i
    )
  }

  /**
   * Detect patterns in codebase
   */
  async detectPatterns(
    projects: string[],
    systems: string[]
  ): Promise<PatternMatch[]> {
    const matches: PatternMatch[] = []

    // Check each known pattern
    for (const [patternName, patternRegex] of Array.from(this.knownPatterns.entries())) {
      const evidence: string[] = []
      let matchCount = 0

      // Check projects
      for (const project of projects) {
        if (patternRegex.test(project)) {
          evidence.push(`Project: ${project}`)
          matchCount++
        }
      }

      // Check systems
      for (const system of systems) {
        if (patternRegex.test(system)) {
          evidence.push(`System: ${system}`)
          matchCount++
        }
      }

      // If matches found, create pattern match
      if (matchCount > 0) {
        const confidence = Math.min(matchCount / (projects.length + systems.length), 1.0)
        
        matches.push({
          pattern: patternName,
          confidence,
          projects: projects.filter(p => patternRegex.test(p)),
          systems: systems.filter(s => patternRegex.test(s)),
          evidence,
        })
      }
    }

    return matches
  }

  /**
   * Auto-register convergence opportunities from patterns
   */
  async autoRegisterOpportunities(
    projects: string[],
    systems: string[]
  ): Promise<ConvergenceOpportunity[]> {
    const patterns = await this.detectPatterns(projects, systems)
    const opportunities: ConvergenceOpportunity[] = []

    for (const match of patterns) {
      if (match.confidence >= 0.5) {
        const opportunity: ConvergenceOpportunity = {
          id: `auto-${match.pattern.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`,
          pattern: match.pattern,
          impact: match.confidence >= 0.8 ? 'critical' : match.confidence >= 0.6 ? 'high' : 'medium',
          effort: 'medium',
          status: 'pending',
          projects: match.projects,
          systems: match.systems,
          convergenceFormula: `${match.pattern} × CONVERGE × ONE`,
          timestamp: Date.now(),
        }

        convergenceExecutor.registerOpportunity(opportunity)
        opportunities.push(opportunity)
      }
    }

    return opportunities
  }
}

// Export singleton instance
export const patternDetector = new PatternDetector()

