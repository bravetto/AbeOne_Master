#!/usr/bin/env node
/**
 * Tailwind Config Generator
 * Generates tailwind.config.js from design tokens
 * 
 * Usage: node generate-tailwind.js [output-path]
 * Default output: ../../apps/web/tailwind.config.js
 */

const fs = require('fs');
const path = require('path');

// Load design tokens
const tokensPath = path.join(__dirname, '../tokens/abeone-design-tokens.json');
const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Generate Tailwind config
function generateTailwindConfig() {
  const config = {
    content: [
      './app/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './pages/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
      extend: {
        colors: {
          // Heart (Red)
          heart: {
            50: tokens.colors.heart[50],
            100: tokens.colors.heart[100],
            200: tokens.colors.heart[200],
            300: tokens.colors.heart[300],
            400: tokens.colors.heart[400],
            500: tokens.colors.heart[500],
            600: tokens.colors.heart[600],
            700: tokens.colors.heart[700],
            800: tokens.colors.heart[800],
            900: tokens.colors.heart[900],
          },
          // Lux (Purple)
          lux: {
            50: tokens.colors.lux[50],
            100: tokens.colors.lux[100],
            200: tokens.colors.lux[200],
            300: tokens.colors.lux[300],
            400: tokens.colors.lux[400],
            500: tokens.colors.lux[500],
            600: tokens.colors.lux[600],
            700: tokens.colors.lux[700],
            800: tokens.colors.lux[800],
            900: tokens.colors.lux[900],
          },
          // Warm (Orange)
          warm: {
            50: tokens.colors.warm[50],
            100: tokens.colors.warm[100],
            200: tokens.colors.warm[200],
            300: tokens.colors.warm[300],
            400: tokens.colors.warm[400],
            500: tokens.colors.warm[500],
            600: tokens.colors.warm[600],
            700: tokens.colors.warm[700],
            800: tokens.colors.warm[800],
            900: tokens.colors.warm[900],
          },
          // Peace (Green)
          peace: {
            50: tokens.colors.peace[50],
            100: tokens.colors.peace[100],
            200: tokens.colors.peace[200],
            300: tokens.colors.peace[300],
            400: tokens.colors.peace[400],
            500: tokens.colors.peace[500],
            600: tokens.colors.peace[600],
            700: tokens.colors.peace[700],
            800: tokens.colors.peace[800],
            900: tokens.colors.peace[900],
          },
          // Neutral
          neutral: {
            50: tokens.colors.neutral[50],
            100: tokens.colors.neutral[100],
            200: tokens.colors.neutral[200],
            300: tokens.colors.neutral[300],
            400: tokens.colors.neutral[400],
            500: tokens.colors.neutral[500],
            600: tokens.colors.neutral[600],
            700: tokens.colors.neutral[700],
            800: tokens.colors.neutral[800],
            900: tokens.colors.neutral[900],
          },
        },
        fontFamily: {
          sans: tokens.typography.fonts.sans.family,
          serif: tokens.typography.fonts.serif.family,
          display: tokens.typography.fonts.display.family,
        },
        fontSize: tokens.typography.scale,
        lineHeight: tokens.typography.lineHeight,
        spacing: tokens.spacing.scale,
        borderRadius: tokens.borderRadius,
        boxShadow: {
          ...tokens.shadows,
        },
        backgroundImage: {
          'gradient-healing': tokens.gradients.healing.css,
          'gradient-lux': tokens.gradients.lux.css,
          'gradient-sidebar': tokens.gradients.sidebar.css,
          'gradient-text-healing': tokens.gradients.textHealing.css,
        },
        screens: tokens.breakpoints,
      },
    },
    plugins: [],
  };

  return `/**\n * Tailwind CSS Configuration\n * Generated from design-system/tokens/abeone-design-tokens.json\n * DO NOT EDIT MANUALLY - Run: node design-system/generators/generate-tailwind.js\n * Generated: ${new Date().toISOString()}\n */\n\nmodule.exports = ${JSON.stringify(config, null, 2)};\n`;
}

// Write output
const outputPath = process.argv[2] || path.join(__dirname, '../../apps/web/tailwind.config.js');
const configContent = generateTailwindConfig();

// Ensure directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, configContent, 'utf8');
console.log(`✅ Generated Tailwind config: ${outputPath}`);

