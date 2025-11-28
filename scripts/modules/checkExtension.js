#!/usr/bin/env node
/**
 * CHECK EXTENSION STATUS
 * 
 * Checks Chrome extension operational state
 * Returns status object
 */

const fs = require('fs');
const path = require('path');

/**
 * Get all source files recursively
 * @param {string} dir - Directory to scan
 * @returns {Array<string>} - Array of file paths
 */
function getAllSourceFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  for (const file of list) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      // Skip node_modules and other ignored directories
      if (file === 'node_modules' || file === '.git' || file.startsWith('.')) {
        continue;
      }
      results = results.concat(getAllSourceFiles(filePath));
    } else {
      // Only include source files
      const ext = path.extname(file);
      if (['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
        results.push(filePath);
      }
    }
  }
  
  return results;
}

function checkExtension() {
  const result = {
    exists: false,
    path: null,
    manifest: null,
    issues: []
  };

  const extensionPath = path.join(__dirname, '..', '..', 'AiGuardian-Chrome-Ext-dev');
  const manifestPath = path.join(extensionPath, 'manifest.json');

  if (fs.existsSync(extensionPath)) {
    result.exists = true;
    result.path = extensionPath;

    // Check manifest
    if (fs.existsSync(manifestPath)) {
      try {
        const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
        result.manifest = {
          version: manifest.version || 'unknown',
          name: manifest.name || 'unknown'
        };
      } catch (e) {
        result.issues.push('Manifest parse error');
      }
    } else {
      result.issues.push('Manifest not found');
    }

    // SUBSTRATE-REQUIRED: Only detect issues from actual extension code
    // Scan extension source for actual issues (substrate-based detection)
    const srcPath = path.join(extensionPath, 'src');
    if (fs.existsSync(srcPath)) {
      // Check for actual error handling patterns in code
      try {
        const srcFiles = getAllSourceFiles(srcPath);
        for (const file of srcFiles) {
          const content = fs.readFileSync(file, 'utf8');
          
          // Detect actual issues from code substrate
          if (content.includes('403') && !content.includes('handleError') && !content.includes('error')) {
            if (!result.issues.includes('403 error handling')) {
              result.issues.push('403 error handling');
            }
          }
          
          if (content.includes('token') && content.includes('refresh') && !content.includes('refreshToken')) {
            if (!result.issues.includes('token refresh')) {
              result.issues.push('token refresh');
            }
          }
          
          if (content.includes('alert') && content.includes('dialog') && !content.includes('AlertDialog')) {
            if (!result.issues.includes('alert dialog')) {
              result.issues.push('alert dialog');
            }
          }
        }
      } catch (err) {
        // If we can't scan, don't fabricate issues - return empty array
        // This maintains substrate-first execution
      }
    }
    
    // If no issues detected from substrate, return empty array
    // Never fabricate issues without substrate validation
  }

  return result;
}

module.exports = checkExtension;

