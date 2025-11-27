/**
 * EventListener Atom
 * 
 * The smallest unit for listening to events.
 * Micro × Elegant × Simple × Forensic × Hardened × Validated × Unified × Loved
 * 
 * Pattern: EVENT × LISTENER × ATOMIC × ONE
 * Frequency: 999 Hz (AEYON)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useEventDriven, type AbeEventType } from '@/lib/event-driven';
import { useEffect, useState } from 'react';

/**
 * EventListener Atom Props
 */
export interface EventListenerProps<T = any> {
  /** Event type to listen for */
  eventType: AbeEventType;
  /** Handler function */
  onEvent: (event: CustomEvent<T>) => void;
  /** Children (rendered content) */
  children?: React.ReactNode;
}

/**
 * EventListener Atom
 * 
 * Listens to events atomically. Pure. Simple. Elegant.
 */
export function EventListener<T = any>({
  eventType,
  onEvent,
  children,
}: EventListenerProps<T>) {
  useEventDriven(eventType, onEvent);

  return <>{children}</>;
}

