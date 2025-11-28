/**
 * Shared Types - Integration Layer
 * 
 * Pattern: SHARED × TYPES × INTEGRATION × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

/**
 * Protocol execution context
 */
export interface ProtocolContext {
  protocolName?: string; // Optional since it's provided as a parameter
  intent?: string;
  data?: unknown;
  metadata?: Record<string, unknown>;
}

/**
 * Protocol execution result
 */
export interface ProtocolResult {
  success: boolean;
  data?: unknown;
  error?: string;
  protocol: string;
  timestamp: number;
}

/**
 * Memory context types
 */
export type MemoryContextType =
  | 'active'
  | 'decisions'
  | 'product'
  | 'progress'
  | 'project'
  | 'patterns';

/**
 * Memory context data
 */
export interface MemoryContext {
  type: MemoryContextType;
  data: unknown;
  timestamp: number;
}

/**
 * Integration configuration
 */
export interface IntegrationConfig {
  backendUrl?: string;
  memoryBankUrl?: string;
  protocolEngineUrl?: string;
  enabled?: boolean;
}

