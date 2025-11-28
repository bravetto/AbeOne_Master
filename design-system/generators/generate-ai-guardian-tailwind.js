#!/usr/bin/env node

/**
 * AI Guardian Tailwind Config Generator
 * 
 * Generates Tailwind CSS configuration from AI Guardian design tokens
 * 
 * Pattern: GENERATOR × TAILWIND × AI_GUARDIAN × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

const fs = require('fs');
const path = require('path');

const tokensPath = path.join(__dirname, '../tokens/ai-guardian-design-tokens.json');
const outputPath = path.join(__dirname, '../generated/tailwind-ai-guardian.config.js');

// Read design tokens
const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Generate Tailwind config
const config = `/** 
 * AI Guardian Tailwind CSS Configuration
 * 
 * Generated from: ai-guardian-design-tokens.json
 * Source: AI Guardian Brand Book v1.0
 * 
 * Pattern: TAILWIND × AI_GUARDIAN × CONFIG × ONE
 * Copyright: © 2025 BiasGuards.ai LLC - All Rights Reserved
 * 
 * ∞ AbëONE ∞
 */

module.exports = {
  theme: {
    extend: {
      colors: {
        // Oxford Blue - Primary Brand Color
        oxfordBlue: {
          50: '${tokens.colors.oxfordBlue.shades['50'].hex}',
          100: '${tokens.colors.oxfordBlue.shades['100'].hex}',
          200: '${tokens.colors.oxfordBlue.shades['200'].hex}',
          300: '${tokens.colors.oxfordBlue.shades['300'].hex}',
          400: '${tokens.colors.oxfordBlue.shades['400'].hex}',
          500: '${tokens.colors.oxfordBlue.shades['500'].hex}', // Primary
          600: '${tokens.colors.oxfordBlue.shades['600'].hex}',
          700: '${tokens.colors.oxfordBlue.shades['700'].hex}',
          800: '${tokens.colors.oxfordBlue.shades['800'].hex}',
          900: '${tokens.colors.oxfordBlue.shades['900'].hex}',
        },
        // Brand Colors (when extracted)
        deepSkyBlue: {
          // TODO: Extract from brand palette (3.1)
          DEFAULT: '#TBD',
        },
        metallicSilver: {
          // TODO: Extract from brand palette (3.1)
          DEFAULT: '#TBD',
        },
        softWhite: {
          // TODO: Extract from brand palette (3.1)
          DEFAULT: '#TBD',
        },
        darkCharcoal: {
          // TODO: Extract from brand palette (3.1)
          DEFAULT: '#TBD',
        },
        // Neutral Colors
        black: '${tokens.colors.black.hex}',
        white: '${tokens.colors.white.hex}',
      },
      fontSize: {
        // Typography Scale - 50% increase per level
        'body-copy': ['${tokens.typography.scale.levels.bodyCopy.sizePx}px', {
          lineHeight: '${tokens.typography.scale.levels.bodyCopy.lineHeight}',
          fontWeight: '${tokens.typography.scale.levels.bodyCopy.weight}',
        }],
        'subheader': ['${tokens.typography.scale.levels.subheader.sizePx}px', {
          lineHeight: '${tokens.typography.scale.levels.subheader.lineHeight}',
          fontWeight: '${tokens.typography.scale.levels.subheader.weight}',
        }],
        'header': ['${tokens.typography.scale.levels.header.sizePx}px', {
          lineHeight: '${tokens.typography.scale.levels.header.lineHeight}',
          fontWeight: '${tokens.typography.scale.levels.header.weight}',
        }],
      },
      backgroundImage: {
        // AI Guardian Gradients
        'gradient-ai-01': 'linear-gradient(0deg, ${tokens.colors.gradients.gradient01.stops[0].color} 0%, ${tokens.colors.gradients.gradient01.stops[1].color} 100%)',
        'gradient-ai-02': 'linear-gradient(0deg, ${tokens.colors.gradients.gradient02.stops[0].color} 0%, ${tokens.colors.gradients.gradient02.stops[1].color} 100%)',
        'gradient-ai-03': 'linear-gradient(30deg, ${tokens.colors.gradients.gradient03.stops[0].color} 0%, ${tokens.colors.gradients.gradient03.stops[1].color} 50%, ${tokens.colors.gradients.gradient03.stops[2].color} 100%)',
        'gradient-ai-04': 'linear-gradient(0deg, ${tokens.colors.gradients.gradient04.stops[0].color} 0%, ${tokens.colors.gradients.gradient04.stops[1].color} 50%, ${tokens.colors.gradients.gradient04.stops[2].color} 100%)',
        'gradient-ai-05': 'linear-gradient(90deg, ${tokens.colors.gradients.gradient05.stops[0].color} 0%, ${tokens.colors.gradients.gradient05.stops[1].color} 50%, ${tokens.colors.gradients.gradient05.stops[2].color} 100%)',
        'gradient-ai-06': 'linear-gradient(90deg, ${tokens.colors.gradients.gradient06.stops[0].color} 0%, ${tokens.colors.gradients.gradient06.stops[1].color} 50%, ${tokens.colors.gradients.gradient06.stops[2].color} 100%)',
      },
    },
  },
  plugins: [],
};
`;

// Write output
fs.writeFileSync(outputPath, config, 'utf8');
console.log(`✅ Generated: ${outputPath}`);

