/**
 * Backend Connection Test
 * 
 * Test connection to Jimmy's AI Agent Suite backend.
 * 
 * Pattern: TEST × BACKEND × CONNECTION × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { UnifiedAPIClient } from './frontend-backend-api';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

console.log('🧪 Testing Backend Connection...\n');
console.log(`Backend URL: ${BACKEND_URL}\n`);

const client = new UnifiedAPIClient(BACKEND_URL);

async function testBackendConnection() {
  console.log('1️⃣ Testing Health Endpoint...');
  try {
    // Try direct fetch first
    const healthResponse = await fetch(`${BACKEND_URL}/health`);
    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      console.log('   ✅ Health check passed');
      console.log('   Response:', JSON.stringify(healthData, null, 2));
    } else {
      console.log(`   ⚠️  Health check returned status: ${healthResponse.status}`);
    }
  } catch (error: any) {
    console.log(`   ❌ Health check failed: ${error.message}`);
    console.log('   💡 Make sure backend is running on port 8000');
    return false;
  }

  console.log('\n2️⃣ Testing Protocol List...');
  try {
    const protocols = await client.listProtocols();
    console.log('   ✅ Protocol list retrieved');
    console.log(`   Found ${protocols.length} protocols`);
    if (protocols.length > 0) {
      console.log('   Sample protocols:');
      protocols.slice(0, 3).forEach((p: any) => {
        console.log(`     - ${p.name || p}`);
      });
    }
  } catch (error: any) {
    console.log(`   ⚠️  Protocol list failed: ${error.message}`);
  }

  console.log('\n3️⃣ Testing Protocol Execution...');
  try {
    const result = await client.executeProtocol('Secure Code Implementation', {
      data: { test: true }
    });
    if (result.success) {
      console.log('   ✅ Protocol execution successful');
      console.log('   Result:', JSON.stringify(result, null, 2).substring(0, 200) + '...');
    } else {
      console.log('   ⚠️  Protocol execution returned error:', result.error);
    }
  } catch (error: any) {
    console.log(`   ⚠️  Protocol execution failed: ${error.message}`);
  }

  console.log('\n4️⃣ Testing Memory Context...');
  try {
    const memory = await client.getMemoryContext('active');
    console.log('   ✅ Memory context retrieved');
    console.log('   Memory:', JSON.stringify(memory, null, 2).substring(0, 200) + '...');
  } catch (error: any) {
    console.log(`   ⚠️  Memory context failed: ${error.message}`);
  }

  console.log('\n✅ Backend connection tests complete!');
  return true;
}

// Run tests
testBackendConnection().catch(console.error);

