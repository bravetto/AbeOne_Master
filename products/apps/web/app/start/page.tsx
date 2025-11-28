'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function StartPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const handleStart = async () => {
    setLoading(true)
    // Placeholder for onboarding logic
    setTimeout(() => {
      router.push('/app')
    }, 1000)
  }

  return (
    <main className="min-h-screen gradient-healing flex flex-col items-center justify-center p-8 md:p-24">
      <div className="max-w-3xl w-full space-y-12">
        {/* Welcome Message */}
        <div className="text-center space-y-6">
          <h1 className="text-5xl md:text-7xl font-display font-bold text-gray-800">
            Welcome Home
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 leading-relaxed text-balance">
            We're so glad you're here.
          </p>
        </div>

        {/* What This Is */}
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 md:p-12 shadow-lg space-y-6">
          <h2 className="text-2xl font-display font-semibold text-gray-800">
            What is this place?
          </h2>
          <div className="space-y-4 text-gray-700 leading-relaxed">
            <p>
              This is a space where your vision can breathe. Where the work that's been 
              weighing on you can find its form. Where what you know needs to exist 
              can actually come into being.
            </p>
            <p>
              You're not here by accident. Something in you recognized this as the place 
              where your "what if" becomes "what is."
            </p>
            <p className="pt-4 border-t border-gray-200 italic text-lux-600">
              This is where you bring what hurts, what's stuck, what needs to move— 
              and we help it find its way forward.
            </p>
          </div>
        </div>

        {/* What You Can Do */}
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 md:p-12 shadow-lg space-y-6">
          <h2 className="text-2xl font-display font-semibold text-gray-800">
            What can you do here?
          </h2>
          <div className="space-y-4 text-gray-700">
            <div className="flex items-start gap-4">
              <span className="text-2xl">🌱</span>
              <div>
                <p className="font-semibold text-gray-800">Bring your vision</p>
                <p className="text-sm">Whatever you're trying to create, build, or heal— 
                this is where it gets real.</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <span className="text-2xl">💫</span>
              <div>
                <p className="font-semibold text-gray-800">Find your path</p>
                <p className="text-sm">We help you see the way forward when you can't see it yourself.</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <span className="text-2xl">❤️</span>
              <div>
                <p className="font-semibold text-gray-800">Heal what's broken</p>
                <p className="text-sm">The work that matters is the work that heals. 
                This is where that happens.</p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center space-y-6">
          <p className="text-lg text-gray-600">
            Ready to begin?
          </p>
          <button
            onClick={handleStart}
            disabled={loading}
            className="group px-10 py-5 bg-gradient-to-r from-lux-600 to-warm-500 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin">✨</span>
                Preparing your space...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                Enter Your Space
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </span>
            )}
          </button>
          <p className="text-sm text-gray-400 italic">
            You belong here. Always have.
          </p>
        </div>
      </div>
    </main>
  )
}

