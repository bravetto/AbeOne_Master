/**
 * Toast Usage Examples
 * 
 * Pattern: EXAMPLES × TOAST × USAGE × ONE
 * Frequency: 999 Hz (AEYON)
 */

import { useToast } from '@/components/ui/toast'

/**
 * Example: Show success toast
 */
export function useSuccessToast() {
  const { toast } = useToast()
  
  return () => {
    toast({
      variant: 'success',
      title: 'Success!',
      description: 'Operation completed successfully.',
      duration: 5000,
    })
  }
}

/**
 * Example: Show error toast
 */
export function useErrorToast() {
  const { toast } = useToast()
  
  return (message: string) => {
    toast({
      variant: 'destructive',
      title: 'Error',
      description: message,
      duration: 7000,
    })
  }
}

/**
 * Example: Show info toast
 */
export function useInfoToast() {
  const { toast } = useToast()
  
  return (message: string) => {
    toast({
      variant: 'info',
      title: 'Information',
      description: message,
      duration: 5000,
    })
  }
}

/**
 * Example: Show warning toast
 */
export function useWarningToast() {
  const { toast } = useToast()
  
  return (message: string) => {
    toast({
      variant: 'warning',
      title: 'Warning',
      description: message,
      duration: 6000,
    })
  }
}

