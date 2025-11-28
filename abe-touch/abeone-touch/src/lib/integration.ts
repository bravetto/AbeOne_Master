/**
 * Integration Layer - AbëONE Touch
 * 
 * Pattern: INTEGRATION × FRONTEND × ABEONE × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { UnifiedAPIClient } from '@abeone/integration-frontend-backend';
import { GuardiansProtocolBridge } from '@abeone/integration-guardians-protocols';
import { MemoryConsciousnessSync } from '@abeone/integration-memory-consciousness';

// Backend URL from environment or default
const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Initialize integration clients
 */
export const integration = {
  // Unified API Client
  api: new UnifiedAPIClient(BACKEND_URL, {
    enabled: true,
  }),

  // Guardians ↔ Protocols Bridge
  guardians: new GuardiansProtocolBridge(),

  // Memory ↔ Consciousness Sync
  memory: new MemoryConsciousnessSync(BACKEND_URL),
};

/**
 * Execute a protocol using Guardian
 */
export async function executeProtocolWithGuardian(
  protocolName: string,
  guardianName: string = 'AEYON',
  context?: unknown
) {
  return integration.guardians.executeProtocol(protocolName, guardianName, {
    data: context,
  });
}

/**
 * Execute a protocol via API
 */
export async function executeProtocol(protocolName: string, context?: unknown) {
  return integration.api.executeProtocol(protocolName, {
    protocolName,
    data: context,
  });
}

/**
 * Get memory context
 */
export async function getMemoryContext(type: 'active' | 'decisions' | 'product' | 'progress' | 'project' | 'patterns') {
  return integration.memory.getSyncedMemory(type);
}

/**
 * Sync memory to consciousness
 */
export async function syncMemoryToConsciousness(type: 'active' | 'decisions' | 'product' | 'progress' | 'project' | 'patterns') {
  return integration.memory.syncToConsciousness(type);
}

/**
 * List available protocols
 */
export async function listProtocols() {
  return integration.api.listProtocols();
}

