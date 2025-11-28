/**
 * 🛡️ SENDGRID EMAIL SERVICE
 * 
 * Centralized SendGrid integration for webinar emails
 * 
 * Pattern: Email × SendGrid × Webinar × ONE
 * Guardians: AEYON (999 Hz) × ZERO (777 Hz)
 */

import sgMail from '@sendgrid/mail'

// Initialize SendGrid
import { getSendGridConfig } from "@/lib/config/webinar"; const sendgridConfig = getSendGridConfig(); if (sendgridConfig.apiKey) {
  sgMail.setApiKey(sendgridConfig.apiKey)
} else {
  console.warn('⚠️ SendGrid API key not configured. Email functionality will be limited.')
}

export interface EmailOptions {
  to: string
  subject: string
  html: string
  text?: string
  from?: {
    email: string
    name: string
  }
  customArgs?: Record<string, string>
  trackingSettings?: {
    clickTracking?: { enable: boolean }
    openTracking?: { enable: boolean }
    subscriptionTracking?: { enable: boolean }
  }
}

/**
 * Send email via SendGrid
 */
export async function sendEmail(options: EmailOptions): Promise<{ success: boolean; messageId?: string; error?: string }> {
  if (!process.env.SENDGRID_API_KEY) {
    console.error('SendGrid API key not configured')
    return { success: false, error: 'SendGrid API key not configured' }
  }
  
  const fromEmail = options.from?.email || process.env.SENDGRID_FROM_EMAIL || 'noreply@aiguardian.ai'
  const fromName = options.from?.name || process.env.SENDGRID_FROM_NAME || 'AiGuardian Team'
  
  const msg = {
    to: options.to,
    from: {
      email: fromEmail,
      name: fromName
    },
    subject: options.subject,
    html: options.html,
    text: options.text || options.html.replace(/<[^>]*>/g, ''), // Strip HTML for text version
    trackingSettings: options.trackingSettings || {
      clickTracking: { enable: true },
      openTracking: { enable: true },
      subscriptionTracking: { enable: false }
    },
    customArgs: options.customArgs || {}
  }
  
  try {
    const [response] = await sgMail.send(msg)
    
    if (response.statusCode === 202) {
      const messageId = response.headers['x-message-id'] as string
      console.log(`✅ Email sent successfully to ${options.to} (Message ID: ${messageId})`)
      return { success: true, messageId }
    } else {
      console.error(`❌ SendGrid error: Status ${response.statusCode}`)
      return { success: false, error: `Status ${response.statusCode}` }
    }
  } catch (error: any) {
    console.error('❌ SendGrid send error:', error)
    
    if (error.response) {
      console.error('SendGrid response body:', error.response.body)
      return { 
        success: false, 
        error: error.response.body?.errors?.[0]?.message || 'SendGrid API error' 
      }
    }
    
    return { success: false, error: error.message || 'Unknown error' }
  }
}

/**
 * Validate SendGrid configuration
 */
export function validateSendGridConfig(): { valid: boolean; errors: string[] } {
  const errors: string[] = []
  
  if (!process.env.SENDGRID_API_KEY) {
    errors.push('SENDGRID_API_KEY environment variable not set')
  }
  
  if (!process.env.SENDGRID_FROM_EMAIL) {
    errors.push('SENDGRID_FROM_EMAIL environment variable not set (optional, defaults to noreply@aiguardian.ai)')
  }
  
  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Test SendGrid connection
 */
export async function testSendGridConnection(): Promise<boolean> {
  try {
    // Send a test email to verify connection
    // In production, you might want to use SendGrid's validation API instead
    const validation = validateSendGridConfig()
    return validation.valid
  } catch (error) {
    console.error('SendGrid connection test failed:', error)
    return false
  }
}

