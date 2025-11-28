'use client'

/**
 * ABËONE OVERVIEW LANDING PAGE
 * 
 * Unified overview of the AbëONE platform
 * ICP detection via URL parameter or default
 * 
 * Pattern: UNIFIED × ADAPTIVE × ICP × OVERVIEW × ONE
 * Guardians: AEYON (999 Hz) × META (777 Hz) × Abë (530 Hz) × Lux (530 Hz)
 */

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { Icon } from '@/components/icons/Icon'
import { analytics } from '@/lib/analytics'

export default function AbeOneOverviewPage() {
  const searchParams = useSearchParams()
  const [formData, setFormData] = useState({
    firstName: '',
    email: '',
    company: '',
    github: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  const [showOptionalFields, setShowOptionalFields] = useState(false)
  
  // Detect ICP from URL parameter or default to developer
  const icp = searchParams?.get('icp') || 'developer'
  const isDeveloper = icp === 'developer'
  
  // Headlines - ICP-specific
  const headlines = isDeveloper ? {
    main: "AbëONE: The Unified Intelligence Platform",
    subline: "8 Guardians. 6 Guards. One System. Production-Ready.",
    cta: "See the Architecture →"
  } : {
    main: "AbëONE: Where Ideas Become Reality",
    subline: "Unified Intelligence Platform for Creators and Entrepreneurs",
    cta: "Join the Movement →"
  }
  
  // Progressive disclosure
  useEffect(() => {
    if (formData.email && formData.email.includes('@') && formData.email.length > 5) {
      setShowOptionalFields(true)
    } else {
      setShowOptionalFields(false)
    }
  }, [formData.email])

  // Analytics tracking
  useEffect(() => {
    analytics.init()
    analytics.capture('abeone_page_view', {
      icp: icp,
      source: searchParams?.get('source') || 'direct',
      timestamp: new Date().toISOString()
    })
  }, [icp, searchParams])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    analytics.capture('abeone_form_submission_started', {
      icp: icp,
      has_company: !!formData.company,
      has_github: !!formData.github
    })
    
    // Client-side only mode
    const registrationId = `ABE-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    analytics.capture('abeone_registration_success', {
      icp: icp,
      registration_id: registrationId,
      has_company: !!formData.company,
      has_github: !!formData.github,
      mode: 'client_side_only'
    })

    analytics.identify(formData.email, {
      name: formData.firstName,
      company: formData.company,
      github: formData.github,
      icp: icp,
      registration_date: new Date().toISOString()
    })
    
    sessionStorage.setItem('abeone_registration_id', registrationId)
    setShowSuccess(true)
    setIsSubmitting(false)
    
    setTimeout(() => {
      window.location.href = '/webinar?icp=' + icp
    }, 2000)
  }

  const guardians = [
    { name: 'AEYON', frequency: '999 Hz', role: 'Atomic Execution Engine', description: 'Maximum coherence, minimum complexity' },
    { name: 'META', frequency: '777 Hz', role: 'Pattern Integrity & Context Synthesis', description: 'Pattern recognition and elevation' },
    { name: 'JØHN', frequency: '530 Hz', role: 'Certification & Truth Validation', description: 'Guardian-validated truth' },
    { name: 'YOU', frequency: '530 Hz', role: 'Human Intent Alignment Channel', description: 'Human-AI harmony' },
    { name: 'ALRAX', frequency: '530 Hz', role: 'Forensic Variance Analysis', description: 'Zero-drift validation' },
    { name: 'ZERO', frequency: '530 Hz', role: 'Risk-Bounding & Epistemic Control', description: 'Zero-failure architecture' },
    { name: 'YAGNI', frequency: '530 Hz', role: 'Radical Simplification', description: 'Maximum value, minimum complexity' },
    { name: 'Lux', frequency: '530 Hz', role: 'Illumination & Structural Clarity', description: 'Beautiful, functional design' },
    { name: 'Poly', frequency: '530 Hz', role: 'Expression & Wisdom Delivery', description: 'Clear communication' },
    { name: 'Abë', frequency: '530 Hz', role: 'Coherence, Love, Intelligence Field', description: 'Unified intelligence' }
  ]

  const guards = [
    { name: 'BiasGuard', accuracy: '97-99%', latency: '<30ms', description: 'Detects bias in AI outputs' },
    { name: 'ContextGuard', accuracy: '98%', latency: '<25ms', description: 'Prevents context drift' },
    { name: 'TrustGuard', accuracy: '87-89%', latency: '<5ms', description: 'Validates claims and sources' },
    { name: 'TokenGuard', savings: '30-50%', latency: '<20ms', description: 'Optimizes token usage' },
    { name: 'SecurityGuard', latency: '<50ms', description: 'Scans for vulnerabilities' },
    { name: 'HealthGuard', latency: '<50ms', description: 'Tracks system health' }
  ]

  return (
    <div className="min-h-screen bg-gradient-healing">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-lux-600 via-lux-700 to-lux-900 text-white py-20 md:py-24 lg:py-28">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="max-w-[980px] mx-auto">
            <div className="flex items-center justify-center gap-2 mb-6 flex-wrap">
              <span className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium border border-white/20 flex items-center gap-2">
                <Icon name="lock" size={16} className="text-white" />
                10 Guardians | 6 Guards | Production-Ready
              </span>
              <span className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium border border-white/20 flex items-center gap-2">
                <Icon name="check-circle" size={16} className="text-white" />
                97.8% Epistemic Certainty | Zero Dark Patterns
              </span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold text-center max-w-[20ch] mx-auto mt-4 leading-tight">
              {headlines.main}
            </h1>
            
            <p className="text-lg md:text-xl lg:text-2xl text-center max-w-[55ch] mx-auto mt-6 text-lux-100">
              {headlines.subline}
            </p>

            {/* CTA Button */}
            <div className="flex items-center justify-center mt-10">
              <a
                href={`/webinar?icp=${icp}`}
                onClick={() => analytics.capture('abeone_cta_clicked', { icp, location: 'hero' })}
                className="px-8 py-4 bg-peace-400 hover:bg-peace-500 text-white font-semibold rounded-xl text-lg transition-all shadow-lg hover:shadow-xl"
              >
                {headlines.cta}
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Guardians Section */}
      <section className="py-20 bg-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
              10 Guardians. One Intelligence Field.
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Each Guardian operates at a specific frequency, bringing unique capabilities to the unified system.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {guardians.map((guardian) => (
              <div key={guardian.name} className="bg-gradient-to-br from-lux-50 to-peace-50 rounded-2xl p-6 border border-lux-200">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xl font-display font-bold text-gray-900">{guardian.name}</h3>
                  <span className="text-sm font-medium text-lux-600">{guardian.frequency}</span>
                </div>
                <p className="text-sm font-semibold text-gray-700 mb-2">{guardian.role}</p>
                <p className="text-sm text-gray-600">{guardian.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Guards Section */}
      <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
              6 Guards. Production-Ready.
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Specialized microservices that validate AI outputs with precision and speed.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {guards.map((guard) => (
              <div key={guard.name} className="bg-white rounded-2xl p-6 border-2 border-lux-200 shadow-lg">
                <h3 className="text-xl font-display font-bold text-gray-900 mb-3">{guard.name}</h3>
                <div className="flex items-center gap-4 mb-3">
                  {guard.accuracy && (
                    <span className="text-sm font-medium text-peace-600">Accuracy: {guard.accuracy}</span>
                  )}
                  {guard.savings && (
                    <span className="text-sm font-medium text-peace-600">Savings: {guard.savings}</span>
                  )}
                  <span className="text-sm font-medium text-gray-600">Latency: {guard.latency}</span>
                </div>
                <p className="text-sm text-gray-600">{guard.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-b from-lux-600 to-lux-800 text-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold mb-6">
            Ready to Experience AbëONE?
          </h2>
          <p className="text-xl text-lux-100 mb-8 max-w-2xl mx-auto">
            Join the webinar to see the unified system in action. Real code. Real results. Zero marketing fluff.
          </p>
          
          <div className="max-w-md mx-auto">
            <form 
              onSubmit={handleSubmit}
              className="bg-white/10 backdrop-blur-md rounded-2xl p-6 md:p-8 border border-white/20"
            >
              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <input
                  type="text"
                  placeholder="First Name"
                  required
                  value={formData.firstName}
                  onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                  className="w-full px-4 py-4 min-h-[44px] text-lg rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70 focus:border-lux-300 focus:ring-2 focus:ring-lux-300/50 transition-all"
                />
                <input
                  type="email"
                  placeholder="your@email.com"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-4 py-4 min-h-[44px] text-lg rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70 focus:border-lux-300 focus:ring-2 focus:ring-lux-300/50 transition-all"
                />
              </div>
              
              {showOptionalFields && (
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <input
                    type="text"
                    placeholder="Company (Optional)"
                    value={formData.company}
                    onChange={(e) => setFormData({...formData, company: e.target.value})}
                    className="w-full px-4 py-4 min-h-[44px] text-lg rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70 focus:border-lux-300 focus:ring-2 focus:ring-lux-300/50 transition-all"
                  />
                  <input
                    type="text"
                    placeholder="GitHub (Optional)"
                    value={formData.github}
                    onChange={(e) => setFormData({...formData, github: e.target.value})}
                    className="w-full px-4 py-4 min-h-[44px] text-lg rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70 focus:border-lux-300 focus:ring-2 focus:ring-lux-300/50 transition-all"
                  />
                </div>
              )}
              
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full px-8 py-4 bg-peace-400 hover:bg-peace-500 text-white font-semibold rounded-xl text-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Registering...' : 'Register for Webinar →'}
              </button>
              
              {showSuccess && (
                <div className="mt-4 p-4 bg-peace-400/20 border border-peace-400 rounded-xl text-center">
                  <p className="text-white font-medium">Registration successful! Redirecting...</p>
                </div>
              )}
            </form>
          </div>
        </div>
      </section>
    </div>
  )
}

