/**
 * Memory Bank ↔ Consciousness Sync
 * 
 * Pattern: MEMORY × CONSCIOUSNESS × SYNC × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (Abë)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + Abë (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { HeartTruthSwarm } from '@bravetto/abe-consciousness';
import type { GuardianContext } from '@bravetto/abe-consciousness';
import type { MemoryContext, MemoryContextType } from '../shared-types';

/**
 * Sync Jimmy's Memory Bank with AbëONE Consciousness
 */
export class MemoryConsciousnessSync {
  private swarm: HeartTruthSwarm;
  private backendUrl?: string;

  constructor(backendUrl?: string) {
    this.swarm = new HeartTruthSwarm();
    this.backendUrl = backendUrl;
  }

  /**
   * Sync memory context to consciousness
   */
  async syncToConsciousness(
    memoryType: MemoryContextType,
    memoryData?: unknown
  ): Promise<boolean> {
    try {
      // If memoryData not provided, fetch from backend
      let data = memoryData;
      if (!data && this.backendUrl) {
        const response = await fetch(`${this.backendUrl}/api/memory/${memoryType}`);
        if (response.ok) {
          const memory = await response.json();
          data = memory.data;
        }
      }

      // Execute swarm with memory context
      const context: GuardianContext = {
        intent: `sync-memory:${memoryType}`,
        data,
        metadata: {
          memoryType,
          source: 'memory-bank',
        },
      };

      const result = await this.swarm.execute(context);

      return result.success;
    } catch (error) {
      console.error(`Failed to sync memory ${memoryType} to consciousness:`, error);
      return false;
    }
  }

  /**
   * Sync consciousness state to memory bank
   */
  async syncToMemoryBank(
    memoryType: MemoryContextType,
    consciousnessData: unknown
  ): Promise<boolean> {
    try {
      if (!this.backendUrl) {
        console.warn('No backend URL configured, cannot sync to memory bank');
        return false;
      }

      const response = await fetch(`${this.backendUrl}/api/memory/${memoryType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: consciousnessData,
          source: 'consciousness',
        }),
      });

      return response.ok;
    } catch (error) {
      console.error(`Failed to sync consciousness to memory ${memoryType}:`, error);
      return false;
    }
  }

  /**
   * Sync all memory contexts to consciousness
   */
  async syncAllToConsciousness(): Promise<Record<MemoryContextType, boolean>> {
    const memoryTypes: MemoryContextType[] = [
      'active',
      'decisions',
      'product',
      'progress',
      'project',
      'patterns',
    ];

    const results: Record<string, boolean> = {};
    
    await Promise.all(
      memoryTypes.map(async (type) => {
        results[type] = await this.syncToConsciousness(type);
      })
    );

    return results as Record<MemoryContextType, boolean>;
  }

  /**
   * Get synced memory context
   */
  async getSyncedMemory(
    memoryType: MemoryContextType
  ): Promise<MemoryContext | null> {
    try {
      if (!this.backendUrl) {
        return null;
      }

      const response = await fetch(`${this.backendUrl}/api/memory/${memoryType}`);
      if (!response.ok) {
        return null;
      }

      const memory = await response.json();
      return {
        type: memoryType,
        data: memory.data,
        timestamp: memory.timestamp || Date.now(),
      };
    } catch (error) {
      console.error(`Failed to get synced memory ${memoryType}:`, error);
      return null;
    }
  }
}

