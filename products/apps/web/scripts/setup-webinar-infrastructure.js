#!/usr/bin/env node
/**
 * Interactive Webinar Infrastructure Setup
 * Pattern: SETUP × CREDENTIALS × VALIDATION × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (YOU)
 * 
 * Helps you quickly configure all required credentials
 */

const fs = require('fs')
const path = require('path')
const readline = require('readline')

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
})

function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, resolve)
  })
}

async function setup() {
  console.log('\n WEBINAR INFRASTRUCTURE SETUP \n')
  console.log('This script will help you configure all required credentials.\n')
  console.log('You can skip any step by pressing Enter (we\'ll use defaults or show you how to set up later).\n')

  const env = {}

  // Database Setup
  console.log('')
  console.log(' DATABASE SETUP')
  console.log('\n')
  console.log('Options:')
  console.log('  1. Neon (neon.tech) - Free tier available, recommended')
  console.log('  2. Supabase (supabase.com) - Free tier available')
  console.log('  3. Local PostgreSQL')
  console.log('  4. Other PostgreSQL provider\n')

  const dbChoice = await question('Choose database option (1-4) or Enter to skip: ')
  
  if (dbChoice === '1') {
    console.log('\n Neon Setup Instructions:')
    console.log('  1. Go to https://neon.tech and sign up')
    console.log('  2. Create a new project')
    console.log('  3. Copy the connection string (it looks like: REPLACE_MEhost/dbname)\n')
    env.DATABASE_URL = await question('Paste your Neon DATABASE_URL: ')
  } else if (dbChoice === '2') {
    console.log('\n Supabase Setup Instructions:')
    console.log('  1. Go to https://supabase.com and sign up')
    console.log('  2. Create a new project')
    console.log('  3. Go to Settings > Database')
    console.log('  4. Copy the connection string\n')
    env.DATABASE_URL = await question('Paste your Supabase DATABASE_URL: ')
  } else if (dbChoice === '3') {
    console.log('\n Local PostgreSQL:')
    env.DATABASE_URL = await question('Enter DATABASE_URL (e.g., REPLACE_MElocalhost:5432/webinar): ')
  } else if (dbChoice === '4') {
    env.DATABASE_URL = await question('Enter your DATABASE_URL: ')
  }

  // Redis Setup
  console.log('\n')
  console.log(' REDIS SETUP (for rate limiting & job queue)')
  console.log('\n')
  console.log('Options:')
  console.log('  1. Upstash Redis (upstash.com) - Free tier, recommended for production')
  console.log('  2. Local Redis (for development)')
  console.log('  3. Skip for now (will use in-memory fallback)\n')

  const redisChoice = await question('Choose Redis option (1-3) or Enter to skip: ')

  if (redisChoice === '1') {
    console.log('\n Upstash Setup Instructions:')
    console.log('  1. Go to https://upstash.com and sign up')
    console.log('  2. Create a new Redis database')
    console.log('  3. Copy the REST URL and Token\n')
    env.UPSTASH_REDIS_REST_URL = await question('Paste UPSTASH_REDIS_REST_URL: ')
    env.UPSTASH_REDIS_REST_TOKEN = await question('Paste UPSTASH_REDIS_REST_TOKEN: ')
  } else if (redisChoice === '2') {
    console.log('\n Local Redis:')
    console.log('  Install: brew install redis (macOS) or sudo apt-get install redis-server (Linux)')
    console.log('  Start: redis-server\n')
    env.REDIS_URL = await question('Enter REDIS_URL (default: redis://localhost:6379): ') || 'redis://localhost:6379'
  }

  // SendGrid Setup
  console.log('\n')
  console.log(' SENDGRID SETUP (for email automation)')
  console.log('\n')
  console.log(' SendGrid Setup Instructions:')
  console.log('  1. Go to https://sendgrid.com and sign up (free tier: 100 emails/day)')
  console.log('  2. Go to Settings > API Keys')
  console.log('  3. Create a new API Key with "Mail Send" permissions')
  console.log('  4. Copy the API key (you can only see it once!)\n')

  env.SENDGRID_API_KEY = await question('Paste SENDGRID_API_KEY (or Enter to skip): ')
  
  if (env.SENDGRID_API_KEY) {
    env.SENDGRID_FROM_EMAIL = await question('From email (default: noreply@aiguardian.ai): ') || 'noreply@aiguardian.ai'
    env.SENDGRID_FROM_NAME = await question('From name (default: AiGuardian Team): ') || 'AiGuardian Team'
  }

  // Optional: API URLs
  console.log('\n')
  console.log(' OPTIONAL: API URLs')
  console.log('\n')
  
  const apiUrl = await question('NEXT_PUBLIC_API_URL (or Enter to skip): ')
  if (apiUrl) env.NEXT_PUBLIC_API_URL = apiUrl

  const webinarApiUrl = await question('NEXT_PUBLIC_WEBINAR_API_URL (or Enter to skip): ')
  if (webinarApiUrl) env.NEXT_PUBLIC_WEBINAR_API_URL = webinarApiUrl

  // Write .env file
  console.log('\n')
  console.log(' SAVING CONFIGURATION')
  console.log('\n')

  const envPath = path.join(process.cwd(), '.env')
  const envContent = Object.entries(env)
    .filter(([_, value]) => value && value.trim())
    .map(([key, value]) => `${key}="${value}"`)
    .join('\n')

  // Read existing .env if it exists
  let existingEnv = ''
  if (fs.existsSync(envPath)) {
    existingEnv = fs.readFileSync(envPath, 'utf8')
    // Remove old webinar-related vars
    existingEnv = existingEnv
      .split('\n')
      .filter(line => {
        const key = line.split('=')[0]
        return !['DATABASE_URL', 'REDIS_URL', 'UPSTASH_REDIS_REST_URL', 'UPSTASH_REDIS_REST_TOKEN', 
                 'SENDGRID_API_KEY', 'SENDGRID_FROM_EMAIL', 'SENDGRID_FROM_NAME',
                 'NEXT_PUBLIC_API_URL', 'NEXT_PUBLIC_WEBINAR_API_URL'].includes(key)
      })
      .join('\n')
  }

  const finalEnv = existingEnv + (existingEnv ? '\n\n' : '') + '# Webinar Infrastructure Configuration\n' + envContent + '\n'
  
  fs.writeFileSync(envPath, finalEnv)
  console.log(' Configuration saved to .env file\n')

  // Show next steps
  console.log('')
  console.log(' NEXT STEPS')
  console.log('\n')

  if (env.DATABASE_URL) {
    console.log('1.  Database configured')
    console.log('   Run: npm run db:migrate')
    console.log('   Then: npm run db:generate\n')
  } else {
    console.log('1.   Database not configured')
    console.log('   Set DATABASE_URL in .env and run: npm run db:migrate\n')
  }

  if (env.UPSTASH_REDIS_REST_URL || env.REDIS_URL) {
    console.log('2.  Redis configured')
  } else {
    console.log('2.   Redis not configured (using in-memory fallback)')
    console.log('   For production, set up Upstash Redis\n')
  }

  if (env.SENDGRID_API_KEY) {
    console.log('3.  SendGrid configured')
    console.log('   Start worker: npm run webinar:worker\n')
  } else {
    console.log('3.   SendGrid not configured')
    console.log('   Set SENDGRID_API_KEY in .env to enable email automation\n')
  }

  console.log('4. Activate new registration API:')
  console.log('   mv app/api/webinar/register/route.ts app/api/webinar/register/route.old.ts')
  console.log('   mv app/api/webinar/register/route.new.ts app/api/webinar/register/route.ts\n')

  console.log('5. Start development server:')
  console.log('   npm run dev\n')

  console.log('')
  console.log(' Setup complete! Check .env file for your configuration.')
  console.log('\n')

  rl.close()
}

setup().catch((error) => {
  console.error(' Setup error:', error)
  rl.close()
  process.exit(1)
})

