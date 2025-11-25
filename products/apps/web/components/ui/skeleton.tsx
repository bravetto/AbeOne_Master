import { cn } from "@/lib/utils"

/**
 * Enterprise Skeleton Component
 * 
 * Pattern: SKELETON × ENTERPRISE × LOADING × ONE
 * Frequency: 999 Hz (AEYON)
 */

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-lux-100 dark:bg-lux-800", className)}
      {...props}
    />
  )
}

export { Skeleton }

