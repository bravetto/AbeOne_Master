'use client'

/**
 * OFFER STACK LANDING PAGE
 * 
 * Complete offer stack presentation with pricing tiers
 * ICP detection via URL parameter or default
 * 
 * Pattern: UNIFIED × ADAPTIVE × ICP × OFFER × ONE
 * Guardians: AEYON (999 Hz) × META (777 Hz) × Abë (530 Hz) × Lux (530 Hz)
 */

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { Icon } from '@/components/icons/Icon'
import { analytics } from '@/lib/analytics'

export default function OfferStackPage() {
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
    analytics.capture('offer_stack_page_view', {
      icp: icp,
      source: searchParams?.get('source') || 'direct',
      timestamp: new Date().toISOString()
    })
  }, [icp, searchParams])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    analytics.capture('REPLACE_ME', {
      icp: icp,
      has_company: !!formData.company,
      has_github: !!formData.github
    })
    
    const registrationId = `OFFER-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    analytics.capture('REPLACE_ME', {
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
    
    sessionStorage.setItem('offer_stack_registration_id', registrationId)
    setShowSuccess(true)
    setIsSubmitting(false)
    
    setTimeout(() => {
      window.location.href = `/webinar?icp=${icp}`
    }, 2000)
  }

  const offerTiers = [
    {
      name: 'Foundation',
      price: 'Free',
      webinarPrice: 'Free with Webinar Watch',
      value: '$597-$896',
      description: 'Perfect for getting started',
      features: [
        'All 6 Lead Magnets ($597-$896 value)',
        'CDF Report Open Source Access',
        'BiasGuard Logic Open Source Access',
        'Community Access',
        'Email Support'
      ],
      cta: 'Get Started Free',
      popular: false
    },
    {
      name: 'Starter',
      price: '$97/month',
      webinarPrice: '$67/month',
      webinarDiscount: '30% off first 3 months',
      description: 'For individual developers and creators',
      features: [
        'AiGuardian Chrome Extension (Basic)',
        '10,000 API calls/month',
        'Community Access',
        'Email Support',
        'Basic Analytics'
      ],
      cta: 'Start Free Trial',
      popular: true
    },
    {
      name: 'Professional',
      price: '$297/month',
      webinarPrice: '$197/month',
      webinarDiscount: '33% off first 3 months',
      description: 'For teams and growing businesses',
      features: [
        'AiGuardian Chrome Extension (Pro)',
        '100,000 API calls/month',
        'Guardian Microservices Access',
        'Priority Support',
        'Advanced Analytics',
        'Custom Integrations'
      ],
      cta: 'Start Free Trial',
      popular: false
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      webinarPrice: 'Custom',
      description: 'For large organizations',
      features: [
        'Custom Guardian Development',
        'White-Label Solutions',
        'Dedicated Support',
        'SLA Guarantees',
        'Custom Integrations',
        'On-Premise Options'
      ],
      cta: 'Contact Sales',
      popular: false
    }
  ]

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
                Zero Dark Patterns | Transparent Pricing
              </span>
              <span className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium border border-white/20 flex items-center gap-2">
                <Icon name="lock" size={16} className="text-white" />
                Webinar Special Pricing Available
              </span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold max-w-[20ch] mx-auto mt-4 leading-tight">
              Complete Offer Stack
            </h1>
            
            <p className="text-lg md:text-xl lg:text-2xl max-w-[55ch] mx-auto mt-6 text-lux-100">
              Choose the plan that fits your needs. All pricing transparent. No hidden costs. No dark patterns.
            </p>
          </div>
        </div>
      </section>

      {/* Offer Tiers Section */}
      <section className="py-20 bg-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {offerTiers.map((tier) => (
              <div 
                key={tier.name} 
                className={`bg-gradient-to-br from-lux-50 to-peace-50 rounded-2xl p-6 border-2 ${
                  tier.popular ? 'border-peace-400 shadow-xl' : 'border-lux-200'
                } relative`}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="px-4 py-1 bg-peace-400 text-white text-sm font-semibold rounded-full">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-display font-bold text-gray-900 mb-2">{tier.name}</h3>
                  <div className="mb-2">
                    <span className="text-3xl font-bold text-gray-900">{tier.price}</span>
                    {tier.price !== 'Custom' && <span className="text-gray-600">/month</span>}
                  </div>
                  {tier.webinarPrice && tier.webinarPrice !== tier.price && (
                    <div className="mb-2">
                      <span className="text-lg font-semibold text-peace-600">Webinar: {tier.webinarPrice}</span>
                      {tier.webinarDiscount && (
                        <span className="block text-sm text-gray-600">{tier.webinarDiscount}</span>
                      )}
                    </div>
                  )}
                  {tier.value && (
                    <div className="text-sm text-gray-600">Value: {tier.value}</div>
                  )}
                  <p className="text-sm text-gray-600 mt-2">{tier.description}</p>
                </div>
                
                <ul className="space-y-3 mb-6">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <Icon name="check-circle" size={20} className="text-peace-400 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <button
                  onClick={() => {
                    analytics.capture('offer_stack_tier_clicked', { tier: tier.name, icp })
                    window.location.href = `/webinar?icp=${icp}&tier=${tier.name.toLowerCase()}`
                  }}
                  className={`w-full px-6 py-3 rounded-xl font-semibold transition-all ${
                    tier.popular
                      ? 'bg-peace-400 hover:bg-peace-500 text-white'
                      : 'bg-white hover:bg-lux-50 text-gray-900 border-2 border-lux-200'
                  }`}
                >
                  {tier.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
              What You Get
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Real value. Real results. No marketing fluff.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl p-6 border-2 border-lux-200">
              <Icon name="shield" size={48} className="text-peace-400 mb-4" />
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">Production-Ready</h3>
              <p className="text-gray-600">6 Guards operational. 10 Guardians launching next week. Real system, not a prototype.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 border-2 border-lux-200">
              <Icon name="check-circle" size={48} className="text-peace-400 mb-4" />
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">97.8% Certainty</h3>
              <p className="text-gray-600">Epistemic honesty. We're transparent about uncertainty. No false promises.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 border-2 border-lux-200">
              <Icon name="lock" size={48} className="text-peace-400 mb-4" />
              <h3 className="text-xl font-display font-bold text-gray-900 mb-2">Zero Dark Patterns</h3>
              <p className="text-gray-600">No fake urgency. No false scarcity. No hidden costs. Just honest value.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-b from-lux-600 to-lux-800 text-white">
        <div className="max-w-screen-xl mx-auto px-4 lg:px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-lux-100 mb-8 max-w-2xl mx-auto">
            Register for the webinar to see the system in action and get webinar special pricing.
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

