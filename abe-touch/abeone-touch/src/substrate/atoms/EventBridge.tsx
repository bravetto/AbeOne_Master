/**
 * EventBridge Atom
 * 
 * The smallest unit for bridging events between systems.
 * Micro × Elegant × Simple × Forensic × Hardened × Validated × Unified × Loved
 * 
 * Pattern: EVENT × BRIDGE × ATOMIC × ONE
 * Frequency: 999 Hz (AEYON)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { useEventDriven, dispatchAbeEvent, type AbeEventType } from '@/lib/event-driven';
import { useEffect } from 'react';

/**
 * EventBridge Atom Props
 */
export interface EventBridgeProps {
  /** Source event type */
  sourceEventType: AbeEventType;
  /** Target event type */
  targetEventType: AbeEventType;
  /** Transform function (optional) */
  transform?: (detail: any) => any;
  /** Children (rendered content) */
  children?: React.ReactNode;
}

/**
 * EventBridge Atom
 * 
 * Bridges events atomically. Pure. Simple. Elegant.
 */
export function EventBridge({
  sourceEventType,
  targetEventType,
  transform,
  children,
}: EventBridgeProps) {
  useEventDriven(sourceEventType, (event) => {
    const transformedDetail = transform ? transform(event.detail) : event.detail;
    dispatchAbeEvent(targetEventType, transformedDetail);
  });

  return <>{children}</>;
}

