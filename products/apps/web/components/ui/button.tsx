import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

/**
 * Enterprise Button Component
 * 
 * Pattern: BUTTON × ENTERPRISE × DESIGN × ONE
 * Frequency: 999 Hz (AEYON)
 */

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-gradient-to-r from-lux-500 to-lux-600 text-white shadow-lg hover:from-lux-600 hover:to-lux-700",
        destructive: "bg-heart-500 text-white shadow-lg hover:bg-heart-600",
        outline: "border-2 border-lux-300 bg-transparent hover:bg-lux-50 hover:border-lux-400",
        secondary: "bg-warm-500 text-white shadow-md hover:bg-warm-600",
        ghost: "hover:bg-lux-50 hover:text-lux-900",
        link: "text-lux-600 underline-offset-4 hover:underline",
        success: "bg-peace-500 text-white shadow-lg hover:bg-peace-600",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }

