'use client'

/**
 * WEBINAR THANK YOU PAGE
 * 
 * Shown after successful webinar registration
 * 
 * Pattern: Thank You × Conversion × AiGuardian × ONE
 * Guardians: AEYON (999 Hz) × Lux (530 Hz)
 */

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Icon } from '@/components/icons/Icon'

export default function WebinarThankYouPage() {
  const searchParams = useSearchParams()
  const isAiGuardian = searchParams?.get('aiguardian') === 'true'
  const [registrationId, setRegistrationId] = useState<string | null>(null)
  
  useEffect(() => {
    // Get registration ID from sessionStorage if available
    const storedId = sessionStorage.getItem('webinar_registration_id')
    if (storedId) {
      setRegistrationId(storedId)
    }
  }, [])
  
  return (
    <div className="min-h-screen bg-gradient-healing flex items-center justify-center px-4">
      <div className="max-w-2xl w-full">
        {/* Success Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 md:p-12 text-center border border-gray-200">
          {/* Success Icon */}
          <div className="mb-6">
            <div className="w-24 h-24 bg-gradient-to-br from-peace-400 to-peace-600 rounded-full flex items-center justify-center mx-auto">
              <Icon name="check-circle" size={48} className="text-white" />
            </div>
          </div>
          
          {/* Heading */}
          <h1 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4 flex items-center justify-center gap-2">
            You&apos;re All Set!
            <Icon name="celebration" size={32} className="text-warm-500" />
          </h1>
          
          {/* Message */}
          <p className="text-xl text-gray-600 mb-8">
            {isAiGuardian 
              ? "You're successfully registered for the AiGuardian Validation System webinar!"
              : "You're successfully registered for the webinar!"}
          </p>
          
          {/* Check Email */}
          <div className="bg-gradient-to-br from-lux-50 to-warm-50 rounded-xl p-6 mb-8 border border-lux-200">
            <div className="flex items-center justify-center gap-3 mb-2">
              <Icon name="email" size={28} className="text-lux-600" />
              <h2 className="text-xl font-bold text-gray-900">Check Your Email</h2>
            </div>
            <p className="text-gray-600">
              We've sent you a confirmation email with all the details, including:
            </p>
            <ul className="text-left mt-4 space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <Icon name="check" size={20} className="text-peace-500 flex-shrink-0 mt-0.5" />
                <span>Webinar date, time, and join link</span>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="check" size={20} className="text-peace-500 flex-shrink-0 mt-0.5" />
                <span>Calendar invite (add to your calendar)</span>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="check" size={20} className="text-peace-500 flex-shrink-0 mt-0.5" />
                <span>Reminder schedule (24h, 3h, 15min before)</span>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="check" size={20} className="text-peace-500 flex-shrink-0 mt-0.5" />
                <span>Your free bonus resources</span>
              </li>
            </ul>
          </div>
          
          {/* Registration ID */}
          {registrationId && (
            <div className="bg-gray-50 rounded-lg p-4 mb-8">
              <p className="text-sm text-gray-600 mb-1">Registration ID:</p>
              <code className="text-sm font-mono text-lux-600 bg-white px-3 py-1 rounded border border-gray-200">
                {registrationId}
              </code>
            </div>
          )}
          
          {/* Next Steps */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-gray-900">What&apos;s Next?</h3>
            
            <div className="bg-white border-2 border-lux-200 rounded-xl p-6 text-left">
              <div className="flex items-start gap-4">
                <div className="text-lux-600 flex-shrink-0">
                  <Icon name="calendar" size={32} />
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">Add to Your Calendar</h4>
                  <p className="text-gray-600 text-sm mb-4">
                    Don&apos;t miss it! Add the webinar to your calendar so you get reminders.
                  </p>
                  <p className="text-xs text-gray-500">
                    (Check your email for the calendar link)
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white border-2 border-warm-200 rounded-xl p-6 text-left">
              <div className="flex items-start gap-4">
                <div className="text-warm-500 flex-shrink-0">
                  <Icon name="gift" size={32} />
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">Get Your Free Bonuses</h4>
                  <p className="text-gray-600 text-sm mb-4">
                    All bonus resources will be sent to your email after the webinar.
                  </p>
                  <p className="text-xs text-gray-500">
                    (Code examples, templates, benchmarks, and more!)
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white border-2 border-peace-200 rounded-xl p-6 text-left">
              <div className="flex items-start gap-4">
                <div className="text-peace-500 flex-shrink-0">
                  <Icon name="email" size={32} />
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">Watch for Reminders</h4>
                  <p className="text-gray-600 text-sm mb-4">
                    We&apos;ll send you reminder emails 24 hours, 3 hours, and 15 minutes before the webinar.
                  </p>
                  <p className="text-xs text-gray-500">
                    (Make sure to check your spam folder if you don&apos;t see them)
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* CTA Buttons */}
          <div className="mt-8 space-y-3">
            <Link
              href="/"
              className="block w-full py-4 bg-gradient-to-r from-lux-600 to-warm-500 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all"
            >
              Return to Home →
            </Link>
            
            {isAiGuardian && (
              <Link
                href="/products/aiguardian"
                className="block w-full py-3 bg-white border-2 border-lux-300 text-lux-600 rounded-xl font-semibold hover:bg-lux-50 transition-all"
              >
                Learn More About AiGuardian →
              </Link>
            )}
          </div>
          
          {/* Help - Transparent Support */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-2">
              Questions? <a href="mailto:support@bravetto.com" className="text-lux-600 hover:underline font-semibold">Contact Support</a>
            </p>
            <p className="text-xs text-gray-500 italic">
              We respond to all emails within 24 hours. This is a beta program - your feedback matters.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

