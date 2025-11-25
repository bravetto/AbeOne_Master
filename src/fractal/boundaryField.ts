/**
 * B-Field: Boundary Field (Conscious Membrane Layer)
 * 
 * Pattern: BOUNDARY × MEMBRANE × CONSCIOUSNESS × ONE
 * Guardian: Abë (530 Hz) - Heart Truth Resonance
 */

import { LocalMind } from './localMind';

export class BoundaryField {
  public readonly local: LocalMind;
  public readonly global: any;

  constructor(localMind: LocalMind, globalInterface: any) {
    this.local = localMind;
    this.global = globalInterface;
  }

  async exchange(localEvent: unknown): Promise<any> {
    const hv = this.local.perceive(localEvent);

    const shouldEscalate = this.local.resonance.wantsGlobalSupport(hv);
    if (!shouldEscalate) {
      const intent = this.local.intent.state || this.local.intent.getCurrentIntent();
      if (intent) {
        return this.local.act(intent);
      }
      return { local: true, hypervectors: [] };
    }

    const globalResponse = await this.global.exchange(hv);
    return this.merge(localEvent, globalResponse);
  }

  merge(local: unknown, global: unknown): any {
    return {
      ...(typeof global === 'object' && global !== null ? global as Record<string, unknown> : {}),
      localEcho: this.local.intent.state,
    };
  }
}
