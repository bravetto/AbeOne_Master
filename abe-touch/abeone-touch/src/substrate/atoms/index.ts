/**
 * AbëONE Substrate: Atoms
 * 
 * The fundamental building blocks. Indivisible. Pure.
 * Each atom serves one purpose and serves it perfectly.
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

// =============================================================================
// INTERACTIVE
// =============================================================================

export {
  NeuromorphicButton,
  NeuromorphicIconButton,
  NeuromorphicToggle,
  neuromorphicButtonVariants,
  type NeuromorphicButtonProps,
  type NeuromorphicIconButtonProps,
  type NeuromorphicToggleProps,
} from './NeuromorphicButton';

export {
  TranscendentButton,
  type TranscendentButtonProps,
} from './TranscendentButton';

// =============================================================================
// FEEDBACK
// =============================================================================

export {
  StatusLED,
  StatusLEDGroup,
  ConnectionStatus,
  statusLEDVariants,
  type StatusLEDProps,
  type StatusLEDGroupProps,
  type ConnectionStatusProps,
  type LEDState,
  type LEDColor,
  type ConnectionState,
} from './StatusLED';

export {
  VoiceWaveform,
  voiceWaveformVariants,
  type VoiceWaveformProps,
  type WaveformState,
  type WaveformVariant,
  type AudioAnalysis,
} from './VoiceWaveform';

// =============================================================================
// EVENT SYSTEM
// =============================================================================

export {
  EventEmitter,
  type EventEmitterProps,
} from './EventEmitter';

export {
  EventListener,
  type EventListenerProps,
} from './EventListener';

export {
  EventBridge,
  type EventBridgeProps,
} from './EventBridge';

// =============================================================================
// SPEECH
// =============================================================================

export {
  SpeechSynthesis,
  useSpeechSynthesis,
  getVoices,
  getVoiceByName,
  getVoiceByLang,
  type SpeechSynthesisProps,
  type UseSpeechSynthesisOptions,
} from './SpeechSynthesis';

export {
  useSpeechRecognition,
  isSpeechRecognitionAvailable,
  type UseSpeechRecognitionOptions,
  type SpeechRecognitionError,
} from './SpeechRecognition';

export {
  useConversationContext,
  type UseConversationContextOptions,
  type ConversationMessage,
} from './ConversationContext';

export {
  usePermissionHandler,
  type UsePermissionHandlerOptions,
  type PermissionType,
  type PermissionState,
} from './PermissionHandler';

export {
  ErrorRecovery,
  useErrorRecovery,
  type ErrorRecoveryProps,
  type UseErrorRecoveryOptions,
} from './ErrorRecovery';

// =============================================================================
// SUMMARY
// =============================================================================
/**
 * Current Atom Inventory:
 * 
 * Interactive (3):
 *   1. NeuromorphicButton - Soft UI button with tactile depth
 *   2. NeuromorphicIconButton - Icon-only variant
 *   3. NeuromorphicToggle - Stateful toggle button
 * 
 * Feedback (4):
 *   4. StatusLED - Hardware-inspired indicator
 *   5. StatusLEDGroup - Multiple LEDs in formation
 *   6. ConnectionStatus - Pre-configured connection states
 *   7. VoiceWaveform - Audio visualization
 * 
 * Event System (3):
 *   8. EventEmitter - Dispatch events atomically
 *   9. EventListener - Listen to events atomically
 *   10. EventBridge - Bridge events between systems
 * 
 * Speech (2):
 *   11. SpeechSynthesis - Text-to-speech using Web Speech API
 *   12. SpeechRecognition - Speech-to-text using Web Speech Recognition API
 * 
 * Context & UX (3):
 *   13. ConversationContext - Conversation history and context management
 *   14. PermissionHandler - Browser permission handling
 *   15. ErrorRecovery - Error recovery UI and retry logic
 * 
 * TOTAL: 15 Atoms
 * COMBINATIONS: 15^n = INFINITE
 */
