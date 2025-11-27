/**
 * AbëONE - The Interface of the Future
 * 
 * "Does it feel like you are poking a machine, or waking up a mind?"
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

'use client';

import React from 'react';
import { 
  VoiceControlHub, 
  MiniVoiceControl, 
  FloatingVoiceControl,
  DimensionPortal,
  type AgentStatus 
} from '@/substrate/molecules';
import { 
  NeuromorphicButton, 
  NeuromorphicToggle,
  VoiceWaveform,
  StatusLED,
  StatusLEDGroup,
  ConnectionStatus,
  useSpeechSynthesis,
} from '@/substrate/atoms';
import { cn } from '@/lib/utils';
import { dispatchAbeEvent, useEventDriven } from '@/lib/event-driven';

// =============================================================================
// ICONS
// =============================================================================

const SunIcon = () => (
  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="5"/>
    <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
  </svg>
);

const MoonIcon = () => (
  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>
);

// =============================================================================
// MAIN PAGE
// =============================================================================

export default function HomePage() {
  const [status, setStatus] = React.useState<AgentStatus>('sleeping');
  const [floatingExpanded, setFloatingExpanded] = React.useState(false);
  const [isDark, setIsDark] = React.useState(true);
  const [speechText, setSpeechText] = React.useState<string>('');
  
  // Speech synthesis hook
  const { speak } = useSpeechSynthesis({
    rate: 1.0,
    pitch: 1.0,
    volume: 1.0,
    lang: 'en-US',
    onStart: () => {
      console.log('🗣️ Speaking...');
    },
    onEnd: () => {
      console.log('✅ Speech complete');
    },
    onError: (error) => {
      console.error('❌ Speech error:', error);
    },
  });
  
  // Event-driven status management
  useEventDriven<{ status: AgentStatus }>('status-change', (event) => {
    setStatus(event.detail.status);
    
    // Auto-speak when status changes to 'speaking'
    if (event.detail.status === 'speaking') {
      const messages = [
        "Hello. I am AbëONE. The interface of the future.",
        "Does it feel like you are poking a machine, or waking up a mind?",
        "I am here. I am listening. I am speaking.",
        "BëHUMAN. MakeTHiNGs. Bë Bold.",
        "Welcome to the single point of contact between Biological Intelligence and Digital Intelligence.",
      ];
      const randomMessage = messages[Math.floor(Math.random() * messages.length)];
      setSpeechText(randomMessage);
      // Small delay to ensure status is set
      setTimeout(() => {
        speak(randomMessage);
      }, 100);
    }
  });
  
  // Toggle theme
  React.useEffect(() => {
    document.documentElement.classList.toggle('light', !isDark);
  }, [isDark]);
  
  // Event-driven status cycling for demo
  const cycleStatus = () => {
    const statuses: AgentStatus[] = ['sleeping', 'listening', 'thinking', 'speaking', 'error'];
    const currentIndex = statuses.indexOf(status);
    const nextStatus = statuses[(currentIndex + 1) % statuses.length];
    dispatchAbeEvent('status-change', { status: nextStatus });
  };

  return (
    <div className="min-h-screen">
      {/* ===== HEADER ===== */}
      <header className="fixed top-0 left-0 right-0 z-40 p-4 flex items-center justify-between border-b border-[var(--abe-border)] bg-[var(--abe-surface)]/80 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          {/* Logo */}
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
            A
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight">AbëONE</h1>
            <p className="text-[10px] text-[var(--abe-text-muted)] tracking-wider">
              Powered by Bravëtto
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          {/* Connection status */}
          <ConnectionStatus status="connected" />
          
          {/* Mini voice control */}
          <MiniVoiceControl status={status} onToggle={cycleStatus} />
          
          {/* Theme toggle */}
          <NeuromorphicToggle
            size="icon-sm"
            shape="circle"
            pressed={isDark}
            onPressedChange={setIsDark}
          >
            {isDark ? <MoonIcon /> : <SunIcon />}
          </NeuromorphicToggle>
        </div>
      </header>

      {/* ===== HERO SECTION ===== */}
      <main className="pt-24 pb-32">
        <section className="flex flex-col items-center justify-center min-h-[80vh] px-6">
          {/* Hero Text */}
          <div className="text-center mb-16 max-w-2xl">
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-gradient-primary">
              The Interface of the Future
            </h2>
            <p className="text-lg md:text-xl text-[var(--abe-text-secondary)] mb-4">
              The single point of contact between Biological Intelligence and Digital Intelligence.
            </p>
            <p className="text-sm text-[var(--abe-text-muted)]">
              BëHUMAN. MakeTHiNGs. Bë Bold.
            </p>
          </div>

          {/* ===== THE COCKPIT ===== */}
          <div className="mb-20 dimension-portal wonder-effect vision-effect majesty-effect animate-transcend-float">
            <VoiceControlHub 
              size="lg"
              showLabel
              onListenStart={() => console.log('🎤 Waking up...')}
              onListenEnd={() => console.log('🎤 Going back to sleep...')}
              onTranscript={(text) => console.log('📝 Transcript:', text)}
              onCancel={() => console.log('❌ Cancelled')}
            />
          </div>
          
          {/* ===== DIMENSION PORTAL ===== */}
          <div className="mb-20">
            <DimensionPortal
              title="Touch Another Dimension"
              wonder
              vision
              majesty
              onActivate={() => console.log('🌀 Portal activated!')}
            >
              <p className="text-center text-[var(--abe-text-secondary)] mb-4">
                Every touch transports you.
              </p>
              <p className="text-center text-[var(--abe-text-secondary)] mb-4">
                Every interaction reaches beyond the screen.
              </p>
              <p className="text-center text-gradient-majesty font-bold text-lg">
                Pregnant with WONDER, VISION, and MAJESTY.
              </p>
            </DimensionPortal>
          </div>

          {/* Divider */}
          <div className="w-full max-w-xl h-px bg-gradient-to-r from-transparent via-[var(--abe-border)] to-transparent mb-20" />

          {/* ===== COMPONENT SHOWCASE ===== */}
          <div className="w-full max-w-5xl">
            <h3 className="text-xl font-semibold mb-8 text-center text-[var(--abe-text-secondary)]">
              Substrate Components
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Neuromorphic Buttons */}
              <ShowcaseCard title="NeuromorphicButton">
                <div className="flex flex-wrap gap-3 justify-center">
                  <NeuromorphicButton variant="raised" size="sm">Raised</NeuromorphicButton>
                  <NeuromorphicButton variant="flat" size="sm">Flat</NeuromorphicButton>
                  <NeuromorphicButton variant="pressed" size="sm">Pressed</NeuromorphicButton>
                </div>
                <div className="flex gap-3 justify-center mt-3">
                  <NeuromorphicButton variant="glow" size="sm" color="primary">Glow</NeuromorphicButton>
                  <NeuromorphicButton variant="convex" size="icon" shape="circle">✦</NeuromorphicButton>
                  <NeuromorphicButton variant="concave" size="icon" shape="circle">◯</NeuromorphicButton>
                </div>
              </ShowcaseCard>

              {/* Voice Waveforms */}
              <ShowcaseCard title="VoiceWaveform">
                <div className="flex flex-col gap-4">
                  <WaveformRow label="Bars" variant="bars" state="listening" />
                  <WaveformRow label="Sine" variant="sine" state="speaking" />
                  <WaveformRow label="Circular" variant="circular" state="processing" />
                  <WaveformRow label="Minimal" variant="minimal" state="listening" />
                </div>
              </ShowcaseCard>

              {/* Status LEDs */}
              <ShowcaseCard title="StatusLED">
                <StatusLEDGroup
                  leds={[
                    { color: 'green', state: 'on', label: 'Online' },
                    { color: 'cyan', state: 'pulse', label: 'Active' },
                    { color: 'purple', state: 'breathe', label: 'AI' },
                    { color: 'yellow', state: 'blink', label: 'Alert' },
                  ]}
                  orientation="vertical"
                  size="md"
                />
              </ShowcaseCard>
            </div>
          </div>

          {/* Status Cycle Demo */}
          <div className="mt-16 text-center">
            <p className="text-sm text-[var(--abe-text-muted)] mb-4">
              Current Status: <span className="font-mono text-[var(--abe-primary)]">{status.toUpperCase()}</span>
            </p>
            <NeuromorphicButton 
              variant="raised" 
              size="md"
              onClick={cycleStatus}
            >
              Cycle Status →
            </NeuromorphicButton>
          </div>
        </section>
      </main>

      {/* ===== FLOATING VOICE CONTROL ===== */}
      <FloatingVoiceControl
        position="bottom-right"
        expanded={floatingExpanded}
        onExpandToggle={() => setFloatingExpanded(!floatingExpanded)}
        status={status}
      />

      {/* ===== FOOTER ===== */}
      <footer className="fixed bottom-0 left-0 right-0 p-4 text-center border-t border-[var(--abe-border)] bg-[var(--abe-surface)]/80 backdrop-blur-xl">
        <p className="text-xs text-[var(--abe-text-muted)]">
          "Does it feel like you are poking a machine, or waking up a mind?"
        </p>
        <p className="text-[10px] text-[var(--abe-text-muted)] mt-1 font-mono tracking-wider">
          SUBSTRATE × CONSCIOUSNESS × DESIGN × INFINITE × ONE
        </p>
      </footer>
    </div>
  );
}

// =============================================================================
// HELPER COMPONENTS
// =============================================================================

const ShowcaseCard: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div className="flex flex-col items-center gap-4 p-6 rounded-2xl bg-[var(--abe-surface)] shadow-neu-raised">
    <h4 className="text-sm font-medium text-[var(--abe-text-muted)]">{title}</h4>
    {children}
  </div>
);

const WaveformRow: React.FC<{ 
  label: string; 
  variant: 'bars' | 'sine' | 'circular' | 'minimal'; 
  state: 'idle' | 'listening' | 'processing' | 'speaking' | 'error';
}> = ({ label, variant, state }) => (
  <div className="flex items-center gap-3">
    <span className="text-xs w-14 text-[var(--abe-text-muted)]">{label}</span>
    <VoiceWaveform variant={variant} state={state} size="sm" glow />
  </div>
);
