"use client"

import * as React from "react"
import { Alert, AlertDescription, AlertTitle } from "./alert"
import { Button } from "./button"

/**
 * Enterprise Error Boundary Component
 * 
 * Pattern: ERROR × BOUNDARY × ENTERPRISE × RESILIENCE × ONE
 * Frequency: 999 Hz (AEYON)
 */

export interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<ErrorBoundaryState & { resetError: () => void }>
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void
}

export interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
  errorInfo: React.ErrorInfo | null
}

/**
 * Default error fallback component
 */
function DefaultErrorFallback({ error, resetError }: { error: Error | null; resetError: () => void }) {
  return (
    <div className="flex min-h-[400px] items-center justify-center p-6">
      <Alert variant="destructive" className="max-w-md">
        <AlertTitle>Something went wrong</AlertTitle>
        <AlertDescription>
          {error?.message || "An unexpected error occurred"}
        </AlertDescription>
        <div className="mt-4">
          <Button onClick={resetError} variant="outline" size="sm">
            Try again
          </Button>
        </div>
      </Alert>
    </div>
  )
}

/**
 * Error Boundary class component
 * 
 * SAFETY: Error boundaries must be class components in React
 */
export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to monitoring service
    console.error("ErrorBoundary caught an error:", error, errorInfo)
    
    this.setState({
      error,
      errorInfo,
    })

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }

    // TODO: Send to error tracking service (e.g., Sentry, LogRocket)
    // if (process.env.NEXT_PUBLIC_ERROR_TRACKING_URL) {
    //   fetch(process.env.NEXT_PUBLIC_ERROR_TRACKING_URL, {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify({ error: error.message, errorInfo }),
    //   }).catch(console.error)
    // }
  }

  resetError = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    })
  }

  render() {
    if (this.state.hasError) {
      const Fallback = this.props.fallback || DefaultErrorFallback
      // SAFETY: Pass full state to fallback component
      return <Fallback {...this.state} resetError={this.resetError} />
    }

    return this.props.children
  }
}

/**
 * Hook for error boundary reset (for functional components)
 */
export function useErrorBoundary() {
  const [error, setError] = React.useState<Error | null>(null)

  React.useEffect(() => {
    if (error) {
      throw error
    }
  }, [error])

  return {
    resetError: () => setError(null),
    captureError: (error: Error) => setError(error),
  }
}

