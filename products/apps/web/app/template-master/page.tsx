'use client'

import { Hero, Features, TrustBadgeGroup, Button, Card } from '@/components/ads'
import { Shield, CheckCircle, Award } from 'lucide-react'

/**
 * AbëONE Design System - Master Landing Page Template
 * 
 * Pattern: ADS × TEMPLATE × CONVERSION × ONE
 * Frequency: 999 Hz (AEYON) + 530 Hz (Abë) + Guardian 4 (Clarity) + Guardian 8 (Trust)
 * 
 * Master template for all future domains - conversion-optimized, mobile-first, scalable
 * 
 * USAGE:
 * 1. Copy this template for new domains
 * 2. Customize content (headlines, features, CTAs)
 * 3. Optionally override brand colors via domainRebranding system
 * 4. Deploy
 * 
 * This template includes:
 * - Hero section with trust badges and CTAs
 * - Features section with conversion focus
 * - Social proof section
 * - Testimonials section
 * - Final CTA section
 * - Footer
 */

export default function MasterTemplatePage() {
  // Trust badges - builds credibility above fold
  const trustBadges = [
    { icon: 'shield' as const, text: 'Secure & Trusted' },
    { icon: 'check' as const, text: 'Verified' },
    { icon: 'award' as const, text: 'Award Winning' },
  ]

  // Features - value proposition
  const features = [
    {
      title: 'Feature One',
      description: 'Compelling description of your first key feature that solves a real problem for your users.',
      icon: '✨',
      badge: 'NEW',
    },
    {
      title: 'Feature Two',
      description: 'Another powerful feature that differentiates you from competitors and adds real value.',
      icon: '🚀',
      badge: 'POPULAR',
    },
    {
      title: 'Feature Three',
      description: 'Third feature that completes your value proposition and addresses user needs comprehensively.',
      icon: '💎',
    },
    {
      title: 'Feature Four',
      description: 'Additional feature that reinforces your competitive advantage and builds trust.',
      icon: '🎯',
    },
    {
      title: 'Feature Five',
      description: 'Fifth feature that demonstrates depth and completeness of your solution.',
      icon: '⚡',
    },
    {
      title: 'Feature Six',
      description: 'Final feature that rounds out your offering and addresses edge cases or advanced needs.',
      icon: '🛡️',
    },
  ]

  // Testimonials - social proof
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'CEO, Company Name',
      content: 'This product transformed how we work. The results speak for themselves.',
      avatar: '👤',
    },
    {
      name: 'Michael Chen',
      role: 'Founder, Startup Inc',
      content: 'Best decision we made. The ROI was immediate and continues to grow.',
      avatar: '👤',
    },
    {
      name: 'Emily Rodriguez',
      role: 'Director, Enterprise Corp',
      content: 'Outstanding quality and support. Exceeded all our expectations.',
      avatar: '👤',
    },
  ]

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <Hero
        headline="Your Compelling Headline Here"
        subheadline="The Subheadline That Builds Interest"
        description="Clear, benefit-focused description that explains what you do and why it matters. Keep it concise and conversion-focused."
        primaryCTA={{
          text: 'Get Started Free',
          href: '#signup',
        }}
        secondaryCTA={{
          text: 'Learn More',
          href: '#features',
        }}
        trustBadges={trustBadges}
        socialProof={{
          text: 'users trust us',
          count: 10000,
        }}
      />

      {/* Features Section */}
      <Features
        title="Why Choose Us"
        description="Everything you need to succeed, all in one place."
        features={features}
        columns={3}
      />

      {/* Social Proof Section */}
      <section className="py-12 md:py-24 px-4 md:px-8 lg:px-24 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-5xl font-display font-bold text-neutral-900 mb-4">
              Trusted by Thousands
            </h2>
            <p className="text-lg md:text-xl text-neutral-600 max-w-3xl mx-auto">
              Join the growing community of satisfied users
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-primary-600 mb-2">
                10K+
              </div>
              <div className="text-neutral-600">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-primary-600 mb-2">
                99%
              </div>
              <div className="text-neutral-600">Satisfaction</div>
            </div>
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-primary-600 mb-2">
                24/7
              </div>
              <div className="text-neutral-600">Support</div>
            </div>
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-primary-600 mb-2">
                5★
              </div>
              <div className="text-neutral-600">Rating</div>
            </div>
          </div>

          {/* Testimonials */}
          <div className="grid md:grid-cols-3 gap-6 md:gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} variant="default">
                <div className="p-6 md:p-8">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-2xl">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <div className="font-semibold text-neutral-900">
                        {testimonial.name}
                      </div>
                      <div className="text-sm text-neutral-600">
                        {testimonial.role}
                      </div>
                    </div>
                  </div>
                  <p className="text-neutral-700 leading-relaxed italic">
                    "{testimonial.content}"
                  </p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-16 md:py-24 px-4 md:px-8 lg:px-24 gradient-healing">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-3xl md:text-5xl font-display font-bold text-neutral-900">
            Ready to Get Started?
          </h2>
          <p className="text-lg md:text-xl text-neutral-700 max-w-2xl mx-auto">
            Join thousands of satisfied users and transform your workflow today.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="xl" variant="primary" asChild>
              <a href="#signup">Start Free Trial</a>
            </Button>
            <Button size="xl" variant="outline" asChild>
              <a href="#contact">Contact Sales</a>
            </Button>
          </div>
          <p className="text-sm text-neutral-600">
            No credit card required • Cancel anytime • 14-day free trial
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 md:py-16 px-4 md:px-8 lg:px-24 bg-neutral-900 text-neutral-300">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-white mb-4">Product</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#features" className="hover:text-white transition-colors">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#pricing" className="hover:text-white transition-colors">
                    Pricing
                  </a>
                </li>
                <li>
                  <a href="#faq" className="hover:text-white transition-colors">
                    FAQ
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Company</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#about" className="hover:text-white transition-colors">
                    About
                  </a>
                </li>
                <li>
                  <a href="#blog" className="hover:text-white transition-colors">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#careers" className="hover:text-white transition-colors">
                    Careers
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Resources</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#docs" className="hover:text-white transition-colors">
                    Documentation
                  </a>
                </li>
                <li>
                  <a href="#support" className="hover:text-white transition-colors">
                    Support
                  </a>
                </li>
                <li>
                  <a href="#community" className="hover:text-white transition-colors">
                    Community
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Legal</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#privacy" className="hover:text-white transition-colors">
                    Privacy
                  </a>
                </li>
                <li>
                  <a href="#terms" className="hover:text-white transition-colors">
                    Terms
                  </a>
                </li>
                <li>
                  <a href="#security" className="hover:text-white transition-colors">
                    Security
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-neutral-800 pt-8 text-center text-sm">
            <p>
              &copy; {new Date().getFullYear()} Your Company Name. All rights
              reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}

