/**
 * AbëONE Atom: NeuromorphicButton
 * 
 * Soft UI button with realistic depth, tactile feedback, and organic feel.
 * The primary interaction element for the Interface of the Future.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// =============================================================================
// VARIANTS
// =============================================================================

const neuromorphicButtonVariants = cva(
  [
    'inline-flex items-center justify-center font-medium transition-all duration-200',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
    'focus-visible:ring-[var(--abe-primary)] focus-visible:ring-offset-[var(--abe-surface)]',
    'disabled:pointer-events-none disabled:opacity-50',
    'select-none cursor-pointer',
    'bg-[var(--abe-surface)]',
  ],
  {
    variants: {
      variant: {
        raised: [
          'shadow-[6px_6px_12px_var(--neu-shadow-dark),-6px_-6px_12px_var(--neu-shadow-light)]',
          'hover:shadow-[8px_8px_16px_var(--neu-shadow-dark),-8px_-8px_16px_var(--neu-shadow-light)]',
          'active:shadow-[inset_4px_4px_8px_var(--neu-shadow-dark),inset_-4px_-4px_8px_var(--neu-shadow-light)]',
          'active:scale-[0.98]',
        ],
        flat: [
          'shadow-[2px_2px_4px_var(--neu-shadow-dark),-2px_-2px_4px_var(--neu-shadow-light)]',
          'hover:shadow-[4px_4px_8px_var(--neu-shadow-dark),-4px_-4px_8px_var(--neu-shadow-light)]',
          'active:shadow-[inset_2px_2px_4px_var(--neu-shadow-dark),inset_-2px_-2px_4px_var(--neu-shadow-light)]',
        ],
        pressed: [
          'shadow-[inset_4px_4px_8px_var(--neu-shadow-dark),inset_-4px_-4px_8px_var(--neu-shadow-light)]',
          'hover:shadow-[inset_6px_6px_10px_var(--neu-shadow-dark),inset_-6px_-6px_10px_var(--neu-shadow-light)]',
        ],
        glow: [
          'shadow-[6px_6px_12px_var(--neu-shadow-dark),-6px_-6px_12px_var(--neu-shadow-light),0_0_15px_var(--abe-primary)]',
          'hover:shadow-[8px_8px_16px_var(--neu-shadow-dark),-8px_-8px_16px_var(--neu-shadow-light),0_0_25px_var(--abe-primary)]',
          'active:shadow-[inset_4px_4px_8px_var(--neu-shadow-dark),inset_-4px_-4px_8px_var(--neu-shadow-light)]',
        ],
        convex: [
          'shadow-[6px_6px_12px_var(--neu-shadow-dark),-6px_-6px_12px_var(--neu-shadow-light)]',
          'bg-gradient-to-br from-[var(--abe-elevated)] to-[var(--abe-background)]',
          'hover:shadow-[8px_8px_16px_var(--neu-shadow-dark),-8px_-8px_16px_var(--neu-shadow-light)]',
          'active:scale-[0.98]',
        ],
        concave: [
          'shadow-[inset_4px_4px_8px_var(--neu-shadow-dark),inset_-4px_-4px_8px_var(--neu-shadow-light)]',
          'bg-gradient-to-br from-[var(--abe-background)] to-[var(--abe-elevated)]',
        ],
      },
      size: {
        sm: 'h-9 px-4 text-sm rounded-lg gap-2',
        md: 'h-11 px-6 text-base rounded-xl gap-2',
        lg: 'h-14 px-8 text-lg rounded-2xl gap-3',
        xl: 'h-16 px-10 text-xl rounded-2xl gap-3',
        icon: 'h-11 w-11 rounded-xl',
        'icon-sm': 'h-9 w-9 rounded-lg',
        'icon-lg': 'h-14 w-14 rounded-2xl',
        'icon-xl': 'h-20 w-20 rounded-3xl',
      },
      shape: {
        rounded: '',
        pill: 'rounded-full',
        square: 'rounded-lg',
        circle: 'rounded-full aspect-square',
      },
      color: {
        surface: 'text-[var(--abe-text-primary)]',
        primary: 'text-[var(--abe-primary)]',
        accent: 'text-[var(--abe-accent)]',
        success: 'text-[var(--abe-success)]',
        warning: 'text-[var(--abe-warning)]',
        error: 'text-[var(--abe-error)]',
      },
    },
    defaultVariants: {
      variant: 'raised',
      size: 'md',
      shape: 'rounded',
      color: 'surface',
    },
  }
);

// =============================================================================
// TYPES
// =============================================================================

export interface NeuromorphicButtonProps
  extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'color'>,
    VariantProps<typeof neuromorphicButtonVariants> {
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  pulse?: boolean;
}

// =============================================================================
// COMPONENT
// =============================================================================

export const NeuromorphicButton = React.forwardRef<
  HTMLButtonElement,
  NeuromorphicButtonProps
>(
  (
    {
      className,
      variant,
      size,
      shape,
      color,
      loading = false,
      leftIcon,
      rightIcon,
      pulse = false,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          neuromorphicButtonVariants({ variant, size, shape, color }),
          pulse && 'animate-pulse',
          className
        )}
        {...props}
      >
        {loading ? (
          <LoadingSpinner size={size} />
        ) : (
          <>
            {leftIcon && <span className="shrink-0">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="shrink-0">{rightIcon}</span>}
          </>
        )}
      </button>
    );
  }
);

NeuromorphicButton.displayName = 'NeuromorphicButton';

// =============================================================================
// LOADING SPINNER
// =============================================================================

const LoadingSpinner: React.FC<{ size?: string | null }> = ({ size }) => {
  const sizeClass = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
    xl: 'h-7 w-7',
    icon: 'h-5 w-5',
    'icon-sm': 'h-4 w-4',
    'icon-lg': 'h-6 w-6',
    'icon-xl': 'h-8 w-8',
  }[size ?? 'md'];

  return (
    <svg
      className={cn('animate-spin', sizeClass)}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
};

// =============================================================================
// ICON BUTTON VARIANT
// =============================================================================

export interface NeuromorphicIconButtonProps
  extends Omit<NeuromorphicButtonProps, 'leftIcon' | 'rightIcon' | 'children'> {
  icon: React.ReactNode;
  'aria-label': string;
}

export const NeuromorphicIconButton = React.forwardRef<
  HTMLButtonElement,
  NeuromorphicIconButtonProps
>(({ icon, size = 'icon', shape = 'circle', className, ...props }, ref) => {
  return (
    <NeuromorphicButton
      ref={ref}
      size={size}
      shape={shape}
      className={className}
      {...props}
    >
      {icon}
    </NeuromorphicButton>
  );
});

NeuromorphicIconButton.displayName = 'NeuromorphicIconButton';

// =============================================================================
// TOGGLE VARIANT
// =============================================================================

export interface NeuromorphicToggleProps
  extends Omit<NeuromorphicButtonProps, 'variant'> {
  pressed?: boolean;
  defaultPressed?: boolean;
  onPressedChange?: (pressed: boolean) => void;
}

export const NeuromorphicToggle = React.forwardRef<
  HTMLButtonElement,
  NeuromorphicToggleProps
>(
  (
    {
      pressed: controlledPressed,
      defaultPressed = false,
      onPressedChange,
      className,
      ...props
    },
    ref
  ) => {
    const [internalPressed, setInternalPressed] = React.useState(defaultPressed);
    const isControlled = controlledPressed !== undefined;
    const pressed = isControlled ? controlledPressed : internalPressed;

    const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
      const newPressed = !pressed;
      if (!isControlled) {
        setInternalPressed(newPressed);
      }
      onPressedChange?.(newPressed);
      props.onClick?.(e);
    };

    return (
      <NeuromorphicButton
        ref={ref}
        variant={pressed ? 'pressed' : 'raised'}
        aria-pressed={pressed}
        className={className}
        {...props}
        onClick={handleClick}
      />
    );
  }
);

NeuromorphicToggle.displayName = 'NeuromorphicToggle';

// =============================================================================
// EXPORTS
// =============================================================================

export { neuromorphicButtonVariants };
