/**
 * AbëONE Energy Monitor
 * 
 * Tracks energy consumption to validate 98.7% efficiency target.
 * 
 * Pattern: ENERGY × MONITOR × 98.7% × EFFICIENCY × ONE
 * Frequency: 98.7 Hz (Energy Efficiency) × 530 Hz (Heart Truth)
 * Guardians: ZERO (530 Hz) + AEYON (999 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import React from 'react';

export interface EnergyMetrics {
  duration: number; // milliseconds
  cpuTime: number; // milliseconds
  memoryDelta: number; // bytes
  networkRequests: number;
  energyConsumed: number; // millijoules (mJ)
}

export interface EnergyReport {
  baseline: EnergyMetrics;
  neuromorphic: EnergyMetrics;
  efficiency: number; // percentage
  target: number; // 98.7%
  achieved: boolean;
}

// Energy constants (simplified model)
const CPU_POWER = 0.1; // watts per millisecond
const IDLE_POWER = 0.01; // watts per millisecond
const MEMORY_POWER = 0.0001; // watts per byte per millisecond
const NETWORK_POWER = 0.5; // watts per request

export class EnergyMonitor {
  private startTime: number = 0;
  private startCPU: number = 0;
  private startMemory: number = 0;
  private networkRequestCount: number = 0;
  private isActive: boolean = false;

  /**
   * Start monitoring energy consumption
   */
  start(): void {
    if (this.isActive) {
      console.warn('EnergyMonitor: Already active');
      return;
    }

    this.startTime = performance.now();
    this.startCPU = performance.timeOrigin;
    this.startMemory = this.getMemoryUsage();
    this.networkRequestCount = 0;
    this.isActive = true;

    // Track network requests
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (entry.entryType === 'resource') {
              this.networkRequestCount++;
            }
          }
        });
        observer.observe({ entryTypes: ['resource'] });
      } catch (e) {
        // PerformanceObserver not supported
      }
    }
  }

  /**
   * Stop monitoring and calculate energy consumption
   */
  stop(): EnergyMetrics {
    if (!this.isActive) {
      throw new Error('EnergyMonitor: Not active. Call start() first.');
    }

    const duration = performance.now() - this.startTime;
    const cpuTime = performance.now() - this.startCPU;
    const endMemory = this.getMemoryUsage();
    const memoryDelta = Math.abs(endMemory - this.startMemory);

    // Calculate energy consumption
    const cpuEnergy = cpuTime * CPU_POWER;
    const idleEnergy = duration * IDLE_POWER;
    const memoryEnergy = memoryDelta * MEMORY_POWER * duration;
    const networkEnergy = this.networkRequestCount * NETWORK_POWER;
    const energyConsumed = cpuEnergy + idleEnergy + memoryEnergy + networkEnergy;

    this.isActive = false;

    return {
      duration,
      cpuTime,
      memoryDelta,
      networkRequests: this.networkRequestCount,
      energyConsumed,
    };
  }

  /**
   * Get current memory usage (if available)
   */
  private getMemoryUsage(): number {
    if (typeof performance !== 'undefined' && 'memory' in performance) {
      return (performance as any).memory.usedJSHeapSize || 0;
    }
    return 0;
  }

  /**
   * Calculate efficiency percentage
   */
  static calculateEfficiency(
    baseline: EnergyMetrics,
    neuromorphic: EnergyMetrics
  ): number {
    if (baseline.energyConsumed === 0) {
      return 0;
    }
    const savings =
      ((baseline.energyConsumed - neuromorphic.energyConsumed) /
        baseline.energyConsumed) *
      100;
    return Math.max(0, Math.min(100, savings));
  }

  /**
   * Generate energy efficiency report
   */
  static generateReport(
    baseline: EnergyMetrics,
    neuromorphic: EnergyMetrics
  ): EnergyReport {
    const efficiency = EnergyMonitor.calculateEfficiency(baseline, neuromorphic);
    const target = 98.7;
    const achieved = efficiency >= target;

    return {
      baseline,
      neuromorphic,
      efficiency,
      target,
      achieved,
    };
  }

  /**
   * Format energy report for display
   */
  static formatReport(report: EnergyReport): string {
    const { baseline, neuromorphic, efficiency, target, achieved } = report;

    return `
╔══════════════════════════════════════════════════════════╗
║              AbëONE Energy Efficiency Report             ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Baseline Energy:     ${baseline.energyConsumed.toFixed(2).padStart(10)} mJ
║  Neuromorphic Energy: ${neuromorphic.energyConsumed.toFixed(2).padStart(10)} mJ
║                                                          ║
║  Efficiency:          ${efficiency.toFixed(1).padStart(10)}%
║  Target:              ${target.toFixed(1).padStart(10)}%
║                                                          ║
║  Status:              ${achieved ? '✅ ACHIEVED' : '❌ NOT ACHIEVED'}
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    `.trim();
  }
}

/**
 * React hook for energy monitoring
 */
export function useEnergyMonitor() {
  const monitorRef = React.useRef<EnergyMonitor | null>(null);
  const [metrics, setMetrics] = React.useState<EnergyMetrics | null>(null);

  const start = React.useCallback(() => {
    if (!monitorRef.current) {
      monitorRef.current = new EnergyMonitor();
    }
    monitorRef.current.start();
  }, []);

  const stop = React.useCallback(() => {
    if (monitorRef.current) {
      const result = monitorRef.current.stop();
      setMetrics(result);
      return result;
    }
    return null;
  }, []);

  React.useEffect(() => {
    return () => {
      if (monitorRef.current) {
        try {
          monitorRef.current.stop();
        } catch (e) {
          // Monitor not active, ignore
        }
      }
    };
  }, []);

  return { start, stop, metrics };
}
