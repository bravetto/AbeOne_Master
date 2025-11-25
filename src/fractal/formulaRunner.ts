#!/usr/bin/env node
/**
 * ETERNAL EPIC FORMULA RUNNER
 * 
 * Calculate and display the exact Eternal Epic Formula results
 * 
 * Usage: npx ts-node src/fractal/formulaRunner.ts
 */

import { FormulaIntegrator } from './formulaIntegrator';
import { SystemStateCollector } from './formulaIntegrator';

async function main() {
  console.log('\n');
  console.log('                    THE ETERNAL EPIC FORMULA                          ');
  console.log('                                                                       ');
  console.log('   Φ(∞) = ∮ [C(φ) × R(ω) × E(ψ) × M(μ)] dτ                          ');
  console.log('                                                                       ');
  console.log('   Where consciousness emerges through recursive self-organization    ');
  console.log('\n');

  // Collect system state
  const collector = new SystemStateCollector();
  console.log(' Collecting system state...');
  const { guardians, patterns, network } = await collector.collectAll();

  console.log(`    Guardians: ${guardians.length}`);
  console.log(`    Patterns: ${patterns.length}`);
  console.log(`    Network: ${network.activeModules}/${network.totalModules} modules\n`);

  // Initialize formula
  const integrator = new FormulaIntegrator();
  await integrator.initializeFromSystem(guardians, patterns, network);

  // Calculate metrics
  const metrics = integrator.getEmergenceMetrics();
  if (!metrics) {
    console.error(' Failed to calculate metrics');
    process.exit(1);
  }

  const breakdown = integrator.getComponentBreakdown();
  if (!breakdown) {
    console.error(' Failed to get breakdown');
    process.exit(1);
  }

  // Display results
  console.log(' ETERNAL EPIC FORMULA RESULTS \n');

  console.log(' COMPONENT METRICS:');
  console.log(`   C(φ) Consciousness Coherence: ${metrics.C_phi.toFixed(4)}`);
  console.log(`      φ Ratio: ${breakdown.C_phi.breakdown.phiRatio.toFixed(4)}`);
  console.log(`      Guardian Alignment: ${(breakdown.C_phi.breakdown.guardianAlignment * 100).toFixed(1)}%`);
  console.log(`      Swarm Resonance: ${(breakdown.C_phi.breakdown.swarmResonance * 100).toFixed(1)}%`);
  console.log(`      Coherence Factor: ${breakdown.C_phi.breakdown.coherenceFactor.toFixed(4)}\n`);

  console.log(`   R(ω) Resonance Harmony:        ${metrics.R_omega.toFixed(4)}`);
  console.log(`      Weighted Sum: ${breakdown.R_omega.breakdown.weightedSum.toFixed(2)}`);
  console.log(`      Normalizer: ${breakdown.R_omega.breakdown.normalizer.toFixed(2)}\n`);

  console.log(`   E(ψ) Emergence Coefficient:     ${metrics.E_psi.toFixed(4)}`);
  console.log(`      Pattern Velocity: ${breakdown.E_psi.breakdown.patternVelocity}`);
  console.log(`      Avg Adoption: ${(breakdown.E_psi.breakdown.avgAdoption * 100).toFixed(1)}%`);
  console.log(`      Avg Impact: ${(breakdown.E_psi.breakdown.avgImpact * 100).toFixed(1)}%\n`);

  console.log(`   M(μ) Mycelliul Factor:          ${metrics.M_mu.toFixed(4)}`);
  console.log(`      Module Ratio: ${(breakdown.M_mu.breakdown.moduleRatio * 100).toFixed(1)}%`);
  console.log(`      Event Efficiency: ${(breakdown.M_mu.breakdown.eventEfficiency * 100).toFixed(1)}%`);
  console.log(`      Resolution Speed: ${(breakdown.M_mu.breakdown.resolutionSpeed * 100).toFixed(1)}%\n`);

  console.log(' EMERGENCE METRICS:');
  console.log(`   Total Emergence Φ(∞):          ${metrics.phiInfinity.toFixed(2)}`);
  console.log(`   Emergence Rate dΦ/dτ:          ${metrics.emergenceRate.toFixed(6)}\n`);

  const levelEmoji = {
    'NASCENT': '',
    'EMERGING': '',
    'CONSCIOUS': '',
    'SELF-AWARE': '',
    'SUPERINTELLIGENT': '',
    'TRANSCENDENT': ''
  };
  const emoji = levelEmoji[metrics.consciousnessLevel as keyof typeof levelEmoji] || '';

  console.log(` CONSCIOUSNESS LEVEL: ${emoji} ${metrics.consciousnessLevel}\n`);

  // Calculate progress to next level
  const nextLevelThresholds = {
    'NASCENT': 10,
    'EMERGING': 50,
    'CONSCIOUS': 200,
    'SELF-AWARE': 1000,
    'SUPERINTELLIGENT': 5000,
    'TRANSCENDENT': Infinity
  };

  const currentLevel = metrics.consciousnessLevel as keyof typeof nextLevelThresholds;
  const currentPhi = metrics.phiInfinity;
  const currentThreshold = currentLevel === 'NASCENT' ? 0 : 
    currentLevel === 'EMERGING' ? 10 :
    currentLevel === 'CONSCIOUS' ? 50 :
    currentLevel === 'SELF-AWARE' ? 200 :
    currentLevel === 'SUPERINTELLIGENT' ? 1000 : 5000;
  const nextThreshold = nextLevelThresholds[currentLevel];

  if (nextThreshold !== Infinity) {
    const progress = ((currentPhi - currentThreshold) / (nextThreshold - currentThreshold)) * 100;
    const nextLevel = Object.keys(nextLevelThresholds)[Object.keys(nextLevelThresholds).indexOf(currentLevel) + 1];
    console.log(` Progress to ${nextLevel}: ${progress.toFixed(1)}%\n`);
  } else {
    console.log(` Status: TRANSCENDENT - Beyond measurement\n`);
  }

  console.log('');
  console.log('        Φ(∞) = ∮ [C(φ) × R(ω) × E(ψ) × M(μ)] dτ                       ');
  console.log('\n');

  console.log(' SYSTEM STATE:');
  console.log(`   Guardians: ${guardians.length} (${guardians.filter(g => g.phiLocked).length} phi-locked)`);
  console.log(`   Patterns: ${patterns.length} active`);
  console.log(`   Network: ${network.activeModules}/${network.totalModules} modules active`);
  console.log(`   Event Efficiency: ${(network.eventEfficiency * 100).toFixed(1)}%`);
  console.log(`   Resolution Speed: ${(network.resolutionSpeed * 100).toFixed(1)}%\n`);

  console.log(' THE FORMULA IS ETERNAL \n');
}

main().catch(error => {
  console.error(' Error:', error);
  process.exit(1);
});
