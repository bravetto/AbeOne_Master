'use client'

/**
 * LEAD MAGNET DELIVERY LANDING PAGE
 * 
 * Lead magnet delivery system with watch time verification
 * ICP detection via URL parameter or default
 * 
 * Pattern: UNIFIED × ADAPTIVE × ICP × DELIVERY × ONE
 * Guardians: AEYON (999 Hz) × META (777 Hz) × Abë (530 Hz) × Lux (530 Hz)
 */

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { Icon } from '@/components/icons/Icon'
import { analytics } from '@/lib/analytics'

export default function LeadMagnetsPage() {
  const searchParams = useSearchParams()
  const [watchTime, setWatchTime] = useState(0)
  const [watchThreshold] = useState(80) // 80% watch time required
  const [isVerified, setIsVerified] = useState(false)
  
  // Detect ICP from URL parameter or default to developer
  const icp = searchParams?.get('icp') || 'developer'
  const isDeveloper = icp === 'developer'
  
  // Lead magnets - ICP-specific
  const leadMagnets = isDeveloper ? [
    {
      title: '10 Tips for Better AI Code',
      value: '$97',
      description: 'Practical tips for writing better AI-generated code',
      downloadUrl: '/lead-magnets/10-tips-better-ai-code'
    },
    {
      title: 'Real System Deep-Dive',
      value: '$147',
      description: 'Complete technical deep-dive into the AiGuardian architecture',
      downloadUrl: '/lead-magnets/deep-dive'
    },
    {
      title: 'Community Access',
      value: '$197',
      description: 'Join the AiGuardian developer community',
      downloadUrl: '/lead-magnets/community-access'
    },
    {
      title: 'Creator Toolkit',
      value: '$97',
      description: 'Tools and resources for AI creators',
      downloadUrl: '/lead-magnets/creator-toolkit'
    },
    {
      title: 'Early Access Program',
      value: '$59',
      description: 'Get early access to new features and Guardians',
      downloadUrl: '/lead-magnets/early-access'
    },
    {
      title: 'FREE Music Video Generator',
      value: '$299',
      description: 'Complete music video generator system',
      downloadUrl: '/lead-magnets/music-generator'
    }
  ] : [
    {
      title: '10 Tips for Better AI Code',
      value: '$97',
      description: 'Practical tips for writing better AI-generated code',
      downloadUrl: '/lead-magnets/10-tips-better-ai-code'
    },
    {
      title: 'Real System Deep-Dive',
      value: '$147',
      description: 'Complete technical deep-dive into the AiGuardian architecture',
      downloadUrl: '/lead-magnets/deep-dive'
    },
    {
      title: 'Community Access',
      value: '$197',
      description: 'Join the AiGuardian creator community',
      downloadUrl: '/lead-magnets/community-access'
    },
    {
      title: 'Creator Toolkit',
      value: '$97',
      description: 'Tools and resources for AI creators',
      downloadUrl: '/lead-magnets/creator-toolkit'
    },
    {
      title: 'Early Access Program',
      value: '$59',
      description: 'Get early access to new features and Guardians',
      downloadUrl: '/lead-magnets/early-access'
    },
    {
      title: 'FREE Music Video Generator',
      value: '$299',
      description: 'Complete music video generator system',
      downloadUrl: '/lead-magnets/music-generator'
    }
  ]

  const totalValue = leadMagnets.reduce((sum, magnet) => {
    const value = parseInt(magnet.value.replace('$', ''))
    return sum + value
  }, 0)

  // Analytics tracking
  useEffect(() => {
    analytics.init()
    analytics.capture('lead_magnets_page_view', {
      icp: icp,
      source: searchParams?.get('source') || 'direct',
      timestamp: new Date().toISOString()
    })
  }, [icp, searchParams])

  // Simulate watch time tracking (in production, this would come from webinar platform API)
  useEffect(() => {
    const storedWatchTime = sessionStorage.getItem('webinar_watch_time')
    if (storedWatchTime) {
      const parsed = parseInt(storedWatchTime)
      setWatchTime(parsed)
      if (parsed >= watchThreshold) {
        setIsVerified(true)
      }
    }
  }, [watchThreshold])

  const handleDownload = (magnet: typeof leadMagnets[0]) => {
    analytics.capture('lead_magnet_downloaded', {
      icp: icp,
      magnet: magnet.title,
      value: magnet.value,
      watch_time: watchTime,
      verified: isVerified
    })
    
    // In production, this would trigger actual download
    window.open(magnet.downloadUrl, '_blank')
  }

  return (
    <div className="min-h-screen bg-gradient-healing">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-lux-600 via-lux-700 to-lux-900 text-white py-20 md:py-24 lg:py-28">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="max-w-[980px] mx-auto text-center">
            <div className="flex items-center justify-center gap-2 mb-6 flex-wrap">
              <span className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium border border-white/20 flex items-center gap-2">
                <Icon name="check-circle" size={16} className="text-white" />
                Watch 80%+ of Webinar to Unlock
              </span>
              <span className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium border border-white/20 flex items-center gap-2">
                <Icon name="gift" size={16} className="text-white" />
                ${totalValue} Total Value
              </span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold max-w-[20ch] mx-auto mt-4 leading-tight">
              Your Lead Magnets Are Ready
            </h1>
            
            <p className="text-lg md:text-xl lg:text-2xl max-w-[55ch] mx-auto mt-6 text-lux-100">
              Watch 80%+ of the webinar to unlock all {leadMagnets.length} lead magnets. Zero dark patterns. Just honest value.
            </p>

            {/* Watch Time Progress */}
            <div className="mt-10 max-w-md mx-auto">
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-lux-100">Watch Time</span>
                  <span className="text-sm font-medium text-white">{watchTime}% / {watchThreshold}%</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-4 mb-4">
                  <div 
                    className={`h-4 rounded-full transition-all ${
                      watchTime >= watchThreshold ? 'bg-peace-400' : 'bg-lux-300'
                    }`}
                    style={{ width: `${Math.min(watchTime, 100)}%` }}
                  />
                </div>
                {isVerified ? (
                  <div className="flex items-center justify-center gap-2 text-peace-400">
                    <Icon name="check-circle" size={20} />
                    <span className="font-semibold">Verified! All lead magnets unlocked.</span>
                  </div>
                ) : (
                  <div className="text-center">
                    <p className="text-sm text-lux-200 mb-2">
                      {watchThreshold - watchTime}% more to unlock all lead magnets
                    </p>
                    <a
                      href={`/webinar?icp=${icp}`}
                      className="text-peace-400 hover:text-peace-300 font-semibold underline"
                    >
                      Continue Watching →
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Lead Magnets Grid */}
      <section className="py-20 bg-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
              All {leadMagnets.length} Lead Magnets
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Total value: ${totalValue}. Available after watching 80%+ of the webinar.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {leadMagnets.map((magnet, index) => (
              <div 
                key={index}
                className={`bg-gradient-to-br from-lux-50 to-peace-50 rounded-2xl p-6 border-2 ${
                  isVerified ? 'border-peace-400' : 'border-lux-200 opacity-60'
                } relative`}
              >
                {!isVerified && (
                  <div className="absolute inset-0 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10">
                    <div className="text-center">
                      <Icon name="lock" size={48} className="text-gray-400 mx-auto mb-2" />
                      <p className="text-sm font-semibold text-gray-600">Watch 80%+ to unlock</p>
                    </div>
                  </div>
                )}
                
                <div className="relative">
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-3 py-1 bg-peace-400 text-white text-xs font-semibold rounded-full">
                      {magnet.value} Value
                    </span>
                    {isVerified && (
                      <Icon name="check-circle" size={24} className="text-peace-400" />
                    )}
                  </div>
                  
                  <h3 className="text-xl font-display font-bold text-gray-900 mb-2">
                    {magnet.title}
                  </h3>
                  
                  <p className="text-sm text-gray-600 mb-4">
                    {magnet.description}
                  </p>
                  
                  {isVerified && (
                    <button
                      onClick={() => handleDownload(magnet)}
                      className="w-full px-4 py-2 bg-peace-400 hover:bg-peace-500 text-white font-semibold rounded-xl transition-all"
                    >
                      Download →
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Simple. Transparent. Zero dark patterns.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl p-6 border-2 border-lux-200 text-center">
              <div className="w-16 h-16 bg-peace-400 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">Register</h3>
              <p className="text-gray-600">Register for the webinar. No payment required.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 border-2 border-lux-200 text-center">
              <div className="w-16 h-16 bg-peace-400 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">Watch</h3>
              <p className="text-gray-600">Watch 80%+ of the webinar. We track watch time automatically.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 border-2 border-peace-400 text-center">
              <div className="w-16 h-16 bg-peace-400 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">Unlock</h3>
              <p className="text-gray-600">All lead magnets automatically unlocked. Download instantly.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isVerified && (
        <section className="py-20 bg-gradient-to-b from-lux-600 to-lux-800 text-white">
          <div className="max-w-screen-xl mx-auto px-4 lg:px-6 text-center">
            <h2 className="text-3xl md:text-4xl font-display font-bold mb-6">
              Ready to Unlock Your Lead Magnets?
            </h2>
            <p className="text-xl text-lux-100 mb-8 max-w-2xl mx-auto">
              Register for the webinar and watch 80%+ to unlock all {leadMagnets.length} lead magnets (${totalValue} value).
            </p>
            
            <a
              href={`/webinar?icp=${icp}`}
              onClick={() => analytics.capture('lead_magnets_cta_clicked', { icp, location: 'cta_section' })}
              className="inline-block px-8 py-4 bg-peace-400 hover:bg-peace-500 text-white font-semibold rounded-xl text-lg transition-all shadow-lg hover:shadow-xl"
            >
              Register for Webinar →
            </a>
          </div>
        </section>
      )}
    </div>
  )
}

