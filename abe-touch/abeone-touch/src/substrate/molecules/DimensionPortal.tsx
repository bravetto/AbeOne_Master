/**
 * AbëONE Molecule: DimensionPortal
 * 
 * A portal to another dimension of reality.
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
import { TranscendentButton } from '@/substrate/atoms/TranscendentButton';

export interface DimensionPortalProps {
  /** Portal title */
  title?: string;
  /** Portal content */
  children: React.ReactNode;
  /** Show wonder effect */
  wonder?: boolean;
  /** Show vision effect */
  vision?: boolean;
  /** Show majesty effect */
  majesty?: boolean;
  /** Custom class name */
  className?: string;
  /** On portal activate */
  onActivate?: () => void;
}

export const DimensionPortal: React.FC<DimensionPortalProps> = ({
  title = 'Enter Another Dimension',
  children,
  wonder = true,
  vision = true,
  majesty = true,
  className,
  onActivate,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [mousePosition, setMousePosition] = React.useState({ x: 50, y: 50 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    setMousePosition({ x, y });
  };

  const handleActivate = () => {
    setIsOpen(!isOpen);
    onActivate?.();
  };

  return (
    <div
      className={cn(
        'relative w-full max-w-2xl mx-auto',
        'dimension-portal',
        wonder && 'wonder-effect',
        vision && 'vision-effect',
        majesty && 'majesty-effect',
        'animate-transcend-float',
        className
      )}
      onMouseMove={handleMouseMove}
      style={{
        '--mouse-x': `${mousePosition.x}%`,
        '--mouse-y': `${mousePosition.y}%`,
      } as React.CSSProperties}
    >
      {/* Portal glow */}
      <div
        className={cn(
          'absolute inset-0 rounded-3xl',
          'opacity-0 transition-opacity duration-600',
          'hover:opacity-100'
        )}
        style={{
          background: `radial-gradient(circle at ${mousePosition.x}% ${mousePosition.y}%, rgba(6, 182, 212, 0.3) 0%, rgba(168, 85, 247, 0.2) 50%, transparent 100%)`,
        }}
      />

      {/* Portal border */}
      <div
        className={cn(
          'absolute inset-0 rounded-3xl',
          'border-2 border-[var(--abe-primary)]',
          'opacity-0 transition-opacity duration-600',
          'hover:opacity-50',
          'animate-majesty-glow'
        )}
      />

      {/* Portal content */}
      <div
        className={cn(
          'relative z-10 p-8 rounded-3xl',
          'bg-[var(--abe-surface)]/80 backdrop-blur-xl',
          'border border-[var(--abe-border)]',
          'transition-all duration-600',
          isOpen && 'animate-portal-open'
        )}
      >
        {/* Title */}
        {title && (
          <h3 className="text-2xl font-bold mb-6 text-gradient-majesty text-center">
            {title}
          </h3>
        )}

        {/* Content */}
        <div className="mb-6">{children}</div>

        {/* Activate button */}
        <div className="flex justify-center">
          <TranscendentButton
            wonder={wonder}
            vision={vision}
            majesty={majesty}
            multiModal
            portal
            size="lg"
            glowColor="purple"
            onClick={handleActivate}
          >
            <span className="relative z-10">
              {isOpen ? 'Close Portal' : 'Open Portal'}
            </span>
          </TranscendentButton>
        </div>
      </div>

      {/* Dimension particles */}
      {wonder && (
        <div className="absolute inset-0 rounded-3xl pointer-events-none overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-[var(--abe-primary)] rounded-full opacity-50"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animation: `float ${3 + Math.random() * 2}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`,
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};
