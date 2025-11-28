/**
 * BiasGuard Core Validation Engine
 * JAHmere Webb Freedom Mission - August 25, 2025
 * 
 * Recursive Intelligence System that validates:
 * - Framework contamination (React/Vue/Angular)
 * - Mission story authenticity
 * - Performance anti-patterns
 * - Code quality standards
 */

export interface ValidationResult {
  valid: boolean;
  score: number;
  issues: string[];
  recommendations?: string[];
  framework?: string;
  missionCompliant?: boolean;
}

export interface FrameworkConfig {
  name: string;
  goodPatterns: string[];
  badPatterns: string[];
  fileExtensions: string[];
}

export class BiasGuardValidator {
  private static readonly JAHMERE_WEBB_FACTS = {
    courtDate: 'August 25, 2025',
    crisisAmount: '$26,500',
    crisisTime: '2:42:56 AM',
    crisisDate: 'July 14, 2025',
    revenueToJustice: '15%'
  };

  private static readonly FRAMEWORKS: Record<string, FrameworkConfig> = {
    react: {
      name: 'React',
      goodPatterns: ['useState', 'useEffect', 'className', 'jsx', 'tsx'],
      badPatterns: ['v-if', 'v-for', '$state', '$derived', '@click'],
      fileExtensions: ['.jsx', '.tsx', '.js', '.ts']
    },
    vue: {
      name: 'Vue',
      goodPatterns: ['v-if', 'v-for', 'v-model', '@click', 'ref(', 'reactive('],
      badPatterns: ['useState', 'useEffect', 'className', '$state', '$derived'],
      fileExtensions: ['.vue', '.js', '.ts']
    },
    svelte: {
      name: 'Svelte',
      goodPatterns: ['$state', '$derived', '$effect', '$props', 'bind:', 'on:'],
      badPatterns: ['useState', 'useEffect', 'className', 'v-if', 'v-for'],
      fileExtensions: ['.svelte', '.js', '.ts']
    },
    angular: {
      name: 'Angular',
      goodPatterns: ['@Component', '@Injectable', '*ngIf', '*ngFor', '(click)'],
      badPatterns: ['useState', 'useEffect', 'v-if', '$state', '$derived'],
      fileExtensions: ['.component.ts', '.service.ts', '.module.ts', '.html']
    }
  };

  private static readonly PERFORMANCE_ANTI_PATTERNS = [
    'width:', 'height:', 'top:', 'left:', // Non-GPU animations
    'document.getElementById', // Direct DOM manipulation
    'setTimeout(', 'setInterval(' // Unmanaged timers
  ];

  public static validate(code: string, targetFramework?: string): ValidationResult {
    const issues: string[] = [];
    let score = 100;
    let framework: string | undefined;
    let missionCompliant = true;

    // Detect and prevent recursive BiasGuard analysis
    if (this.isBiasGuardOutput(code)) {
      return {
        valid: true,
        score: 100,
        issues: ['🔄 Recursive analysis detected - BiasGuard output cannot analyze itself'],
        recommendations: ['Analyze original source code instead of BiasGuard results'],
        framework: 'BiasGuard Output',
        missionCompliant: true
      };
    }

    // Detect framework contamination
    if (targetFramework) {
      const config = this.FRAMEWORKS[targetFramework];
      if (config) {
        framework = config.name;
        
        // Check for bad patterns from other frameworks
        Object.entries(this.FRAMEWORKS).forEach(([key, otherConfig]) => {
          if (key !== targetFramework) {
            otherConfig.goodPatterns.forEach(pattern => {
              if (code.includes(pattern)) {
                issues.push(`❌ ${otherConfig.name} contamination detected: ${pattern}`);
                score -= 20;
              }
            });
          }
        });

        // Check for good patterns in target framework
        const hasGoodPatterns = config.goodPatterns.some(pattern => 
          code.includes(pattern)
        );
        
        if (!hasGoodPatterns && code.includes('<script') || code.includes('function') || code.includes('const')) {
          issues.push(`⚠️  Missing ${config.name} patterns. Use: ${config.goodPatterns.slice(0, 3).join(', ')}`);
          score -= 15;
        }
      }
    }

    // Validate JAHmere Webb mission facts
    const wrongFacts = [
      { wrong: 'July 28', correct: 'August 25', context: 'court date' },
      { wrong: '$25,000', correct: '$26,500', context: 'crisis amount' },
      { wrong: '$27,000', correct: '$26,500', context: 'crisis amount' },
      { wrong: '10%', correct: '15%', context: 'revenue to justice' },
      { wrong: '20%', correct: '15%', context: 'revenue to justice' }
    ];

    wrongFacts.forEach(fact => {
      if (code.includes(fact.wrong)) {
        issues.push(`🚨 Wrong JAHmere Webb ${fact.context}: Use ${fact.correct}, not ${fact.wrong}`);
        score -= 30;
        missionCompliant = false;
      }
    });

    // Check for performance anti-patterns
    this.PERFORMANCE_ANTI_PATTERNS.forEach(pattern => {
      if (code.includes(pattern)) {
        issues.push(`⚡ Performance issue: Avoid ${pattern}`);
        score -= 10;
      }
    });

    // Generate recommendations
    const recommendations: string[] = [];
    if (score < 80) {
      recommendations.push('Review framework patterns and mission facts');
    }
    if (issues.some(i => i.includes('contamination'))) {
      recommendations.push('Remove cross-framework patterns');
    }
    if (!missionCompliant) {
      recommendations.push('Verify JAHmere Webb story authenticity');
    }

    return {
      valid: issues.length === 0,
      score: Math.max(0, score),
      issues,
      recommendations: recommendations.length > 0 ? recommendations : undefined,
      framework,
      missionCompliant
    };
  }

  public static validateFile(filePath: string, content: string, targetFramework?: string): ValidationResult {
    // Auto-detect framework from file extension if not specified
    if (!targetFramework) {
      for (const [key, config] of Object.entries(this.FRAMEWORKS)) {
        if (config.fileExtensions.some(ext => filePath.endsWith(ext))) {
          targetFramework = key;
          break;
        }
      }
    }

    return this.validate(content, targetFramework);
  }

  public static getSupportedFrameworks(): string[] {
    return Object.keys(this.FRAMEWORKS);
  }

  public static getFrameworkConfig(framework: string): FrameworkConfig | undefined {
    return this.FRAMEWORKS[framework];
  }

  /**
   * Detect if the input text is BiasGuard analysis output
   * This prevents infinite recursive analysis loops
   */
  private static isBiasGuardOutput(code: string): boolean {
    const biasGuardSignatures = [
      '[BiasGuard]',
      'BiasGuard Analysis Results',
      '🔴 FIX (',
      '🟡 REVIEW (',
      '🟢 PASS (',
      'Feature Creep:',
      'Assumption Bias:',
      'Context Waste:',
      'Analyzed Text:',
      '=================================================='
    ];

    // Check if text contains multiple BiasGuard signatures
    const signatureCount = biasGuardSignatures.filter(signature => 
      code.includes(signature)
    ).length;

    // If 3+ signatures found, it's likely BiasGuard output
    return signatureCount >= 3;
  }

  /**
   * Clean analysis method that strips BiasGuard output and analyzes original content
   */
  public static cleanAnalyze(input: string, targetFramework?: string): ValidationResult {
    // Extract original content if BiasGuard output is detected
    if (this.isBiasGuardOutput(input)) {
      const lines = input.split('\n');
      let originalContentStart = -1;
      
      // Find "Analyzed Text:" section
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('Analyzed Text:') || lines[i].includes('--------------------')) {
          originalContentStart = i + 1;
          break;
        }
      }
      
      if (originalContentStart > -1) {
        // Extract content after "Analyzed Text:" marker
        const originalContent = lines.slice(originalContentStart)
          .filter(line => !line.includes('[BiasGuard]') && !line.includes('===================='))
          .join('\n')
          .trim();
          
        if (originalContent) {
          return this.validate(originalContent, targetFramework);
        }
      }
      
      // If we can't extract original content, return recursion warning
      return {
        valid: false,
        score: 0,
        issues: ['🔄 Recursive BiasGuard analysis detected. Please provide original source code.'],
        recommendations: ['Submit the original code file instead of BiasGuard analysis results'],
        framework: 'Recursive Input',
        missionCompliant: true
      };
    }
    
    // If not BiasGuard output, proceed with normal validation
    return this.validate(input, targetFramework);
  }
}
