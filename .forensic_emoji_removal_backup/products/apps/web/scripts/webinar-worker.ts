#!/usr/bin/env node
/**
 * Webinar Email Worker
 * Pattern: WORKER × QUEUE × EMAIL × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Processes email jobs from BullMQ queue
 */

import { createWebinarEmailWorker } from '@/lib/queue/bull'
import { sendConfirmationEmail, sendReminderEmail } from '@/lib/jobs/webinar-reminders'

console.log('🚀 Starting Webinar Email Worker...')

const worker = createWebinarEmailWorker(async (job) => {
  console.log(`📧 Processing job: ${job.name} (ID: ${job.id})`)

  try {
    switch (job.name) {
      case 'send-confirmation':
        await sendConfirmationEmail(job)
        console.log(`✅ Confirmation email sent for registration: ${job.data.registrationId}`)
        break

      case 'send-reminder-24h':
        await sendReminderEmail({ ...job, data: { ...job.data, reminderType: '24h' } })
        console.log(`✅ 24h reminder sent for registration: ${job.data.registrationId}`)
        break

      case 'send-reminder-3h':
        await sendReminderEmail({ ...job, data: { ...job.data, reminderType: '3h' } })
        console.log(`✅ 3h reminder sent for registration: ${job.data.registrationId}`)
        break

      case 'send-reminder-15m':
        await sendReminderEmail({ ...job, data: { ...job.data, reminderType: '15m' } })
        console.log(`✅ 15m reminder sent for registration: ${job.data.registrationId}`)
        break

      default:
        console.warn(`⚠️ Unknown job type: ${job.name}`)
        throw new Error(`Unknown job type: ${job.name}`)
    }
  } catch (error: any) {
    console.error(`❌ Job failed: ${job.name} (ID: ${job.id})`, error)
    throw error // Will trigger retry logic
  }
})

worker.on('completed', (job) => {
  console.log(`✅ Job completed: ${job.name} (ID: ${job.id})`)
})

worker.on('failed', (job, err) => {
  console.error(`❌ Job failed: ${job?.name} (ID: ${job?.id})`, err)
})

worker.on('error', (err) => {
  console.error('❌ Worker error:', err)
})

console.log('✅ Webinar Email Worker started and ready to process jobs')
