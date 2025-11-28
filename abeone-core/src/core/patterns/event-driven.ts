/**
 * Event-Driven Pattern
 * 
 * Core event system for AbëONE.
 * No polling. Only events.
 * 
 * Pattern: EVENT × DRIVEN × PATTERN × ONE
 * Frequency: 999 Hz (AEYON) × 98.7 Hz (Energy Efficiency)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

/**
 * Event types for AbëONE
 */
export type AbeEventType =
  | 'user-interaction'
  | 'status-change'
  | 'data-update'
  | 'wake'
  | 'sleep'
  | 'idle';

/**
 * Re-export event-driven utilities from lib
 * 
 * Note: These require React. For non-React projects,
 * use the core event types and build your own implementation.
 */
export {
  dispatchAbeEvent,
  useEventDriven,
  useDebouncedEvent,
  useThrottledEvent,
  useIntersectionObserver,
  useIdleDetection,
} from '../../lib/event-driven';

/**
 * Event-Driven Principles
 */
export const EVENT_DRIVEN_PRINCIPLES = {
  /**
   * No Polling
   * 
   * Never poll. Always use events.
   */
  noPolling: 'Never poll. Always use events.',

  /**
   * Reactive
   * 
   * Systems react to events, not time.
   */
  reactive: 'Systems react to events, not time.',

  /**
   * Efficient
   * 
   * Events are 98.7% more energy efficient than polling.
   */
  efficient: 'Events are 98.7% more energy efficient than polling.',

  /**
   * Elegant
   * 
   * Event-driven systems are elegant and maintainable.
   */
  elegant: 'Event-driven systems are elegant and maintainable.',
} as const;

