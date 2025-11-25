#!/usr/bin/env node
/**
 * CSS Variables Generator
 * Generates CSS custom properties from design tokens
 * 
 * Usage: node generate-css-vars.js [output-path]
 * Default output: ../../design-system/generated/css-variables.css
 */

const fs = require('fs');
const path = require('path');

// Load design tokens
const tokensPath = path.join(__dirname, '../tokens/abeone-design-tokens.json');
const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Generate CSS variables
function generateCSSVariables() {
  let css = `/**
 * AbëONE Design System - CSS Variables
 * Generated from design-system/tokens/abeone-design-tokens.json
 * DO NOT EDIT MANUALLY - Run: node design-system/generators/generate-css-vars.js
 * Generated: ${new Date().toISOString()}
 */

:root {
  /* Colors - Heart (Red) */
`;

  // Heart colors
  Object.keys(tokens.colors.heart).forEach(key => {
    if (key !== 'semantic' && key !== 'usage') {
      css += `  --heart-${key}: ${tokens.colors.heart[key]};\n`;
    }
  });

  css += `\n  /* Colors - Lux (Purple) */\n`;
  Object.keys(tokens.colors.lux).forEach(key => {
    if (key !== 'semantic' && key !== 'usage') {
      css += `  --lux-${key}: ${tokens.colors.lux[key]};\n`;
    }
  });

  css += `\n  /* Colors - Warm (Orange) */\n`;
  Object.keys(tokens.colors.warm).forEach(key => {
    if (key !== 'semantic' && key !== 'usage') {
      css += `  --warm-${key}: ${tokens.colors.warm[key]};\n`;
    }
  });

  css += `\n  /* Colors - Peace (Green) */\n`;
  Object.keys(tokens.colors.peace).forEach(key => {
    if (key !== 'semantic' && key !== 'usage') {
      css += `  --peace-${key}: ${tokens.colors.peace[key]};\n`;
    }
  });

  css += `\n  /* Colors - Neutral */\n`;
  Object.keys(tokens.colors.neutral).forEach(key => {
    if (key !== 'semantic' && key !== 'usage') {
      css += `  --neutral-${key}: ${tokens.colors.neutral[key]};\n`;
    }
  });

  css += `\n  /* Typography - Font Families */\n`;
  css += `  --font-sans: ${tokens.typography.fonts.sans.family.join(', ')};\n`;
  css += `  --font-serif: ${tokens.typography.fonts.serif.family.join(', ')};\n`;
  css += `  --font-display: ${tokens.typography.fonts.display.family.join(', ')};\n`;

  css += `\n  /* Typography - Font Sizes */\n`;
  Object.keys(tokens.typography.scale).forEach(key => {
    css += `  --text-${key}: ${tokens.typography.scale[key]};\n`;
  });

  css += `\n  /* Typography - Line Heights */\n`;
  Object.keys(tokens.typography.lineHeight).forEach(key => {
    css += `  --leading-${key}: ${tokens.typography.lineHeight[key]};\n`;
  });

  css += `\n  /* Spacing */\n`;
  Object.keys(tokens.spacing.scale).forEach(key => {
    css += `  --spacing-${key}: ${tokens.spacing.scale[key]};\n`;
  });

  css += `\n  /* Border Radius */\n`;
  Object.keys(tokens.borderRadius).forEach(key => {
    css += `  --radius-${key}: ${tokens.borderRadius[key]};\n`;
  });

  css += `\n  /* Shadows */\n`;
  Object.keys(tokens.shadows).forEach(key => {
    css += `  --shadow-${key}: ${tokens.shadows[key]};\n`;
  });

  css += `\n  /* Gradients */\n`;
  css += `  --gradient-healing: ${tokens.gradients.healing.css};\n`;
  css += `  --gradient-lux: ${tokens.gradients.lux.css};\n`;
  css += `  --gradient-sidebar: ${tokens.gradients.sidebar.css};\n`;
  css += `  --gradient-text-healing: ${tokens.gradients.textHealing.css};\n`;

  css += `\n  /* Breakpoints */\n`;
  Object.keys(tokens.breakpoints).forEach(key => {
    css += `  --breakpoint-${key}: ${tokens.breakpoints[key]};\n`;
  });

  css += `}\n`;

  // Add utility classes
  css += `\n/* Utility Classes */\n`;
  css += `.bg-gradient-healing { background: var(--gradient-healing); }\n`;
  css += `.bg-gradient-lux { background: var(--gradient-lux); }\n`;
  css += `.bg-gradient-sidebar { background: var(--gradient-sidebar); }\n`;
  css += `.text-gradient-healing { background: var(--gradient-text-healing); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }\n`;

  return css;
}

// Write output
const outputPath = process.argv[2] || path.join(__dirname, '../generated/css-variables.css');
const cssContent = generateCSSVariables();

// Ensure directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, cssContent, 'utf8');
console.log(`✅ Generated CSS variables: ${outputPath}`);

