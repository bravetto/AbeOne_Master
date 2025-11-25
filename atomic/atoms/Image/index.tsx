/**
 * AbëONE Atomic Design System - Image
 * 
 * Pattern: ATOM × IMAGE × DESIGN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import * as React from 'react'
import NextImage from 'next/image'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const imageVariants = cva('', {
  variants: {
    variant: {
      default: '',
      developer: 'border border-aeBlue-500/20',
      creative: 'rounded-lg shadow-lg',
      enterprise: 'border border-aeMidnight-200',
    },
    size: {
      xs: 'w-8 h-8',
      sm: 'w-12 h-12',
      md: 'w-16 h-16',
      lg: 'w-24 h-24',
      xl: 'w-32 h-32',
      '2xl': 'w-48 h-48',
      full: 'w-full h-full',
    },
    rounded: {
      none: 'rounded-none',
      sm: 'rounded-sm',
      md: 'rounded-md',
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl',
      full: 'rounded-full',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'md',
    rounded: 'md',
  },
})

export interface ImageProps
  extends React.ImgHTMLAttributes<HTMLImageElement>,
    VariantProps<typeof imageVariants> {
  src: string
  alt: string
  useNextImage?: boolean
  width?: number
  height?: number
}

const Image = React.forwardRef<HTMLImageElement, ImageProps>(
  ({ className, variant, size, rounded, src, alt, useNextImage = false, width, height, ...props }, ref) => {
    if (useNextImage && width && height) {
      return (
        <NextImage
          src={src}
          alt={alt}
          width={width}
          height={height}
          className={cn(imageVariants({ variant, size, rounded }), className)}
          {...props}
        />
      )
    }
    
    return (
      <img
        src={src}
        alt={alt}
        className={cn(imageVariants({ variant, size, rounded }), className)}
        ref={ref}
        {...props}
      />
    )
  }
)
Image.displayName = 'Image'

export { Image, imageVariants }

