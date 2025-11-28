'use client'

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'

/**
 * Enterprise Toast Notification System
 * 
 * Pattern: TOAST × ENTERPRISE × NOTIFICATION × ONE
 * Frequency: 999 Hz (AEYON)
 */

const toastVariants = cva(
  'group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all',
  {
    variants: {
      variant: {
        default: 'border-lux-200 bg-background text-foreground',
        success: 'border-peace-500 bg-peace-50 text-peace-900 dark:bg-peace-950 dark:text-peace-400',
        destructive: 'border-heart-500 bg-heart-50 text-heart-900 dark:bg-heart-950 dark:text-heart-400',
        warning: 'border-warm-500 bg-warm-50 text-warm-900 dark:bg-warm-950 dark:text-warm-400',
        info: 'border-lux-500 bg-lux-50 text-lux-900 dark:bg-lux-950 dark:text-lux-400',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

const iconMap = {
  default: Info,
  success: CheckCircle,
  destructive: AlertCircle,
  warning: AlertTriangle,
  info: Info,
}

export interface ToastProps extends VariantProps<typeof toastVariants> {
  id: string
  title?: string
  description?: string
  action?: React.ReactNode
  onClose?: () => void
  duration?: number
}

export function Toast({
  id,
  variant,
  title,
  description,
  action,
  onClose,
  duration = 5000,
}: ToastProps) {
  const Icon = variant ? iconMap[variant] : iconMap.default

  React.useEffect(() => {
    if (duration > 0 && onClose) {
      const timer = setTimeout(() => {
        onClose()
      }, duration)

      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  return (
    <div className={cn(toastVariants({ variant }))} role="alert">
      <div className="flex items-start gap-3 flex-1">
        <Icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
        <div className="flex-1 space-y-1">
          {title && (
            <div className="text-sm font-semibold">{title}</div>
          )}
          {description && (
            <div className="text-sm opacity-90">{description}</div>
          )}
        </div>
      </div>
      {action && <div className="flex-shrink-0">{action}</div>}
      {onClose && (
        <button
          onClick={onClose}
          className="absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100"
        >
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </button>
      )}
    </div>
  )
}

/**
 * Toast Context and Provider
 */
interface ToastContextValue {
  toasts: ToastProps[]
  toast: (props: Omit<ToastProps, 'id'>) => string
  dismiss: (id: string) => void
}

const ToastContext = React.createContext<ToastContextValue | undefined>(undefined)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastProps[]>([])

  const toast = React.useCallback((props: Omit<ToastProps, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 9)
    const newToast: ToastProps = { ...props, id }
    
    setToasts((prev) => [...prev, newToast])
    
    return id
  }, [])

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toasts, toast, dismiss }}>
      {children}
      <ToastContainer toasts={toasts} onDismiss={dismiss} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = React.useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return context
}

/**
 * Toast Container
 */
function ToastContainer({
  toasts,
  onDismiss,
}: {
  toasts: ToastProps[]
  onDismiss: (id: string) => void
}) {
  if (toasts.length === 0) return null

  return (
    <div
      className="fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]"
      aria-live="polite"
      aria-atomic="true"
    >
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          {...toast}
          onClose={() => onDismiss(toast.id)}
        />
      ))}
    </div>
  )
}

