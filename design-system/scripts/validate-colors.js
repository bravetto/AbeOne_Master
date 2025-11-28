#!/usr/bin/env node
/**
 * Color System Validator
 * Validates color system for accessibility and consistency
 * 
 * Usage: node design-system/scripts/validate-colors.js
 */

const fs = require('fs');
const path = require('path');

// Load unified color system
const tokensPath = path.join(__dirname, '../tokens/abeone-unified-color-system-v2.json');
const system = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Simple contrast ratio calculator (relative luminance)
function getLuminance(hex) {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map(val => {
    val = val / 255;
    return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16)
  ] : null;
}

function getContrastRatio(color1, color2) {
  const lum1 = getLuminance(color1);
  const lum2 = getLuminance(color2);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Validate colors
function validateColors() {
  const issues = [];
  const warnings = [];
  const passed = [];

  const white = '#FFFFFF';
  const midnight = system.colorSystem.palettes.technicalCalm.colors.aeMidnight['500'];

  // Validate Healing Palette
  const healing = system.colorSystem.palettes.healing.colors;
  Object.keys(healing).forEach(colorName => {
    const color = healing[colorName];
    const baseColor = color['500'];
    const contrast = getContrastRatio(baseColor, white);
    
    if (contrast >= 4.5) {
      passed.push(`✅ ${colorName}-500: ${contrast.toFixed(2)}:1 on white (AA pass)`);
    } else {
      issues.push(`❌ ${colorName}-500: ${contrast.toFixed(2)}:1 on white (AA fail)`);
    }
  });

  // Validate Technical Calm Palette
  const technicalCalm = system.colorSystem.palettes.technicalCalm.colors;
  
  // Aë Blue
  const aeBlueContrast = getContrastRatio(technicalCalm.aeBlue['500'], white);
  if (aeBlueContrast >= 4.5) {
    passed.push(`✅ aeBlue-500: ${aeBlueContrast.toFixed(2)}:1 on white (AA pass)`);
  } else {
    issues.push(`❌ aeBlue-500: ${aeBlueContrast.toFixed(2)}:1 on white (AA fail)`);
  }

  // Aë Indigo
  const aeIndigoContrast = getContrastRatio(technicalCalm.aeIndigo['500'], white);
  if (aeIndigoContrast >= 4.5) {
    passed.push(`✅ aeIndigo-500: ${aeIndigoContrast.toFixed(2)}:1 on white (AA pass)`);
  } else {
    issues.push(`❌ aeIndigo-500: ${aeIndigoContrast.toFixed(2)}:1 on white (AA fail)`);
  }

  // Aë Midnight
  const aeMidnightContrast = getContrastRatio(technicalCalm.aeMidnight['500'], white);
  if (aeMidnightContrast >= 7.0) {
    passed.push(`✅ aeMidnight-500: ${aeMidnightContrast.toFixed(2)}:1 on white (AAA pass)`);
  } else if (aeMidnightContrast >= 4.5) {
    passed.push(`✅ aeMidnight-500: ${aeMidnightContrast.toFixed(2)}:1 on white (AA pass)`);
  } else {
    issues.push(`❌ aeMidnight-500: ${aeMidnightContrast.toFixed(2)}:1 on white (AA fail)`);
  }

  // Aë Aqua (should be used on dark)
  const aeAquaContrastWhite = getContrastRatio(technicalCalm.aeAqua['500'], white);
  const aeAquaContrastDark = getContrastRatio(technicalCalm.aeAqua['500'], midnight);
  if (aeAquaContrastWhite < 4.5 && aeAquaContrastDark >= 4.5) {
    warnings.push(`⚠️  aeAqua-500: ${aeAquaContrastWhite.toFixed(2)}:1 on white (use on dark), ${aeAquaContrastDark.toFixed(2)}:1 on midnight (AA pass)`);
  } else if (aeAquaContrastDark >= 4.5) {
    passed.push(`✅ aeAqua-500: ${aeAquaContrastDark.toFixed(2)}:1 on midnight (AA pass)`);
  } else {
    issues.push(`❌ aeAqua-500: ${aeAquaContrastDark.toFixed(2)}:1 on midnight (AA fail)`);
  }

  // Aë Mint (should be used on dark)
  const aeMintContrastWhite = getContrastRatio(technicalCalm.aeMint['500'], white);
  const aeMintContrastDark = getContrastRatio(technicalCalm.aeMint['500'], midnight);
  if (aeMintContrastWhite < 4.5 && aeMintContrastDark >= 4.5) {
    warnings.push(`⚠️  aeMint-500: ${aeMintContrastWhite.toFixed(2)}:1 on white (use on dark), ${aeMintContrastDark.toFixed(2)}:1 on midnight (AA pass)`);
  } else if (aeMintContrastDark >= 4.5) {
    passed.push(`✅ aeMint-500: ${aeMintContrastDark.toFixed(2)}:1 on midnight (AA pass)`);
  } else {
    issues.push(`❌ aeMint-500: ${aeMintContrastDark.toFixed(2)}:1 on midnight (AA fail)`);
  }

  return { issues, warnings, passed };
}

// Run validation
console.log('🔍 Validating AbëONE Unified Color System v2.0...\n');
const results = validateColors();

console.log('✅ PASSED:');
results.passed.forEach(msg => console.log(`  ${msg}`));

if (results.warnings.length > 0) {
  console.log('\n⚠️  WARNINGS:');
  results.warnings.forEach(msg => console.log(`  ${msg}`));
}

if (results.issues.length > 0) {
  console.log('\n❌ ISSUES:');
  results.issues.forEach(msg => console.log(`  ${msg}`));
  process.exit(1);
}

console.log('\n✅ All colors validated successfully!');
process.exit(0);

