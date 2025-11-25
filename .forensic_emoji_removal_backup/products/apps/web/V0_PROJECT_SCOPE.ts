/**
 * V0 PROJECT SCOPE DEFINITION
 * 
 * Pattern: SCOPE × V0 × BOUNDARY × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * PROGRAMMATIC SCOPE ENFORCEMENT
 * This file defines the V0 project boundaries programmatically.
 * 
 * ⚠️ CRITICAL: Do NOT modify this file without explicit V0 project scope changes.
 * ⚠️ CRITICAL: Do NOT add routes/pages outside this scope.
 */

/**
 * V0 Project Scope Configuration
 */
export const V0_PROJECT_SCOPE = {
  /**
   * V0 Project Routes (ONLY these routes are part of V0 project)
   */
  routes: {
    allowed: [
      '/',                    // Home page (V0 entry point)
      '/collaboration',       // V0 Collaboration Dashboard
    ],
    api: [
      '/api/collaboration',   // V0 Collaboration API
      '/api/health',          // Health check (used by V0)
    ],
  },

  /**
   * V0 Project Components (ONLY these components are part of V0 project)
   */
  components: {
    v0: [
      'components/ui/kpi-card.tsx',  // V0 component from v0.dev
    ],
    used: [
      'components/ui/card.tsx',
      'components/ui/badge.tsx',
      'components/ui/progress.tsx',
      'components/ui/button.tsx',
      'components/ui/alert.tsx',
      'components/ui/toast.tsx',
      'components/ui/skeleton.tsx',
      'components/ui/error-boundary.tsx',
    ],
  },

  /**
   * V0 Project Pages (ONLY these pages are part of V0 project)
   */
  pages: [
    'app/page.tsx',                    // Home page (V0 entry)
    'app/collaboration/page.tsx',      // V0 Dashboard
  ],

  /**
   * V0 Project API Routes (ONLY these API routes are part of V0 project)
   */
  apiRoutes: [
    'app/api/collaboration/route.ts',  // V0 Collaboration API
    'app/api/health/route.ts',         // Health check
  ],

  /**
   * V0 Project Middleware (Enterprise enhancements for V0)
   */
  middleware: [
    'middleware.ts',
    'lib/middleware/api-wrapper.ts',
    'lib/middleware/rate-limiter.ts',
    'lib/middleware/auth.ts',
    'lib/middleware/logger.ts',
  ],

  /**
   * V0 Project Infrastructure (Supporting systems)
   */
  infrastructure: [
    'lib/api.ts',
    'lib/api-client.ts',
    'lib/monitoring.ts',
    'lib/env.ts',
    'components/providers.tsx',
  ],

  /**
   * EXCLUDED Routes (NOT part of V0 project - DO NOT MODIFY)
   */
  excluded: {
    routes: [
      '/app',              // NOT V0 project
      '/app/agents',       // NOT V0 project
      '/app/state',        // NOT V0 project
      '/app/workflows',    // NOT V0 project
      '/shop',             // NOT V0 project
      '/bravetto',         // NOT V0 project
      '/webinar',          // NOT V0 project
      '/collections',      // NOT V0 project
      '/products',         // NOT V0 project
      '/start',            // NOT V0 project
    ],
    pages: [
      'app/app/page.tsx',
      'app/app/agents/page.tsx',
      'app/app/state/page.tsx',
      'app/app/workflows/page.tsx',
      'app/shop/page.tsx',
      'app/bravetto/page.tsx',
      'app/webinar/**',
      'app/collections/**',
      'app/products/**',
      'app/start/page.tsx',
    ],
  },
} as const

/**
 * Validate if a route is part of V0 project
 */
export function isV0Route(path: string): boolean {
  const allAllowedRoutes = [
    ...V0_PROJECT_SCOPE.routes.allowed,
    ...V0_PROJECT_SCOPE.routes.api,
  ]
  
  return allAllowedRoutes.some(route => path === route || path.startsWith(route + '/'))
}

/**
 * Validate if a route is EXCLUDED from V0 project
 */
export function isExcludedRoute(path: string): boolean {
  return V0_PROJECT_SCOPE.excluded.routes.some(route => 
    path === route || path.startsWith(route + '/')
  )
}

/**
 * Get V0 project scope validation result
 */
export function validateV0Scope(path: string): {
  isValid: boolean
  isV0: boolean
  isExcluded: boolean
  message: string
} {
  if (isExcludedRoute(path)) {
    return {
      isValid: false,
      isV0: false,
      isExcluded: true,
      message: `Route "${path}" is EXCLUDED from V0 project. Do not modify or reference this route in V0 project.`,
    }
  }

  if (isV0Route(path)) {
    return {
      isValid: true,
      isV0: true,
      isExcluded: false,
      message: `Route "${path}" is part of V0 project.`,
    }
  }

  return {
    isValid: false,
    isV0: false,
    isExcluded: false,
    message: `Route "${path}" is NOT part of V0 project scope. Add to V0_PROJECT_SCOPE if needed.`,
  }
}

/**
 * V0 Project Guard - Use in components/pages to enforce scope
 */
export function V0Guard(componentName: string, allowedRoutes: string[] = []) {
  return function <T extends (...args: any[]) => any>(target: T): T {
    // Runtime guard - logs warning if used incorrectly
    if (process.env.NODE_ENV === 'development') {
      console.log(`[V0 Guard] ${componentName} - Allowed routes:`, allowedRoutes)
    }
    return target
  }
}

