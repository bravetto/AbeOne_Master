#!/usr/bin/env node
/**
 * Unified Tailwind Config Generator
 * Generates tailwind.config.js from unified color system v2
 * 
 * Usage: node generate-unified-tailwind.js [output-path]
 * Default output: ../../apps/web/tailwind.config.js
 */

const fs = require('fs');
const path = require('path');

// Load unified color system
const tokensPath = path.join(__dirname, '../tokens/abeone-unified-color-system-v2.json');
const unifiedSystem = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Load original design tokens for typography/spacing/etc
const originalTokensPath = path.join(__dirname, '../tokens/abeone-design-system-v1.json');
const originalTokens = JSON.parse(fs.readFileSync(originalTokensPath, 'utf8'));

// Generate Tailwind config
function generateTailwindConfig() {
  const healing = unifiedSystem.colorSystem.palettes.healing.colors;
  const technicalCalm = unifiedSystem.colorSystem.palettes.technicalCalm.colors;
  const vermillion = unifiedSystem.colorSystem.palettes.vermillion.colors.vermillion;
  const neutral = unifiedSystem.colorSystem.neutral;

  const config = {
    darkMode: ['class'],
    content: [
      './pages/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
      extend: {
        colors: {
          // Healing Palette - Preserved
          lux: {
            50: healing.lux['50'],
            100: healing.lux['100'],
            200: healing.lux['200'],
            300: healing.lux['300'],
            400: healing.lux['400'],
            500: healing.lux['500'],
            600: healing.lux['600'],
            700: healing.lux['700'],
            800: healing.lux['800'],
            900: healing.lux['900'],
          },
          warm: {
            50: healing.warm['50'],
            100: healing.warm['100'],
            200: healing.warm['200'],
            300: healing.warm['300'],
            400: healing.warm['400'],
            500: healing.warm['500'],
            600: healing.warm['600'],
            700: healing.warm['700'],
            800: healing.warm['800'],
            900: healing.warm['900'],
          },
          heart: {
            50: healing.heart['50'],
            100: healing.heart['100'],
            200: healing.heart['200'],
            300: healing.heart['300'],
            400: healing.heart['400'],
            500: healing.heart['500'],
            600: healing.heart['600'],
            700: healing.heart['700'],
            800: healing.heart['800'],
            900: healing.heart['900'],
          },
          peace: {
            50: healing.peace['50'],
            100: healing.peace['100'],
            200: healing.peace['200'],
            300: healing.peace['300'],
            400: healing.peace['400'],
            500: healing.peace['500'],
            600: healing.peace['600'],
            700: healing.peace['700'],
            800: healing.peace['800'],
            900: healing.peace['900'],
          },
          // Technical Calm Palette - New
          aeBlue: {
            50: technicalCalm.aeBlue['50'],
            100: technicalCalm.aeBlue['100'],
            200: technicalCalm.aeBlue['200'],
            300: technicalCalm.aeBlue['300'],
            400: technicalCalm.aeBlue['400'],
            500: technicalCalm.aeBlue['500'],
            600: technicalCalm.aeBlue['600'],
            700: technicalCalm.aeBlue['700'],
            800: technicalCalm.aeBlue['800'],
            900: technicalCalm.aeBlue['900'],
          },
          aeIndigo: {
            50: technicalCalm.aeIndigo['50'],
            100: technicalCalm.aeIndigo['100'],
            200: technicalCalm.aeIndigo['200'],
            300: technicalCalm.aeIndigo['300'],
            400: technicalCalm.aeIndigo['400'],
            500: technicalCalm.aeIndigo['500'],
            600: technicalCalm.aeIndigo['600'],
            700: technicalCalm.aeIndigo['700'],
            800: technicalCalm.aeIndigo['800'],
            900: technicalCalm.aeIndigo['900'],
          },
          aeMidnight: {
            50: technicalCalm.aeMidnight['50'],
            100: technicalCalm.aeMidnight['100'],
            200: technicalCalm.aeMidnight['200'],
            300: technicalCalm.aeMidnight['300'],
            400: technicalCalm.aeMidnight['400'],
            500: technicalCalm.aeMidnight['500'],
            600: technicalCalm.aeMidnight['600'],
            700: technicalCalm.aeMidnight['700'],
            800: technicalCalm.aeMidnight['800'],
            900: technicalCalm.aeMidnight['900'],
          },
          aeAqua: {
            50: technicalCalm.aeAqua['50'],
            100: technicalCalm.aeAqua['100'],
            200: technicalCalm.aeAqua['200'],
            300: technicalCalm.aeAqua['300'],
            400: technicalCalm.aeAqua['400'],
            500: technicalCalm.aeAqua['500'],
            600: technicalCalm.aeAqua['600'],
            700: technicalCalm.aeAqua['700'],
            800: technicalCalm.aeAqua['800'],
            900: technicalCalm.aeAqua['900'],
          },
          aeMint: {
            50: technicalCalm.aeMint['50'],
            100: technicalCalm.aeMint['100'],
            200: technicalCalm.aeMint['200'],
            300: technicalCalm.aeMint['300'],
            400: technicalCalm.aeMint['400'],
            500: technicalCalm.aeMint['500'],
            600: technicalCalm.aeMint['600'],
            700: technicalCalm.aeMint['700'],
            800: technicalCalm.aeMint['800'],
            900: technicalCalm.aeMint['900'],
          },
          // Vermillion - The POP
          vermillion: {
            50: vermillion['50'],
            100: vermillion['100'],
            200: vermillion['200'],
            300: vermillion['300'],
            400: vermillion['400'],
            500: vermillion['500'],
            600: vermillion['600'],
            700: vermillion['700'],
            800: vermillion['800'],
            900: vermillion['900'],
            POP: vermillion['POP'],
            VIBRANT: vermillion['VIBRANT'],
            PURE: vermillion['PURE'],
          },
          // Neutral - Shared
          neutral: {
            50: neutral['50'],
            100: neutral['100'],
            200: neutral['200'],
            300: neutral['300'],
            400: neutral['400'],
            500: neutral['500'],
            600: neutral['600'],
            700: neutral['700'],
            800: neutral['800'],
            900: neutral['900'],
          },
          // Semantic aliases (backward compatibility)
          primary: {
            50: healing.lux['50'],
            100: healing.lux['100'],
            200: healing.lux['200'],
            300: healing.lux['300'],
            400: healing.lux['400'],
            500: healing.lux['500'],
            600: healing.lux['600'],
            700: healing.lux['700'],
            800: healing.lux['800'],
            900: healing.lux['900'],
          },
          secondary: {
            50: healing.warm['50'],
            100: healing.warm['100'],
            200: healing.warm['200'],
            300: healing.warm['300'],
            400: healing.warm['400'],
            500: healing.warm['500'],
            600: healing.warm['600'],
            700: healing.warm['700'],
            800: healing.warm['800'],
            900: healing.warm['900'],
          },
          accent: {
            50: healing.heart['50'],
            100: healing.heart['100'],
            200: healing.heart['200'],
            300: healing.heart['300'],
            400: healing.heart['400'],
            500: healing.heart['500'],
            600: healing.heart['600'],
            700: healing.heart['700'],
            800: healing.heart['800'],
            900: healing.heart['900'],
          },
          success: {
            50: healing.peace['50'],
            100: healing.peace['100'],
            200: healing.peace['200'],
            300: healing.peace['300'],
            400: healing.peace['400'],
            500: healing.peace['500'],
            600: healing.peace['600'],
            700: healing.peace['700'],
            800: healing.peace['800'],
            900: healing.peace['900'],
          },
        },
        fontFamily: {
          sans: originalTokens.typography.fonts.sans.family,
          serif: originalTokens.typography.fonts.serif.family,
          display: originalTokens.typography.fonts.display.family,
        },
        borderRadius: {
          lg: 'var(--radius)',
          md: 'calc(var(--radius) - 2px)',
          sm: 'calc(var(--radius) - 4px)',
        },
      },
    },
    plugins: [require("tailwindcss-animate")],
  };

  return `/** @type {import('tailwindcss').Config} */
/**
 * AbëONE Unified Color System v2.0 - Tailwind Config
 * Generated from design-system/tokens/abeone-unified-color-system-v2.json
 * DO NOT EDIT MANUALLY - Run: node design-system/generators/generate-unified-tailwind.js
 * Generated: ${new Date().toISOString()}
 */
module.exports = ${JSON.stringify(config, null, 2)};
`;
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
console.log(`✅ Generated unified Tailwind config: ${outputPath}`);

