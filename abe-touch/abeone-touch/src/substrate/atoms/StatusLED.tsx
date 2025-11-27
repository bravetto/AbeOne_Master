/**
 * AbëONE Atom: StatusLED
 * 
 * Hardware-inspired LED indicator with realistic glow and animations.
 * Provides immediate visual feedback on system state.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

export type LEDState = 
  | 'off' 
  | 'on' 
  | 'pulse' 
  | 'blink' 
  | 'breathe' 
  | 'flicker';

export type LEDColor = 
  | 'green' 
  | 'red' 
  | 'yellow' 
  | 'blue' 
  | 'orange' 
  | 'purple' 
  | 'cyan' 
  | 'white';

// =============================================================================
// COLOR CONFIG
// =============================================================================

const ledColors: Record<LEDColor, { base: string; glow: string; dark: string }> = {
  green:  { base: '#22c55e', glow: 'rgba(34, 197, 94, 0.6)',  dark: '#166534' },
  red:    { base: '#ef4444', glow: 'rgba(239, 68, 68, 0.6)',  dark: '#991b1b' },
  yellow: { base: '#eab308', glow: 'rgba(234, 179, 8, 0.6)',  dark: '#a16207' },
  blue:   { base: '#3b82f6', glow: 'rgba(59, 130, 246, 0.6)', dark: '#1e40af' },
  orange: { base: '#f97316', glow: 'rgba(249, 115, 22, 0.6)', dark: '#c2410c' },
  purple: { base: '#a855f7', glow: 'rgba(168, 85, 247, 0.6)', dark: '#6b21a8' },
  cyan:   { base: '#06b6d4', glow: 'rgba(6, 182, 212, 0.6)',  dark: '#0e7490' },
  white:  { base: '#f8fafc', glow: 'rgba(248, 250, 252, 0.6)', dark: '#94a3b8' },
};

// =============================================================================
// VARIANTS
// =============================================================================

const statusLEDVariants = cva(
  'relative rounded-full transition-all duration-300',
  {
    variants: {
      size: {
        xs: 'h-1.5 w-1.5',
        sm: 'h-2 w-2',
        md: 'h-3 w-3',
        lg: 'h-4 w-4',
        xl: 'h-6 w-6',
      },
      variant: {
        standard: '',
        recessed: 'ring-1 ring-black/20 ring-inset',
        raised: 'shadow-sm',
        flat: '',
        industrial: 'ring-2 ring-[var(--abe-border)]',
      },
    },
    defaultVariants: {
      size: 'md',
      variant: 'standard',
    },
  }
);

// =============================================================================
// ANIMATIONS CSS
// =============================================================================

const animationStyles = `
  @keyframes led-pulse {
    0%, 100% { opacity: 0.6; transform: scale(0.95); }
    50% { opacity: 1; transform: scale(1); }
  }
  @keyframes led-blink {
    0%, 100% { opacity: 0.1; }
    50% { opacity: 1; }
  }
  @keyframes led-breathe {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
  }
  @keyframes led-flicker {
    0% { opacity: 1; }
    10% { opacity: 0.8; }
    20% { opacity: 0.9; }
    30% { opacity: 0.7; }
    40% { opacity: 1; }
    50% { opacity: 0.6; }
    60% { opacity: 0.9; }
    70% { opacity: 0.8; }
    80% { opacity: 1; }
    90% { opacity: 0.7; }
    100% { opacity: 0.9; }
  }
`;

// =============================================================================
// COMPONENT
// =============================================================================

export interface StatusLEDProps extends VariantProps<typeof statusLEDVariants> {
  color?: LEDColor;
  state?: LEDState;
  glow?: boolean;
  label?: string;
  showLabel?: boolean;
  className?: string;
}

export const StatusLED: React.FC<StatusLEDProps> = ({
  size = 'md',
  variant = 'standard',
  color = 'green',
  state = 'on',
  glow = false,
  label,
  showLabel = false,
  className,
}) => {
  const colorConfig = ledColors[color];
  const isOn = state !== 'off';
  
  const glowSizes: Record<string, string> = {
    xs: '4px',
    sm: '6px',
    md: '8px',
    lg: '12px',
    xl: '16px',
  };
  
  const animations: Record<LEDState, string> = {
    off: '',
    on: '',
    pulse: 'led-pulse 1.5s ease-in-out infinite',
    blink: 'led-blink 0.5s step-end infinite',
    breathe: 'led-breathe 3s ease-in-out infinite',
    flicker: 'led-flicker 0.3s linear infinite',
  };

  const ledStyle: React.CSSProperties = {
    backgroundColor: isOn ? colorConfig.base : colorConfig.dark,
    opacity: isOn ? 1 : 0.3,
    boxShadow: isOn && glow 
      ? `0 0 ${glowSizes[size ?? 'md']} ${colorConfig.glow}, inset 0 0 2px rgba(255,255,255,0.5)`
      : isOn 
        ? 'inset 0 0 2px rgba(255,255,255,0.5)'
        : 'none',
    animation: animations[state],
  };

  return (
    <>
      <style>{animationStyles}</style>
      <div className={cn('flex items-center gap-2', className)}>
        <div
          className={cn(statusLEDVariants({ size, variant }))}
          style={ledStyle}
          role="status"
          aria-label={label ?? `Status: ${state}`}
        >
          {/* Inner highlight for glass effect */}
          {isOn && (
            <div
              className="absolute rounded-full"
              style={{
                top: '15%',
                left: '15%',
                width: '35%',
                height: '35%',
                background: 'radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 100%)',
              }}
            />
          )}
        </div>
        {showLabel && label && (
          <span className="text-xs text-[var(--abe-text-muted)]">{label}</span>
        )}
      </div>
    </>
  );
};

// =============================================================================
// LED GROUP
// =============================================================================

export interface StatusLEDGroupProps {
  leds: Array<{
    color: LEDColor;
    state: LEDState;
    label?: string;
  }>;
  size?: StatusLEDProps['size'];
  orientation?: 'horizontal' | 'vertical';
  gap?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusLEDGroup: React.FC<StatusLEDGroupProps> = ({
  leds,
  size = 'md',
  orientation = 'horizontal',
  gap = 'md',
  className,
}) => {
  const gapClasses = { sm: 'gap-1', md: 'gap-2', lg: 'gap-3' };
  
  return (
    <div
      className={cn(
        'flex items-center',
        orientation === 'vertical' ? 'flex-col' : 'flex-row',
        gapClasses[gap],
        className
      )}
    >
      {leds.map((led, index) => (
        <StatusLED
          key={index}
          size={size}
          color={led.color}
          state={led.state}
          label={led.label}
          showLabel={!!led.label}
          glow
        />
      ))}
    </div>
  );
};

// =============================================================================
// PRESET: CONNECTION STATUS
// =============================================================================

export type ConnectionState = 'connected' | 'connecting' | 'disconnected' | 'error';

export interface ConnectionStatusProps {
  status: ConnectionState;
  showLabel?: boolean;
  size?: StatusLEDProps['size'];
  className?: string;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  status,
  showLabel = true,
  size = 'sm',
  className,
}) => {
  const configs: Record<ConnectionState, { color: LEDColor; state: LEDState; label: string }> = {
    connected:    { color: 'green',  state: 'on',      label: 'Connected' },
    connecting:   { color: 'yellow', state: 'pulse',   label: 'Connecting...' },
    disconnected: { color: 'red',    state: 'off',     label: 'Disconnected' },
    error:        { color: 'red',    state: 'flicker', label: 'Error' },
  };
  
  const config = configs[status];
  
  return (
    <StatusLED
      size={size}
      color={config.color}
      state={config.state}
      label={config.label}
      showLabel={showLabel}
      glow
      className={className}
    />
  );
};

// =============================================================================
// EXPORTS
// =============================================================================

export { statusLEDVariants };
