"use client"

import * as React from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import { cn } from "@/lib/utils"

export interface KPICardProps {
  title: string
  value: string | number
  description?: string
  change?: number
  trend?: "up" | "down" | "neutral"
  progress?: number
  icon?: React.ReactNode
  className?: string
}

export function KPICard({
  title,
  value,
  description,
  change,
  trend,
  progress,
  icon,
  className,
}: KPICardProps) {
  const trendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus
  const TrendIcon = trendIcon
  const trendColor =
    trend === "up"
      ? "text-green-600 dark:text-green-400"
      : trend === "down"
        ? "text-red-600 dark:text-red-400"
        : "text-gray-600 dark:text-gray-400"

  return (
    <Card className={cn("relative overflow-hidden", className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon && <div className="h-4 w-4 text-muted-foreground">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <CardDescription className="mt-1 text-xs">{description}</CardDescription>
        )}
        {change !== undefined && (
          <div className="mt-2 flex items-center gap-1 text-xs">
            <TrendIcon className={cn("h-3 w-3", trendColor)} />
            <span className={trendColor}>
              {change > 0 ? "+" : ""}
              {change}%
            </span>
            <span className="text-muted-foreground">from last period</span>
          </div>
        )}
        {progress !== undefined && (
          <div className="mt-4">
            <Progress value={progress} className="h-2" />
          </div>
        )}
      </CardContent>
    </Card>
  )
}

