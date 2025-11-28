/**
 * AbëONE Atom: ConversationContext
 * 
 * Manages conversation history and context.
 * Independent of backend format - can adapt when Jimmy responds.
 * 
 * Pattern: CONVERSATION × CONTEXT × ATOM × MEMORY × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import * as React from 'react';

/**
 * Conversation Message
 */
export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  metadata?: {
    tokens?: number;
    model?: string;
    confidence?: number;
  };
}

/**
 * Conversation Context Options
 */
export interface UseConversationContextOptions {
  /** Maximum number of messages to keep (default: 50) */
  maxMessages?: number;
  /** Maximum context length in characters (default: 10000) */
  maxContextLength?: number;
  /** System prompt */
  systemPrompt?: string;
  /** Callback when conversation updates */
  onUpdate?: (messages: ConversationMessage[]) => void;
}

/**
 * useConversationContext Hook
 */
export function useConversationContext(options: UseConversationContextOptions = {}) {
  const {
    maxMessages = 50,
    maxContextLength = 10000,
    systemPrompt,
    onUpdate,
  } = options;

  const [messages, setMessages] = React.useState<ConversationMessage[]>(() => {
    // Initialize with system prompt if provided
    if (systemPrompt) {
      return [{
        id: 'system-0',
        role: 'system',
        content: systemPrompt,
        timestamp: Date.now(),
      }];
    }
    return [];
  });

  /**
   * Add message to conversation
   */
  const addMessage = React.useCallback((message: Omit<ConversationMessage, 'id' | 'timestamp'>) => {
    setMessages((prev) => {
      const newMessage: ConversationMessage = {
        ...message,
        id: `${message.role}-${Date.now()}-${Math.random().toString(36).substring(7)}`,
        timestamp: Date.now(),
      };

      const updated = [...prev, newMessage];

      // Trim to max messages
      const trimmed = updated.slice(-maxMessages);

      // Trim to max context length
      let contextLength = 0;
      const finalMessages: ConversationMessage[] = [];
      
      for (let i = trimmed.length - 1; i >= 0; i--) {
        const msg = trimmed[i];
        const msgLength = msg.content.length;
        
        if (contextLength + msgLength <= maxContextLength || msg.role === 'system') {
          finalMessages.unshift(msg);
          if (msg.role !== 'system') {
            contextLength += msgLength;
          }
        } else {
          break;
        }
      }

      onUpdate?.(finalMessages);
      return finalMessages;
    });
  }, [maxMessages, maxContextLength, onUpdate]);

  /**
   * Get conversation context (for LLM request)
   * Returns array of messages in format ready for backend
   */
  const getContext = React.useCallback((): string[] => {
    return messages
      .filter(msg => msg.role !== 'system')
      .map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`);
  }, [messages]);

  /**
   * Get system prompt
   */
  const getSystemPrompt = React.useCallback((): string | undefined => {
    const systemMsg = messages.find(msg => msg.role === 'system');
    return systemMsg?.content || systemPrompt;
  }, [messages, systemPrompt]);

  /**
   * Clear conversation (keep system prompt)
   */
  const clearConversation = React.useCallback(() => {
    setMessages((prev) => {
      const systemMsg = prev.find(msg => msg.role === 'system');
      const cleared = systemMsg ? [systemMsg] : [];
      onUpdate?.(cleared);
      return cleared;
    });
  }, [onUpdate]);

  /**
   * Get conversation summary (for display)
   */
  const getSummary = React.useCallback(() => {
    return {
      totalMessages: messages.length,
      userMessages: messages.filter(msg => msg.role === 'user').length,
      assistantMessages: messages.filter(msg => msg.role === 'assistant').length,
      contextLength: messages.reduce((sum, msg) => sum + msg.content.length, 0),
    };
  }, [messages]);

  return {
    messages,
    addMessage,
    getContext,
    getSystemPrompt,
    clearConversation,
    getSummary,
  };
}

