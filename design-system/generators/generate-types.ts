/**
 * TypeScript Types Generator
 * Generates TypeScript type definitions from design tokens
 * 
 * Usage: npx tsx generate-types.ts [output-path]
 * Default output: ../../design-system/generated/design-tokens.d.ts
 */

import * as fs from 'fs';
import * as path from 'path';

// Load design tokens
const tokensPath = path.join(__dirname, '../tokens/abeone-design-tokens.json');
const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));

// Generate TypeScript types
function generateTypeScriptTypes(): string {
  let types = `/**
 * AbëONE Design System - TypeScript Type Definitions
 * Generated from design-system/tokens/abeone-design-tokens.json
 * DO NOT EDIT MANUALLY - Run: npx tsx design-system/generators/generate-types.ts
 * Generated: ${new Date().toISOString()}
 */

export interface ColorScale {
  50: string;
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;
  600: string;
  700: string;
  800: string;
  900: string;
  semantic: string;
  usage: string;
}

export interface DesignTokens {
  meta: {
    name: string;
    version: string;
    description: string;
    created: string;
    guardians: string[];
  };
  colors: {
    heart: ColorScale;
    lux: ColorScale;
    warm: ColorScale;
    peace: ColorScale;
    neutral: ColorScale;
  };
  typography: {
    fonts: {
      sans: {
        family: string[];
        weights: number[];
        usage: string;
        googleFont: string;
      };
      serif: {
        family: string[];
        weights: number[];
        usage: string;
        googleFont: string;
      };
      display: {
        family: string[];
        weights: number[];
        usage: string;
        googleFont: string;
      };
    };
    scale: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
      '4xl': string;
      '5xl': string;
      '6xl': string;
    };
    lineHeight: {
      tight: string;
      snug: string;
      normal: string;
      relaxed: string;
      loose: string;
    };
  };
  spacing: {
    scale: Record<string, string>;
  };
  borderRadius: Record<string, string>;
  shadows: Record<string, string>;
  gradients: {
    healing: {
      direction: string;
      stops: Array<{ color: string; position: string }>;
      css: string;
      usage: string;
    };
    lux: {
      direction: string;
      stops: Array<{ color: string; position: string }>;
      css: string;
      usage: string;
    };
    sidebar: {
      direction: string;
      stops: Array<{ color: string; position: string }>;
      css: string;
      usage: string;
    };
    textHealing: {
      direction: string;
      stops: Array<{ color: string; position: string }>;
      css: string;
      usage: string;
    };
  };
  components: {
    sidebar: {
      width: string;
      background: string;
      border: string;
      padding: {
        header: string;
        nav: string;
        footer: string;
      };
    };
    topbar: {
      background: string;
      backdrop: string;
      border: string;
      padding: string;
      height: string;
    };
    card: {
      background: string;
      backdrop: string;
      borderRadius: string;
      padding: string;
      shadow: string;
      border: string;
    };
    button: {
      primary: {
        background: string;
        color: string;
        padding: string;
        borderRadius: string;
        fontWeight: string;
        shadow: string;
      };
      secondary: {
        background: string;
        color: string;
        padding: string;
        borderRadius: string;
      };
    };
  };
  animations: {
    pulse: {
      duration: string;
      timing: string;
      keyframes: Array<{ opacity: string; offset: string }>;
    };
    fadeIn: {
      duration: string;
      timing: string;
      keyframes: Array<{ opacity: string; offset: string }>;
    };
  };
  breakpoints: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
}

// Import tokens
import tokensData from '../tokens/abeone-design-tokens.json';

export const tokens: DesignTokens = tokensData as DesignTokens;

// Color helper types
export type ColorName = 'heart' | 'lux' | 'warm' | 'peace' | 'neutral';
export type ColorShade = '50' | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900';

// Helper functions
export function getColor(colorName: ColorName, shade: ColorShade = '500'): string {
  return tokens.colors[colorName][shade];
}

export function getGradient(gradientName: 'healing' | 'lux' | 'sidebar' | 'textHealing'): string {
  return tokens.gradients[gradientName].css;
}

export function getSpacing(size: string): string {
  return tokens.spacing.scale[size] || size;
}

export function getFontSize(size: keyof DesignTokens['typography']['scale']): string {
  return tokens.typography.scale[size];
}

export function getBreakpoint(size: keyof DesignTokens['breakpoints']): string {
  return tokens.breakpoints[size];
}
`;

  return types;
}

// Write output
const outputPath = process.argv[2] || path.join(__dirname, '../generated/design-tokens.d.ts');
const typesContent = generateTypeScriptTypes();

// Ensure directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, typesContent, 'utf8');
console.log(`✅ Generated TypeScript types: ${outputPath}`);

