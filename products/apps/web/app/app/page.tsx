'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import CommandDeck from '@/components/CommandDeck'
import { getKernelStatus } from '@/lib/api'

export default function AppPage() {
  const [kernelStatus, setKernelStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadKernelStatus()
  }, [])

  const loadKernelStatus = async () => {
    try {
      const status = await getKernelStatus()
      console.log('Kernel status loaded:', status)
      setKernelStatus(status)
    } catch (error) {
      console.error('Failed to load kernel status:', error)
      // Set error status so user knows backend isn't connected
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
          <CommandDeck kernelStatus={kernelStatus} onRefresh={loadKernelStatus} />
        </main>
      </div>
    </div>
  )
}

