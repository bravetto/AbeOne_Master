'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import { getKernelStatus } from '@/lib/api'

export default function AgentsPage() {
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
                Your Agents
              </h2>
              <p className="text-gray-600 leading-relaxed">
                The beings who work alongside you. The helpers who carry your vision forward.
              </p>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
              <div className="text-center py-12 space-y-4">
                <span className="text-6xl">🤖</span>
                <h3 className="text-xl font-display font-semibold text-gray-800">
                  Coming Soon
                </h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  This space is being prepared for you. Your agents will gather here, 
                  ready to help bring your vision into being.
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

