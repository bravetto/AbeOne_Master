# Frontend-Backend Integration Guide

## Overview

This guide covers integrating the AI Guardians backend with various frontend applications, including web apps, VS Code extensions, and Chrome extensions.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  VS Code Ext    │    │ Chrome Ext      │
│   (React/Vue)   │    │   (TypeScript)  │    │ (JavaScript)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    AI Guardians API      │
                    │   (FastAPI Gateway)      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Guard Services         │
                    │  (TokenGuard, TrustGuard, │
                    │   ContextGuard, BiasGuard,│
                    │   HealthGuard)            │
                    └───────────────────────────┘
```

## API Integration

### Base Configuration

#### API Client Setup
```typescript
// api-client.ts
export class AIGuardianAPI {
  private baseURL: string;
  private apiKey: string;
  private clientType: string;

  constructor(config: {
    baseURL: string;
    apiKey: string;
    clientType: 'web' | 'vscode' | 'chrome' | 'api';
  }) {
    this.baseURL = config.baseURL;
    this.apiKey = config.apiKey;
    this.clientType = config.clientType;
  }

  async processGuardRequest(request: GuardRequest): Promise<GuardResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'X-Client-Type': this.clientType
      },
      body: JSON.stringify({
        ...request,
        client_type: this.clientType
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }
}
```

#### Type Definitions
```typescript
// types.ts
export interface GuardRequest {
  service_type: 'tokenguard' | 'trustguard' | 'contextguard' | 'biasguard' | 'healthguard';
  payload: {
    text: string;
    context?: Record<string, any>;
    options?: Record<string, any>;
  };
  user_id?: string;
  session_id?: string;
  priority?: number;
  timeout?: number;
  fallback_enabled?: boolean;
  client_type?: 'web' | 'vscode' | 'chrome' | 'api';
  client_version?: string;
  request_metadata?: Record<string, any>;
}

export interface GuardResponse {
  request_id: string;
  service_type: string;
  success: boolean;
  data?: Record<string, any>;
  error?: string;
  processing_time?: number;
  service_used?: string;
  fallback_used?: boolean;
  client_type?: string;
  confidence_score?: number;
  warnings?: string[];
  recommendations?: string[];
  metadata?: Record<string, any>;
}
```

## Web Frontend Integration

### React Integration

#### Hook for Guard Services
```typescript
// hooks/useGuardService.ts
import { useState, useCallback } from 'react';
import { AIGuardianAPI } from '../api/api-client';

export const useGuardService = (apiKey: string) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const api = new AIGuardianAPI({
    baseURL: process.env.REACT_APP_API_URL || 'https://api.aiguardian.ai',
    apiKey,
    clientType: 'web'
  });

  const analyzeText = useCallback(async (
    text: string,
    serviceType: GuardRequest['service_type'],
    options?: Record<string, any>
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.processGuardRequest({
        service_type: serviceType,
        payload: {
          text,
          options: options || {}
        },
        client_type: 'web'
      });

      return response;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [api]);

  return {
    analyzeText,
    loading,
    error
  };
};
```

#### React Component
```tsx
// components/TextAnalyzer.tsx
import React, { useState } from 'react';
import { useGuardService } from '../hooks/useGuardService';

interface TextAnalyzerProps {
  apiKey: string;
}

export const TextAnalyzer: React.FC<TextAnalyzerProps> = ({ apiKey }) => {
  const [text, setText] = useState('');
  const [serviceType, setServiceType] = useState<'tokenguard' | 'trustguard' | 'contextguard' | 'biasguard' | 'healthguard'>('tokenguard');
  const [result, setResult] = useState<GuardResponse | null>(null);
  
  const { analyzeText, loading, error } = useGuardService(apiKey);

  const handleAnalyze = async () => {
    try {
      const response = await analyzeText(text, serviceType);
      setResult(response);
    } catch (err) {
      console.error('Analysis failed:', err);
    }
  };

  return (
    <div className="text-analyzer">
      <div className="input-section">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze..."
          rows={10}
        />
        
        <select
          value={serviceType}
          onChange={(e) => setServiceType(e.target.value as any)}
        >
          <option value="tokenguard">Token Optimization</option>
          <option value="trustguard">Trust Validation</option>
          <option value="contextguard">Context Analysis</option>
          <option value="biasguard">Bias Detection</option>
          <option value="healthguard">Health Monitoring</option>
        </select>
        
        <button onClick={handleAnalyze} disabled={loading || !text.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Text'}
        </button>
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="result">
          <h3>Analysis Result</h3>
          <div className="confidence">
            Confidence: {(result.confidence_score || 0) * 100}%
          </div>
          
          {result.warnings && result.warnings.length > 0 && (
            <div className="warnings">
              <h4>Warnings</h4>
              <ul>
                {result.warnings.map((warning, index) => (
                  <li key={index}>{warning}</li>
                ))}
              </ul>
            </div>
          )}
          
          {result.recommendations && result.recommendations.length > 0 && (
            <div className="recommendations">
              <h4>Recommendations</h4>
              <ul>
                {result.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

### Vue.js Integration

#### Composable for Guard Services
```typescript
// composables/useGuardService.ts
import { ref, computed } from 'vue';
import { AIGuardianAPI } from '../api/api-client';

export const useGuardService = (apiKey: string) => {
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  const api = new AIGuardianAPI({
    baseURL: import.meta.env.VITE_API_URL || 'https://api.aiguardian.ai',
    apiKey,
    clientType: 'web'
  });

  const analyzeText = async (
    text: string,
    serviceType: GuardRequest['service_type'],
    options?: Record<string, any>
  ) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.processGuardRequest({
        service_type: serviceType,
        payload: {
          text,
          options: options || {}
        },
        client_type: 'web'
      });

      return response;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    analyzeText,
    loading: computed(() => loading.value),
    error: computed(() => error.value)
  };
};
```

## VS Code Extension Integration

### Extension Structure
```
extension/
├── src/
│   ├── extension.ts
│   ├── providers/
│   │   ├── guardProvider.ts
│   │   └── diagnosticProvider.ts
│   ├── services/
│   │   └── apiService.ts
│   └── types/
│       └── index.ts
├── package.json
└── README.md
```

### API Service
```typescript
// src/services/apiService.ts
import * as vscode from 'vscode';
import { AIGuardianAPI } from './api-client';

export class APIService {
  private api: AIGuardianAPI;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.api = new AIGuardianAPI({
      baseURL: 'https://api.aiguardian.ai',
      apiKey: this.getApiKey(),
      clientType: 'vscode'
    });
  }

  private getApiKey(): string {
    const config = vscode.workspace.getConfiguration('aiguardian');
    return config.get<string>('apiKey') || '';
  }

  async analyzeDocument(document: vscode.TextDocument): Promise<GuardResponse[]> {
    const text = document.getText();
    const results: GuardResponse[] = [];

    // Analyze with different guard services
    const services: GuardRequest['service_type'][] = [
      'tokenguard',
      'trustguard',
      'contextguard',
      'biasguard'
    ];

    for (const service of services) {
      try {
        const response = await this.api.processGuardRequest({
          service_type: service,
          payload: {
            text,
            context: {
              file_path: document.fileName,
              language: document.languageId
            }
          },
          client_type: 'vscode',
          client_version: this.context.extension.packageJSON.version
        });

        results.push(response);
      } catch (error) {
        console.error(`Error analyzing with ${service}:`, error);
      }
    }

    return results;
  }
}
```

### Diagnostic Provider
```typescript
// src/providers/diagnosticProvider.ts
import * as vscode from 'vscode';
import { APIService } from '../services/apiService';

export class DiagnosticProvider {
  private diagnosticCollection: vscode.DiagnosticCollection;
  private apiService: APIService;

  constructor(context: vscode.ExtensionContext) {
    this.diagnosticCollection = vscode.languages.createDiagnosticCollection('aiguardian');
    this.apiService = new APIService(context);
    
    context.subscriptions.push(this.diagnosticCollection);
  }

  async analyzeDocument(document: vscode.TextDocument) {
    try {
      const results = await this.apiService.analyzeDocument(document);
      const diagnostics: vscode.Diagnostic[] = [];

      for (const result of results) {
        if (result.success && result.data) {
          // Convert API results to VS Code diagnostics
          const issues = result.data.issues || [];
          
          for (const issue of issues) {
            const range = new vscode.Range(
              issue.start_line || 0,
              issue.start_column || 0,
              issue.end_line || 0,
              issue.end_column || 0
            );

            const diagnostic = new vscode.Diagnostic(
              range,
              issue.message || 'AI Guardian Issue',
              this.getSeverity(issue.severity || 'warning')
            );

            diagnostic.source = 'AI Guardian';
            diagnostic.code = issue.code;
            
            if (issue.suggestions) {
              diagnostic.relatedInformation = issue.suggestions.map(suggestion => 
                new vscode.DiagnosticRelatedInformation(
                  new vscode.Location(document.uri, range),
                  suggestion
                )
              );
            }

            diagnostics.push(diagnostic);
          }
        }
      }

      this.diagnosticCollection.set(document.uri, diagnostics);
    } catch (error) {
      console.error('Error analyzing document:', error);
    }
  }

  private getSeverity(severity: string): vscode.DiagnosticSeverity {
    switch (severity.toLowerCase()) {
      case 'error':
        return vscode.DiagnosticSeverity.Error;
      case 'warning':
        return vscode.DiagnosticSeverity.Warning;
      case 'info':
        return vscode.DiagnosticSeverity.Information;
      default:
        return vscode.DiagnosticSeverity.Warning;
    }
  }
}
```

### Extension Activation
```typescript
// src/extension.ts
import * as vscode from 'vscode';
import { DiagnosticProvider } from './providers/diagnosticProvider';

export function activate(context: vscode.ExtensionContext) {
  const diagnosticProvider = new DiagnosticProvider(context);

  // Register commands
  const analyzeCommand = vscode.commands.registerCommand(
    'aiguardian.analyze',
    () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        diagnosticProvider.analyzeDocument(editor.document);
      }
    }
  );

  // Register document change handler
  const documentChangeHandler = vscode.workspace.onDidChangeTextDocument(
    (event) => {
      diagnosticProvider.analyzeDocument(event.document);
    }
  );

  context.subscriptions.push(analyzeCommand, documentChangeHandler);
}

export function deactivate() {}
```

## Chrome Extension Integration

### Manifest Configuration
```json
// manifest.json
{
  "manifest_version": 3,
  "name": "AI Guardians",
  "version": "1.0.0",
  "description": "AI-powered content analysis and protection",
  "permissions": [
    "activeTab",
    "storage",
    "scripting"
  ],
  "host_permissions": [
    "https://api.aiguardian.ai/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["content.css"]
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_title": "AI Guardians"
  },
  "options_page": "options.html"
}
```

### Background Script
```javascript
// background.js
class AIGuardianBackground {
  constructor() {
    this.apiKey = null;
    this.init();
  }

  async init() {
    // Load API key from storage
    const result = await chrome.storage.sync.get(['apiKey']);
    this.apiKey = result.apiKey;
  }

  async analyzeText(text, serviceType = 'biasguard') {
    if (!this.apiKey) {
      throw new Error('API key not configured');
    }

    const response = await fetch('https://api.aiguardian.ai/api/v1/guards/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'chrome'
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }

  async setApiKey(apiKey) {
    this.apiKey = apiKey;
    await chrome.storage.sync.set({ apiKey });
  }
}

const aiGuardian = new AIGuardianBackground();

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyze') {
    aiGuardian.analyzeText(request.text, request.serviceType)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep message channel open for async response
  }
});
```

### Content Script
```javascript
// content.js
class AIGuardianContent {
  constructor() {
    this.highlights = [];
    this.init();
  }

  init() {
    // Listen for page load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.analyzePage());
    } else {
      this.analyzePage();
    }
  }

  async analyzePage() {
    const text = this.extractText();
    if (!text.trim()) return;

    try {
      const result = await this.sendMessage({
        action: 'analyze',
        text: text,
        serviceType: 'biasguard'
      });

      if (result.success) {
        this.displayResults(result.data);
      }
    } catch (error) {
      console.error('AI Guardian analysis failed:', error);
    }
  }

  extractText() {
    // Extract text from common content areas
    const selectors = [
      'article',
      'main',
      '.content',
      '.post',
      '.article',
      'p'
    ];

    let text = '';
    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      for (const element of elements) {
        text += element.textContent + ' ';
      }
    }

    return text.trim();
  }

  async sendMessage(message) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(message, resolve);
    });
  }

  displayResults(data) {
    // Create badge
    this.createBadge(data);

    // Highlight issues
    if (data.data && data.data.issues) {
      this.highlightIssues(data.data.issues);
    }
  }

  createBadge(data) {
    const badge = document.createElement('div');
    badge.className = 'ai-guardian-badge';
    badge.textContent = data.data?.issues_count || '✓';
    badge.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${data.data?.issues_count > 0 ? '#ff4444' : '#44ff44'};
      color: white;
      padding: 8px 12px;
      border-radius: 4px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      z-index: 10000;
      cursor: pointer;
    `;

    badge.addEventListener('click', () => {
      this.showDetails(data);
    });

    document.body.appendChild(badge);
  }

  highlightIssues(issues) {
    // Implementation for highlighting issues in text
    // This would involve finding text ranges and adding highlights
  }

  showDetails(data) {
    // Show detailed analysis in popup or modal
    const modal = document.createElement('div');
    modal.className = 'ai-guardian-modal';
    modal.innerHTML = `
      <div class="modal-content">
        <h3>AI Guardian Analysis</h3>
        <div class="confidence">
          Confidence: ${(data.confidence_score || 0) * 100}%
        </div>
        ${data.warnings ? `
          <div class="warnings">
            <h4>Warnings</h4>
            <ul>
              ${data.warnings.map(warning => `<li>${warning}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        ${data.recommendations ? `
          <div class="recommendations">
            <h4>Recommendations</h4>
            <ul>
              ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        <button onclick="this.parentElement.parentElement.remove()">Close</button>
      </div>
    `;

    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 10001;
    `;

    document.body.appendChild(modal);
  }
}

// Initialize content script
new AIGuardianContent();
```

## Error Handling

### Common Error Patterns
```typescript
// error-handling.ts
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export const handleAPIError = (error: any): APIError => {
  if (error instanceof APIError) {
    return error;
  }

  if (error.response) {
    return new APIError(
      error.response.data?.message || 'API Error',
      error.response.status,
      error.response.data
    );
  }

  if (error.request) {
    return new APIError(
      'Network Error: Unable to reach API',
      0,
      error.request
    );
  }

  return new APIError(
    error.message || 'Unknown Error',
    0,
    error
  );
};
```

## Testing

### Unit Tests
```typescript
// __tests__/api-client.test.ts
import { AIGuardianAPI } from '../api-client';

describe('AIGuardianAPI', () => {
  let api: AIGuardianAPI;

  beforeEach(() => {
    api = new AIGuardianAPI({
      baseURL: 'https://api.aiguardian.ai',
      apiKey: 'test-key',
      clientType: 'web'
    });
  });

  it('should process guard request', async () => {
    // Mock fetch
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        success: true,
        data: { confidence: 0.85 }
      })
    });

    const result = await api.processGuardRequest({
      service_type: 'tokenguard',
      payload: { text: 'test' }
    });

    expect(result.success).toBe(true);
    expect(result.data.confidence).toBe(0.85);
  });
});
```

## Getting Help

- [API Documentation](./API_DOCUMENTATION.md)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [Chrome Extension API](https://developer.chrome.com/docs/extensions/)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

