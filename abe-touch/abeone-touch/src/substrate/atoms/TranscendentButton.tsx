/**
 * AbëONE Atom: TranscendentButton
 * 
 * A button that feels like touching another dimension of reality.
 * Pregnant with WONDER, VISION, and MAJESTY.
 * 
 * Multi-modal, animated, transcendent interactions.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface TranscendentButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Show wonder effect */
  wonder?: boolean;
  /** Show vision effect */
  vision?: boolean;
  /** Show majesty effect */
  majesty?: boolean;
  /** Multi-modal feedback */
  multiModal?: boolean;
  /** Portal effect */
  portal?: boolean;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Glow color */
  glowColor?: 'primary' | 'accent' | 'success' | 'purple' | 'cyan' | 'pink';
}

const sizeClasses = {
  sm: 'h-9 px-4 text-sm rounded-lg',
  md: 'h-11 px-6 text-base rounded-xl',
  lg: 'h-14 px-8 text-lg rounded-2xl',
  xl: 'h-16 px-10 text-xl rounded-2xl',
};

const glowColors = {
  primary: 'rgba(6, 182, 212, 0.3)',
  accent: 'rgba(168, 85, 247, 0.3)',
  success: 'rgba(34, 197, 94, 0.3)',
  purple: 'rgba(168, 85, 247, 0.4)',
  cyan: 'rgba(6, 182, 212, 0.4)',
  pink: 'rgba(236, 72, 153, 0.4)',
};

export const TranscendentButton = React.forwardRef<
  HTMLButtonElement,
  TranscendentButtonProps
>(
  (
    {
      className,
      wonder = true,
      vision = true,
      majesty = true,
      multiModal = true,
      portal = true,
      size = 'md',
      glowColor = 'primary',
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const [isPressed, setIsPressed] = React.useState(false);
    const [mousePosition, setMousePosition] = React.useState({ x: 50, y: 50 });
    const [rippleKey, setRippleKey] = React.useState(0);

    const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setMousePosition({ x, y });
    };

    const handleMouseDown = (e: React.MouseEvent<HTMLButtonElement>) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setMousePosition({ x, y });
      setIsPressed(true);
      setRippleKey(prev => prev + 1);
    };

    return (
      <button
        ref={ref}
        disabled={disabled}
        className={cn(
          'relative overflow-hidden',
          'bg-[var(--abe-surface)]',
          'text-[var(--abe-text-primary)]',
          'font-medium',
          'transition-all duration-400',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-[var(--abe-primary)]',
          'disabled:pointer-events-none disabled:opacity-50',
          'select-none cursor-pointer',
          sizeClasses[size],
          wonder && 'wonder-effect',
          vision && 'vision-effect',
          majesty && 'majesty-effect',
          portal && 'dimension-portal',
          multiModal && 'multi-modal-interactive',
          'transcendent-touch',
          'animate-breathe',
          className
        )}
        style={{
          '--mouse-x': `${mousePosition.x}%`,
          '--mouse-y': `${mousePosition.y}%`,
        } as React.CSSProperties}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={() => setIsPressed(false)}
        onMouseLeave={() => setIsPressed(false)}
        {...props}
      >
        {/* Glow effect */}
        <div
          className={cn(
            'absolute inset-0 rounded-inherit',
            'opacity-0 transition-opacity duration-400',
            !disabled && 'hover:opacity-100'
          )}
          style={{
            boxShadow: `0 0 30px ${glowColors[glowColor]}, 0 0 60px ${glowColors[glowColor]}`,
          }}
        />

        {/* Ripple effect - expands from touch point */}
        {multiModal && (
          <div
            key={rippleKey}
            className={cn(
              'absolute rounded-full pointer-events-none',
              'bg-gradient-radial from-white/40 via-white/20 to-transparent',
              'animate-ripple-expand'
            )}
            style={{
              left: `${mousePosition.x}%`,
              top: `${mousePosition.y}%`,
              width: '4px',
              height: '4px',
              transform: 'translate(-50%, -50%)',
            }}
          />
        )}

        {/* Content */}
        <span className="relative z-10 flex items-center justify-center gap-2">
          {children}
        </span>

        {/* Dimension lines */}
        {portal && (
          <div className="absolute inset-0 rounded-inherit pointer-events-none">
            <div
              className={cn(
                'absolute inset-0 rounded-inherit',
                'border border-[var(--abe-primary)]',
                'opacity-0 transition-opacity duration-400',
                !disabled && 'hover:opacity-30'
              )}
            />
          </div>
        )}

        {/* Shimmer effect */}
        {wonder && (
          <div
            className={cn(
              'absolute inset-0 rounded-inherit',
              'animate-wonder-shimmer',
              'opacity-0 transition-opacity duration-400',
              !disabled && 'hover:opacity-100'
            )}
          />
        )}
      </button>
    );
  }
);

TranscendentButton.displayName = 'TranscendentButton';
