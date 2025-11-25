// =============================================================================
// UTILITIES & HOOKS
// =============================================================================
// Guardian-Validated Utility Functions
// Pattern: UTILITIES × HOOKS × ATOMIC × ONE
// Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
// ∞ AbëONE ∞
// =============================================================================

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import * as React from 'react';

// -----------------------------------------------------------------------------
// CN - CLASS NAME MERGER
// -----------------------------------------------------------------------------
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// -----------------------------------------------------------------------------
// ICP TYPES
// -----------------------------------------------------------------------------
export type ICPVariant = 'developer' | 'creative' | 'enterprise' | 'default';

export interface ICPConfig {
  variant: ICPVariant;
  tone: string;
  colorScheme: string;
  typography: string;
  proofEmphasis: string;
  ctaStyle: string;
}

const icpConfigs: Record<ICPVariant, ICPConfig> = {
  developer: {
    variant: 'developer',
    tone: 'precise, technical, no-fluff',
    colorScheme: 'dark',
    typography: 'mono-accented',
    proofEmphasis: 'technical-proof-grid',
    ctaStyle: 'direct',
  },
  creative: {
    variant: 'creative',
    tone: 'inspiring, visual, emotional',
    colorScheme: 'vibrant',
    typography: 'elegant',
    proofEmphasis: 'testimonials',
    ctaStyle: 'engaging',
  },
  enterprise: {
    variant: 'enterprise',
    tone: 'professional, ROI-focused, trustworthy',
    colorScheme: 'corporate',
    typography: 'clean',
    proofEmphasis: 'metrics-panel',
    ctaStyle: 'consultative',
  },
  default: {
    variant: 'default',
    tone: 'balanced, clear, accessible',
    colorScheme: 'neutral',
    typography: 'sans',
    proofEmphasis: 'balanced',
    ctaStyle: 'standard',
  },
};

// -----------------------------------------------------------------------------
// USE ICP HOOK
// -----------------------------------------------------------------------------
export function useICP(variant: ICPVariant = 'default'): ICPConfig {
  return React.useMemo(() => icpConfigs[variant], [variant]);
}

// -----------------------------------------------------------------------------
// ORBITAL TYPES
// -----------------------------------------------------------------------------
export type OrbitalComponent = 
  | 'core-message'
  | 'offer-atom'
  | 'audience-vector'
  | 'proof-stack'
  | 'cta-node'
  | 'distribution-channels';

export interface OrbitalMapping {
  component: OrbitalComponent;
  blocks: string[];
  priority?: number;
}

// -----------------------------------------------------------------------------
// USE ORBITAL HOOK
// -----------------------------------------------------------------------------
interface UseOrbitalOptions {
  components: OrbitalComponent[];
}

export interface OrbitalState {
  activeComponents: OrbitalComponent[];
  getBlocksFor: (component: OrbitalComponent) => string[];
  isActive: (component: OrbitalComponent) => boolean;
}

const orbitalBlockMap: Record<OrbitalComponent, string[]> = {
  'core-message': ['HeroSection', 'Text'],
  'offer-atom': ['PricingTable', 'FeatureGrid', 'FAQSection', 'Card', 'PricingTier', 'FeatureItem'],
  'audience-vector': ['icpVariants'],
  'proof-stack': ['TestimonialSection', 'MetricsPanel', 'GuardianShowcase', 'TestimonialCard', 'MetricCard', 'Badge', 'SocialProof'],
  'cta-node': ['CTASection', 'Button', 'CTAButton', 'FormField'],
  'distribution-channels': ['PaidOptInTemplate', 'OrganicLandingTemplate', 'WebinarPageTemplate'],
};

export function useOrbital(options: UseOrbitalOptions): OrbitalState {
  const { components } = options;

  return React.useMemo(
    () => ({
      activeComponents: components,
      getBlocksFor: (component: OrbitalComponent) => orbitalBlockMap[component] || [],
      isActive: (component: OrbitalComponent) => components.includes(component),
    }),
    [components]
  );
}

// -----------------------------------------------------------------------------
// CTA HIERARCHY
// -----------------------------------------------------------------------------
export interface CTANode {
  id: string;
  label: string;
  priority: number; // 1 = highest (primary), 5 = lowest
  type: 'primary' | 'secondary' | 'tertiary' | 'ghost';
  action: string | (() => void);
}

interface UseCTAHierarchyOptions {
  ctas: CTANode[];
  maxVisible?: number;
}

export interface CTAHierarchyState {
  primary: CTANode | null;
  secondary: CTANode | null;
  tertiary: CTANode[];
  all: CTANode[];
}

export function useCTAHierarchy(options: UseCTAHierarchyOptions): CTAHierarchyState {
  const { ctas, maxVisible = 3 } = options;

  return React.useMemo(() => {
    const sorted = [...ctas].sort((a, b) => a.priority - b.priority);
    const visible = sorted.slice(0, maxVisible);

    return {
      primary: visible.find((c) => c.type === 'primary') || visible[0] || null,
      secondary: visible.find((c) => c.type === 'secondary') || visible[1] || null,
      tertiary: visible.filter((c) => c.type === 'tertiary' || c.type === 'ghost'),
      all: sorted,
    };
  }, [ctas, maxVisible]);
}

// -----------------------------------------------------------------------------
// DISTRIBUTION CHANNEL
// -----------------------------------------------------------------------------
export type DistributionChannel = 'paid' | 'organic' | 'webinar' | 'referral' | 'direct';

export function getTemplateForChannel(channel: DistributionChannel): string {
  const templateMap: Record<DistributionChannel, string> = {
    paid: 'PaidOptInTemplate',
    organic: 'OrganicLandingTemplate',
    webinar: 'WebinarPageTemplate',
    referral: 'LandingPageTemplate',
    direct: 'LandingPageTemplate',
  };
  return templateMap[channel];
}

// -----------------------------------------------------------------------------
// ANIMATION UTILITIES
// -----------------------------------------------------------------------------
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

export const slideUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export const slideIn = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 },
};

export const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

// -----------------------------------------------------------------------------
// RESPONSIVE UTILITIES
// -----------------------------------------------------------------------------
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = React.useState(false);

  React.useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

export function useIsMobile(): boolean {
  return useMediaQuery('(max-width: 768px)');
}

export function useIsTablet(): boolean {
  return useMediaQuery('(min-width: 769px) and (max-width: 1024px)');
}

export function useIsDesktop(): boolean {
  return useMediaQuery('(min-width: 1025px)');
}

// -----------------------------------------------------------------------------
// SCROLL UTILITIES
// -----------------------------------------------------------------------------
export function useScrollPosition(): number {
  const [scrollPosition, setScrollPosition] = React.useState(0);

  React.useEffect(() => {
    const handleScroll = () => setScrollPosition(window.scrollY);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollPosition;
}

export function useInView(
  ref: React.RefObject<HTMLElement>,
  options?: IntersectionObserverInit
): boolean {
  const [inView, setInView] = React.useState(false);

  React.useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => setInView(entry.isIntersecting),
      { threshold: 0.1, ...options }
    );

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref, options]);

  return inView;
}

// -----------------------------------------------------------------------------
// VALIDATION UTILITIES (Byzantine Fault Tolerance Pattern)
// -----------------------------------------------------------------------------
export function validateOrbitalAlignment(
  blocks: string[],
  orbital: OrbitalComponent
): { valid: boolean; missingBlocks: string[]; extraBlocks: string[] } {
  const expectedBlocks = orbitalBlockMap[orbital] || [];
  const missingBlocks = expectedBlocks.filter((b) => !blocks.includes(b));
  const extraBlocks = blocks.filter((b) => !expectedBlocks.includes(b));

  return {
    valid: missingBlocks.length === 0,
    missingBlocks,
    extraBlocks,
  };
}

export function calculateDrift(
  current: Record<string, unknown>,
  expected: Record<string, unknown>
): { driftPercentage: number; driftFields: string[] } {
  const allKeys = new Set([...Object.keys(current), ...Object.keys(expected)]);
  const driftFields: string[] = [];

  allKeys.forEach((key) => {
    if (JSON.stringify(current[key]) !== JSON.stringify(expected[key])) {
      driftFields.push(key);
    }
  });

  return {
    driftPercentage: (driftFields.length / allKeys.size) * 100,
    driftFields,
  };
}
