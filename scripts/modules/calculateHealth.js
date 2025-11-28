#!/usr/bin/env node
/**
 * CALCULATE HEALTH
 * 
 * Calculates overall system health score
 * Based on component statuses
 */

function calculateHealth(status) {
  // Default health if no status provided
  if (!status) {
    return {
      score: 0,
      status: 'UNKNOWN',
      message: 'No status data available'
    };
  }

  let score = 100;
  const issues = [];

  // Backend health (30% weight)
  if (!status.backend || !status.backend.running) {
    score -= 30;
    issues.push('Backend not running');
  } else if (!status.backend.health) {
    score -= 10;
    issues.push('Backend health endpoint not responding');
  }

  // Extension health (20% weight)
  if (!status.extension || !status.extension.exists) {
    score -= 20;
    issues.push('Extension not found');
  } else if (status.extension.issues && status.extension.issues.length > 0) {
    score -= (status.extension.issues.length * 5); // -5 per issue, max -20
    issues.push(...status.extension.issues.map(i => `Extension: ${i}`));
  }

  // Git health (10% weight)
  if (!status.commit || status.commit === 'unknown') {
    score -= 10;
    issues.push('Git commit unknown');
  }

  // Ensure score doesn't go below 0
  score = Math.max(0, score);

  // Determine status
  let healthStatus = 'HEALTHY';
  if (score < 50) {
    healthStatus = 'CRITICAL';
  } else if (score < 75) {
    healthStatus = 'DEGRADED';
  } else if (score < 90) {
    healthStatus = 'WARNING';
  }

  return {
    score: Math.round(score),
    status: healthStatus,
    issues: issues,
    timestamp: new Date().toISOString()
  };
}

module.exports = calculateHealth;

