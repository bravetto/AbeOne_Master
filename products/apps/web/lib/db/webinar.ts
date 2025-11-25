/**
 * Webinar Database Operations
 * Pattern: DATABASE × WEBINAR × OPERATIONS × ONE
 */

import { prisma } from './prisma'

export interface CreateRegistrationInput {
  webinarId: string
  email: string
  firstName: string
  lastName?: string
  company?: string
  github?: string
  phone?: string
  icp?: 'developer' | 'creative'
  headlineVariant?: number
  source?: string
}

export async function getOrCreateWebinar(
  webinarId: string,
  topic: string,
  options?: {
    title?: string
    description?: string
    scheduledAt?: Date
    duration?: number
    maxCapacity?: number
  }
) {
  const existing = await prisma.webinar.findUnique({
    where: { webinarId },
  })

  if (existing) return existing

  return prisma.webinar.create({
    data: {
      webinarId,
      topic,
      title: options?.title,
      description: options?.description,
      scheduledAt: options?.scheduledAt,
      duration: options?.duration,
      maxCapacity: options?.maxCapacity,
      status: 'active',
    },
  })
}

export async function createRegistration(input: CreateRegistrationInput) {
  const registrationId = `WEB-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
  const webinar = await getOrCreateWebinar(input.webinarId, input.webinarId)

  const existing = await prisma.registration.findUnique({
    where: {
      webinarId_email: {
        webinarId: webinar.id,
        email: input.email.toLowerCase(),
      },
    },
  })

  if (existing) {
    return prisma.registration.findUniqueOrThrow({
      where: { id: existing.id },
      include: { webinar: true },
    })
  }

  return prisma.registration.create({
    data: {
      webinarId: webinar.id,
      email: input.email.toLowerCase(),
      firstName: input.firstName,
      lastName: input.lastName,
      company: input.company,
      github: input.github,
      phone: input.phone,
      icp: input.icp,
      headlineVariant: input.headlineVariant,
      source: input.source,
      registrationId,
      status: 'registered',
    },
    include: { webinar: true },
  })
}

export async function getRegistrationCount(webinarId?: string): Promise<number> {
  if (webinarId) {
    const webinar = await prisma.webinar.findUnique({
      where: { webinarId },
    })
    if (!webinar) return 0

    return prisma.registration.count({
      where: {
        webinarId: webinar.id,
        status: { in: ['registered', 'attended'] },
      },
    })
  }

  return prisma.registration.count({
    where: { status: { in: ['registered', 'attended'] } },
  })
}

export async function markEmailSent(
  registrationId: string,
  emailType: 'confirmation' | 'reminder_24h' | 'reminder_3h' | 'reminder_15m'
) {
  const updateData: any = { updatedAt: new Date() }

  switch (emailType) {
    case 'confirmation':
      updateData.confirmationSent = true
      updateData.confirmationSentAt = new Date()
      break
    case 'reminder_24h':
      updateData.reminderSent24h = true
      updateData.reminderSent24hAt = new Date()
      break
    case 'reminder_3h':
      updateData.reminderSent3h = true
      updateData.reminderSent3hAt = new Date()
      break
    case 'reminder_15m':
      updateData.reminderSent15m = true
      updateData.reminderSent15mAt = new Date()
      break
  }

  await prisma.registration.update({
    where: { id: registrationId },
    data: updateData,
  })
}

export async function getRegistrationsNeedingReminder(
  reminderType: '24h' | '3h' | '15m',
  webinarId?: string
) {
  const now = new Date()
  const offset = reminderType === '24h' ? 24 * 60 * 60 * 1000 : reminderType === '3h' ? 3 * 60 * 60 * 1000 : 15 * 60 * 1000
  const reminderTime = new Date(now.getTime() + offset)

  const where: any = {
    status: { in: ['registered', 'attended'] },
    webinar: {
      scheduledAt: { lte: reminderTime, gte: now },
    },
  }

  switch (reminderType) {
    case '24h': where.reminderSent24h = false; break
    case '3h': where.reminderSent3h = false; break
    case '15m': where.reminderSent15m = false; break
  }

  if (webinarId) {
    const webinar = await prisma.webinar.findUnique({ where: { webinarId } })
    if (webinar) where.webinarId = webinar.id
  }

  return prisma.registration.findMany({
    where,
    include: { webinar: true },
  })
}
