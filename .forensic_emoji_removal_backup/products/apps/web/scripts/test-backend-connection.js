#!/usr/bin/env node

/**
 * Backend Connection Test Script
 * 
 * Pattern: TEST × BACKEND × CONNECTION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Tests FastAPI backend connectivity and collaboration metrics endpoint.
 * 
 * Usage:
 *   node scripts/test-backend-connection.js
 *   or
 *   BACKEND_API_URL=http://localhost:8000 node scripts/test-backend-connection.js
 */

const BACKEND_API_URL = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const TIMEOUT = 5000 // 5 seconds

async function testBackendConnection() {
  console.log('🔍 Testing Backend Connection\n')
  console.log(`Backend URL: ${BACKEND_API_URL}\n`)
  
  // Test 1: Health check
  console.log('1️⃣ Testing health endpoint...')
  try {
    const healthResponse = await fetchWithTimeout(`${BACKEND_API_URL}/health`, TIMEOUT)
    if (healthResponse.ok) {
      const healthData = await healthResponse.json()
      console.log('✅ Health check passed')
      console.log(`   Status: ${healthData.status || 'unknown'}`)
      console.log(`   Operational: ${healthData.operational !== undefined ? healthData.operational : 'unknown'}\n`)
    } else {
      console.log(`❌ Health check failed: ${healthResponse.status}\n`)
    }
  } catch (error) {
    console.log(`❌ Health check failed: ${error.message}\n`)
  }
  
  // Test 2: Collaboration metrics endpoint
  console.log('2️⃣ Testing collaboration metrics endpoint...')
  try {
    const metricsResponse = await fetchWithTimeout(`${BACKEND_API_URL}/api/collaboration/metrics`, TIMEOUT)
    if (metricsResponse.ok) {
      const metricsData = await metricsResponse.json()
      console.log('✅ Collaboration metrics endpoint working')
      console.log(`   Partnership Strength: ${metricsData.metrics?.partnershipStrength || 'N/A'}%`)
      console.log(`   Total Collaborations: ${metricsData.metrics?.totalCollaborations || 'N/A'}`)
      console.log(`   Active Collaborations: ${metricsData.metrics?.activeCollaborations || 'N/A'}`)
      console.log(`   Success Rate: ${metricsData.metrics?.successRate || 'N/A'}%`)
      console.log(`   Data Source: ${metricsData.source || 'backend'}\n`)
    } else {
      console.log(`❌ Metrics endpoint failed: ${metricsResponse.status}\n`)
      const errorText = await metricsResponse.text()
      console.log(`   Error: ${errorText}\n`)
    }
  } catch (error) {
    console.log(`❌ Metrics endpoint failed: ${error.message}\n`)
  }
  
  // Test 3: Next.js API route (proxy)
  console.log('3️⃣ Testing Next.js API route (proxy)...')
  try {
    const proxyResponse = await fetchWithTimeout('http://localhost:3000/api/collaboration', TIMEOUT)
    if (proxyResponse.ok) {
      const proxyData = await proxyResponse.json()
      const dataSource = proxyResponse.headers.get('X-Data-Source') || 'unknown'
      console.log('✅ Next.js API route working')
      console.log(`   Data Source: ${dataSource}`)
      console.log(`   Partnership Strength: ${proxyData.metrics?.partnershipStrength || 'N/A'}%`)
      if (dataSource === 'fallback') {
        console.log(`   ⚠️  Using fallback data (backend unavailable)`)
      }
      console.log('')
    } else {
      console.log(`❌ Next.js API route failed: ${proxyResponse.status}\n`)
    }
  } catch (error) {
    console.log(`❌ Next.js API route failed: ${error.message}`)
    console.log(`   Note: Make sure Next.js dev server is running (npm run dev)\n`)
  }
  
  console.log('✅ Backend connection test complete\n')
}

function fetchWithTimeout(url, timeout) {
  return Promise.race([
    fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      },
    }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeout)
    ),
  ])
}

// Run test
testBackendConnection().catch((error) => {
  console.error('Test failed:', error)
  process.exit(1)
})

