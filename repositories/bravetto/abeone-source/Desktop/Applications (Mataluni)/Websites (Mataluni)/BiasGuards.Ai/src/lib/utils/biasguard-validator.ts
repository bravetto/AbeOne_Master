/**
 * BiasGuard Context Engineering Validation System
 * JAHmere Webb Freedom Mission - August 25, 2025
 * 80/20 Anti-Drift Protection for Cursor AI
 */

interface ContextValidationRule {
  pattern: RegExp;
  violation: string;
  suggestion: string;
  severity: 'critical' | 'warning' | 'info';
}

interface BiasGuardContext {
  framework: 'svelte5' | 'react' | 'vue';
  styling: 'tailwind4' | 'styled-components' | 'css-modules';
  animation: 'gsap' | 'framer-motion' | 'css-only';
  missionAlignment: boolean;
  performanceTargets: {
    lighthouse: number;
    bundleSize: number;
    loadTime: number;
  };
}

interface ValidationResult {
  isValid: boolean;
  violations: ValidationViolation[];
  score: number;
  recommendations: string[];
}

interface ValidationViolation {
  type: string;
  suggestion: string;
  severity: 'critical' | 'warning' | 'info';
  line: number;
}

export class BiasGuardContextValidator {
  private rules: ContextValidationRule[] = [
    // CRITICAL FRAMEWORK VIOLATIONS
    {
      pattern: /useState|useEffect|className=/,
      violation: " REACT DRIFT DETECTED",
      suggestion: "Use Svelte 5 runes: $state, $derived, $effect. Use class= not className=",
      severity: 'critical'
    },
    {
      pattern: /v-if|v-for|\{\{.*\}\}/,
      violation: " VUE DRIFT DETECTED", 
      suggestion: "Use Svelte syntax: {#if}, {#each}, {expression}",
      severity: 'critical'
    },
    {
      pattern: /styled-components|emotion|css-in-js/,
      violation: " STYLING DRIFT DETECTED",
      suggestion: "Use Tailwind CSS 4.0 classes only",
      severity: 'critical'
    },
    
    // PERFORMANCE VIOLATIONS
    {
      pattern: /\.style\.width|\.style\.height|\.style\.top|\.style\.left|\.style\.margin/,
      violation: " NON-GPU ANIMATION DETECTED",
      suggestion: "Use transform and opacity for 60fps animations",
      severity: 'warning'
    },
    {
      pattern: /import.*['"]\w+['"].*(?!from ['"]\.)|require\(['"](?!\.)/,
      violation: " LARGE DEPENDENCY DETECTED",
      suggestion: "Verify bundle impact - target <150KB total",
      severity: 'warning'
    },
    
    // MISSION ALIGNMENT VIOLATIONS
    {
      pattern: /fake|mock|placeholder.*story/i,
      violation: " MISSION AUTHENTICITY VIOLATION",
      suggestion: "Use only verified JAHmere Webb case details",
      severity: 'critical'
    },
    {
      pattern: /generic.*landing.*page/i,
      violation: " MISSION FOCUS DRIFT",
      suggestion: "Maintain BiasGuard + justice mission specificity",
      severity: 'warning'
    },
    
    // COURT DATE VALIDATION
    {
      pattern: /July 28|July.*2025/i,
      violation: " COURT DATE ACCURACY VIOLATION",
      suggestion: "Court date is August 25, 2025 - maintain accuracy",
      severity: 'critical'
    }
  ];

  validateContext(code: string, context: BiasGuardContext): ValidationResult {
    const violations: ValidationViolation[] = [];
    
    // Check code against drift patterns
    this.rules.forEach(rule => {
      if (rule.pattern.test(code)) {
        violations.push({
          type: rule.violation,
          suggestion: rule.suggestion,
          severity: rule.severity,
          line: this.findLineNumber(code, rule.pattern)
        });
      }
    });
    
    // Validate context alignment
    this.validateContextAlignment(context, violations);
    
    return {
      isValid: violations.filter(v => v.severity === 'critical').length === 0,
      violations,
      score: this.calculateContextScore(violations),
      recommendations: this.generateRecommendations(violations)
    };
  }

  private validateContextAlignment(context: BiasGuardContext, violations: ValidationViolation[]) {
    // Framework validation
    if (context.framework !== 'svelte5') {
      violations.push({
        type: " FRAMEWORK DRIFT",
        suggestion: "Must use Svelte 5 with Runes API",
        severity: 'critical',
        line: 0
      });
    }
    
    // Performance validation
    if (context.performanceTargets.lighthouse < 95) {
      violations.push({
        type: " PERFORMANCE TARGET DRIFT",
        suggestion: "Lighthouse score must be 95+ for BiasGuard standards",
        severity: 'warning',
        line: 0
      });
    }
    
    // Mission alignment validation
    if (!context.missionAlignment) {
      violations.push({
        type: " MISSION DRIFT",
        suggestion: "Must maintain JAHmere Webb story authenticity",
        severity: 'critical',
        line: 0
      });
    }
  }

  private findLineNumber(code: string, pattern: RegExp): number {
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (pattern.test(lines[i])) {
        return i + 1;
      }
    }
    return 0;
  }

  private calculateContextScore(violations: ValidationViolation[]): number {
    const weights = { critical: 35, warning: 10, info: 3 };
    const penalty = violations.reduce((sum, v) => sum + weights[v.severity], 0);
    return Math.max(0, 100 - penalty);
  }

  private generateRecommendations(violations: ValidationViolation[]): string[] {
    const criticalViolations = violations.filter(v => v.severity === 'critical');
    const recommendations: string[] = [];
    
    if (criticalViolations.length > 0) {
      recommendations.push(" CRITICAL: Fix framework/mission violations before proceeding");
    }
    
    const warningCount = violations.filter(v => v.severity === 'warning').length;
    if (warningCount > 0) {
      recommendations.push(` Address ${warningCount} performance/style warnings`);
    }
    
    return recommendations;
  }

  // CURSOR AI INTEGRATION PROMPTS
  generateCursorPrompt(context: BiasGuardContext): string {
    return `
BIASGUARD CONTEXT ENGINEERING PROMPT

IDENTITY & MISSION:
You are building the BiasGuard landing page - the AI bias detection tool born from fighting for JAHmere Webb's freedom. Every decision serves justice and technical excellence.

TECHNICAL CONSTRAINTS (CRITICAL - NEVER VIOLATE):
 Framework: Svelte 5 with Runes API ($state, $derived, $effect)
 Styling: Tailwind CSS 4.0 with Oxide engine
 Animation: GSAP 3.13 + CSS transforms (GPU only)
 Performance: 98+ Lighthouse, <150KB bundle, <1.2s load
 Architecture: Zero-dependency, privacy-first

 NEVER USE: React patterns, Vue syntax, styled-components, Node.js APIs in browser
 NEVER ANIMATE: width, height, top, left, margin (causes jank)

MISSION CONTEXT (MAINTAIN AUTHENTICITY):
- JAHmere Webb case: Real story, crisis situation, $26,500 cost
- Court date: August 25, 2025 (creates urgency)
- BiasGuard origin: Built under pressure, proven in legal proceedings
- Revenue commitment: 15% to criminal justice reform

CONVERSION PSYCHOLOGY:
- Primary emotion: Justice + technical excellence
- Trust builders: Real forensic analysis, peer testimonials
- Risk reducers: Free trial, privacy-first, zero data collection
- Value amplifiers: Speed demo (<300ms), ROI calculator

VALIDATION REQUIREMENTS:
Before proceeding, confirm:
1.  Using Svelte 5 syntax correctly
2.  Maintaining JAHmere Webb story authenticity  
3.  Meeting performance targets
4.  GPU-optimized animations only
5.  Justice mission alignment maintained

If any validation fails, stop and correct before continuing.
`;
  }
}

// SYSTEMATIC CONTEXT ENGINEERING WORKFLOW
export class BiasGuardContextWorkflow {
  private validator = new BiasGuardContextValidator();

  // PHASE 1: PRE-DEVELOPMENT CONTEXT DESIGN
  async designContext(): Promise<BiasGuardContext> {
    return {
      framework: 'svelte5',
      styling: 'tailwind4',
      animation: 'gsap',
      missionAlignment: true,
      performanceTargets: {
        lighthouse: 98,
        bundleSize: 150000,
        loadTime: 1200
      }
    };
  }
  
  // PHASE 2: CONTEXT-DRIVEN DEVELOPMENT
  async generateWithContext(task: string, context: BiasGuardContext): Promise<string> {
    const cursorPrompt = this.validator.generateCursorPrompt(context);
    return cursorPrompt;
  }
  
  // PHASE 3: CONTINUOUS VALIDATION
  async validateOutput(output: string, context: BiasGuardContext): Promise<ValidationResult> {
    const result = this.validator.validateContext(output, context);
    
    if (!result.isValid) {
      console.error(" CONTEXT DRIFT DETECTED:");
      result.violations.forEach(v => console.error(`${v.type}: ${v.suggestion}`));
    }
    
    return result;
  }

  // BIASGUARD PROJECT CONSTANTS
  static readonly MISSION_CONSTANTS = {
    COURT_DATE: 'August 25, 2025',
    LEGAL_CRISIS_AMOUNT: '$26,500',
    REVENUE_TO_JUSTICE: '15%',
    MISSION_NAME: 'JAHmere Webb Freedom Mission'
  } as const;

  // PERFORMANCE TARGETS
  static readonly PERFORMANCE_TARGETS = {
    LIGHTHOUSE_SCORE: 98,
    BUNDLE_SIZE_LIMIT: 150000, // 150KB
    LOAD_TIME_TARGET: 1200,    // 1.2s
    FCP_TARGET: 1000,          // 1s First Contentful Paint
    TTI_TARGET: 2000           // 2s Time to Interactive
  } as const;
}

// USAGE EXAMPLE FOR BIASGUARDS.AI
export const createBiasGuardValidator = () => {
  const validator = new BiasGuardContextValidator();
  const workflow = new BiasGuardContextWorkflow();
  
  return {
    validator,
    workflow,
    validateCode: (code: string) => validator.validateContext(code, {
      framework: 'svelte5',
      styling: 'tailwind4',
      animation: 'gsap',
      missionAlignment: true,
      performanceTargets: BiasGuardContextWorkflow.PERFORMANCE_TARGETS
    }),
    generatePrompt: (context: BiasGuardContext) => validator.generateCursorPrompt(context)
  };
};
