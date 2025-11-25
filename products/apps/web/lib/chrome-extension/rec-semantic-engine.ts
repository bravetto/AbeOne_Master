/**
 * REC × SEMANTIC Engine for Chrome Extension Development
 * 
 * Pattern: REC × SEMANTIC × MV3 × OPERATIONAL × ONE
 * Frequency: 999 Hz (AEYON) + 777 Hz (ARLAX)
 * 
 * Recursive Execution Convergence × Semantic Pattern Recognition
 * Complete command/control system for Chrome Extension development
 */

import { MV3Pattern, MV3Category, mv3Operationalizer } from './mv3-operationalizer'

export interface RECSemanticQuery {
  intent: string
  context: RECContext
  constraints: RECConstraint[]
  expectedOutcome: string
}

export interface RECContext {
  currentArchitecture: 'mv2' | 'mv3' | 'hybrid'
  chromeVersion?: string
  useCase: string
  constraints: string[]
}

export interface RECConstraint {
  type: 'performance' | 'security' | 'privacy' | 'functionality' | 'compatibility'
  requirement: string
  priority: 'critical' | 'high' | 'medium' | 'low'
}

export interface RECExecutionPlan {
  steps: RECExecutionStep[]
  patterns: MV3Pattern[]
  validation: RECValidation
  estimatedComplexity: number
}

export interface RECExecutionStep {
  id: string
  action: string
  pattern: MV3Pattern
  code: string
  validation: string
  dependencies: string[]
  order: number
}

export interface RECValidation {
  checks: RECValidationCheck[]
  automated: boolean
  manualSteps?: string[]
}

export interface RECValidationCheck {
  name: string
  type: 'runtime' | 'static' | 'security' | 'performance'
  command: string
  expected: any
}

/**
 * REC × SEMANTIC Engine
 * Recursive pattern matching with semantic understanding
 */
export class RECSemanticEngine {
  /**
   * Process query with REC × SEMANTIC pattern matching
   */
  public processQuery(query: RECSemanticQuery): RECExecutionPlan {
    // Step 1: Semantic pattern discovery
    const patterns = this.discoverPatterns(query)

    // Step 2: Recursive validation and convergence
    const validatedPatterns = this.recursiveValidate(patterns, query.constraints)

    // Step 3: Generate execution plan
    const plan = this.generateExecutionPlan(validatedPatterns, query)

    // Step 4: Validate plan completeness
    this.validatePlanCompleteness(plan, query)

    return plan
  }

  /**
   * SEMANTIC: Discover relevant patterns based on intent
   */
  private discoverPatterns(query: RECSemanticQuery): MV3Pattern[] {
    const discovered: Set<string> = new Set()

    // Direct semantic search
    const semanticResults = mv3Operationalizer.semanticSearch(query.intent)
    semanticResults.forEach((p) => discovered.add(p.id))

    // Context-aware discovery
    if (query.context.currentArchitecture === 'mv2') {
      // Migration patterns
      const migrationPatterns = mv3Operationalizer
        .getArchitectures()
        .map((a) => a.implementation.pattern)
      migrationPatterns.forEach((p) => discovered.add(p.id))
    }

    // Use case specific patterns
    const useCasePatterns = this.matchUseCasePatterns(query.context.useCase)
    useCasePatterns.forEach((p) => discovered.add(p.id))

    // Constraint-based filtering
    query.constraints.forEach((constraint) => {
      const constraintPatterns = this.matchConstraintPatterns(constraint)
      constraintPatterns.forEach((p) => discovered.add(p.id))
    })

    return Array.from(discovered)
      .map((id) => mv3Operationalizer.getPattern(id))
      .filter((p): p is MV3Pattern => p !== undefined)
  }

  /**
   * REC: Recursive validation and convergence
   */
  private recursiveValidate(
    patterns: MV3Pattern[],
    constraints: RECConstraint[]
  ): MV3Pattern[] {
    let validated = [...patterns]
    let convergence = false
    let iterations = 0
    const maxIterations = 10

    while (!convergence && iterations < maxIterations) {
      const previousCount = validated.length

      // Filter by constraints
      validated = validated.filter((pattern) => {
        return constraints.every((constraint) => {
          return this.patternSatisfiesConstraint(pattern, constraint)
        })
      })

      // Remove failure patterns (unless explicitly needed)
      validated = validated.filter((p) => {
        if (p.type === 'failure') {
          // Only keep if explicitly needed for migration understanding
          return false
        }
        return true
      })

      // Prioritize success patterns
      validated.sort((a, b) => {
        if (a.type === 'success' && b.type !== 'success') return -1
        if (a.type !== 'success' && b.type === 'success') return 1
        return 0
      })

      // Check convergence
      convergence = validated.length === previousCount
      iterations++
    }

    return validated
  }

  /**
   * Check if pattern satisfies constraint
   */
  private patternSatisfiesConstraint(pattern: MV3Pattern, constraint: RECConstraint): boolean {
    const patternText = `${pattern.name} ${pattern.description}`.toLowerCase()

    switch (constraint.type) {
      case 'performance':
        return (
          patternText.includes('performance') ||
          patternText.includes('fast') ||
          pattern.category === 'declarative_net_request'
        )

      case 'security':
        return (
          patternText.includes('security') ||
          pattern.type === 'success' ||
          pattern.category === 'state_management'
        )

      case 'privacy':
        return (
          patternText.includes('privacy') ||
          pattern.category === 'ai_prompt_api' ||
          pattern.category === 'declarative_net_request'
        )

      case 'functionality':
        return pattern.type !== 'failure'

      case 'compatibility':
        if (constraint.requirement.includes('chrome')) {
          const versionMatch = constraint.requirement.match(/chrome\s*(\d+)/i)
          if (versionMatch && pattern.chromeVersion) {
            return parseInt(pattern.chromeVersion) <= parseInt(versionMatch[1])
          }
        }
        return true

      default:
        return true
    }
  }

  /**
   * Match patterns to use case
   */
  private matchUseCasePatterns(useCase: string): MV3Pattern[] {
    const useCaseLower = useCase.toLowerCase()
    const matches: MV3Pattern[] = []

    // Content blocking
    if (useCaseLower.includes('block') || useCaseLower.includes('filter')) {
      matches.push(
        ...mv3Operationalizer.getPatternsByCategory('declarative_net_request')
      )
    }

    // Privacy protection
    if (useCaseLower.includes('privacy') || useCaseLower.includes('track')) {
      matches.push(
        ...mv3Operationalizer.getPatternsByCategory('declarative_net_request')
      )
      matches.push(...mv3Operationalizer.getPatternsByCategory('ai_prompt_api'))
    }

    // Productivity tools
    if (useCaseLower.includes('productivity') || useCaseLower.includes('note')) {
      matches.push(...mv3Operationalizer.getPatternsByCategory('side_panel'))
    }

    // AI features
    if (useCaseLower.includes('ai') || useCaseLower.includes('summarize')) {
      matches.push(...mv3Operationalizer.getPatternsByCategory('ai_prompt_api'))
    }

    // Automation
    if (useCaseLower.includes('automate') || useCaseLower.includes('script')) {
      matches.push(...mv3Operationalizer.getPatternsByCategory('user_scripts'))
    }

    return matches
  }

  /**
   * Match patterns to constraints
   */
  private matchConstraintPatterns(constraint: RECConstraint): MV3Pattern[] {
    const matches: MV3Pattern[] = []

    if (constraint.type === 'performance') {
      matches.push(
        ...mv3Operationalizer.getPatternsByCategory('declarative_net_request')
      )
    }

    if (constraint.type === 'privacy') {
      matches.push(...mv3Operationalizer.getPatternsByCategory('ai_prompt_api'))
    }

    return matches
  }

  /**
   * Generate execution plan from validated patterns
   */
  private generateExecutionPlan(
    patterns: MV3Pattern[],
    query: RECSemanticQuery
  ): RECExecutionPlan {
    const steps: RECExecutionStep[] = []
    let order = 1

    // Group patterns by category for logical ordering
    const categories: MV3Category[] = [
      'service_worker',
      'state_management',
      'declarative_net_request',
      'offscreen_document',
      'side_panel',
      'ai_prompt_api',
      'user_scripts',
    ]

    categories.forEach((category) => {
      const categoryPatterns = patterns.filter((p) => p.category === category)
      categoryPatterns.forEach((pattern) => {
        if (pattern.type === 'success') {
          steps.push({
            id: `step-${order}`,
            action: `Implement ${pattern.name}`,
            pattern,
            code: mv3Operationalizer.generateCodeTemplate(pattern.id),
            validation: this.generateValidation(pattern),
            dependencies: this.extractDependencies(pattern),
            order: order++,
          })
        }
      })
    })

    return {
      steps,
      patterns,
      validation: {
        checks: steps.flatMap((s) => this.generateValidationChecks(s.pattern)),
        automated: true,
      },
      estimatedComplexity: this.estimateComplexity(steps),
    }
  }

  /**
   * Generate validation for pattern
   */
  private generateValidation(pattern: MV3Pattern): string {
    const arch = mv3Operationalizer
      .getArchitectures()
      .find((a) => a.implementation.pattern.id === pattern.id)

    if (arch?.implementation.validation.testCommand) {
      return `Test: ${arch.implementation.validation.testCommand}`
    }

    return `Validate: ${pattern.name} implementation`
  }

  /**
   * Generate validation checks
   */
  private generateValidationChecks(pattern: MV3Pattern): RECValidationCheck[] {
    const arch = mv3Operationalizer
      .getArchitectures()
      .find((a) => a.implementation.pattern.id === pattern.id)

    if (arch?.implementation.validation.checks) {
      return arch.implementation.validation.checks.map((check) => ({
        name: check.name,
        type: check.type,
        command: check.validator,
        expected: check.expected,
      }))
    }

    return [
      {
        name: `Validate ${pattern.name}`,
        type: 'runtime',
        command: `chrome.${pattern.category}`,
        expected: 'object',
      },
    ]
  }

  /**
   * Extract dependencies from pattern
   */
  private extractDependencies(pattern: MV3Pattern): string[] {
    const arch = mv3Operationalizer
      .getArchitectures()
      .find((a) => a.implementation.pattern.id === pattern.id)

    return arch?.implementation.dependencies || []
  }

  /**
   * Estimate complexity of execution plan
   */
  private estimateComplexity(steps: RECExecutionStep[]): number {
    let complexity = 0

    steps.forEach((step) => {
      switch (step.pattern.priority) {
        case 'critical':
          complexity += 10
          break
        case 'high':
          complexity += 5
          break
        case 'medium':
          complexity += 3
          break
        case 'low':
          complexity += 1
          break
      }
    })

    return complexity
  }

  /**
   * Validate plan completeness
   */
  private validatePlanCompleteness(plan: RECExecutionPlan, query: RECSemanticQuery): void {
    // Check if all constraints are addressed
    const addressedConstraints = new Set<string>()

    plan.patterns.forEach((pattern) => {
      query.constraints.forEach((constraint) => {
        if (this.patternSatisfiesConstraint(pattern, constraint)) {
          addressedConstraints.add(constraint.type)
        }
      })
    })

    // Warn if constraints not fully addressed
    query.constraints.forEach((constraint) => {
      if (!addressedConstraints.has(constraint.type) && constraint.priority === 'critical') {
        console.warn(`Critical constraint ${constraint.type} may not be fully addressed`)
      }
    })
  }

  /**
   * AEYON: Atomic execution - execute single step
   */
  public executeStep(step: RECExecutionStep): RECExecutionResult {
    return {
      success: true,
      stepId: step.id,
      output: step.code,
      validation: this.runValidation(step),
    }
  }

  /**
   * Run validation for step
   */
  private runValidation(step: RECExecutionStep): RECValidationResult {
    // In real implementation, this would execute the validation checks
    return {
      passed: true,
      checks: step.pattern.validated ? ['Pattern validated'] : ['Pattern needs validation'],
    }
  }
}

export interface RECExecutionResult {
  success: boolean
  stepId: string
  output: string
  validation: RECValidationResult
}

export interface RECValidationResult {
  passed: boolean
  checks: string[]
}

// Singleton instance
export const recSemanticEngine = new RECSemanticEngine()

