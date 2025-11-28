/**
 * AbëONE Atom: PermissionHandler
 * 
 * Handles browser permissions for microphone and other features.
 * 
 * Pattern: PERMISSION × HANDLER × ATOM × UX × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz) + YAGNI (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import * as React from 'react';

/**
 * Permission Types
 */
export type PermissionType = 'microphone' | 'camera' | 'notifications' | 'geolocation';

/**
 * Permission State
 */
export type PermissionState = 'granted' | 'denied' | 'prompt' | 'unsupported';

/**
 * Permission Handler Options
 */
export interface UsePermissionHandlerOptions {
  /** Permission type to check */
  permission: PermissionType;
  /** Callback when permission changes */
  onPermissionChange?: (state: PermissionState) => void;
  /** Auto-request permission on mount */
  autoRequest?: boolean;
}

/**
 * Map permission type to browser permission name
 */
function getPermissionName(type: PermissionType): PermissionName {
  switch (type) {
    case 'microphone':
      return 'microphone';
    case 'camera':
      return 'camera';
    case 'notifications':
      return 'notifications';
    case 'geolocation':
      return 'geolocation';
    default:
      return 'microphone';
  }
}

/**
 * usePermissionHandler Hook
 */
export function usePermissionHandler(options: UsePermissionHandlerOptions) {
  const { permission, onPermissionChange, autoRequest = false } = options;
  
  const [state, setState] = React.useState<PermissionState>('prompt');
  const [isChecking, setIsChecking] = React.useState(false);

  /**
   * Check permission state
   */
  const checkPermission = React.useCallback(async (): Promise<PermissionState> => {
    if (typeof navigator === 'undefined' || !navigator.permissions) {
      return 'unsupported';
    }

    try {
      setIsChecking(true);
      const permissionName = getPermissionName(permission);
      const result = await navigator.permissions.query({ name: permissionName });
      
      let permissionState: PermissionState = 'prompt';
      
      if (result.state === 'granted') {
        permissionState = 'granted';
      } else if (result.state === 'denied') {
        permissionState = 'denied';
      } else {
        permissionState = 'prompt';
      }

      setState(permissionState);
      onPermissionChange?.(permissionState);
      return permissionState;
    } catch (error) {
      console.warn('Permission check failed:', error);
      // Fallback: try to check via getUserMedia for microphone
      if (permission === 'microphone') {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          stream.getTracks().forEach(track => track.stop());
          setState('granted');
          return 'granted';
        } catch (err) {
          setState('denied');
          return 'denied';
        }
      }
      setState('unsupported');
      return 'unsupported';
    } finally {
      setIsChecking(false);
    }
  }, [permission, onPermissionChange]);

  /**
   * Request permission
   */
  const requestPermission = React.useCallback(async (): Promise<PermissionState> => {
    if (typeof navigator === 'undefined') {
      return 'unsupported';
    }

    try {
      setIsChecking(true);

      if (permission === 'microphone') {
        // Request microphone via getUserMedia
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        setState('granted');
        onPermissionChange?.('granted');
        return 'granted';
      } else if (permission === 'notifications') {
        // Request notifications
        const result = await Notification.requestPermission();
        const permissionState = result === 'granted' ? 'granted' : 'denied';
        setState(permissionState);
        onPermissionChange?.(permissionState);
        return permissionState;
      } else {
        // For other permissions, check current state
        return await checkPermission();
      }
    } catch (error) {
      console.error('Permission request failed:', error);
      setState('denied');
      onPermissionChange?.('denied');
      return 'denied';
    } finally {
      setIsChecking(false);
    }
  }, [permission, checkPermission, onPermissionChange]);

  // Check permission on mount
  React.useEffect(() => {
    checkPermission();
  }, [checkPermission]);

  // Auto-request if enabled
  React.useEffect(() => {
    if (autoRequest && state === 'prompt') {
      requestPermission();
    }
  }, [autoRequest, state, requestPermission]);

  return {
    state,
    isChecking,
    checkPermission,
    requestPermission,
    isGranted: state === 'granted',
    isDenied: state === 'denied',
    isPrompt: state === 'prompt',
    isUnsupported: state === 'unsupported',
  };
}

