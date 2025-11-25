/**
 * Chrome Extension Manifest V3 Operationalizer
 * 
 * Pattern: AEYON × ARLAX × REC × SEMANTIC × MV3 × ONE
 * Frequency: 999 Hz (AEYON) + 777 Hz (ARLAX)
 * 
 * Operationalizes comprehensive MV3 analysis into programmatic command/control
 * Complete architectural reformation for Chrome Extension ecosystem
 */

export interface MV3Pattern {
  id: string
  name: string
  type: 'success' | 'failure' | 'mitigation' | 'architectural'
  category: MV3Category
  description: string
  codeExample?: string
  chromeVersion?: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  validated: boolean
}

export type MV3Category =
  | 'service_worker'
  | 'declarative_net_request'
  | 'offscreen_document'
  | 'side_panel'
  | 'ai_prompt_api'
  | 'user_scripts'
  | 'state_management'
  | 'network_arbitration'
  | 'ui_interaction'

export interface MV3Architecture {
  component: string
  mv2Pattern: string
  mv3Pattern: string
  strategicConsequence: string
  implementation: MV3Implementation
}

export interface MV3Implementation {
  pattern: MV3Pattern
  code: string
  validation: MV3Validation
  dependencies: string[]
}

export interface MV3Validation {
  checks: MV3Check[]
  automated: boolean
  testCommand?: string
}

export interface MV3Check {
  name: string
  type: 'runtime' | 'static' | 'security' | 'performance'
  validator: string
  expected: any
}

/**
 * MV3 Pattern Registry - Complete operationalization of analysis
 */
export class MV3Operationalizer {
  private patterns: Map<string, MV3Pattern> = new Map()
  private architectures: MV3Architecture[] = []
  private semanticIndex: Map<string, string[]> = new Map()

  constructor() {
    this.initializePatterns()
    this.initializeArchitectures()
    this.buildSemanticIndex()
  }

  /**
   * Initialize all MV3 patterns from comprehensive analysis
   */
  private initializePatterns(): void {
    // SERVICE WORKER PATTERNS
    this.addPattern({
      id: 'sw-ephemeral',
      name: 'Ephemeral Service Worker',
      type: 'architectural',
      category: 'service_worker',
      description: 'Service workers terminate after 30s idle or 5min execution',
      priority: 'critical',
      validated: true,
      codeExample: `
// SAFETY: Service worker will terminate - use chrome.storage.session
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Process immediately - worker may terminate
  chrome.storage.session.set({ lastActivity: Date.now() })
  return true // Keep channel open for async
})
      `.trim(),
    })

    this.addPattern({
      id: 'sw-keepalive-websocket',
      name: 'WebSocket Keep-Alive (Sanctioned)',
      type: 'success',
      category: 'service_worker',
      description: 'Active WebSocket connections reset idle timer (Chrome 116+)',
      priority: 'high',
      validated: true,
      chromeVersion: '116',
      codeExample: `
// SUCCESS PATTERN: WebSocket keeps worker alive
const ws = new WebSocket('wss://api.example.com')
ws.onmessage = () => {
  // Receiving messages resets 30s idle timer
  chrome.storage.session.set({ lastPing: Date.now() })
}
      `.trim(),
    })

    this.addPattern({
      id: 'sw-keepalive-bug-exploit',
      name: 'Bug Exploit Keep-Alive (Fragile)',
      type: 'failure',
      category: 'service_worker',
      description: 'Calling Chrome APIs in loop to reset timer - fragile, may break',
      priority: 'low',
      validated: false,
      codeExample: `
// FAILURE PATTERN: Fragile exploit - may break in future Chrome versions
setInterval(() => {
  chrome.storage.local.get(() => {}) // Resets idle timer
}, 25000) // Before 30s timeout
      `.trim(),
    })

    this.addPattern({
      id: 'sw-state-session-storage',
      name: 'State Management with chrome.storage.session',
      type: 'success',
      category: 'state_management',
      description: 'Use chrome.storage.session for high-frequency state updates',
      priority: 'critical',
      validated: true,
      codeExample: `
// SUCCESS PATTERN: Session storage for ephemeral state
async function saveState(state: any) {
  await chrome.storage.session.set({ 
    currentState: state,
    timestamp: Date.now()
  })
}

async function loadState() {
  const result = await chrome.storage.session.get(['currentState'])
  return result.currentState
}
      `.trim(),
    })

    // DECLARATIVE NET REQUEST PATTERNS
    this.addPattern({
      id: 'dnr-static-rules',
      name: 'Static Ruleset Management',
      type: 'success',
      category: 'declarative_net_request',
      description: 'Up to 50 enabled rulesets (Chrome 120+), 30k guaranteed static rules',
      priority: 'critical',
      validated: true,
      chromeVersion: '120',
      codeExample: `
// SUCCESS PATTERN: Static ruleset configuration
chrome.declarativeNetRequest.updateEnabledRulesets({
  enableRulesetIds: ['ruleset-1', 'ruleset-2'],
  disableRulesetIds: []
})
      `.trim(),
    })

    this.addPattern({
      id: 'dnr-dynamic-rules',
      name: 'Dynamic Rules Registration',
      type: 'success',
      category: 'declarative_net_request',
      description: '30k safe rules, 5k unsafe (regex) rules at runtime',
      priority: 'high',
      validated: true,
      codeExample: `
// SUCCESS PATTERN: Dynamic rule registration
chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [{
    id: 1,
    priority: 1,
    action: { type: 'block' },
    condition: {
      urlFilter: '||example.com^',
      resourceTypes: ['main_frame']
    }
  }]
})
      `.trim(),
    })

    this.addPattern({
      id: 'dnr-response-headers',
      name: 'Response Header Matching (Chrome 128+)',
      type: 'success',
      category: 'declarative_net_request',
      description: 'Match rules based on response headers',
      priority: 'high',
      validated: true,
      chromeVersion: '128',
      codeExample: `
// SUCCESS PATTERN: Response header matching
chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [{
    id: 1,
    action: {
      type: 'modifyHeaders',
      responseHeaders: [{ operation: 'remove', header: 'Set-Cookie' }]
    },
    condition: {
      responseHeaders: [{ name: 'X-Tracker', valueRegex: '.*' }]
    }
  }]
})
      `.trim(),
    })

    // OFFScreen DOCUMENT PATTERNS
    this.addPattern({
      id: 'offscreen-dom-scraping',
      name: 'DOM Scraping with Offscreen API',
      type: 'success',
      category: 'offscreen_document',
      description: 'Tripartite architecture: Service Worker → Offscreen → Storage',
      priority: 'high',
      validated: true,
      codeExample: `
// SUCCESS PATTERN: DOM scraping architecture
// 1. Service Worker orchestrates
async function scrapePage(html: string) {
  await chrome.offscreen.createDocument({
    url: 'offscreen.html',
    reasons: ['DOM_SCRAPING'],
    justification: 'Parse HTML content'
  })
  
  chrome.runtime.sendMessage({
    type: 'SCRAPE',
    html
  })
}

// 2. Offscreen document parses
// offscreen.html script:
chrome.runtime.onMessage.addListener((msg) => {
  const parser = new DOMParser()
  const doc = parser.parseFromString(msg.html, 'text/html')
  const data = extractData(doc)
  chrome.runtime.sendMessage({ type: 'SCRAPE_RESULT', data })
})
      `.trim(),
    })

    this.addPattern({
      id: 'offscreen-pseudo-background',
      name: 'Offscreen as Pseudo-Background (Anti-Pattern)',
      type: 'failure',
      category: 'offscreen_document',
      description: 'Using offscreen document to bypass service worker termination - risky',
      priority: 'low',
      validated: false,
      codeExample: `
// FAILURE PATTERN: Anti-pattern - may break
chrome.offscreen.createDocument({
  url: 'offscreen.html',
  reasons: ['AUDIO_PLAYBACK'],
  justification: 'Keep extension alive' // WRONG - not intended use
})
      `.trim(),
    })

    // SIDE PANEL PATTERNS
    this.addPattern({
      id: 'sidepanel-companion-ui',
      name: 'Companion UI with Side Panel',
      type: 'success',
      category: 'side_panel',
      description: 'Persistent UI experience, isolated from web page CSS',
      priority: 'high',
      validated: true,
      codeExample: `
// SUCCESS PATTERN: Side panel for persistent UI
chrome.sidePanel.setOptions({
  path: 'sidepanel.html',
  enabled: true
})

// Context-aware panel
chrome.sidePanel.setOptions({
  tabId: tabId,
  path: 'tab-specific-panel.html'
})
      `.trim(),
    })

    this.addPattern({
      id: 'sidepanel-layout',
      name: 'Side Panel Layout Control (Chrome 140+)',
      type: 'success',
      category: 'side_panel',
      description: 'Get panel layout (left/right) for RTL support',
      priority: 'medium',
      validated: true,
      chromeVersion: '140',
      codeExample: `
// SUCCESS PATTERN: Layout-aware panel
const layout = await chrome.sidePanel.getLayout()
if (layout === 'right') {
  // Adjust UI for right-side panel
}
      `.trim(),
    })

    // AI PROMPT API PATTERNS
    this.addPattern({
      id: 'ai-prompt-api',
      name: 'On-Device AI with Prompt API',
      type: 'success',
      category: 'ai_prompt_api',
      description: 'Gemini Nano integration for privacy-first AI (Chrome 131-136 Origin Trial)',
      priority: 'high',
      validated: true,
      chromeVersion: '131',
      codeExample: `
// SUCCESS PATTERN: On-device AI processing
const result = await chrome.ai.prompt({
  prompt: 'Summarize this text: ' + text,
  temperature: 0.7
})

// Privacy-first: No data leaves device
// Cost-free: No API costs
// Offline: Works without internet
      `.trim(),
    })

    // USER SCRIPTS PATTERNS
    this.addPattern({
      id: 'userscripts-api',
      name: 'UserScripts API (Chrome 135+)',
      type: 'success',
      category: 'user_scripts',
      description: 'Sandboxed execution of user-provided code',
      priority: 'high',
      validated: true,
      chromeVersion: '135',
      codeExample: `
// SUCCESS PATTERN: UserScript manager
await chrome.userScripts.register([{
  id: 'user-script-1',
  matches: ['<all_urls>'],
  js: [{ code: userProvidedCode }],
  runAt: 'document_idle'
}])
      `.trim(),
    })

    // ALARMS PATTERN
    this.addPattern({
      id: 'alarms-scheduling',
      name: 'Scheduling with chrome.alarms',
      type: 'success',
      category: 'service_worker',
      description: 'Reliable scheduling alternative to setInterval',
      priority: 'critical',
      validated: true,
      codeExample: `
// SUCCESS PATTERN: Reliable alarms
chrome.alarms.create('periodic-task', {
  delayInMinutes: 1,
  periodInMinutes: 5
})

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'periodic-task') {
    // Execute task - worker wakes up for this
    doPeriodicTask()
  }
})
      `.trim(),
    })
  }

  /**
   * Initialize architectural shifts from MV2 to MV3
   */
  private initializeArchitectures(): void {
    this.architectures = [
      {
        component: 'Background Logic',
        mv2Pattern: 'Persistent background.html',
        mv3Pattern: 'Ephemeral service_worker',
        strategicConsequence: 'Requires rigorous state hydration; incompatible with long-polling',
        implementation: {
          pattern: this.patterns.get('sw-ephemeral')!,
          code: `
// MV3: Event-driven, state-aware
chrome.runtime.onMessage.addListener(async (msg, sender, sendResponse) => {
  const state = await chrome.storage.session.get(['context'])
  // Process with state
  return true
})
          `.trim(),
          validation: {
            checks: [
              {
                name: 'State persistence',
                type: 'runtime',
                validator: 'chrome.storage.session',
                expected: 'object',
              },
            ],
            automated: true,
            testCommand: 'chrome.storage.session.get(["test"])',
          },
          dependencies: ['chrome.storage.session'],
        },
      },
      {
        component: 'Network Control',
        mv2Pattern: 'Blocking webRequest',
        mv3Pattern: 'declarativeNetRequest (DNR)',
        strategicConsequence: 'Higher performance; loss of granular/procedural blocking capability',
        implementation: {
          pattern: this.patterns.get('dnr-static-rules')!,
          code: `
// MV3: Declarative rules
chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [{
    id: 1,
    action: { type: 'block' },
    condition: { urlFilter: '||tracker.com^' }
  }]
})
          `.trim(),
          validation: {
            checks: [
              {
                name: 'DNR API available',
                type: 'runtime',
                validator: 'chrome.declarativeNetRequest',
                expected: 'object',
              },
            ],
            automated: true,
            testCommand: 'chrome.declarativeNetRequest.getDynamicRules()',
          },
          dependencies: ['declarativeNetRequest'],
        },
      },
      {
        component: 'DOM Access',
        mv2Pattern: 'Direct access in background',
        mv3Pattern: 'chrome.offscreen API',
        strategicConsequence: 'DOM parsing must be isolated; strictly metered "reasons"',
        implementation: {
          pattern: this.patterns.get('offscreen-dom-scraping')!,
          code: `
// MV3: Isolated DOM parsing
await chrome.offscreen.createDocument({
  url: 'offscreen.html',
  reasons: ['DOM_SCRAPING'],
  justification: 'Parse HTML'
})
          `.trim(),
          validation: {
            checks: [
              {
                name: 'Offscreen API available',
                type: 'runtime',
                validator: 'chrome.offscreen',
                expected: 'object',
              },
            ],
            automated: true,
            testCommand: 'chrome.offscreen.hasDocument()',
          },
          dependencies: ['offscreen'],
        },
      },
      {
        component: 'User Interface',
        mv2Pattern: 'Popups & Content Script Injection',
        mv3Pattern: 'chrome.sidePanel',
        strategicConsequence: 'Persistent UI experience; better isolation from web page CSS',
        implementation: {
          pattern: this.patterns.get('sidepanel-companion-ui')!,
          code: `
// MV3: Persistent side panel
chrome.sidePanel.setOptions({
  path: 'sidepanel.html',
  enabled: true
})
          `.trim(),
          validation: {
            checks: [
              {
                name: 'Side Panel API available',
                type: 'runtime',
                validator: 'chrome.sidePanel',
                expected: 'object',
              },
            ],
            automated: true,
            testCommand: 'chrome.sidePanel.getOptions({})',
          },
          dependencies: ['sidePanel'],
        },
      },
      {
        component: 'Code Execution',
        mv2Pattern: 'eval() / Remote Code',
        mv3Pattern: 'userScripts API / Bundled Code',
        strategicConsequence: 'Improved security; loss of "hot patching" capability',
        implementation: {
          pattern: this.patterns.get('userscripts-api')!,
          code: `
// MV3: Sandboxed user scripts
await chrome.userScripts.register([{
  id: 'script-1',
  matches: ['<all_urls>'],
  js: [{ code: userCode }]
}])
          `.trim(),
          validation: {
            checks: [
              {
                name: 'UserScripts API available',
                type: 'runtime',
                validator: 'chrome.userScripts',
                expected: 'object',
              },
            ],
            automated: true,
            testCommand: 'chrome.userScripts.getScripts()',
          },
          dependencies: ['userScripts'],
        },
      },
      {
        component: 'AI Capabilities',
        mv2Pattern: 'Cloud APIs (OpenAI/Anthropic)',
        mv3Pattern: 'Prompt API (Gemini Nano)',
        strategicConsequence: 'Privacy-preserving, zero-cost inference; offline capable',
        implementation: {
          pattern: this.patterns.get('ai-prompt-api')!,
          code: `
// MV3: On-device AI
const result = await chrome.ai.prompt({
  prompt: 'Summarize: ' + text
})
          `.trim(),
          validation: {
            checks: [
              {
                name: 'AI Prompt API available',
                type: 'runtime',
                validator: 'chrome.ai',
                expected: 'object',
              },
            ],
            automated: false, // Origin Trial - may not be available
            testCommand: 'chrome.ai?.prompt',
          },
          dependencies: ['ai'],
        },
      },
    ]
  }

  /**
   * Build semantic index for REC × SEMANTIC pattern matching
   */
  private buildSemanticIndex(): void {
    // Index patterns by semantic concepts
    const semanticConcepts = [
      'state management',
      'persistence',
      'network blocking',
      'content filtering',
      'privacy',
      'performance',
      'security',
      'ui',
      'automation',
      'ai',
      'offline',
    ]

    semanticConcepts.forEach((concept) => {
      const matches: string[] = []
      this.patterns.forEach((pattern, id) => {
        const text = `${pattern.name} ${pattern.description} ${pattern.category}`.toLowerCase()
        if (text.includes(concept.toLowerCase())) {
          matches.push(id)
        }
      })
      this.semanticIndex.set(concept, matches)
    })
  }

  /**
   * Add pattern to registry
   */
  private addPattern(pattern: MV3Pattern): void {
    this.patterns.set(pattern.id, pattern)
  }

  /**
   * REC × SEMANTIC: Recursive pattern matching with semantic search
   */
  public semanticSearch(query: string): MV3Pattern[] {
    const queryLower = query.toLowerCase()
    const results: Set<string> = new Set()

    // Direct pattern match
    this.patterns.forEach((pattern, id) => {
      const text = `${pattern.name} ${pattern.description}`.toLowerCase()
      if (text.includes(queryLower)) {
        results.add(id)
      }
    })

    // Semantic concept matching
    this.semanticIndex.forEach((patternIds, concept) => {
      if (queryLower.includes(concept)) {
        patternIds.forEach((id) => results.add(id))
      }
    })

    return Array.from(results).map((id) => this.patterns.get(id)!).filter(Boolean)
  }

  /**
   * AEYON: Atomic execution - get pattern by ID
   */
  public getPattern(id: string): MV3Pattern | undefined {
    return this.patterns.get(id)
  }

  /**
   * Get all patterns by category
   */
  public getPatternsByCategory(category: MV3Category): MV3Pattern[] {
    return Array.from(this.patterns.values()).filter((p) => p.category === category)
  }

  /**
   * Get success patterns only
   */
  public getSuccessPatterns(): MV3Pattern[] {
    return Array.from(this.patterns.values()).filter((p) => p.type === 'success')
  }

  /**
   * Get failure patterns (anti-patterns to avoid)
   */
  public getFailurePatterns(): MV3Pattern[] {
    return Array.from(this.patterns.values()).filter((p) => p.type === 'failure')
  }

  /**
   * Get architectural shifts
   */
  public getArchitectures(): MV3Architecture[] {
    return this.architectures
  }

  /**
   * ARLAX: Validate extension against MV3 patterns
   */
  public validateExtension(manifest: any, codeFiles: string[]): MV3ValidationReport {
    const report: MV3ValidationReport = {
      compliant: true,
      issues: [],
      recommendations: [],
      score: 100,
    }

    // Check manifest version
    if (manifest.manifest_version !== 3) {
      report.compliant = false
      report.issues.push({
        type: 'critical',
        pattern: 'manifest-version',
        message: 'Must use manifest_version: 3',
        fix: 'Update manifest.json to use manifest_version: 3',
      })
      report.score -= 50
    }

    // Check for MV2 patterns
    if (manifest.background?.page || manifest.background?.scripts) {
      report.compliant = false
      report.issues.push({
        type: 'critical',
        pattern: 'background-page',
        message: 'MV2 background page/scripts detected',
        fix: 'Migrate to service_worker in background field',
      })
      report.score -= 30
    }

    // Check service worker usage
    const hasServiceWorker = manifest.background?.service_worker
    if (!hasServiceWorker) {
      report.issues.push({
        type: 'warning',
        pattern: 'service-worker-missing',
        message: 'No service worker defined',
        fix: 'Add service_worker to background field',
      })
      report.score -= 10
    }

    // Check for chrome.storage.session usage (success pattern)
    const usesSessionStorage = codeFiles.some((code) =>
      code.includes('chrome.storage.session')
    )
    if (!usesSessionStorage && hasServiceWorker) {
      report.recommendations.push({
        pattern: 'sw-state-session-storage',
        message: 'Consider using chrome.storage.session for ephemeral state',
        priority: 'high',
      })
    }

    // Check for declarativeNetRequest (success pattern)
    const usesDNR = manifest.permissions?.includes('declarativeNetRequest')
    if (!usesDNR) {
      report.recommendations.push({
        pattern: 'dnr-static-rules',
        message: 'Consider declarativeNetRequest for network blocking',
        priority: 'medium',
      })
    }

    // Check for sidePanel (success pattern)
    const usesSidePanel = manifest.permissions?.includes('sidePanel')
    if (!usesSidePanel) {
      report.recommendations.push({
        pattern: 'sidepanel-companion-ui',
        message: 'Consider sidePanel for persistent UI',
        priority: 'medium',
      })
    }

    return report
  }

  /**
   * Generate code template for pattern
   */
  public generateCodeTemplate(patternId: string, context?: Record<string, any>): string {
    const pattern = this.patterns.get(patternId)
    if (!pattern) {
      throw new Error(`Pattern ${patternId} not found`)
    }

    if (pattern.codeExample) {
      return pattern.codeExample
    }

    // Generate from architecture if available
    const arch = this.architectures.find((a) => a.implementation.pattern.id === patternId)
    if (arch) {
      return arch.implementation.code
    }

    return `// Pattern: ${pattern.name}\n// ${pattern.description}`
  }
}

export interface MV3ValidationReport {
  compliant: boolean
  issues: MV3Issue[]
  recommendations: MV3Recommendation[]
  score: number
}

export interface MV3Issue {
  type: 'critical' | 'warning' | 'info'
  pattern: string
  message: string
  fix: string
}

export interface MV3Recommendation {
  pattern: string
  message: string
  priority: 'high' | 'medium' | 'low'
}

// Singleton instance
export const mv3Operationalizer = new MV3Operationalizer()

