'use client'

/**
 * Product Idea Submission Form
 * 
 * Pattern: PRODUCT × IDEA × SUBMISSION × FLOW × ONE
 * Guardian: AEYON (999 Hz) × Lux (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useState } from 'react'
import { AnimatedCard } from './AnimatedCard'

interface ProductIdeaSubmissionFormProps {
  onSuccess?: () => void
  onCancel?: () => void
}

export function ProductIdeaSubmissionForm({ onSuccess, onCancel }: ProductIdeaSubmissionFormProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const [formData, setFormData] = useState({
    name: '',
    quickContext: '',
    whatWereBuilding: '',
    whyThisMatters: '',
    whatsReady: {
      researchComplete: false,
      marketValidationDone: false,
      technicalFeasibilityConfirmed: false,
      designMockupsReady: false,
      userStoriesDefined: false,
    },
    criticalConsiderations: '',
    whatWeNeedFromYou: '',
    currentStatus: 'READY FOR REVIEW',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitError(null)

    try {
      const response = await fetch('/api/portal/product-ideas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          submitted_at: new Date().toISOString(),
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit product idea')
      }

      setSubmitSuccess(true)
      setTimeout(() => {
        setIsOpen(false)
        setSubmitSuccess(false)
        setFormData({
          name: '',
          quickContext: '',
          whatWereBuilding: '',
          whyThisMatters: '',
          whatsReady: {
            researchComplete: false,
            marketValidationDone: false,
            technicalFeasibilityConfirmed: false,
            designMockupsReady: false,
            userStoriesDefined: false,
          },
          criticalConsiderations: '',
          whatWeNeedFromYou: '',
          currentStatus: 'READY FOR REVIEW',
        })
        onSuccess?.()
      }, 2000)
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'An error occurred')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) {
    return (
      <AnimatedCard delay={0}>
        <button
          onClick={() => setIsOpen(true)}
          style={{
            padding: '13px 21px',
            backgroundColor: '#0080ff',
            color: '#ffffff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: '500',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            textShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#0066cc'
            e.currentTarget.style.transform = 'scale(1.02)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#0080ff'
            e.currentTarget.style.transform = 'scale(1)'
          }}
        >
          + Submit Product Idea
        </button>
      </AnimatedCard>
    )
  }

  return (
    <AnimatedCard delay={0}>
      <div style={{
        padding: '34px',
        backgroundColor: '#0a0a0a',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        maxWidth: '800px',
        margin: '0 auto',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '21px',
        }}>
          <h2 style={{
            fontSize: '28px',
            fontWeight: '600',
            color: '#ffffff',
            letterSpacing: '-0.01em',
          }}>
            Submit Product Idea
          </h2>
          <button
            onClick={() => {
              setIsOpen(false)
              onCancel?.()
            }}
            style={{
              background: 'none',
              border: 'none',
              color: '#a0a0a0',
              fontSize: '24px',
              cursor: 'pointer',
              padding: '0',
              width: '32px',
              height: '32px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            ×
          </button>
        </div>

        {submitSuccess && (
          <div style={{
            padding: '13px 21px',
            backgroundColor: '#00ff8820',
            border: '1px solid #00ff88',
            borderRadius: '8px',
            color: '#00ff88',
            marginBottom: '21px',
          }}>
            ✅ Product idea submitted successfully!
          </div>
        )}

        {submitError && (
          <div style={{
            padding: '13px 21px',
            backgroundColor: '#ff444420',
            border: '1px solid #ff4444',
            borderRadius: '8px',
            color: '#ff4444',
            marginBottom: '21px',
          }}>
            ❌ {submitError}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              Product Name *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
              }}
              placeholder="e.g., Real-Time Collaboration in AbëDESKs"
            />
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              Quick Context *
            </label>
            <textarea
              required
              value={formData.quickContext}
              onChange={(e) => setFormData({ ...formData, quickContext: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                minHeight: '80px',
                resize: 'vertical',
              }}
              placeholder="1-2 sentences - what problem does this solve?"
            />
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              What We're Building *
            </label>
            <textarea
              required
              value={formData.whatWereBuilding}
              onChange={(e) => setFormData({ ...formData, whatWereBuilding: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                minHeight: '120px',
                resize: 'vertical',
              }}
              placeholder="Clear, specific description of features/functionality"
            />
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              Why This Matters *
            </label>
            <textarea
              required
              value={formData.whyThisMatters}
              onChange={(e) => setFormData({ ...formData, whyThisMatters: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                minHeight: '120px',
                resize: 'vertical',
              }}
              placeholder="Problem statement, market opportunity, business value"
            />
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              What's Ready
            </label>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
            }}>
              {Object.entries(formData.whatsReady).map(([key, value]) => (
                <label key={key} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  color: '#a0a0a0',
                  fontSize: '14px',
                }}>
                  <input
                    type="checkbox"
                    checked={value}
                    onChange={(e) => setFormData({
                      ...formData,
                      whatsReady: {
                        ...formData.whatsReady,
                        [key]: e.target.checked,
                      },
                    })}
                    style={{
                      width: '16px',
                      height: '16px',
                      cursor: 'pointer',
                    }}
                  />
                  <span style={{ textTransform: 'capitalize' }}>
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              Critical Considerations
            </label>
            <textarea
              value={formData.criticalConsiderations}
              onChange={(e) => setFormData({ ...formData, criticalConsiderations: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                minHeight: '100px',
                resize: 'vertical',
              }}
              placeholder="Any blockers, risks, dependencies, resource requirements"
            />
          </div>

          <div style={{ marginBottom: '21px' }}>
            <label style={{
              display: 'block',
              fontSize: '14px',
              fontWeight: '500',
              color: '#ffffff',
              marginBottom: '8px',
            }}>
              What We Need From You *
            </label>
            <textarea
              required
              value={formData.whatWeNeedFromYou}
              onChange={(e) => setFormData({ ...formData, whatWeNeedFromYou: e.target.value })}
              style={{
                width: '100%',
                padding: '13px',
                backgroundColor: '#141414',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                minHeight: '100px',
                resize: 'vertical',
              }}
              placeholder="Specific questions/approvals needed"
            />
          </div>

          <div style={{
            display: 'flex',
            gap: '13px',
            justifyContent: 'flex-end',
          }}>
            <button
              type="button"
              onClick={() => {
                setIsOpen(false)
                onCancel?.()
              }}
              style={{
                padding: '13px 21px',
                backgroundColor: 'transparent',
                color: '#a0a0a0',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                fontSize: '16px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              style={{
                padding: '13px 21px',
                backgroundColor: isSubmitting ? '#666666' : '#0080ff',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '500',
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s ease',
                textShadow: '0 0 10px rgba(0, 128, 255, 0.3)',
              }}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Product Idea'}
            </button>
          </div>
        </form>
      </div>
    </AnimatedCard>
  )
}

