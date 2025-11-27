/**
 * AbëONE Atom: SpeechSynthesis
 * 
 * Text-to-Speech using Web Speech API.
 * She speaks. She listens. She knows.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { useEventDriven, dispatchAbeEvent, type AbeEventType } from '@/lib/event-driven';

// =============================================================================
// TYPES
// =============================================================================

export interface SpeechSynthesisProps {
  /** Text to speak */
  text?: string;
  /** Voice to use (by name or index) */
  voice?: string | number;
  /** Speech rate (0.1 to 10, default 1) */
  rate?: number;
  /** Speech pitch (0 to 2, default 1) */
  pitch?: number;
  /** Speech volume (0 to 1, default 1) */
  volume?: number;
  /** Language code (e.g., 'en-US') */
  lang?: string;
  /** Event type to listen for speech requests */
  eventType?: AbeEventType;
  /** Auto-speak when text changes */
  autoSpeak?: boolean;
  /** Callback when speech starts */
  onStart?: () => void;
  /** Callback when speech ends */
  onEnd?: () => void;
  /** Callback when speech errors */
  onError?: (error: Error) => void;
  /** Children (optional) */
  children?: React.ReactNode;
}

// =============================================================================
// SPEECH SYNTHESIS HOOK
// =============================================================================

export function useSpeechSynthesis(options: {
  text?: string;
  voice?: string | number;
  rate?: number;
  pitch?: number;
  volume?: number;
  lang?: string;
  onStart?: () => void;
  onEnd?: () => void;
  onError?: (error: Error) => void;
} = {}) {
  const {
    text,
    voice,
    rate = 1,
    pitch = 1,
    volume = 1,
    lang = 'en-US',
    onStart,
    onEnd,
    onError,
  } = options;

  const utteranceRef = React.useRef<SpeechSynthesisUtterance | null>(null);
  const isSpeakingRef = React.useRef(false);

  const speak = React.useCallback((speechText: string) => {
    if (!('speechSynthesis' in window)) {
      onError?.(new Error('Speech synthesis not supported'));
      return;
    }

    // Cancel any ongoing speech
    if (isSpeakingRef.current) {
      window.speechSynthesis.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(speechText);
    utterance.rate = rate;
    utterance.pitch = pitch;
    utterance.volume = volume;
    utterance.lang = lang;

    // Set voice if specified
    if (voice !== undefined) {
      const voices = window.speechSynthesis.getVoices();
      if (typeof voice === 'number' && voices[voice]) {
        utterance.voice = voices[voice];
      } else if (typeof voice === 'string') {
        const foundVoice = voices.find((v) => v.name === voice || v.lang === voice);
        if (foundVoice) {
          utterance.voice = foundVoice;
        }
      }
    }

    // Event handlers
    utterance.onstart = () => {
      isSpeakingRef.current = true;
      onStart?.();
      dispatchAbeEvent('status-change', { status: 'speaking' });
    };

    utterance.onend = () => {
      isSpeakingRef.current = false;
      onEnd?.();
      dispatchAbeEvent('status-change', { status: 'sleeping' });
    };

    utterance.onerror = (event) => {
      isSpeakingRef.current = false;
      onError?.(new Error(`Speech synthesis error: ${event.error}`));
      dispatchAbeEvent('status-change', { status: 'error' });
    };

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  }, [rate, pitch, volume, lang, voice, onStart, onEnd, onError]);

  const stop = React.useCallback(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      isSpeakingRef.current = false;
    }
  }, []);

  const pause = React.useCallback(() => {
    if ('speechSynthesis' in window && isSpeakingRef.current) {
      window.speechSynthesis.pause();
    }
  }, []);

  const resume = React.useCallback(() => {
    if ('speechSynthesis' in window && isSpeakingRef.current) {
      window.speechSynthesis.resume();
    }
  }, []);

  const isSpeaking = React.useCallback(() => {
    return isSpeakingRef.current;
  }, []);

  // Auto-speak when text changes
  React.useEffect(() => {
    if (text && options.autoSpeak !== false) {
      speak(text);
    }
  }, [text, speak, options.autoSpeak]);

  return {
    speak,
    stop,
    pause,
    resume,
    isSpeaking,
  };
}

// =============================================================================
// SPEECH SYNTHESIS COMPONENT
// =============================================================================

export const SpeechSynthesis: React.FC<SpeechSynthesisProps> = ({
  text,
  voice,
  rate = 1,
  pitch = 1,
  volume = 1,
  lang = 'en-US',
  eventType = 'data-update',
  autoSpeak = true,
  onStart,
  onEnd,
  onError,
  children,
}) => {
  const { speak, stop } = useSpeechSynthesis({
    voice,
    rate,
    pitch,
    volume,
    lang,
    onStart,
    onEnd,
    onError,
    autoSpeak: false, // We'll handle it manually
  });

  // Listen for speech events
  useEventDriven<{ text?: string; action?: 'speak' | 'stop' }>(
    eventType,
    (event) => {
      if (event.detail.action === 'stop') {
        stop();
      } else if (event.detail.text) {
        speak(event.detail.text);
      } else if (text) {
        speak(text);
      }
    }
  );

  // Auto-speak when text changes
  React.useEffect(() => {
    if (text && autoSpeak) {
      speak(text);
    }
  }, [text, autoSpeak, speak]);

  return <>{children}</>;
};

// =============================================================================
// VOICE UTILITIES
// =============================================================================

export function getVoices() {
  if (!('speechSynthesis' in window)) {
    return [];
  }
  return window.speechSynthesis.getVoices();
}

export function getVoiceByName(name: string) {
  return getVoices().find((voice) => voice.name === name);
}

export function getVoiceByLang(lang: string) {
  return getVoices().find((voice) => voice.lang === lang);
}

// =============================================================================
// EXPORTS
// =============================================================================

export default SpeechSynthesis;

