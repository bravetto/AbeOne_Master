#!/usr/bin/env node
/**
 * PULSE - Manual Synchronization
 * 
 * Manually triggers source of truth update and dashboard generation
 * Use when you want to synchronize everything
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 */

console.log("PULSE: Updating organism state...\n");

// Update source of truth
try {
  require('./update-source-of-truth');
  console.log("[OK] Source of truth updated\n");
} catch (error) {
  console.error("[ERROR] Error updating source of truth:", error.message);
  process.exit(1);
}

// Generate dashboards
try {
  require('./generate-dashboards');
  console.log("[OK] Dashboards generated\n");
} catch (error) {
  console.error("[ERROR] Error generating dashboards:", error.message);
  process.exit(1);
}

console.log("PULSE COMPLETE");

