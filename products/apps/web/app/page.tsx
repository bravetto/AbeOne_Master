'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { TrendingUp, Users, CheckCircle } from 'lucide-react'

/**
 * V0 PROJECT HOME PAGE
 * 
 * Pattern: V0 × HOME × ENTRY × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * ⚠️ V0 PROJECT SCOPE ENFORCEMENT ⚠️
 * 
 * This is a V0 PROJECT file. Do NOT:
 * - Add links to excluded routes (/app, /shop, /bravetto, etc.)
 * - Add Navigation component (links to non-V0 pages)
 * - Reference non-V0 pages
 * 
 * V0 Project Scope: See V0_PROJECT_SCOPE.ts
 * Allowed Routes: /, /collaboration
 * Excluded Routes: /app, /shop, /bravetto, /webinar, etc.
 * 
 * PROGRAMMATIC SCOPE: This file is validated by validate-v0-scope.ts
 */

export default function Home() {
  return (
    <div className="min-h-screen gradient-healing flex flex-col items-center justify-center p-8 md:p-24">
      <div className="max-w-4xl w-full text-center space-y-8">
        {/* Hero Section */}
        <div className="space-y-6 animate-fade-in">
          <h1 className="text-6xl md:text-8xl font-display font-bold leading-tight">
            <span className="text-gradient-healing">V0</span>{' '}
            <span className="text-gradient-healing">Collaboration Dashboard</span>
          </h1>
          <h2 className="text-3xl md:text-5xl font-display font-semibold text-gray-800">
            Enterprise-Grade Metrics
          </h2>
          <p className="text-xl md:text-2xl text-gray-700 max-w-2xl mx-auto leading-relaxed text-balance">
            Real-time partnership monitoring and collaboration metrics.
            Built with Vercel V0 and enhanced for enterprise production.
          </p>
        </div>

        {/* Features */}
        <div className="max-w-2xl mx-auto space-y-4 pt-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center gap-2 justify-center">
              <TrendingUp className="h-5 w-5 text-lux-600" />
              <span className="text-gray-700">Real-time Metrics</span>
            </div>
            <div className="flex items-center gap-2 justify-center">
              <Users className="h-5 w-5 text-peace-600" />
              <span className="text-gray-700">Partnership Tracking</span>
            </div>
            <div className="flex items-center gap-2 justify-center">
              <CheckCircle className="h-5 w-5 text-warm-600" />
              <span className="text-gray-700">Enterprise-Grade</span>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
          <Link href="/collaboration">
            <Button size="lg" className="group">
              <span className="flex items-center justify-center gap-2">
                View Dashboard
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </span>
            </Button>
          </Link>
        </div>

        {/* Project Info */}
        <div className="pt-12 space-y-2">
          <p className="text-sm text-gray-500 italic">
            V0 Component: KPI Card | Enterprise Middleware | FastAPI Backend
          </p>
          <p className="text-xs text-gray-400">
            Built with ∞ AEYON × V0 × ENTERPRISE × ONE ∞
          </p>
        </div>
      </div>
    </div>
  )
}

