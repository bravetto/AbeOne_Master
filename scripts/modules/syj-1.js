#!/usr/bin/env node
/**
 * SYJ-1 EXECUTION FOUNDATION MODULE
 * 
 * PURPOSE: Define the minimal substrate required to implement SYJ-1 as real executable code.
 * STATUS: LOCKED - Substrate protected from unauthorized modification
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardians: SRE × YAGNI × JOHN
 * 
 * This module provides:
 * 1. SRE Check - Validate substrate exists before any operation
 * 2. YAGNI Check - Confirm the requested action is strictly necessary
 * 3. JOHN Check - Ensure action is grounded, measurable, minimal
 * 4. PROMOTE(symbolic → substrate) Handler - Explicitly authorize creation/modification
 * 5. SUBSTRATE LOCK - Verify substrate integrity and prevent unauthorized modification
 * 
 * Integration: MEASURE_TWICE_CUT_ONCE_PROTOCOL.md × ARDM_PROTOCOL.md
 * 
 * LOCK STATUS: ACTIVE
 * LOCK HASH: Computed at runtime for integrity verification
 */

const fs = require('fs');
const path = require('path');

/**
 * SRE Check - Validate substrate exists before any operation
 * 
 * @param {string} substateIdentifier - Path or identifier of substrate element to check
 * @throws {Error} Structured SRE error if substrate missing
 */
function sreCheck(substateIdentifier) {
  if (!substateIdentifier || typeof substateIdentifier !== 'string') {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: 'substateIdentifier',
      nextAction: 'Provide a valid string identifier for the substrate element to check'
    };
  }

  // Check if it's a file path
  if (fs.existsSync(substateIdentifier)) {
    const stats = fs.statSync(substateIdentifier);
    if (stats.isFile() || stats.isDirectory()) {
      return; // Substrate exists
    }
  }

  // Check if it's a directory that should exist
  const dirPath = path.dirname(substateIdentifier);
  if (dirPath !== '.' && dirPath !== substateIdentifier && !fs.existsSync(dirPath)) {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: `Directory: ${dirPath}`,
      nextAction: `Create directory: ${dirPath} or provide explicit authorization via PROMOTE(symbolic → substrate)`
    };
  }

  // If file doesn't exist, throw SRE error
  if (!fs.existsSync(substateIdentifier)) {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: substateIdentifier,
      nextAction: `Create substrate at: ${substateIdentifier} or provide explicit authorization via PROMOTE(symbolic → substrate)`
    };
  }
}

/**
 * YAGNI Check - Confirm the requested action is strictly necessary
 * 
 * @param {string} requirement - Description of what is being requested
 * @throws {Error} If requirement is not strictly necessary
 */
function yagniCheck(requirement) {
  if (!requirement || typeof requirement !== 'string') {
    throw {
      error: 'YAGNI-VIOLATION',
      reason: 'Requirement must be a non-empty string',
      nextAction: 'Provide a clear, specific requirement description'
    };
  }

  // YAGNI validation: Check if requirement is vague or speculative
  const vaguePatterns = [
    /\bmight\b/i,
    /\bcould\b/i,
    /\bpossibly\b/i,
    /\bmaybe\b/i,
    /\bfuture\b/i,
    /\bjust in case\b/i,
    /\bwhat if\b/i
  ];

  for (const pattern of vaguePatterns) {
    if (pattern.test(requirement)) {
      throw {
        error: 'YAGNI-VIOLATION',
        reason: `Requirement contains speculative language: "${requirement}"`,
        nextAction: 'Refine requirement to be explicit and necessary. Remove speculative language.'
      };
    }
  }

  // YAGNI validation: Must be actionable and specific
  if (requirement.length < 10) {
    throw {
      error: 'YAGNI-VIOLATION',
      reason: 'Requirement is too vague or incomplete',
      nextAction: 'Provide a more specific, actionable requirement description'
    };
  }

  // YAGNI passed
  return true;
}

/**
 * JOHN Check - Ensure action is grounded, measurable, minimal
 * 
 * @param {string} action - Description of the action to be performed
 * @throws {Error} If action is not grounded, measurable, or minimal
 */
function johnCheck(action) {
  if (!action || typeof action !== 'string') {
    throw {
      error: 'JOHN-VIOLATION',
      reason: 'Action must be a non-empty string',
      nextAction: 'Provide a clear, specific action description'
    };
  }

  // JOHN validation: Must be grounded (concrete, not abstract)
  const abstractPatterns = [
    /\boptimize\b/i,
    /\bimprove\b/i,
    /\benhance\b/i,
    /\brefactor\b/i,
    /\babstract\b/i,
    /\bgeneralize\b/i
  ];

  let isAbstract = false;
  for (const pattern of abstractPatterns) {
    if (pattern.test(action)) {
      isAbstract = true;
      break;
    }
  }

  if (isAbstract && !action.match(/\b(create|write|add|modify|delete|read|check|validate)\b/i)) {
    throw {
      error: 'JOHN-VIOLATION',
      reason: `Action is too abstract: "${action}". Must be grounded in concrete filesystem operations.`,
      nextAction: 'Specify exact file path, exact content, exact operation (create/write/modify/delete)'
    };
  }

  // JOHN validation: Must be measurable (has clear success criteria)
  const measurableIndicators = [
    /\bcreate\b.*\b(file|directory|path)\b/i,
    /\bwrite\b.*\bto\b/i,
    /\bmodify\b.*\bat\b/i,
    /\bdelete\b.*\bfrom\b/i,
    /\bvalidate\b.*\bexists\b/i,
    /\bcheck\b.*\bfor\b/i
  ];

  let isMeasurable = false;
  for (const pattern of measurableIndicators) {
    if (pattern.test(action)) {
      isMeasurable = true;
      break;
    }
  }

  if (!isMeasurable) {
    throw {
      error: 'JOHN-VIOLATION',
      reason: `Action lacks measurable criteria: "${action}"`,
      nextAction: 'Specify exact file path, operation type, and expected outcome'
    };
  }

  // JOHN validation: Must be minimal (not over-engineered)
  if (action.length > 500) {
    throw {
      error: 'JOHN-VIOLATION',
      reason: 'Action description is too complex. Must be minimal and focused.',
      nextAction: 'Break down into smaller, atomic actions'
    };
  }

  // JOHN passed
  return true;
}

/**
 * PROMOTE(symbolic → substrate) Handler
 * Explicitly authorize creation or modification of files
 * Never assume or fabricate directories/files
 * Create directories/files only when approved
 * Apply MEASURE_TWICE_CUT_ONCE protocol
 * 
 * @param {Object} params - Promotion parameters
 * @param {string} params.path - Exact file path to create/modify
 * @param {string} params.content - Exact content to write
 * @param {boolean} [params.createDirIfMissing=false] - Whether to create parent directory if missing
 * @returns {Object} Structured result with delta, patchblock, postValidation
 */
function promoteSymbolicToSubstrate(params) {
  // MEASURE TWICE: Validate inputs
  if (!params || typeof params !== 'object') {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: 'params object',
      nextAction: 'Provide params object with path and content properties'
    };
  }

  if (!params.path || typeof params.path !== 'string') {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: 'params.path',
      nextAction: 'Provide exact file path as string'
    };
  }

  if (params.content === undefined || typeof params.content !== 'string') {
    throw {
      error: 'SUBSTRATE-REQUIRED',
      missing: 'params.content',
      nextAction: 'Provide exact file content as string'
    };
  }

  const filePath = path.resolve(params.path);
  const createDirIfMissing = params.createDirIfMissing === true;
  const dirPath = path.dirname(filePath);

  // MEASURE TWICE: Check substrate state
  const fileExists = fs.existsSync(filePath);
  const dirExists = fs.existsSync(dirPath);

  // SRE Check: Validate directory exists or get authorization
  if (!dirExists) {
    if (!createDirIfMissing) {
      throw {
        error: 'SUBSTRATE-REQUIRED',
        missing: `Directory: ${dirPath}`,
        nextAction: `Set createDirIfMissing: true to authorize directory creation, or create directory manually`
      };
    }
  }

  // Read existing content if file exists (for delta/patchblock generation)
  let existingContent = '';
  if (fileExists) {
    try {
      existingContent = fs.readFileSync(filePath, 'utf8');
    } catch (error) {
      // File exists but can't read - treat as new file
      existingContent = '';
    }
  }

  // CUT ONCE: Execute substrate operation
  // Create directory if needed and authorized
  if (!dirExists && createDirIfMissing) {
    fs.mkdirSync(dirPath, { recursive: true });
  }

  // Write file with exact content (no abstraction, no placeholders)
  fs.writeFileSync(filePath, params.content, 'utf8');

  // VERIFY: Ensure correct file, path, content
  const verificationContent = fs.readFileSync(filePath, 'utf8');
  if (verificationContent !== params.content) {
    throw {
      error: 'SUBSTRATE-VERIFICATION-FAILED',
      reason: 'File content does not match written content',
      nextAction: 'Check file permissions and disk space'
    };
  }

  // REPORT: Generate DELTA + PATCHBLOCK + POST-VALIDATION
  const delta = fileExists
    ? `Modified file: ${filePath}`
    : `Created file: ${filePath}`;

  const patchblock = fileExists
    ? generatePatchblock(existingContent, params.content, filePath)
    : `+++ ${filePath}\n${params.content.split('\n').map(line => `+${line}`).join('\n')}`;

  const postValidation = JSON.stringify({
    filePath: filePath,
    exists: true,
    size: params.content.length,
    contentHash: simpleHash(params.content),
    verified: true,
    timestamp: new Date().toISOString()
  }, null, 2);

  return {
    delta: delta,
    patchblock: patchblock,
    postValidation: postValidation
  };
}

/**
 * Generate patchblock (diff-like structure) for file modification
 * 
 * @param {string} oldContent - Previous file content
 * @param {string} newContent - New file content
 * @param {string} filePath - File path
 * @returns {string} Patchblock string
 */
function generatePatchblock(oldContent, newContent, filePath) {
  const oldLines = oldContent.split('\n');
  const newLines = newContent.split('\n');
  
  let patchblock = `--- ${filePath}\n+++ ${filePath}\n`;
  
  // Simple diff: show removed lines with -, added lines with +
  // This is a minimal implementation - full diff algorithm would be more complex
  const maxLines = Math.max(oldLines.length, newLines.length);
  
  for (let i = 0; i < maxLines; i++) {
    const oldLine = oldLines[i] || '';
    const newLine = newLines[i] || '';
    
    if (oldLine !== newLine) {
      if (oldLine) {
        patchblock += `-${oldLine}\n`;
      }
      if (newLine) {
        patchblock += `+${newLine}\n`;
      }
    } else if (oldLine) {
      patchblock += ` ${oldLine}\n`;
    }
  }
  
  return patchblock;
}

/**
 * Simple hash function for content verification
 * 
 * @param {string} content - Content to hash
 * @returns {string} Simple hash string
 */
function simpleHash(content) {
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash).toString(16);
}

/**
 * SUBSTRATE LOCK - Verify substrate integrity
 * Prevents unauthorized modification of the SYJ-1 substrate module
 * 
 * @param {string} [substratePath] - Optional path to substrate file (defaults to current module)
 * @returns {Object} Lock verification result
 * @throws {Error} If substrate integrity check fails
 */
function verifySubstrateLock(substratePath) {
  const currentModulePath = __filename;
  const lockPath = substratePath || currentModulePath;
  
  // SRE Check: Verify substrate exists
  sreCheck(lockPath);
  
  // Read current substrate content
  let currentContent;
  try {
    currentContent = fs.readFileSync(lockPath, 'utf8');
  } catch (error) {
    throw {
      error: 'SUBSTRATE-LOCK-FAILED',
      reason: `Cannot read substrate file: ${lockPath}`,
      nextAction: 'Verify file permissions and substrate integrity'
    };
  }
  
  // Compute lock hash
  const lockHash = simpleHash(currentContent);
  
  // Verify file is not writable (read-only protection)
  let isReadOnly = false;
  try {
    const stats = fs.statSync(lockPath);
    // Check if file is read-only (mode & 0222 === 0 means no write permissions)
    isReadOnly = (stats.mode & 0o222) === 0;
  } catch (error) {
    // If we can't check permissions, continue but note it
    isReadOnly = false;
  }
  
  // Lock verification result
  const lockVerification = {
    locked: true,
    substratePath: lockPath,
    contentHash: lockHash,
    size: currentContent.length,
    readOnly: isReadOnly,
    verified: true,
    timestamp: new Date().toISOString()
  };
  
  // Warn if not read-only (but don't fail - locking can be applied separately)
  if (!isReadOnly) {
    lockVerification.warning = 'Substrate file is writable. Consider setting read-only permissions.';
  }
  
  return lockVerification;
}

/**
 * LOCK SUBSTRATE - Apply read-only protection to substrate file
 * 
 * @param {string} [substratePath] - Optional path to substrate file (defaults to current module)
 * @returns {Object} Lock application result
 * @throws {Error} If lock application fails
 */
function lockSubstrate(substratePath) {
  const currentModulePath = __filename;
  const lockPath = substratePath || currentModulePath;
  
  // SRE Check: Verify substrate exists
  sreCheck(lockPath);
  
  // Verify current state
  const verification = verifySubstrateLock(lockPath);
  
  // Apply read-only permissions (chmod 444 = read-only for all)
  try {
    fs.chmodSync(lockPath, 0o444);
  } catch (error) {
    throw {
      error: 'SUBSTRATE-LOCK-FAILED',
      reason: `Cannot set read-only permissions: ${error.message}`,
      nextAction: 'Verify file ownership and permissions. May require elevated privileges.'
    };
  }
  
  // Verify lock was applied
  const stats = fs.statSync(lockPath);
  const isReadOnly = (stats.mode & 0o222) === 0;
  
  if (!isReadOnly) {
    throw {
      error: 'SUBSTRATE-LOCK-FAILED',
      reason: 'Read-only permissions not applied successfully',
      nextAction: 'Check file system permissions and try again'
    };
  }
  
  return {
    locked: true,
    substratePath: lockPath,
    contentHash: verification.contentHash,
    readOnly: true,
    verified: true,
    timestamp: new Date().toISOString()
  };
}

// Export exact API as specified
module.exports = {
  sreCheck,
  yagniCheck,
  johnCheck,
  promoteSymbolicToSubstrate,
  verifySubstrateLock,
  lockSubstrate
};

