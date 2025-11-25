/** 
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
          50: '#C9DBF8',
          100: '#A5C3F3',
          200: '#81ABEF',
          300: '#5D93EA',
          400: '#387BE5',
          500: '#1C64D9', // Primary
          600: '#1754B5',
          700: '#134390',
          800: '#0E326C',
          900: '#081C3D',
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
        black: '#000000',
        white: '#FFFFFF',
      },
      fontSize: {
        // Typography Scale - 50% increase per level
        'body-copy': ['60px', {
          lineHeight: '1.5',
          fontWeight: 'regular',
        }],
        'subheader': ['90px', {
          lineHeight: '1.2',
          fontWeight: 'bold',
        }],
        'header': ['135px', {
          lineHeight: '1.1',
          fontWeight: 'bold',
        }],
      },
      backgroundImage: {
        // AI Guardian Gradients
        'gradient-ai-01': 'linear-gradient(0deg, #081C3D 0%, #1C64D9 100%)',
        'gradient-ai-02': 'linear-gradient(0deg, #081C3D 0%, #A5C3F3 100%)',
        'gradient-ai-03': 'linear-gradient(30deg, #A5C3F3 0%, #1754B5 50%, #134390 100%)',
        'gradient-ai-04': 'linear-gradient(0deg, #D6F1FF 0%, #1C64D9 50%, #081C3D 100%)',
        'gradient-ai-05': 'linear-gradient(90deg, #A5C3F3 0%, #1C64D9 50%, #0E326C 100%)',
        'gradient-ai-06': 'linear-gradient(90deg, #081C3D 0%, #1754B5 50%, #5CC6FF 100%)',
      },
    },
  },
  plugins: [],
};
