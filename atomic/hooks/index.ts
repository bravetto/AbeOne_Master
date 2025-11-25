/**
 * AbëONE Atomic Design System - Hooks Export
 * 
 * Pattern: HOOKS × EXPORT × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
 * ∞ AbëONE ∞
 */

// Re-export hooks from lib/utils
export {
  useICP,
  useOrbital,
  useCTAHierarchy,
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useScrollPosition,
  useInView,
  type ICPVariant,
  type ICPConfig,
  type OrbitalComponent,
  type OrbitalMapping,
  type OrbitalState,
  type CTANode,
  type CTAHierarchyState,
  type DistributionChannel,
} from '../lib/utils';

// Re-export utilities
export {
  cn,
  getTemplateForChannel,
  validateOrbitalAlignment,
  calculateDrift,
  fadeIn,
  slideUp,
  slideIn,
  stagger,
} from '../lib/utils';
