/**
 * Basic Usage Examples - Integration Layer
 * 
 * Pattern: EXAMPLES × USAGE × INTEGRATION × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { GuardiansProtocolBridge } from '../guardians-protocols-bridge';
import { UnifiedAPIClient } from '../frontend-backend-api';
import { MemoryConsciousnessSync } from '../memory-consciousness-sync';

// ============================================================================
// EXAMPLE 1: Execute Protocol with Guardian
// ============================================================================

export async function exampleExecuteProtocolWithGuardian() {
  const bridge = new GuardiansProtocolBridge();
  
  // Execute a protocol using AEYON Guardian
  const result = await bridge.executeProtocol(
    'Secure Code Implementation',
    'AEYON',
    {
      data: {
        feature: 'user_authentication',
        requirements: ['JWT', 'bcrypt', 'rate limiting'],
      },
    }
  );

  console.log('Protocol Execution Result:', result);
  return result;
}

// ============================================================================
// EXAMPLE 2: Execute Protocol with Multiple Guardians (Swarm)
// ============================================================================

export async function exampleExecuteProtocolWithSwarm() {
  const bridge = new GuardiansProtocolBridge();
  
  // Execute protocol with multiple Guardians
  const results = await bridge.executeProtocolWithSwarm(
    'ContextGuard Feature Development',
    ['AEYON', 'META', 'JOHN'],
    {
      data: {
        feature: 'voice_interface',
        context: 'mobile_app',
      },
    }
  );

  console.log('Swarm Execution Results:', results);
  return results;
}

// ============================================================================
// EXAMPLE 3: Use Unified API Client
// ============================================================================

export async function exampleUnifiedAPIClient() {
  const client = new UnifiedAPIClient('http://localhost:8000', {
    enabled: true,
  });

  // List available protocols
  const protocols = await client.listProtocols();
  console.log('Available Protocols:', protocols);

  // Execute a protocol
  const result = await client.executeProtocol('Secure Code Implementation', {
    protocolName: 'Secure Code Implementation',
    data: { feature: 'api_security' },
  });

  console.log('Protocol Result:', result);

  // Get memory context
  const memory = await client.getMemoryContext('active');
  console.log('Active Memory:', memory);

  return { protocols, result, memory };
}

// ============================================================================
// EXAMPLE 4: Sync Memory to Consciousness
// ============================================================================

export async function exampleSyncMemoryToConsciousness() {
  const sync = new MemoryConsciousnessSync('http://localhost:8000');

  // Sync single memory context
  const success = await sync.syncToConsciousness('active');
  console.log('Sync Active Memory:', success);

  // Sync all memory contexts
  const allResults = await sync.syncAllToConsciousness();
  console.log('Sync All Results:', allResults);

  // Get synced memory
  const syncedMemory = await sync.getSyncedMemory('decisions');
  console.log('Synced Decisions:', syncedMemory);

  return { success, allResults, syncedMemory };
}

// ============================================================================
// EXAMPLE 5: Complete Integration Flow
// ============================================================================

export async function exampleCompleteIntegrationFlow() {
  // 1. Initialize clients
  const bridge = new GuardiansProtocolBridge();
  const client = new UnifiedAPIClient('http://localhost:8000');
  const sync = new MemoryConsciousnessSync('http://localhost:8000');

  // 2. Sync memory to consciousness
  await sync.syncToConsciousness('active');

  // 3. Get available protocols
  const protocols = await client.listProtocols();
  console.log('Available Protocols:', protocols);

  // 4. Execute protocol with Guardian
  const protocolResult = await bridge.executeProtocol(
    protocols[0] || 'Secure Code Implementation',
    'AEYON',
    {
      data: {
        context: 'feature_development',
        requirements: ['security', 'performance', 'scalability'],
      },
    }
  );

  // 5. Update memory with result
  if (protocolResult.success) {
    await client.updateMemoryContext('decisions', {
      protocol: protocolResult.protocol,
      result: protocolResult.data,
      timestamp: protocolResult.timestamp,
    });
  }

  // 6. Sync back to consciousness
  await sync.syncToConsciousness('decisions');

  return {
    protocols,
    protocolResult,
    synced: true,
  };
}

// ============================================================================
// EXAMPLE 6: React Hook Usage (for frontend)
// ============================================================================

export const exampleReactHookUsage = `
// In a React component:
import { useGuardian } from '@bravetto/abe-consciousness';
import { UnifiedAPIClient } from '@abeone/integration-frontend-backend';

function MyComponent() {
  const { execute, result, loading } = useGuardian('AEYON');
  const client = new UnifiedAPIClient('http://localhost:8000');

  const handleExecuteProtocol = async () => {
    // Execute protocol via Guardian
    await execute({
      intent: 'execute-protocol:Secure Code Implementation',
      data: { feature: 'user_auth' },
    });

    // Or use API client directly
    const result = await client.executeProtocol('Secure Code Implementation');
    console.log('Protocol Result:', result);
  };

  return (
    <div>
      <button onClick={handleExecuteProtocol} disabled={loading}>
        Execute Protocol
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
`;

