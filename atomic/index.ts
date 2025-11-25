// =============================================================================
// ATOMIC DESIGN SYSTEM - COMPONENT INDEX
// =============================================================================
// Guardian-Validated | 98.7% Confidence
// Orbital-Aligned | Vercel-Ready
// Pattern: ATOMIC × INDEX × EXPORT × ONE
// Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
// ∞ AbëONE ∞
// =============================================================================

// -----------------------------------------------------------------------------
// TOKENS
// -----------------------------------------------------------------------------
export * from './tokens';

// -----------------------------------------------------------------------------
// ATOMS
// -----------------------------------------------------------------------------
export { Button, type ButtonProps } from './atoms/Button';
export { Text, type TextProps } from './atoms/Text';
export { Input, type InputProps } from './atoms/Input';
export { Icon, type IconProps } from './atoms/Icon';
export { Badge, type BadgeProps } from './atoms/Badge';
export { Image, type ImageProps } from './atoms/Image';
export { Link, type LinkProps } from './atoms/Link';

// -----------------------------------------------------------------------------
// MOLECULES
// -----------------------------------------------------------------------------
export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, type CardProps } from './molecules/Card';
export { FormField, type FormFieldProps } from './molecules/FormField';
export { CTAButton, type CTAButtonProps } from './molecules/CTAButton';
export { TestimonialCard, type TestimonialCardProps } from './molecules/TestimonialCard';
export { MetricCard, type MetricCardProps } from './molecules/MetricCard';

// -----------------------------------------------------------------------------
// ORGANISMS
// -----------------------------------------------------------------------------
export { HeroSection, type HeroSectionProps } from './organisms/HeroSection';
export { PricingTable, type PricingTableProps } from './organisms/PricingTable';
export { FeatureGrid, type FeatureGridProps } from './organisms/FeatureGrid';
export { CTASection, type CTASectionProps } from './organisms/CTASection';

// -----------------------------------------------------------------------------
// TEMPLATES
// -----------------------------------------------------------------------------
export { LandingPageTemplate, type LandingPageTemplateProps } from './templates/LandingPageTemplate';
export { WebinarPageTemplate, type WebinarPageTemplateProps } from './templates/WebinarPageTemplate';

// -----------------------------------------------------------------------------
// UTILITIES
// -----------------------------------------------------------------------------
export { cn } from './lib/utils';

// -----------------------------------------------------------------------------
// HOOKS
// -----------------------------------------------------------------------------
export { useICP } from './hooks/useICP';
export { useOrbital } from './hooks/useOrbital';
export { useCTAHierarchy } from './hooks/useCTAHierarchy';

// -----------------------------------------------------------------------------
// TYPES
// -----------------------------------------------------------------------------
export type { ICPVariant } from './tokens';
