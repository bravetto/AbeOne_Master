'use client'

import { useState } from 'react'

export function Webinar() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Connect to email service or backend
    setSubmitted(true)
    setEmail('')
    setTimeout(() => setSubmitted(false), 5000)
  }

  return (
    <section id="webinar" className="py-24 px-4 md:px-8 lg:px-24 bg-gradient-to-b from-red-900 via-red-800 to-orange-900">
      <div className="max-w-4xl mx-auto text-center">
        <div className="mb-12">
          <h2 className="text-4xl md:text-6xl font-display font-bold text-white mb-4">
            🎥 Weekly Webinar: Multi-Use Flip-Flops
          </h2>
          <p className="text-xl md:text-2xl text-red-200 mb-6">
            Learn why our flip-flops are the only footwear you'll ever need
          </p>
        </div>

        {/* Webinar Description */}
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 mb-12 border-2 border-red-400/50 text-left">
          <h3 className="text-2xl font-bold text-white mb-4">What You'll Learn:</h3>
          <ul className="space-y-3 text-red-100">
            <li className="flex items-start gap-3">
              <span className="text-yellow-400 text-xl">🏖️</span>
              <span><strong>Beach Mode:</strong> These flip-flops handle sand like a pro. No more burning your feet on hot sand or losing your shoes in the waves.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-yellow-400 text-xl">🍺</span>
              <span><strong>Rum Spill Resistant:</strong> Spilled your drink? No problem. These flip-flops laugh in the face of sticky situations (literally).</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-yellow-400 text-xl">🏴‍☠️</span>
              <span><strong>Gasparilla Ready:</strong> Walk the parade route without your feet hating you. These aren't just flip-flops, they're survival gear.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-yellow-400 text-xl">🏃</span>
              <span><strong>Quick Escape Mode:</strong> Need to make a hasty exit? These flip-flops won't slow you down. (We've tested this. Multiple times.)</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-yellow-400 text-xl">💪</span>
              <span><strong>Questionable Life Choices Approved:</strong> We've put these through hell. They survived. You probably will too.</span>
            </li>
          </ul>
        </div>

        {/* Signup Form */}
        <div className="bg-white rounded-2xl p-8 shadow-2xl">
          {!submitted ? (
            <>
              <h3 className="text-3xl font-display font-bold text-red-900 mb-4">
                Sign Up for Next Webinar
              </h3>
              <p className="text-red-700 mb-6">
                Join us weekly to learn about the most versatile flip-flops in Tampa Bay
              </p>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  required
                  className="w-full px-4 py-3 rounded-lg border-2 border-red-300 focus:border-red-500 focus:outline-none text-lg"
                />
                <button
                  type="submit"
                  className="w-full py-4 bg-gradient-to-r from-red-600 to-orange-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
                >
                  Sign Me Up! 🎥
                </button>
              </form>
            </>
          ) : (
            <div className="text-center py-8">
              <div className="text-6xl mb-4">🎉</div>
              <h3 className="text-3xl font-bold text-red-900 mb-2">
                You're In!
              </h3>
              <p className="text-red-700">
                Check your email for webinar details. See you there, pirate!
              </p>
            </div>
          )}
        </div>

        {/* Why Sign Up */}
        <div className="mt-12 text-center">
          <p className="text-lg text-red-200 mb-4">
            <strong className="text-yellow-400">Why join?</strong> Because you need flip-flops that can handle:
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-red-100">
            <span className="px-4 py-2 bg-white/10 rounded-full">Gasparilla</span>
            <span className="px-4 py-2 bg-white/10 rounded-full">Beach Days</span>
            <span className="px-4 py-2 bg-white/10 rounded-full">Comedy Shows</span>
            <span className="px-4 py-2 bg-white/10 rounded-full">Life</span>
          </div>
        </div>
      </div>
    </section>
  )
}

