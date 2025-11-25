#!/usr/bin/env node
/**
 * CHECK BACKEND STATUS
 * 
 * Checks if backend server is running on port 8000
 * Returns status object
 */

const { execSync } = require('child_process');

function checkBackend() {
  const result = {
    running: false,
    port: 8000,
    health: null,
    error: null
  };

  try {
    // Check if port 8000 is in use
    const portCheck = execSync('lsof -i :8000 2>/dev/null || echo ""', { encoding: 'utf8' });
    if (portCheck.trim()) {
      result.running = true;
      
      // Try health check
      try {
        const healthResponse = execSync('curl -s --max-time 2 http://localhost:8000/health 2>/dev/null || echo ""', { encoding: 'utf8' });
        if (healthResponse.trim()) {
          result.health = healthResponse.trim();
        }
      } catch (e) {
        // Health endpoint may not exist or may be slow
        result.health = null;
      }
    }
  } catch (error) {
    result.error = error.message;
  }

  return result;
}

module.exports = checkBackend;

