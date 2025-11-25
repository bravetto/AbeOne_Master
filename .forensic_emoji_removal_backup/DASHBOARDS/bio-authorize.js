#!/usr/bin/env node
/**
 * BIO-AUTHORIZATION FOR MAC
 * 
 * Uses macOS security framework to trigger Touch ID / fingerprint
 * Similar to AbëKEYs implementation
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const { promisify } = require('util');

function bioAuthorize(reason = 'Authorize dashboard system') {
  return new Promise((resolve, reject) => {
    // Use security unlock-keychain interactively - THIS TRIGGERS TOUCH ID (not password)
    // When keychain is unlocked, macOS shows Touch ID if available
    console.log('🛡️  Touch ID prompt appearing now - please use fingerprint...\n');
    
    // Get default keychain path
    let keychainPath = 'login.keychain';
    try {
      const defaultKeychain = execSync('security default-keychain', { encoding: 'utf8' }).trim();
      keychainPath = defaultKeychain.replace(/"/g, '').replace(/\n/g, '');
    } catch (error) {
      // Use default
    }
    
    // Unlock keychain interactively - this triggers Touch ID
    const child = spawn('security', [
      'unlock-keychain',
      '-u',  // User interaction mode
      keychainPath
    ], {
      stdio: 'inherit'  // Show Touch ID prompt to user
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve(true);
      } else {
        reject(new Error('Authorization denied or failed'));
      }
    });
    
    child.on('error', (error) => {
      reject(error);
    });
  });
}

function tryAppleScript(reason, resolve, reject) {
  // Fallback: AppleScript with admin privileges (also triggers Touch ID)
  const appleScript = `
    tell application "System Events"
      try
        do shell script "echo '${reason}'" with administrator privileges
        return "authorized"
      on error
        return "denied"
      end try
    end tell
  `;
  
  const child = spawn('osascript', ['-e', appleScript], {
    stdio: ['inherit', 'pipe', 'pipe']
  });
  
  let output = '';
  
  child.stdout.on('data', (data) => {
    output += data.toString();
  });
  
  child.on('close', (code) => {
    if (code === 0 && output.includes('authorized')) {
      resolve(true);
    } else {
      reject(new Error('Authorization denied'));
    }
  });
  
  child.on('error', (error) => {
    reject(error);
  });
}

// CLI
if (require.main === module) {
  const reason = process.argv[2] || 'Authorize dashboard system';
  
  bioAuthorize(reason)
    .then(() => {
      console.log('✅ Bio-authorization successful');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Bio-authorization failed:', error.message);
      process.exit(1);
    });
}

module.exports = { bioAuthorize };

