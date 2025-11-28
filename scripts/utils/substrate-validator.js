#!/usr/bin/env node
/**
 * SUBSTRATE VALIDATOR LIBRARY
 * 
 * Enforces Substrate-Required Execution (SRE) pattern
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + SRE Enforcement
 */

/**
 * Require substrate before operation
 * Throws SUBSTRATE-REQUIRED error with future-state success actions if missing
 * 
 * @param {any} value - Value to validate
 * @param {string} operationName - Name of operation requiring substrate
 * @param {string} [source] - Optional source location for better error messages
 * @returns {any} - Returns value if valid
 * @throws {Error} - SUBSTRATE-REQUIRED error with success actions
 */
function requireSubstrate(value, operationName, source = null) {
  if (!value) {
    const sourceInfo = source ? ` (from ${source})` : '';
    const error = new Error(`SUBSTRATE-REQUIRED: Operation halted. Missing ${operationName}${sourceInfo}.`);
    
    // Add future-state success actions
    error.successActions = [
      `1. Provide ${operationName} using exact substrate.`,
      `2. Re-run command with updated context.`,
      `3. Lock file or status block regenerates automatically from substrate.`,
      `4. System revalidates and converges to correct state.`
    ];
    
    error.name = 'SUBSTRATE_REQUIRED';
    throw error;
  }
  
  // Additional validation for arrays
  if (Array.isArray(value) && value.length === 0) {
    // Empty arrays are valid substrate, but warn if operation expects data
    return value;
  }
  
  // Additional validation for objects
  if (typeof value === 'object' && Object.keys(value).length === 0) {
    // Empty objects are valid substrate, but warn if operation expects data
    return value;
  }
  
  return value;
}

/**
 * Validate substrate exists and matches expected structure
 * 
 * @param {any} value - Value to validate
 * @param {string} operationName - Name of operation
 * @param {Function} validator - Optional validator function
 * @returns {boolean} - True if valid
 */
function validateSubstrate(value, operationName, validator = null) {
  if (!value) {
    return false;
  }
  
  if (validator && typeof validator === 'function') {
    try {
      return validator(value);
    } catch (err) {
      return false;
    }
  }
  
  return true;
}

/**
 * Require substrate array and validate it's not hardcoded/fabricated
 * 
 * @param {Array} array - Array to validate
 * @param {string} operationName - Name of operation
 * @param {Function} [substrateChecker] - Function to verify array comes from real substrate
 * @returns {Array} - Returns array if valid
 * @throws {Error} - SUBSTRATE-REQUIRED error if invalid
 */
function requireSubstrateArray(array, operationName, substrateChecker = null) {
  requireSubstrate(array, operationName);
  
  if (!Array.isArray(array)) {
    throw new Error(`SUBSTRATE-REQUIRED: ${operationName} must be an array`);
  }
  
  // If substrate checker provided, validate array comes from real source
  if (substrateChecker && typeof substrateChecker === 'function') {
    const isValid = substrateChecker(array);
    if (!isValid) {
      const error = new Error(`SUBSTRATE-REQUIRED: ${operationName} array appears to be fabricated or hardcoded`);
      error.successActions = [
        `1. Regenerate ${operationName} from actual substrate source.`,
        `2. Remove any hardcoded arrays.`,
        `3. Use substrate-based detection instead.`
      ];
      error.name = 'SUBSTRATE_REQUIRED';
      throw error;
    }
  }
  
  return array;
}

/**
 * Require substrate object and validate structure
 * 
 * @param {Object} obj - Object to validate
 * @param {string} operationName - Name of operation
 * @param {Array<string>} [requiredKeys] - Required keys in object
 * @returns {Object} - Returns object if valid
 * @throws {Error} - SUBSTRATE-REQUIRED error if invalid
 */
function requireSubstrateObject(obj, operationName, requiredKeys = []) {
  requireSubstrate(obj, operationName);
  
  if (typeof obj !== 'object' || Array.isArray(obj)) {
    throw new Error(`SUBSTRATE-REQUIRED: ${operationName} must be an object`);
  }
  
  // Check required keys
  if (requiredKeys.length > 0) {
    const missingKeys = requiredKeys.filter(key => !(key in obj));
    if (missingKeys.length > 0) {
      const error = new Error(`SUBSTRATE-REQUIRED: ${operationName} missing required keys: ${missingKeys.join(', ')}`);
      error.successActions = [
        `1. Provide ${operationName} with required keys: ${requiredKeys.join(', ')}`,
        `2. Regenerate from actual substrate source.`
      ];
      error.name = 'SUBSTRATE_REQUIRED';
      throw error;
    }
  }
  
  return obj;
}

/**
 * Validate hash is not fake/patterned
 * Real SHA256 hashes are uniformly distributed, never contain repeating patterns
 * 
 * @param {string} hash - Hash to validate
 * @param {string} operationName - Name of operation
 * @returns {boolean} - True if hash appears valid
 */
function validateHashNotFake(hash, operationName = 'hash') {
  if (!hash || typeof hash !== 'string') {
    return false;
  }
  
  // Check for repeating byte patterns (e.g., c8c8c8c8... or d9d9d9d9...)
  const repeatingPattern = /(.)\1{7,}/;
  if (repeatingPattern.test(hash)) {
    return false;
  }
  
  // Check for too many consecutive identical characters
  const consecutivePattern = /(.)\1{5,}/;
  if (consecutivePattern.test(hash)) {
    return false;
  }
  
  // SHA256 produces 64 hex characters
  if (hash.length !== 64) {
    return false;
  }
  
  // Check all characters are valid hex
  if (!/^[0-9a-f]{64}$/i.test(hash)) {
    return false;
  }
  
  return true;
}

/**
 * Require valid hash (not fake/patterned)
 * 
 * @param {string} hash - Hash to validate
 * @param {string} operationName - Name of operation
 * @returns {string} - Returns hash if valid
 * @throws {Error} - SUBSTRATE-REQUIRED error if fake
 */
function requireValidHash(hash, operationName = 'hash') {
  requireSubstrate(hash, operationName);
  
  if (!validateHashNotFake(hash, operationName)) {
    const error = new Error(`SUBSTRATE-REQUIRED: ${operationName} appears to be fake or patterned`);
    error.successActions = [
      `1. Regenerate ${operationName} using actual substrate arrays.`,
      `2. Compute digest from exact byte stream (UTF-8 normalized).`,
      `3. Replace any placeholder or patterned digest values.`,
      `4. Run: node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json`
    ];
    error.name = 'SUBSTRATE_REQUIRED';
    throw error;
  }
  
  return hash;
}

module.exports = {
  requireSubstrate,
  validateSubstrate,
  requireSubstrateArray,
  requireSubstrateObject,
  validateHashNotFake,
  requireValidHash
};

