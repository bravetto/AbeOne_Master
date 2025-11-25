/**
 * BiasGuard Context Validator Tests
 * JAHmere Webb Freedom Mission - August 25, 2025
 */

import { describe, it, expect } from 'vitest';
import { BiasGuardContextValidator, BiasGuardContextWorkflow, createBiasGuardValidator } from './biasguard-validator';

describe('BiasGuard Context Validator - JAHmere Webb Freedom Mission', () => {
  const validator = new BiasGuardContextValidator();
  const validContext = {
    framework: 'svelte5' as const,
    styling: 'tailwind4' as const,
    animation: 'gsap' as const,
    missionAlignment: true,
    performanceTargets: {
      lighthouse: 98,
      bundleSize: 150000,
      loadTime: 1200
    }
  };

  describe('Mission Context Validation', () => {
    it('validates August 25, 2025 court date accuracy', () => {
      const validCode = 'const courtDate = "August 25, 2025";';
      const invalidCode = 'const courtDate = "July 28, 2025";';
      
      const validResult = validator.validateContext(validCode, validContext);
      const invalidResult = validator.validateContext(invalidCode, validContext);
      
      expect(validResult.isValid).toBe(true);
      expect(invalidResult.isValid).toBe(false);
      expect(invalidResult.violations[0].type).toContain('COURT DATE ACCURACY');
    });

    it('validates JAHmere Webb mission authenticity', () => {
      const authenticCode = 'const mission = "JAHmere Webb Freedom Mission";';
      const fakeCode = 'const story = "fake placeholder story";';
      
      const authenticResult = validator.validateContext(authenticCode, validContext);
      const fakeResult = validator.validateContext(fakeCode, validContext);
      
      expect(authenticResult.isValid).toBe(true);
      expect(fakeResult.isValid).toBe(false);
      expect(fakeResult.violations[0].type).toContain('MISSION AUTHENTICITY');
    });

    it('validates legal crisis amount accuracy', () => {
      const validAmount = 'const legalCrisis = "$26,500";';
      const result = validator.validateContext(validAmount, validContext);
      expect(result.isValid).toBe(true);
    });
  });

  describe('Framework Drift Detection', () => {
    it('detects React syntax drift', () => {
      const reactCode = 'const [state, setState] = useState(0); <div className="test">React</div>';
      const result = validator.validateContext(reactCode, validContext);
      
      expect(result.isValid).toBe(false);
      expect(result.violations[0].type).toContain('REACT DRIFT');
      expect(result.violations[0].suggestion).toContain('Svelte 5 runes');
    });

    it('detects Vue syntax drift', () => {
      const vueCode = '<div v-if="condition">{{ message }}</div>';
      const result = validator.validateContext(vueCode, validContext);
      
      expect(result.isValid).toBe(false);
      expect(result.violations[0].type).toContain('VUE DRIFT');
      expect(result.violations[0].suggestion).toContain('Svelte syntax');
    });

    it('detects styling framework drift', () => {
      const styledCode = 'import styled from "styled-components";';
      const result = validator.validateContext(styledCode, validContext);
      
      expect(result.isValid).toBe(false);
      expect(result.violations[0].type).toContain('STYLING DRIFT');
      expect(result.violations[0].suggestion).toContain('Tailwind CSS');
    });
  });

  describe('Performance Validation', () => {
    it('detects non-GPU animation patterns', () => {
      const badAnimationCode = 'element.style.width = "100px"; element.style.height = "200px";';
      const result = validator.validateContext(badAnimationCode, validContext);
      
      expect(result.violations.some(v => v.type.includes('NON-GPU ANIMATION'))).toBe(true);
      expect(result.violations[0].suggestion).toContain('transform and opacity');
    });

    it('validates performance targets', () => {
      const lowPerformanceContext = {
        ...validContext,
        performanceTargets: { lighthouse: 80, bundleSize: 200000, loadTime: 3000 }
      };
      
      const result = validator.validateContext('', lowPerformanceContext);
      expect(result.violations.some(v => v.type.includes('PERFORMANCE TARGET'))).toBe(true);
    });
  });

  describe('Context Score Calculation', () => {
    it('calculates perfect score for valid code', () => {
      const validCode = 'let count = $state(0); class="bg-blue-500"';
      const result = validator.validateContext(validCode, validContext);
      
      expect(result.score).toBe(100);
      expect(result.isValid).toBe(true);
    });

    it('penalizes critical violations heavily', () => {
      const criticalViolationCode = 'const [state] = useState(0);';
      const result = validator.validateContext(criticalViolationCode, validContext);
      
      expect(result.score).toBeLessThanOrEqual(65);
      expect(result.isValid).toBe(false);
    });
  });

  describe('Cursor AI Prompt Generation', () => {
    it('generates comprehensive development prompt', () => {
      const prompt = validator.generateCursorPrompt(validContext);
      
      expect(prompt).toContain('BiasGuard landing page');
      expect(prompt).toContain('JAHmere Webb');
      expect(prompt).toContain('August 25, 2025');
      expect(prompt).toContain('Svelte 5 with Runes API');
      expect(prompt).toContain('GSAP 3.13');
      expect(prompt).toContain('98+ Lighthouse');
    });

    it('includes mission context and constraints', () => {
      const prompt = validator.generateCursorPrompt(validContext);
      
      expect(prompt).toContain('$26,500 cost');
      expect(prompt).toContain('15% to criminal justice reform');
      expect(prompt).toContain('NEVER USE: React patterns');
      expect(prompt).toContain('NEVER ANIMATE: width, height');
    });
  });

  describe('BiasGuard Context Workflow', () => {
    const workflow = new BiasGuardContextWorkflow();

    it('designs valid context architecture', async () => {
      const context = await workflow.designContext();
      
      expect(context.framework).toBe('svelte5');
      expect(context.styling).toBe('tailwind4');
      expect(context.animation).toBe('gsap');
      expect(context.missionAlignment).toBe(true);
      expect(context.performanceTargets.lighthouse).toBe(98);
    });

    it('validates mission constants accuracy', () => {
      expect(BiasGuardContextWorkflow.MISSION_CONSTANTS.COURT_DATE).toBe('August 25, 2025');
      expect(BiasGuardContextWorkflow.MISSION_CONSTANTS.LEGAL_CRISIS_AMOUNT).toBe('$26,500');
      expect(BiasGuardContextWorkflow.MISSION_CONSTANTS.REVENUE_TO_JUSTICE).toBe('15%');
      expect(BiasGuardContextWorkflow.MISSION_CONSTANTS.MISSION_NAME).toContain('JAHmere Webb');
    });

    it('validates performance targets', () => {
      expect(BiasGuardContextWorkflow.PERFORMANCE_TARGETS.LIGHTHOUSE_SCORE).toBe(98);
      expect(BiasGuardContextWorkflow.PERFORMANCE_TARGETS.BUNDLE_SIZE_LIMIT).toBe(150000);
      expect(BiasGuardContextWorkflow.PERFORMANCE_TARGETS.LOAD_TIME_TARGET).toBe(1200);
    });
  });

  describe('Integrated Validator Factory', () => {
    it('creates working validator instance', () => {
      const { validator, workflow, validateCode, generatePrompt } = createBiasGuardValidator();
      
      expect(validator).toBeInstanceOf(BiasGuardContextValidator);
      expect(workflow).toBeInstanceOf(BiasGuardContextWorkflow);
      expect(typeof validateCode).toBe('function');
      expect(typeof generatePrompt).toBe('function');
    });

    it('validates code with default BiasGuard context', () => {
      const { validateCode } = createBiasGuardValidator();
      const validCode = 'let state = $state(0); class="bg-justice-blue-600"';
      
      const result = validateCode(validCode);
      expect(result.isValid).toBe(true);
      expect(result.score).toBe(100);
    });
  });
});

// Test utilities for BiasGuard validation
export const BiasGuardTestUtils = {
  createValidSvelteCode: () => 'let count = $state(0); class="bg-blue-500 transform transition-transform"',
  createInvalidReactCode: () => 'const [count, setCount] = useState(0); <div className="test">',
  createValidMissionCode: () => 'const courtDate = "August 25, 2025"; const mission = "JAHmere Webb Freedom Mission"',
  createInvalidMissionCode: () => 'const story = "fake placeholder story"; const date = "July 28"',
  
  validateMissionAlignment: (code: string) => {
    const { validateCode } = createBiasGuardValidator();
    return validateCode(code);
  }
};
