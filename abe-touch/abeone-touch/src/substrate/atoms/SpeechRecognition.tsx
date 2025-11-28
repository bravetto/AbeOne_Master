/**
 * AbëONE Atom: SpeechRecognition
 * 
 * Speech-to-text using Web Speech Recognition API.
 * Event-driven, energy-efficient, type-safe.
 * 
 * Pattern: SPEECH × RECOGNITION × ATOM × EVENT × DRIVEN × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence) × 98.7 Hz (Efficiency)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz) + YAGNI (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import * as React from 'react';
import { dispatchAbeEvent } from '@/lib/event-driven';

/**
 * Speech Recognition Types
 */
export interface SpeechRecognitionError {
  error: string;
  message: string;
}

export interface UseSpeechRecognitionOptions {
  /** Language code (default: 'en-US') */
  lang?: string;
  /** Continuous recognition (default: false) */
  continuous?: boolean;
  /** Interim results (default: true) */
  interimResults?: boolean;
  /** Maximum alternatives (default: 1) */
  maxAlternatives?: number;
  /** Callback when recognition starts */
  onStart?: () => void;
  /** Callback when recognition ends */
  onEnd?: () => void;
  /** Callback with transcript */
  onTranscript?: (text: string, isFinal: boolean) => void;
  /** Callback on error */
  onError?: (error: SpeechRecognitionError) => void;
}

/**
 * Web Speech Recognition API types (using browser types)
 */
interface SpeechRecognition extends EventTarget {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  start(): void;
  stop(): void;
  abort(): void;
  onstart: ((event: Event) => void) | null;
  onend: ((event: Event) => void) | null;
  onresult: ((event: any) => void) | null;
  onerror: ((event: any) => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

/**
 * A constructor type for the browser's SpeechRecognition implementation
 */
type BrowserSpeechRecognitionConstructor = new () => SpeechRecognition;

/**
 * Get Speech Recognition constructor
 */
function getSpeechRecognition(): BrowserSpeechRecognitionConstructor | null {
  if (typeof window === 'undefined') return null;
  
  const SR =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;
  
  return SR ?? null;
}

/**
 * Check if Speech Recognition is available
 */
export function isSpeechRecognitionAvailable(): boolean {
  return getSpeechRecognition() !== null;
}

/**
 * useSpeechRecognition Hook
 */
export function useSpeechRecognition(options: UseSpeechRecognitionOptions = {}) {
  const {
    lang = 'en-US',
    continuous = false,
    interimResults = true,
    maxAlternatives = 1,
    onStart,
    onEnd,
    onTranscript,
    onError,
  } = options;

  const recognitionRef = React.useRef<SpeechRecognition | null>(null);
  const isListeningRef = React.useRef(false);

  // Initialize recognition
  React.useEffect(() => {
    const Recognition = getSpeechRecognition();
    if (!Recognition) {
      console.warn('Speech Recognition API not available');
      return;
    }

    const recognition = new Recognition();
    recognition.lang = lang;
    recognition.continuous = continuous;
    recognition.interimResults = interimResults;
    recognition.maxAlternatives = maxAlternatives;

    // Handle results
    recognition.onresult = (event: any) => {
      const resultItem = event.results[event.resultIndex];
      const transcript = resultItem[0].transcript;
      const confidence = resultItem[0].confidence;
      const isFinal = resultItem.isFinal;

      // Dispatch event
      dispatchAbeEvent('data-update', {
        type: 'transcript',
        transcript,
        confidence,
        isFinal,
      });

      // Call callback
      onTranscript?.(transcript, isFinal);
    };

    // Handle errors
    recognition.onerror = (event: any) => {
      const error: SpeechRecognitionError = {
        error: event.error,
        message: event.message,
      };

      // Dispatch event
      dispatchAbeEvent('data-update', {
        type: 'error',
        error: error.message,
      });

      // Call callback
      onError?.(error);
    };

    // Handle start
    recognition.onstart = () => {
      isListeningRef.current = true;
      dispatchAbeEvent('status-change', { status: 'listening' });
      onStart?.();
    };

    // Handle end
    recognition.onend = () => {
      isListeningRef.current = false;
      dispatchAbeEvent('status-change', { status: 'sleeping' });
      onEnd?.();
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
        recognitionRef.current = null;
      }
    };
  }, [lang, continuous, interimResults, maxAlternatives, onStart, onEnd, onTranscript, onError]);

  // Start recognition
  const start = React.useCallback(() => {
    if (!recognitionRef.current || isListeningRef.current) return;
    
    try {
      recognitionRef.current.start();
    } catch (error) {
      console.error('Failed to start speech recognition:', error);
      onError?.({
        error: 'start-failed',
        message: error instanceof Error ? error.message : 'Failed to start recognition',
      });
    }
  }, [onError]);

  // Stop recognition
  const stop = React.useCallback(() => {
    if (!recognitionRef.current || !isListeningRef.current) return;
    
    try {
      recognitionRef.current.stop();
    } catch (error) {
      console.error('Failed to stop speech recognition:', error);
    }
  }, []);

  // Abort recognition
  const abort = React.useCallback(() => {
    if (!recognitionRef.current) return;
    
    try {
      recognitionRef.current.abort();
      isListeningRef.current = false;
    } catch (error) {
      console.error('Failed to abort speech recognition:', error);
    }
  }, []);

  return {
    start,
    stop,
    abort,
    isAvailable: isSpeechRecognitionAvailable(),
  };
}

