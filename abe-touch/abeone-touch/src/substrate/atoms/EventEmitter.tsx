/**
 * EventEmitter Atom
 * 
 * The smallest unit for dispatching events.
 * Micro × Elegant × Simple × Forensic × Hardened × Validated × Unified × Loved
 * 
 * Pattern: EVENT × EMITTER × ATOMIC × ONE
 * Frequency: 999 Hz (AEYON)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { dispatchAbeEvent, type AbeEventType } from '@/lib/event-driven';

/**
 * EventEmitter Atom Props
 */
export interface EventEmitterProps {
  /** Event type to dispatch */
  eventType: AbeEventType;
  /** Event detail data */
  detail?: any;
  /** Callback when event is dispatched */
  onDispatch?: () => void;
  /** Children (trigger element) */
  children: React.ReactNode;
}

/**
 * EventEmitter Atom
 * 
 * Dispatches events atomically. Pure. Simple. Elegant.
 */
export function EventEmitter({
  eventType,
  detail,
  onDispatch,
  children,
}: EventEmitterProps) {
  const handleDispatch = () => {
    dispatchAbeEvent(eventType, detail);
    onDispatch?.();
  };

  return (
    <div onClick={handleDispatch} style={{ display: 'contents' }}>
      {children}
    </div>
  );
}

