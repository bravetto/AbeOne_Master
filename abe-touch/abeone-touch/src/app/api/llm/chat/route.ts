/**
 * AbëONE API Route: LLM Chat
 * 
 * Next.js API route handler for LLM chat requests.
 * Bridges frontend to abe-41M backend.
 * 
 * Pattern: API × ROUTE × BRIDGE × LLM × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JIMMY) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + JIMMY (530 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { NextRequest, NextResponse } from 'next/server';

/**
 * LLM Request Body
 */
interface LLMRequest {
  message: string;
  context?: string[];
  systemPrompt?: string;
  temperature?: number;
  maxTokens?: number;
}

/**
 * LLM Response
 */
interface LLMResponse {
  response: string;
  metadata?: {
    tokens?: number;
    model?: string;
    timestamp?: string;
  };
}

/**
 * POST /api/llm/chat
 * 
 * Handles LLM chat requests and forwards to abe-41M backend
 */
export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body: LLMRequest = await request.json();
    
    // Validate request
    if (!body.message || typeof body.message !== 'string') {
      return NextResponse.json(
        { error: 'Invalid request: message is required' },
        { status: 400 }
      );
    }

    // Get backend URL from environment or default
    const backendUrl = process.env.LLM_BACKEND_URL || 'http://localhost:8000';
    const apiEndpoint = `${backendUrl}/api/chat`;

    // Prepare request to backend
    const backendRequest = {
      message: body.message,
      context: body.context || [],
      system_prompt: body.systemPrompt || 'You are AbëONE, a helpful AI assistant.',
      temperature: body.temperature ?? 0.7,
      max_tokens: body.maxTokens ?? 500,
    };

    // Forward request to LLM backend
    const backendResponse = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(backendRequest),
      // Timeout after 30 seconds
      signal: AbortSignal.timeout(30000),
    });

    // Handle backend errors
    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error('LLM backend error:', errorText);
      
      return NextResponse.json(
        { 
          error: 'LLM backend error',
          message: backendResponse.statusText,
          status: backendResponse.status,
        },
        { status: backendResponse.status }
      );
    }

    // Parse backend response
    const backendData = await backendResponse.json();

    // Transform to frontend format
    const response: LLMResponse = {
      response: backendData.response || backendData.text || backendData.message || 'No response received',
      metadata: {
        tokens: backendData.tokens,
        model: backendData.model || 'abe-41M',
        timestamp: new Date().toISOString(),
      },
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('LLM API route error:', error);

    // Handle timeout
    if (error instanceof Error && error.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Request timeout: LLM backend took too long to respond' },
        { status: 504 }
      );
    }

    // Handle network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return NextResponse.json(
        { error: 'Network error: Unable to connect to LLM backend' },
        { status: 503 }
      );
    }

    // Generic error
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/llm/chat
 * 
 * Health check endpoint
 */
export async function GET() {
  const backendUrl = process.env.LLM_BACKEND_URL || 'http://localhost:8000';
  
  // Test backend connectivity
  let backendStatus = 'unknown';
  try {
    const healthCheck = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000),
    }).catch(() => null);
    backendStatus = healthCheck?.ok ? 'connected' : 'disconnected';
  } catch {
    backendStatus = 'disconnected';
  }

  return NextResponse.json({
    status: 'ok',
    service: 'AbëONE LLM Chat API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    backend: {
      url: backendUrl,
      status: backendStatus,
    },
  }, {
    headers: {
      'Cache-Control': 'no-store, must-revalidate',
    },
  });
}

