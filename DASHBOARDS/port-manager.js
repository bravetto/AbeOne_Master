#!/usr/bin/env node
/**
 * PORT MANAGER - ETERNAL PORT ASSIGNMENT
 * 
 * Ensures mockups/apps/websites/landing pages
 * always launch on clean unused ports
 * Prevents port conflicts
 * Eternal solution - no more port conflicts
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');
const portRegistryPath = path.join(__dirname, '.port-registry.json');
const registryPath = path.join(__dirname, 'DASHBOARD_REGISTRY.json');

function loadPortRegistry() {
  if (fs.existsSync(portRegistryPath)) {
    return JSON.parse(fs.readFileSync(portRegistryPath, 'utf8'));
  }
  
  // Initialize from dashboard registry
  const dashboardRegistry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
  const portConfig = dashboardRegistry.portManagement || {};
  
  return {
    _meta: {
      version: "1.0.0",
      lastUpdated: new Date().toISOString(),
      eternal: true
    },
    ports: {},
    reserved: portConfig.reservedPorts || [3000, 3001, 8000, 8080, 9090, 16686],
    range: portConfig.portRange || { min: 3000, max: 9999 },
    assignments: {}
  };
}

function savePortRegistry(registry) {
  registry._meta.lastUpdated = new Date().toISOString();
  fs.writeFileSync(portRegistryPath, JSON.stringify(registry, null, 2), 'utf8');
}

function isPortInUse(port) {
  try {
    // Check if port is listening
    const result = execSync(`lsof -ti:${port}`, { encoding: 'utf8', stdio: 'pipe' });
    return result.trim().length > 0;
  } catch (error) {
    return false;
  }
}

function findAvailablePort(registry, preferredPort = null) {
  const { min, max } = registry.range;
  const reserved = registry.reserved || [];
  
  // Try preferred port first if provided
  if (preferredPort && 
      preferredPort >= min && 
      preferredPort <= max &&
      !reserved.includes(preferredPort) &&
      !isPortInUse(preferredPort) &&
      !registry.assignments[preferredPort]) {
    return preferredPort;
  }
  
  // Find first available port
  for (let port = min; port <= max; port++) {
    if (reserved.includes(port)) continue;
    if (isPortInUse(port)) continue;
    if (registry.assignments[port]) continue;
    
    return port;
  }
  
  throw new Error(`No available ports in range ${min}-${max}`);
}

function assignPort(serviceName, preferredPort = null) {
  const registry = loadPortRegistry();
  
  // Check if already assigned
  const existing = Object.entries(registry.assignments).find(
    ([port, assignment]) => assignment.serviceName === serviceName
  );
  
  if (existing) {
    const port = parseInt(existing[0]);
    // Verify port is still available
    if (!isPortInUse(port)) {
      console.log(` Using existing assignment: ${serviceName} → port ${port}`);
      return port;
    } else {
      // Port is in use, reassign
      delete registry.assignments[existing[0]];
    }
  }
  
  // Find available port
  const port = findAvailablePort(registry, preferredPort);
  
  // Assign port
  registry.assignments[port] = {
    serviceName,
    assignedAt: new Date().toISOString(),
    lastUsed: new Date().toISOString(),
    status: 'assigned'
  };
  
  savePortRegistry(registry);
  console.log(` Assigned port ${port} to ${serviceName}`);
  
  return port;
}

function releasePort(port) {
  const registry = loadPortRegistry();
  
  if (registry.assignments[port]) {
    delete registry.assignments[port];
    savePortRegistry(registry);
    console.log(` Released port ${port}`);
    return true;
  }
  
  return false;
}

function listPorts() {
  const registry = loadPortRegistry();
  
  console.log('\n  PORT REGISTRY\n');
  console.log('Reserved Ports:', registry.reserved.join(', '));
  console.log('\nAssigned Ports:');
  
  if (Object.keys(registry.assignments).length === 0) {
    console.log('  (none)');
  } else {
    Object.entries(registry.assignments).forEach(([port, assignment]) => {
      const inUse = isPortInUse(parseInt(port)) ? ' IN USE' : '🟢 Available';
      console.log(`  Port ${port}: ${assignment.serviceName} (${inUse})`);
      console.log(`    Assigned: ${assignment.assignedAt}`);
      console.log(`    Last Used: ${assignment.lastUsed}`);
    });
  }
  
  console.log('\n');
}

function cleanupUnusedPorts() {
  const registry = loadPortRegistry();
  let cleaned = 0;
  
  Object.entries(registry.assignments).forEach(([port, assignment]) => {
    if (!isPortInUse(parseInt(port))) {
      delete registry.assignments[port];
      cleaned++;
    }
  });
  
  if (cleaned > 0) {
    savePortRegistry(registry);
    console.log(` Cleaned up ${cleaned} unused port assignments`);
  } else {
    console.log(' No unused ports to clean up');
  }
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'assign':
    const serviceName = args[1] || 'unknown-service';
    const preferredPort = args[2] ? parseInt(args[2]) : null;
    assignPort(serviceName, preferredPort);
    break;
    
  case 'release':
    const port = parseInt(args[1]);
    if (isNaN(port)) {
      console.error(' Invalid port number');
      process.exit(1);
    }
    releasePort(port);
    break;
    
  case 'list':
    listPorts();
    break;
    
  case 'cleanup':
    cleanupUnusedPorts();
    break;
    
  case 'get':
    const service = args[1];
    if (!service) {
      console.error(' Service name required');
      process.exit(1);
    }
    const assignedPort = assignPort(service);
    console.log(assignedPort);
    break;
    
  default:
    console.log(`
  PORT MANAGER - ETERNAL PORT ASSIGNMENT

Usage:
  node port-manager.js assign <service-name> [preferred-port]
  node port-manager.js release <port>
  node port-manager.js list
  node port-manager.js cleanup
  node port-manager.js get <service-name>

Examples:
  node port-manager.js assign my-app 3000
  node port-manager.js get landing-page
  node port-manager.js list
  node port-manager.js cleanup
`);
}

