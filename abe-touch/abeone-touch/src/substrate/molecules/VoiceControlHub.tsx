/**
 * AbëONE Molecule: VoiceControlHub
 * 
 * THE COCKPIT.
 * 
 * The single point of contact between Biological Intelligence (You) 
 * and Digital Intelligence (AbëONE).
 * 
 * This is not a UI component. This is a PORTAL.
 * 
 * "Does it feel like you are poking a machine, or waking up a mind?"
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { 
  dispatchAbeEvent,
  useEventDriven,
  type AbeEventType,
} from '@/lib/event-driven';
import { 
  NeuromorphicButton,
  StatusLED,
  VoiceWaveform,
  useSpeechRecognition,
  useSpeechSynthesis,
  usePermissionHandler,
  ErrorRecovery,
  type LEDColor,
  type LEDState,
  type WaveformState,
} from '@/substrate/atoms';
import { useLLMClient } from './LLMClient';

// =============================================================================
// TYPES
// =============================================================================

export type AgentStatus = 
  | 'sleeping'    // Dormant, waiting for activation
  | 'listening'   // Actively receiving voice input
  | 'thinking'    // Processing, AI is working
  | 'speaking'    // AI is responding
  | 'error';      // Something went wrong

export interface VoiceControlHubProps {
  /** Callback when voice input starts */
  onListenStart?: () => void;
  /** Callback when voice input ends */
  onListenEnd?: () => void;
  /** Callback with transcribed text */
  onTranscript?: (text: string) => void;
  /** Callback when user cancels */
  onCancel?: () => void;
  /** External status control */
  status?: AgentStatus;
  /** Audio analysis data for waveform */
  audioData?: { volume?: number };
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Show status label */
  showLabel?: boolean;
  /** Custom status labels */
  labels?: Partial<Record<AgentStatus, string>>;
  /** Disable interactions */
  disabled?: boolean;
  /** Custom class name */
  className?: string;
  /** Enable LLM integration (speech → LLM → speech) */
  enableLLM?: boolean;
  /** LLM API endpoint */
  llmEndpoint?: string;
  /** Speech recognition language */
  recognitionLang?: string;
  /** Speech synthesis options */
  speechOptions?: {
    rate?: number;
    pitch?: number;
    volume?: number;
    lang?: string;
  };
  /** Show interim recognition results */
  showInterimResults?: boolean;
  /** Enable mock mode (for testing without backend) */
  mockMode?: boolean;
}

// =============================================================================
// STATUS CONFIGURATION
// =============================================================================

interface StatusConfig {
  led: { color: LEDColor; state: LEDState };
  waveform: WaveformState;
  label: string;
  icon: 'mic' | 'mic-off' | 'loader' | 'volume' | 'alert';
  color: string;
}

const statusConfigs: Record<AgentStatus, StatusConfig> = {
  sleeping: {
    led: { color: 'white', state: 'breathe' },
    waveform: 'idle',
    label: 'TAP TO WAKE',
    icon: 'mic-off',
    color: 'var(--abe-text-muted)',
  },
  listening: {
    led: { color: 'cyan', state: 'pulse' },
    waveform: 'listening',
    label: 'LISTENING',
    icon: 'mic',
    color: 'var(--abe-primary)',
  },
  thinking: {
    led: { color: 'purple', state: 'pulse' },
    waveform: 'processing',
    label: 'THINKING',
    icon: 'loader',
    color: 'var(--abe-accent)',
  },
  speaking: {
    led: { color: 'green', state: 'on' },
    waveform: 'speaking',
    label: 'SPEAKING',
    icon: 'volume',
    color: 'var(--abe-success)',
  },
  error: {
    led: { color: 'red', state: 'flicker' },
    waveform: 'error',
    label: 'ERROR',
    icon: 'alert',
    color: 'var(--abe-error)',
  },
};

// =============================================================================
// ICONS
// =============================================================================

const Icons: Record<string, React.ReactNode> = {
  'mic': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
      <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
      <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
      <line x1="12" x2="12" y1="19" y2="22"/>
    </svg>
  ),
  'mic-off': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
      <line x1="2" x2="22" y1="2" y2="22"/>
      <path d="M18.89 13.23A7.12 7.12 0 0 0 19 12v-2"/>
      <path d="M5 10v2a7 7 0 0 0 12 5"/>
      <path d="M15 9.34V5a3 3 0 0 0-5.68-1.33"/>
      <path d="M9 9v3a3 3 0 0 0 5.12 2.12"/>
      <line x1="12" x2="12" y1="19" y2="22"/>
    </svg>
  ),
  'loader': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full animate-spin">
      <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
    </svg>
  ),
  'volume': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
      <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
      <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
    </svg>
  ),
  'alert': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
      <circle cx="12" cy="12" r="10"/>
      <line x1="12" x2="12" y1="8" y2="12"/>
      <line x1="12" x2="12.01" y1="16" y2="16"/>
    </svg>
  ),
};

// =============================================================================
// NEUROMORPHIC CONTAINER (The "Screen")
// =============================================================================

const NeuromorphicContainer: React.FC<{
  children: React.ReactNode;
  className?: string;
  inset?: boolean;
}> = ({ children, className, inset = true }) => (
  <div
    className={cn(
      'rounded-2xl p-4 transition-all duration-300 bg-[var(--abe-surface)]',
      inset
        ? 'shadow-[inset_4px_4px_8px_var(--neu-shadow-dark),inset_-4px_-4px_8px_var(--neu-shadow-light)]'
        : 'shadow-[6px_6px_12px_var(--neu-shadow-dark),-6px_-6px_12px_var(--neu-shadow-light)]',
      className
    )}
  >
    {children}
  </div>
);

// =============================================================================
// SIZE CONFIGURATIONS
// =============================================================================

const sizeConfigs = {
  sm: {
    button: 'h-16 w-16',
    icon: 'h-6 w-6',
    display: 'w-48 h-16',
    waveform: 'sm' as const,
    led: 'sm' as const,
    gap: 'gap-4',
    text: 'text-[10px]',
  },
  md: {
    button: 'h-20 w-20',
    icon: 'h-8 w-8',
    display: 'w-64 h-20',
    waveform: 'md' as const,
    led: 'md' as const,
    gap: 'gap-6',
    text: 'text-xs',
  },
  lg: {
    button: 'h-24 w-24',
    icon: 'h-10 w-10',
    display: 'w-80 h-24',
    waveform: 'lg' as const,
    led: 'lg' as const,
    gap: 'gap-8',
    text: 'text-sm',
  },
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export const VoiceControlHub: React.FC<VoiceControlHubProps> = ({
  onListenStart,
  onListenEnd,
  onTranscript,
  onCancel,
  status: externalStatus,
  audioData,
  size = 'md',
  showLabel = true,
  labels = {},
  disabled = false,
  className,
  enableLLM = false,
  llmEndpoint = '/api/llm/chat',
  recognitionLang = 'en-US',
  speechOptions = {
    rate: 1.0,
    pitch: 1.0,
    volume: 1.0,
    lang: 'en-US',
  },
  showInterimResults = true,
  mockMode = false,
}) => {
  const [internalStatus, setInternalStatus] = React.useState<AgentStatus>('sleeping');
  const [interimTranscript, setInterimTranscript] = React.useState<string>('');
  const [llmError, setLlmError] = React.useState<Error | null>(null);
  const conversationContextRef = React.useRef<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const status = externalStatus ?? internalStatus;
  
  const config = statusConfigs[status];
  const sizeConfig = sizeConfigs[size];
  const label = labels[status] ?? config.label;
  
  // Permission handler for microphone
  const { state: micPermission, requestPermission: requestMicPermission } = usePermissionHandler({
    permission: 'microphone',
    onPermissionChange: (state) => {
      if (state === 'denied') {
        dispatchAbeEvent('status-change', { status: 'error' });
      }
    },
  });

  // Mock response generator (for testing without backend)
  const generateMockResponse = React.useCallback((message: string): string => {
    const responses = [
      `I heard you say: "${message}". This is a mock response while we wait for the backend.`,
      `Mock response: I understand you said "${message}". The real backend will be connected soon!`,
      `[MOCK] You said: "${message}". This is a placeholder response.`,
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }, []);

  // LLM integration hooks (only if enabled)
  const { sendMessage, abort: abortLLM, isLoading: isLLMLoading } = useLLMClient({
    endpoint: llmEndpoint,
    onRequestStart: () => {
      dispatchAbeEvent('status-change', { status: 'thinking' });
      setLlmError(null);
    },
    onRequestComplete: (response) => {
      // Validate response
      if (!response || !response.response || typeof response.response !== 'string') {
        console.error('Invalid LLM response format');
        dispatchAbeEvent('status-change', { status: 'error' });
        return;
      }
      
      // Store assistant response in conversation context
      conversationContextRef.current.push({ 
        role: 'assistant', 
        content: response.response 
      });
      
      // Trim context to last 20 messages (10 user + 10 assistant)
      if (conversationContextRef.current.length > 20) {
        conversationContextRef.current = conversationContextRef.current.slice(-20);
      }
      
      dispatchAbeEvent('status-change', { status: 'speaking' });
      // Auto-speak LLM response
      if (enableLLM && speak) {
        speak(response.response);
      }
    },
    onError: (error) => {
      console.error('LLM error:', error);
      setLlmError(error);
      dispatchAbeEvent('status-change', { status: 'error' });
    },
  });

  // Speech recognition hook (only if LLM enabled)
  const { start: startRecognition, stop: stopRecognition, isAvailable: recognitionAvailable } = useSpeechRecognition({
    lang: recognitionLang,
    continuous: false,
    interimResults: true,
    onTranscript: (text, isFinal) => {
      if (isFinal) {
        // Stop recognition after final transcript
        stopRecognition();
        setInterimTranscript('');
        
        // Validate transcript
        const trimmedText = text.trim();
        if (!trimmedText || trimmedText.length < 1) {
          console.warn('Empty transcript received');
          dispatchAbeEvent('status-change', { status: 'sleeping' });
          return;
        }
        
        // Sanitize transcript (basic cleaning)
        const sanitizedText = trimmedText
          .replace(/\s+/g, ' ')  // Multiple spaces to single
          .replace(/[^\w\s.,!?;:'"()-]/g, '')  // Remove special chars
          .substring(0, 1000);  // Max length
        
        if (enableLLM) {
          if (mockMode) {
            // Mock mode: generate fake response
            const mockResponse = generateMockResponse(sanitizedText);
            setTimeout(() => {
              dispatchAbeEvent('status-change', { status: 'speaking' });
              if (speak) {
                speak(mockResponse);
              }
            }, 500);
          } else {
            // Real mode: send to LLM with conversation context
            conversationContextRef.current.push({ role: 'user', content: sanitizedText });
            
            // Get conversation context (last 10 messages)
            const context = conversationContextRef.current
              .slice(-10)
              .map((msg: { role: 'user' | 'assistant'; content: string }) => 
                `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`
              );
            
            sendMessage({ 
              message: sanitizedText,
              context: context,
            });
          }
        }
        onTranscript?.(sanitizedText);
      } else {
        // Interim result
        if (showInterimResults) {
          setInterimTranscript(text);
        }
      }
    },
    onError: (error) => {
      console.error('Speech recognition error:', error);
      if (error.error === 'not-allowed' || error.error === 'permission-denied') {
        // Microphone permission denied
        requestMicPermission();
      }
      dispatchAbeEvent('status-change', { status: 'error' });
    },
  });

  // Speech synthesis hook (always available for LLM responses)
  const { speak } = useSpeechSynthesis({
    rate: speechOptions.rate,
    pitch: speechOptions.pitch,
    volume: speechOptions.volume,
    lang: speechOptions.lang,
    onEnd: () => {
      dispatchAbeEvent('status-change', { status: 'sleeping' });
    },
  });
  
  // Event-driven status management
  useEventDriven<{ status: AgentStatus }>('status-change', (event) => {
    if (externalStatus === undefined) {
      setInternalStatus(event.detail.status);
    }
  });
  
  // Handle button interaction (event-driven)
  const handleInteraction = () => {
    if (disabled) return;
    
    if (externalStatus !== undefined) {
      if (status === 'sleeping') {
        dispatchAbeEvent('status-change', { status: 'listening' });
        if (enableLLM && recognitionAvailable) {
          startRecognition();
        }
        onListenStart?.();
      } else {
        // Cancel/stop flow
        if (enableLLM && recognitionAvailable) {
          stopRecognition();
        }
        if (enableLLM) {
          abortLLM(); // Abort any pending LLM request
        }
        dispatchAbeEvent('status-change', { status: 'sleeping' });
        onListenEnd?.();
        onCancel?.();
      }
      return;
    }
    
    // Internal state management (event-driven)
    if (status === 'sleeping') {
      // Dispatch listening event
      dispatchAbeEvent('status-change', { status: 'listening' });
      
      if (enableLLM && recognitionAvailable) {
        // Real speech recognition → LLM → speech synthesis flow
        startRecognition();
      } else {
        // Simulated flow (backward compatible)
        onListenStart?.();
        
        // Dispatch thinking event after 3s
        setTimeout(() => {
          dispatchAbeEvent('status-change', { status: 'thinking' });
        }, 3000);
        
        // Dispatch speaking event after 5s
        setTimeout(() => {
          dispatchAbeEvent('status-change', { status: 'speaking' });
        }, 5000);
        
        // Dispatch sleeping event after 8s
        setTimeout(() => {
          dispatchAbeEvent('status-change', { status: 'sleeping' });
          onTranscript?.('Simulated transcript from voice input');
        }, 8000);
      }
    } else {
      if (enableLLM && recognitionAvailable) {
        stopRecognition();
      }
      dispatchAbeEvent('status-change', { status: 'sleeping' });
      onCancel?.();
    }
  };

  return (
    <div className={cn('flex flex-col items-center', sizeConfig.gap, className)}>
      {/* === THE FEEDBACK DISPLAY (The Screen) === */}
      <NeuromorphicContainer 
        inset 
        className={cn('flex items-center justify-around', sizeConfig.display)}
      >
        <StatusLED
          size={sizeConfig.led}
          color={config.led.color}
          state={config.led.state}
          glow
        />
        
        <VoiceWaveform
          size={sizeConfig.waveform}
          state={config.waveform}
          audioData={audioData}
          color="primary"
          glow
          barCount={10}
        />
      </NeuromorphicContainer>
      
      {/* === THE TRIGGER (The Button) === */}
      <NeuromorphicButton
        variant={status === 'sleeping' ? 'raised' : 'pressed'}
        size="icon-xl"
        shape="circle"
        onClick={handleInteraction}
        disabled={disabled}
        className={cn(
          sizeConfig.button,
          'transition-all duration-300',
          status !== 'sleeping' && status !== 'error' && 'shadow-glow-primary'
        )}
      >
        <div 
          className={cn(sizeConfig.icon, 'transition-colors duration-300')}
          style={{ color: config.color }}
        >
          {Icons[config.icon]}
        </div>
      </NeuromorphicButton>
      
      {/* === INTERIM TRANSCRIPT (if showing) === */}
      {showInterimResults && interimTranscript && status === 'listening' && (
        <div className={cn(
          'text-xs text-[var(--abe-text-muted)] italic max-w-md text-center',
          sizeConfig.text
        )}>
          "{interimTranscript}"
        </div>
      )}
      
      {/* === LOADING INDICATOR (if LLM loading) === */}
      {isLLMLoading && status === 'thinking' && (
        <div className="flex items-center gap-2 text-[var(--abe-accent)]">
          <div className="h-4 w-4 border-2 border-[var(--abe-accent)] border-t-transparent rounded-full animate-spin" />
          <span className={cn('text-xs', sizeConfig.text)}>Processing...</span>
        </div>
      )}
      
      {/* === ERROR RECOVERY === */}
      {llmError && status === 'error' && (
        <ErrorRecovery
          error={llmError}
          onRetry={() => {
            setLlmError(null);
            // Retry last message if we have it
            // (Would need to store last message for full retry)
          }}
          onDismiss={() => {
            setLlmError(null);
            dispatchAbeEvent('status-change', { status: 'sleeping' });
          }}
          size={size}
        />
      )}
      
      {/* === PERMISSION STATE UI === */}
      {micPermission === 'denied' && (
        <div className="flex flex-col items-center gap-2 p-3 rounded-xl bg-[var(--abe-error)]/10 border border-[var(--abe-error)]/20 max-w-md">
          <div className="flex items-center gap-2 text-[var(--abe-error)]">
            <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" x2="12" y1="8" y2="12"/>
              <line x1="12" x2="12.01" y1="16" y2="16"/>
            </svg>
            <span className="text-xs font-medium">Microphone Permission Denied</span>
          </div>
          <p className="text-xs text-[var(--abe-text-secondary)] text-center">
            Please enable microphone access in your browser settings to use voice features.
          </p>
          <NeuromorphicButton
            variant="raised"
            size="sm"
            onClick={requestMicPermission}
          >
            Request Permission
          </NeuromorphicButton>
        </div>
      )}
      
      {micPermission === 'prompt' && status === 'sleeping' && (
        <div className="text-xs text-[var(--abe-text-muted)] text-center max-w-md">
          Microphone permission will be requested when you start speaking.
        </div>
      )}
      
      {/* === THE STATUS LABEL === */}
      {showLabel && (
        <span
          className={cn(
            'font-bold tracking-[0.2em] uppercase transition-all duration-300',
            sizeConfig.text,
            status === 'sleeping' 
              ? 'text-[var(--abe-text-muted)]' 
              : 'text-[var(--abe-text-secondary)]',
            status === 'error' && 'text-[var(--abe-error)]'
          )}
        >
          {label}
        </span>
      )}
    </div>
  );
};

// =============================================================================
// MINI VOICE CONTROL
// =============================================================================

export interface MiniVoiceControlProps {
  status?: AgentStatus;
  onToggle?: () => void;
  disabled?: boolean;
  className?: string;
}

export const MiniVoiceControl: React.FC<MiniVoiceControlProps> = ({
  status = 'sleeping',
  onToggle,
  disabled = false,
  className,
}) => {
  const config = statusConfigs[status];
  
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <StatusLED
        size="sm"
        color={config.led.color}
        state={config.led.state}
        glow
      />
      
      <NeuromorphicButton
        variant={status === 'sleeping' ? 'flat' : 'pressed'}
        size="icon-sm"
        shape="circle"
        onClick={onToggle}
        disabled={disabled}
      >
        <div className="h-4 w-4" style={{ color: config.color }}>
          {Icons[config.icon]}
        </div>
      </NeuromorphicButton>
    </div>
  );
};

// =============================================================================
// FLOATING VOICE CONTROL
// =============================================================================

export interface FloatingVoiceControlProps extends VoiceControlHubProps {
  position?: 'bottom-right' | 'bottom-left' | 'bottom-center';
  expanded?: boolean;
  onExpandToggle?: () => void;
}

export const FloatingVoiceControl: React.FC<FloatingVoiceControlProps> = ({
  position = 'bottom-right',
  expanded = false,
  onExpandToggle,
  ...hubProps
}) => {
  const positionClasses = {
    'bottom-right': 'bottom-6 right-6',
    'bottom-left': 'bottom-6 left-6',
    'bottom-center': 'bottom-6 left-1/2 -translate-x-1/2',
  };
  
  if (!expanded) {
    return (
      <div className={cn('fixed z-50', positionClasses[position])}>
        <NeuromorphicButton
          variant="glow"
          size="icon-xl"
          shape="circle"
          onClick={onExpandToggle}
          className="h-16 w-16 shadow-2xl"
        >
          <div className="h-7 w-7 text-[var(--abe-primary)]">
            {Icons['mic']}
          </div>
        </NeuromorphicButton>
      </div>
    );
  }
  
  return (
    <div 
      className={cn(
        'fixed z-50 p-6 rounded-3xl',
        'bg-[var(--abe-surface)]/95 backdrop-blur-xl',
        'shadow-2xl border border-[var(--abe-border)]',
        positionClasses[position]
      )}
    >
      <button
        onClick={onExpandToggle}
        aria-label="Close voice control"
        title="Close voice control"
        className="absolute top-2 right-2 p-1 text-[var(--abe-text-muted)] hover:text-[var(--abe-text-primary)] transition-colors"
      >
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>
      
      <VoiceControlHub size="sm" {...hubProps} />
    </div>
  );
};

// =============================================================================
// EXPORTS
// =============================================================================

export { NeuromorphicContainer };
