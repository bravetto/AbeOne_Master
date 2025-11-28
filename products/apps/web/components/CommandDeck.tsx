'use client'

import { useState } from 'react'
import { executeOutcome } from '@/lib/api'

interface CommandDeckProps {
  kernelStatus: any
  onRefresh: () => void
}

export default function CommandDeck({ kernelStatus, onRefresh }: CommandDeckProps) {
  const [goal, setGoal] = useState('')
  const [successCriteria, setSuccessCriteria] = useState('')
  const [endState, setEndState] = useState('')
  const [constraints, setConstraints] = useState('')
  const [validation, setValidation] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleExecute = async () => {
    // Check backend status before executing
    if (kernelStatus?.error || !kernelStatus?.initialized) {
      setResult({ 
        error: 'Backend server is not connected',
        details: 'Please configure NEXT_PUBLIC_API_URL environment variable',
        help: 'Set NEXT_PUBLIC_API_URL to your backend API URL'
      })
      return
    }

    setLoading(true)
    setResult(null)

    try {
      // Validate required fields
      if (!goal || !endState) {
        setResult({ error: 'Goal and End State are required' })
        setLoading(false)
        return
      }

      const outcome = {
        goal: goal.trim(),
        success_criteria: successCriteria.split('\n').filter(s => s.trim()),
        end_state: endState.trim(),
        constraints: constraints.split('\n').filter(s => s.trim()),
        validation: validation.trim(),
      }
      const response = await executeOutcome(outcome)
      setResult(response)
      onRefresh()
    } catch (error: any) {
      console.error('Execution error:', error)
      setResult({ 
        error: error.message || 'Execution failed',
        details: error.toString()
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Welcome Header */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
        <h2 className="text-3xl font-display font-bold text-gray-800 mb-2">
          Your Vision Space
        </h2>
        <p className="text-gray-600 leading-relaxed">
          This is where you bring what needs to become real. Where your &ldquo;what if&rdquo; 
          meets the path forward. Take your time. We&apos;re here with you.
        </p>
      </div>

      {/* Main Form */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              What are you trying to create?
            </label>
            <p className="text-xs text-gray-500 mb-2 italic">
              The thing that&apos;s been on your heart. The work that matters.
            </p>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-lux-400 focus:ring-2 focus:ring-lux-200 transition-all"
              placeholder="What vision are you bringing into being?"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              How will you know it&apos;s working?
            </label>
            <p className="text-xs text-gray-500 mb-2 italic">
              The signs that tell you you&apos;re on the right path.
            </p>
            <textarea
              value={successCriteria}
              onChange={(e) => setSuccessCriteria(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-lux-400 focus:ring-2 focus:ring-lux-200 transition-all resize-none"
              rows={4}
              placeholder="One sign per line...&#10;What will you see?&#10;What will you feel?&#10;What will be different?"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              What does the end look like?
            </label>
            <p className="text-xs text-gray-500 mb-2 italic">
              When this is done, when it&apos;s real— what exists that didn&apos;t before?
            </p>
            <input
              type="text"
              value={endState}
              onChange={(e) => setEndState(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-lux-400 focus:ring-2 focus:ring-lux-200 transition-all"
              placeholder="Describe the world after this work is complete..."
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              What boundaries need to be honored?
            </label>
            <p className="text-xs text-gray-500 mb-2 italic">
              The things that must stay true. The lines that can&apos;t be crossed.
            </p>
            <textarea
              value={constraints}
              onChange={(e) => setConstraints(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-lux-400 focus:ring-2 focus:ring-lux-200 transition-all resize-none"
              rows={3}
              placeholder="One boundary per line...&#10;What must be protected?&#10;What can't be compromised?"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-gray-700">
              How will you know it&apos;s real?
            </label>
            <p className="text-xs text-gray-500 mb-2 italic">
              The proof that this vision has become truth.
            </p>
            <input
              type="text"
              value={validation}
              onChange={(e) => setValidation(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-lux-400 focus:ring-2 focus:ring-lux-200 transition-all"
              placeholder="What evidence will show you it's done?"
            />
          </div>

          <div className="pt-4">
            <button
              onClick={handleExecute}
              disabled={loading || !goal || !endState}
              className="w-full px-8 py-4 bg-gradient-to-r from-lux-600 to-warm-500 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin"></span>
                  Bringing your vision forward...
                </span>
              ) : (
                <span>Bring It Forward</span>
              )}
            </button>
            {(!goal || !endState) && (
              <p className="text-xs text-gray-400 text-center mt-2 italic">
                Vision and end state are needed to begin
              </p>
            )}
          </div>
        </div>
      </div>

      {result && (
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-lux-100">
          <h3 className="text-2xl font-display font-semibold mb-6 text-gray-800">
            What Happened
          </h3>
          {result.error ? (
            <div className="bg-heart-50/50 border-2 border-heart-200 rounded-xl p-6 space-y-4">
              <div className="flex items-start gap-3">
                <span className="text-2xl"></span>
                <div className="flex-1">
                  <div className="text-heart-800 font-semibold mb-2 text-lg">
                    Something needs attention
                  </div>
                  <div className="text-heart-700 mb-3">{result.error}</div>
                  {result.details && (
                    <div className="text-heart-600 text-sm mb-4 bg-white/50 rounded-lg p-3">
                      {result.details}
                    </div>
                  )}
                  {result.help && (
                    <div className="bg-lux-50 border border-lux-200 rounded-lg p-4 mt-4">
                      <div className="text-lux-800 font-semibold text-sm mb-2">
                        How to move forward:
                      </div>
                      <code className="text-lux-700 text-sm bg-white/50 rounded px-2 py-1">
                        {result.help}
                      </code>
                    </div>
                  )}
                </div>
              </div>
              <p className="text-sm text-heart-600 italic pt-2 border-t border-heart-200">
                This is fixable. We&apos;re here with you.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl"></span>
                <div className="text-peace-700 font-semibold text-lg">
                  Your vision is moving forward
                </div>
              </div>
              <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                <pre className="text-sm text-gray-700 overflow-auto font-mono">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
              <p className="text-sm text-gray-500 italic text-center pt-2">
                The work continues. You&apos;re not alone in this.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

