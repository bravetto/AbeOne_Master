/**
 * Enterprise Monitoring Utilities
 * 
 * Pattern: MONITORING × ENTERPRISE × OBSERVABILITY × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Production-ready monitoring and metrics collection
 */

export interface Metric {
  name: string
  value: number
  tags?: Record<string, string>
  timestamp?: number
}

export interface LogEntry {
  level: 'info' | 'warn' | 'error' | 'debug'
  message: string
  context?: Record<string, any>
  timestamp?: number
}

export interface ErrorReport {
  error: Error
  context?: Record<string, any>
  userAgent?: string
  url?: string
  userId?: string
}

/**
 * Metrics collector
 */
class MetricsCollector {
  private metrics: Metric[] = []
  private flushInterval: number = 60000 // 1 minute
  private maxBatchSize: number = 100

  constructor() {
    // Auto-flush metrics periodically
    if (typeof window !== 'undefined') {
      setInterval(() => this.flush(), this.flushInterval)
      
      // Flush on page unload
      window.addEventListener('beforeunload', () => {
        this.flush()
      })
    }
  }

  /**
   * Record a metric
   */
  record(metric: Metric): void {
    this.metrics.push({
      ...metric,
      timestamp: metric.timestamp || Date.now(),
    })

    // Auto-flush if batch is full
    if (this.metrics.length >= this.maxBatchSize) {
      this.flush()
    }
  }

  /**
   * Record a counter metric
   */
  increment(name: string, value: number = 1, tags?: Record<string, string>): void {
    this.record({
      name,
      value,
      tags,
    })
  }

  /**
   * Record a gauge metric
   */
  gauge(name: string, value: number, tags?: Record<string, string>): void {
    this.record({
      name,
      value,
      tags: { type: 'gauge', ...tags },
    })
  }

  /**
   * Record a timing metric
   */
  timing(name: string, duration: number, tags?: Record<string, string>): void {
    this.record({
      name,
      value: duration,
      tags: { type: 'timing', ...tags },
    })
  }

  /**
   * Flush metrics to monitoring service
   */
  async flush(): Promise<void> {
    if (this.metrics.length === 0) return

    const metricsToSend = [...this.metrics]
    this.metrics = []

    // Send to monitoring service
    const monitoringUrl = process.env.NEXT_PUBLIC_MONITORING_URL
    
    if (monitoringUrl) {
      try {
        await fetch(monitoringUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            metrics: metricsToSend,
            service: 'abeone-web',
            environment: process.env.NODE_ENV,
          }),
          keepalive: true, // Ensure request completes even if page unloads
        })
      } catch (error) {
        console.error('Failed to send metrics:', error)
        // Re-add metrics to queue if send failed
        this.metrics.unshift(...metricsToSend)
      }
    } else if (process.env.NODE_ENV === 'development') {
      // Log metrics in development
      console.log('[Metrics]', metricsToSend)
    }
  }
}

/**
 * Logger
 */
class Logger {
  /**
   * Log an entry
   */
  log(entry: LogEntry): void {
    const logEntry = {
      ...entry,
      timestamp: entry.timestamp || Date.now(),
    }

    // Send to logging service
    const loggingUrl = process.env.NEXT_PUBLIC_LOGGING_URL
    
    if (loggingUrl) {
      fetch(loggingUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(logEntry),
        keepalive: true,
      }).catch(console.error)
    } else if (process.env.NODE_ENV === 'development') {
      // Console log in development
      const method = entry.level === 'error' ? 'error' : entry.level === 'warn' ? 'warn' : 'log'
      console[method](`[${entry.level.toUpperCase()}]`, entry.message, entry.context || '')
    }
  }

  info(message: string, context?: Record<string, any>): void {
    this.log({ level: 'info', message, context })
  }

  warn(message: string, context?: Record<string, any>): void {
    this.log({ level: 'warn', message, context })
  }

  error(message: string, context?: Record<string, any>): void {
    this.log({ level: 'error', message, context })
  }

  debug(message: string, context?: Record<string, any>): void {
    if (process.env.NODE_ENV === 'development') {
      this.log({ level: 'debug', message, context })
    }
  }
}

/**
 * Error tracker
 */
class ErrorTracker {
  /**
   * Track an error
   */
  track(report: ErrorReport): void {
    const errorReport = {
      ...report,
      error: {
        name: report.error.name,
        message: report.error.message,
        stack: report.error.stack,
      },
      timestamp: Date.now(),
      userAgent: report.userAgent || (typeof window !== 'undefined' ? window.navigator.userAgent : undefined),
      url: report.url || (typeof window !== 'undefined' ? window.location.href : undefined),
    }

    // Send to error tracking service
    const errorTrackingUrl = process.env.NEXT_PUBLIC_ERROR_TRACKING_URL
    
    if (errorTrackingUrl) {
      fetch(errorTrackingUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorReport),
        keepalive: true,
      }).catch(console.error)
    } else if (process.env.NODE_ENV === 'development') {
      console.error('[Error Tracking]', errorReport)
    }

    // Also log as error
    logger.error(`Error: ${report.error.message}`, {
      error: report.error.name,
      stack: report.error.stack,
      ...report.context,
    })
  }
}

/**
 * Performance monitor
 */
class PerformanceMonitor {
  /**
   * Measure function execution time
   */
  async measure<T>(name: string, fn: () => Promise<T>, tags?: Record<string, string>): Promise<T> {
    // SAFETY: Use global performance API, not class property
    const perf = typeof window !== 'undefined' ? window.performance : (typeof globalThis !== 'undefined' ? globalThis.performance : undefined)
    const start = perf?.now ? perf.now() : Date.now()
    
    try {
      const result = await fn()
      const duration = perf?.now ? perf.now() - start : Date.now() - start
      
      metrics.timing(name, duration, tags)
      
      return result
    } catch (error) {
      const duration = perf?.now ? perf.now() - start : Date.now() - start
      metrics.timing(`${name}.error`, duration, tags)
      throw error
    }
  }

  /**
   * Measure synchronous function execution time
   */
  measureSync<T>(name: string, fn: () => T, tags?: Record<string, string>): T {
    const perf = typeof window !== 'undefined' ? window.performance : (typeof globalThis !== 'undefined' ? globalThis.performance : undefined)
    const start = perf?.now ? perf.now() : Date.now()
    
    try {
      const result = fn()
      const duration = perf?.now ? perf.now() - start : Date.now() - start
      
      metrics.timing(name, duration, tags)
      
      return result
    } catch (error) {
      const duration = perf?.now ? perf.now() - start : Date.now() - start
      metrics.timing(`${name}.error`, duration, tags)
      throw error
    }
  }
}

// Singleton instances
export const metrics = new MetricsCollector()
export const logger = new Logger()
export const errorTracker = new ErrorTracker()
export const performance = new PerformanceMonitor()

/**
 * Initialize monitoring (call in app initialization)
 */
export function initMonitoring(): void {
  if (typeof window === 'undefined') return

  // Track page views
  metrics.increment('page.view', 1, {
    path: window.location.pathname,
  })

  // Track unhandled errors
  window.addEventListener('error', (event) => {
    errorTracker.track({
      error: event.error || new Error(event.message),
      context: {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      },
    })
  })

  // Track unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    errorTracker.track({
      error: event.reason instanceof Error ? event.reason : new Error(String(event.reason)),
      context: {
        type: 'unhandledrejection',
      },
    })
  })

  logger.info('Monitoring initialized')
}

