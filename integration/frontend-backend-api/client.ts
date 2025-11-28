/**
 * Frontend ↔ Backend API Client
 * 
 * Pattern: FRONTEND × BACKEND × API × CLIENT × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { APIClient } from '@bravetto/abe-core-body';
import type { ProtocolContext, ProtocolResult, MemoryContext, MemoryContextType, IntegrationConfig } from '../shared-types';

/**
 * Unified API Client connecting AbëONE Frontend with Jimmy's Backend
 */
export class UnifiedAPIClient extends APIClient {
  private config: IntegrationConfig;

  constructor(baseURL: string, config?: IntegrationConfig) {
    super(baseURL);
    this.config = {
      backendUrl: baseURL,
      enabled: true,
      ...config,
    };
  }

  /**
   * Execute a protocol via backend
   */
  async executeProtocol(
    protocolName: string,
    context?: ProtocolContext
  ): Promise<ProtocolResult> {
    if (!this.config.enabled) {
      throw new Error('Integration is disabled');
    }

    try {
      const result = await this.post<ProtocolResult>(
        '/api/protocols/execute',
        {
          protocol: protocolName,
          context: context || {},
        }
      );
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        protocol: protocolName,
        timestamp: Date.now(),
      };
    }
  }

  /**
   * Get memory context from backend
   */
  async getMemoryContext(contextType: MemoryContextType): Promise<MemoryContext | null> {
    if (!this.config.enabled) {
      return null;
    }

    try {
      const result = await this.get<MemoryContext>(
        `/api/memory/${contextType}`
      );
      return result;
    } catch (error) {
      console.error(`Failed to get memory context ${contextType}:`, error);
      return null;
    }
  }

  /**
   * Update memory context in backend
   */
  async updateMemoryContext(
    contextType: MemoryContextType,
    data: unknown
  ): Promise<boolean> {
    if (!this.config.enabled) {
      return false;
    }

    try {
      await this.post(`/api/memory/${contextType}`, { data });
      return true;
    } catch (error) {
      console.error(`Failed to update memory context ${contextType}:`, error);
      return false;
    }
  }

  /**
   * List available protocols
   */
  async listProtocols(): Promise<string[]> {
    if (!this.config.enabled) {
      return [];
    }

    try {
      const result = await this.get<string[]>('/api/protocols');
      return result;
    } catch (error) {
      console.error('Failed to list protocols:', error);
      return [];
    }
  }

  /**
   * Get protocol details
   */
  async getProtocolDetails(protocolName: string): Promise<unknown> {
    if (!this.config.enabled) {
      return null;
    }

    try {
      const result = await this.get(`/api/protocols/${protocolName}`);
      return result;
    } catch (error) {
      console.error(`Failed to get protocol details for ${protocolName}:`, error);
      return null;
    }
  }
}

