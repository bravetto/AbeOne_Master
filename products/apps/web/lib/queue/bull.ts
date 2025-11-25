/**
 * Bull Job Queue Setup
 * Pattern: QUEUE × BULL × JOBS × ONE
 */

import { Queue, Worker } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(
  process.env.REDIS_URL || process.env.UPSTASH_REDIS_REST_URL || 'redis://localhost:6379',
  {
    maxRetriesPerRequest: null,
    enableReadyCheck: false,
  }
)

export const webinarEmailQueue = new Queue('webinar-emails', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: {
      age: 24 * 3600,
      count: 1000,
    },
    removeOnFail: {
      age: 7 * 24 * 3600,
    },
  },
})

export function createWebinarEmailWorker(processor: (job: any) => Promise<void>) {
  return new Worker('webinar-emails', processor, {
    connection,
    concurrency: 5,
    limiter: {
      max: 10,
      duration: 1000,
    },
  })
}

export { connection as redisConnection }
