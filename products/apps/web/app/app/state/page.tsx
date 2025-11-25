'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import { getKernelStatus } from '@/lib/api'

export default function StatePage() {
  const [kernelStatus, setKernelStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadKernelStatus()
  }, [])

  const loadKernelStatus = async () => {
    try {
      const status = await getKernelStatus()
      setKernelStatus(status)
    } catch (error) {
      setKernelStatus({ 
        initialized: false, 
        error: error instanceof Error ? error.message : 'Backend not accessible'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen gradient-healing">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar kernelStatus={kernelStatus} />
        <main className="flex-1 overflow-auto p-6 md:p-8">
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
              <h2 className="text-3xl font-display font-bold text-gray-800 mb-2">
                System State
              </h2>
              <p className="text-gray-600 leading-relaxed">
                The current state of everything. Where things are. What&apos;s happening. 
                The pulse of your space.
              </p>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
              <div className="text-center py-12 space-y-4">
                <span className="text-6xl">📊</span>
                <h3 className="text-xl font-display font-semibold text-gray-800">
                  Coming Soon
                </h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  This space is being prepared for you. Your system state will be visible here, 
                  showing you the heartbeat of everything that&apos;s moving.
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

