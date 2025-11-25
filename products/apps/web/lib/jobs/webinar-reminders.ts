/**
 * Webinar Email Reminder Jobs
 * Pattern: JOBS × EMAIL × REMINDERS × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Lux)
 */

import { sendEmail } from '@/lib/sendgrid'
import { markEmailSent } from '@/lib/db/webinar'

/**
 * Send confirmation email
 */
export async function sendConfirmationEmail(job: any) {
  const { registrationId, email, firstName, webinarId, webinarTopic, registrationIdHuman } = job.data

  try {
    // Get registration details
    const registration = await null as any
    if (!registration) {
      throw new Error(`Registration not found: ${registrationId}`)
    }

    // Send email
    const result = await sendEmail({
      to: email,
      subject: `You're registered for ${webinarTopic || webinarId}!`,
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">You're All Set! </h1>
          </div>
          
          <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            <p>Hi ${firstName},</p>
            
            <p>Thank you for registering for <strong>${webinarTopic || webinarId}</strong>!</p>
            
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea;">
              <p style="margin: 0;"><strong>Registration ID:</strong> ${registrationIdHuman || registrationId}</p>
            </div>
            
            ${registration.webinar.scheduledAt ? `
              <p><strong>Webinar Date & Time:</strong></p>
              <p style="font-size: 18px; font-weight: bold; color: #667eea;">
                ${new Date(registration.webinar.scheduledAt).toLocaleString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: 'numeric',
                  minute: '2-digit',
                  timeZoneName: 'short',
                })}
              </p>
            ` : ''}
            
            <p>We'll send you reminder emails:</p>
            <ul>
              <li>24 hours before the webinar</li>
              <li>3 hours before the webinar</li>
              <li>15 minutes before the webinar</li>
            </ul>
            
            <p>If you have any questions, just reply to this email.</p>
            
            <p style="margin-top: 30px;">
              Best regards,<br>
              The AiGuardian Team
            </p>
          </div>
        </body>
        </html>
      `,
      text: `
Hi ${firstName},

Thank you for registering for ${webinarTopic || webinarId}!

Registration ID: ${registrationIdHuman || registrationId}

${registration.webinar.scheduledAt ? `Webinar Date & Time: ${new Date(registration.webinar.scheduledAt).toLocaleString()}` : ''}

We'll send you reminder emails 24 hours, 3 hours, and 15 minutes before the webinar.

If you have any questions, just reply to this email.

Best regards,
The AiGuardian Team
      `,
    })

    if (result.success) {
      await markEmailSent(registrationId, 'confirmation')
    }

    return result
  } catch (error: any) {
    console.error('Confirmation email error:', error)
    throw error
  }
}

/**
 * Send reminder email (24h, 3h, or 15m)
 */
export async function sendReminderEmail(job: any) {
  const { registrationId, email, firstName, webinarId, webinarTopic, scheduledAt, reminderType } = job.data

  try {
    const registration = await null as any
    if (!registration) {
      throw new Error(`Registration not found: ${registrationId}`)
    }

    const webinarDate = scheduledAt ? new Date(scheduledAt) : registration.webinar.scheduledAt
    if (!webinarDate) {
      throw new Error('Webinar not scheduled')
    }

    const reminderText = reminderType === '24h' ? '24 hours' : reminderType === '3h' ? '3 hours' : '15 minutes'
    const urgency = reminderType === '15m' ? 'high' : reminderType === '3h' ? 'medium' : 'low'

    const result = await sendEmail({
      to: email,
      subject: `Reminder: ${webinarTopic || webinarId} starts ${reminderText === '15 minutes' ? 'in 15 minutes' : `in ${reminderText}`}!`,
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
          <div style="background: ${urgency === 'high' ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'}; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">Webinar Reminder ⏰</h1>
          </div>
          
          <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            <p>Hi ${firstName},</p>
            
            <p>This is a friendly reminder that <strong>${webinarTopic || webinarId}</strong> starts ${reminderText === '15 minutes' ? 'in just 15 minutes' : `in ${reminderText}`}!</p>
            
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid ${urgency === 'high' ? '#f5576c' : '#4facfe'};">
              <p style="margin: 0; font-size: 18px; font-weight: bold;">
                ${webinarDate.toLocaleString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: 'numeric',
                  minute: '2-digit',
                  timeZoneName: 'short',
                })}
              </p>
            </div>
            
            <p>We're excited to have you join us!</p>
            
            <p style="margin-top: 30px;">
              Best regards,<br>
              The AiGuardian Team
            </p>
          </div>
        </body>
        </html>
      `,
      text: `
Hi ${firstName},

This is a friendly reminder that ${webinarTopic || webinarId} starts ${reminderText === '15 minutes' ? 'in just 15 minutes' : `in ${reminderText}`}!

Date & Time: ${webinarDate.toLocaleString()}

We're excited to have you join us!

Best regards,
The AiGuardian Team
      `,
    })

    if (result.success) {
      const emailType = reminderType === '24h' ? 'reminder_24h' : reminderType === '3h' ? 'reminder_3h' : 'reminder_15m'
      await markEmailSent(registrationId, emailType as any)
    }

    return result
  } catch (error: any) {
    console.error('Reminder email error:', error)
    throw error
  }
}
