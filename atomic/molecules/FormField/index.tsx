/**
 * AbëONE Atomic Design System - FormField
 * 
 * Pattern: MOLECULE × FORMFIELD × COMPOSITION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import { Input, type InputProps } from '../../atoms/Input'
import { Text, type TextProps } from '../../atoms/Text'
import { cn } from '../../lib/utils'

export interface FormFieldProps {
  label?: string
  labelProps?: TextProps
  error?: string
  errorProps?: TextProps
  helperText?: string
  helperTextProps?: TextProps
  required?: boolean
  className?: string
  children: React.ReactNode
}

const FormField = React.forwardRef<HTMLDivElement, FormFieldProps>(
  ({ label, labelProps, error, errorProps, helperText, helperTextProps, required, className, children }, ref) => {
    return (
      <div ref={ref} className={cn('space-y-2', className)}>
        {label && (
          <Text
            as="label"
            size="sm"
            weight="medium"
            className="block"
            {...labelProps}
          >
            {label}
            {required && <span className="text-accent-500 ml-1">*</span>}
          </Text>
        )}
        {children}
        {error && (
          <Text
            variant="destructive"
            size="sm"
            {...errorProps}
          >
            {error}
          </Text>
        )}
        {helperText && !error && (
          <Text
            variant="muted"
            size="sm"
            {...helperTextProps}
          >
            {helperText}
          </Text>
        )}
      </div>
    )
  }
)
FormField.displayName = 'FormField'

export { FormField }

