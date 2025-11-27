/**
 * AbëONE Atom: VoiceWaveform
 * 
 * Animated audio visualization for voice interfaces.
 * We see the voice. We feel the presence.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn, clamp, lerp } from '@/lib/utils';
import { useEventDriven, type AbeEventType } from '@/lib/event-driven';

// =============================================================================
// TYPES
// =============================================================================

export type WaveformState = 
  | 'idle'       // Subtle breathing - sleeping
  | 'listening'  // Active organic movement - receiving
  | 'processing' // Wave moving across - thinking
  | 'speaking'   // Dynamic speech pattern - responding
  | 'error';     // Flat with pulse

export type WaveformVariant = 'bars' | 'sine' | 'circular' | 'minimal';

export interface AudioAnalysis {
  frequencyData?: Uint8Array;
  timeDomainData?: Uint8Array;
  volume?: number;
}

// =============================================================================
// VARIANTS
// =============================================================================

const voiceWaveformVariants = cva(
  'relative overflow-hidden',
  {
    variants: {
      size: {
        xs: 'h-6 w-16',
        sm: 'h-8 w-24',
        md: 'h-12 w-32',
        lg: 'h-16 w-48',
        xl: 'h-20 w-64',
        full: 'h-full w-full',
      },
      color: {
        primary: '',
        accent: '',
        success: '',
        white: '',
      },
    },
    defaultVariants: {
      size: 'md',
      color: 'primary',
    },
  }
);

// =============================================================================
// COLOR MAPPING
// =============================================================================

const colorMap: Record<string, { base: string; glow: string }> = {
  primary: { base: 'var(--abe-primary)', glow: 'rgba(6, 182, 212, 0.5)' },
  accent:  { base: 'var(--abe-accent)',  glow: 'rgba(168, 85, 247, 0.5)' },
  success: { base: 'var(--abe-success)', glow: 'rgba(34, 197, 94, 0.5)' },
  white:   { base: '#ffffff',            glow: 'rgba(255, 255, 255, 0.5)' },
};

// =============================================================================
// COMPONENT
// =============================================================================

export interface VoiceWaveformProps extends VariantProps<typeof voiceWaveformVariants> {
  state?: WaveformState;
  variant?: WaveformVariant;
  audioData?: AudioAnalysis;
  barCount?: number;
  glow?: boolean;
  mirrored?: boolean;
  smoothing?: number;
  speed?: number;
  className?: string;
}

export const VoiceWaveform: React.FC<VoiceWaveformProps> = ({
  size = 'md',
  color = 'primary',
  state = 'idle',
  variant = 'bars',
  audioData,
  barCount = 12,
  glow = false,
  mirrored = false,
  smoothing = 0.3,
  speed = 1,
  className,
}) => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const animationRef = React.useRef<number>();
  const timeRef = React.useRef<number>(0);
  const barsRef = React.useRef<number[]>(Array(barCount).fill(0.1));
  const [bars, setBars] = React.useState<number[]>(Array(barCount).fill(0.1));
  const [currentState, setCurrentState] = React.useState<WaveformState>(state);
  
  const colors = colorMap[color ?? 'primary'];
  
  // Event-driven state updates
  useEventDriven<{ status: WaveformState }>('status-change', (event) => {
    setCurrentState(event.detail.status);
  });
  
  // Use current state (from props or events)
  const activeState = state || currentState;
  
  // Event-driven animation loop (only runs when state is active)
  React.useEffect(() => {
    // Skip animation for idle/error states to save energy
    if (activeState === 'idle' || activeState === 'error') {
      // Minimal animation for idle/error
      const animate = () => {
        timeRef.current += 0.016 * speed;
        const newBars = barsRef.current.map((prevHeight, index) => {
          const t = timeRef.current;
          const targetHeight = activeState === 'idle' 
            ? 0.1 + Math.sin(t * 2 + index * 0.3) * 0.05
            : 0.15 + Math.sin(t * 2) * 0.05;
          return lerp(prevHeight, clamp(targetHeight, 0.05, 1), 1 - smoothing);
        });
        barsRef.current = newBars;
        setBars([...newBars]);
        animationRef.current = requestAnimationFrame(animate);
      };
      animationRef.current = requestAnimationFrame(animate);
    } else {
      // Full animation for active states
      const animate = () => {
        timeRef.current += 0.016 * speed;
        
        const newBars = barsRef.current.map((prevHeight, index) => {
          let targetHeight = 0.1;
          const t = timeRef.current;
          const i = index;
          
          // Use real audio data if available
          if (audioData?.frequencyData && audioData.frequencyData.length > 0) {
            const dataIndex = Math.floor((i / barCount) * audioData.frequencyData.length);
            targetHeight = audioData.frequencyData[dataIndex] / 255;
          } else {
            // Simulated animation based on state (event-driven)
            switch (activeState) {
              case 'listening':
                const wave1 = Math.sin(t * 5 + i * 0.5) * 0.3;
                const wave2 = Math.sin(t * 3 + i * 0.3) * 0.2;
                const wave3 = Math.sin(t * 7 + i * 0.7) * 0.15;
                const noise = (Math.random() - 0.5) * 0.1;
                targetHeight = 0.4 + wave1 + wave2 + wave3 + noise;
                break;
              case 'processing':
                const processingWave = Math.sin(t * 4 - i * 0.4);
                targetHeight = 0.3 + processingWave * 0.25;
                break;
              case 'speaking':
                const speech1 = Math.sin(t * 5 + i * 0.5) * 0.25;
                const speech2 = Math.sin(t * 8 + i * 0.3) * 0.2;
                const speech3 = Math.sin(t * 13 + i * 0.2) * 0.15;
                targetHeight = 0.35 + speech1 + speech2 + speech3;
                break;
              default:
                targetHeight = 0.1;
            }
          }
          
          // Smooth interpolation
          return lerp(prevHeight, clamp(targetHeight, 0.05, 1), 1 - smoothing);
        });
        
        barsRef.current = newBars;
        setBars([...newBars]);
        animationRef.current = requestAnimationFrame(animate);
      };
      
      animationRef.current = requestAnimationFrame(animate);
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [activeState, audioData, barCount, smoothing, speed]);

  // Render based on variant
  const renderContent = () => {
    switch (variant) {
      case 'bars':
        return renderBars();
      case 'sine':
        return renderSine();
      case 'circular':
        return renderCircular();
      case 'minimal':
        return renderMinimal();
      default:
        return renderBars();
    }
  };
  
  // Bars variant
  const renderBars = () => {
    const displayBars = mirrored 
      ? [...bars.slice(0, barCount / 2).reverse(), ...bars.slice(0, barCount / 2)]
      : bars;
    
    return (
      <div className="flex items-center justify-center h-full gap-[2px]">
        {displayBars.map((height, index) => (
          <div
            key={index}
            className="flex-1 rounded-full transition-all duration-75"
            style={{
              height: `${height * 100}%`,
              minHeight: '5%',
              backgroundColor: colors.base,
              boxShadow: glow ? `0 0 8px ${colors.glow}` : undefined,
            }}
          />
        ))}
      </div>
    );
  };
  
  // Sine wave variant
  const renderSine = () => {
    const amplitude = state === 'listening' ? 15 : state === 'speaking' ? 12 : 3;
    const frequency = state === 'listening' ? 3 : state === 'speaking' ? 5 : 1;
    const t = timeRef.current;
    
    const points: string[] = [];
    for (let x = 0; x <= 100; x += 2) {
      const y = 50 + Math.sin((x * frequency * Math.PI) / 50 + t * 5) * amplitude;
      points.push(`${x},${y}`);
    }
    
    return (
      <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
        <defs>
          <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: colors.base, stopOpacity: 0.3 }} />
            <stop offset="50%" style={{ stopColor: colors.base, stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: colors.base, stopOpacity: 0.3 }} />
          </linearGradient>
          {glow && (
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          )}
        </defs>
        <polyline
          points={points.join(' ')}
          fill="none"
          stroke="url(#waveGradient)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter={glow ? 'url(#glow)' : undefined}
        />
      </svg>
    );
  };
  
  // Circular variant
  const renderCircular = () => {
    const centerX = 50;
    const centerY = 50;
    const innerRadius = 25;
    const maxLength = 20;
    const t = timeRef.current;
    const rotation = state === 'processing' ? t * 30 : 0;
    
    return (
      <svg viewBox="0 0 100 100" className="w-full h-full">
        <defs>
          {glow && (
            <filter id="circularGlow">
              <feGaussianBlur stdDeviation="1.5" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          )}
        </defs>
        <g transform={`rotate(${rotation} ${centerX} ${centerY})`}>
          {bars.map((height, index) => {
            const angle = (index / barCount) * 2 * Math.PI - Math.PI / 2;
            const x1 = centerX + Math.cos(angle) * innerRadius;
            const y1 = centerY + Math.sin(angle) * innerRadius;
            const length = innerRadius + height * maxLength;
            const x2 = centerX + Math.cos(angle) * length;
            const y2 = centerY + Math.sin(angle) * length;
            
            return (
              <line
                key={index}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={colors.base}
                strokeWidth="3"
                strokeLinecap="round"
                filter={glow ? 'url(#circularGlow)' : undefined}
              />
            );
          })}
          <circle
            cx={centerX}
            cy={centerY}
            r={innerRadius - 5}
            fill="none"
            stroke={colors.base}
            strokeWidth="1"
            opacity={0.3}
          />
        </g>
      </svg>
    );
  };
  
  // Minimal variant - 3 dots
  const renderMinimal = () => {
    const t = timeRef.current;
    
    return (
      <div className="flex items-center justify-center h-full gap-2">
        {[0, 1, 2].map((index) => {
          let scale = 0.3;
          
          if (state === 'listening' || state === 'speaking') {
            scale = 0.5 + Math.sin(t * 5 + index * 0.8) * 0.5;
          } else if (state === 'processing') {
            const phase = (t * 3 + index * 0.5) % 1;
            scale = phase < 0.5 ? 0.3 + phase : 0.8 - (phase - 0.5);
          }
          
          return (
            <div
              key={index}
              className="rounded-full transition-all duration-100"
              style={{
                width: '8px',
                height: '8px',
                backgroundColor: colors.base,
                transform: `scale(${clamp(scale, 0.3, 1)})`,
                boxShadow: glow ? `0 0 6px ${colors.glow}` : undefined,
              }}
            />
          );
        })}
      </div>
    );
  };

  return (
    <div
      ref={containerRef}
      className={cn(voiceWaveformVariants({ size, color }), className)}
    >
      {renderContent()}
    </div>
  );
};

// =============================================================================
// EXPORTS
// =============================================================================

export { voiceWaveformVariants };
