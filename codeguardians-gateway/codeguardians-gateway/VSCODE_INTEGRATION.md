# VS Code Extension Integration Guide

## Overview

This guide covers integrating the AI Guardians platform with VS Code extensions, providing real-time code analysis, bias detection, and AI-powered suggestions.

## Architecture

```
        
   VS Code              Extension            AI Guardians  
   Editor           (TypeScript)     API Gateway   
        
                              
                              
                    
                       Guard Services
                      (TokenGuard,   
                       TrustGuard,   
                       ContextGuard, 
                       BiasGuard)    
                    
```

## Extension Setup

### 1. Project Structure

```
vscode-extension/
 src/
    extension.ts
    providers/
       guardProvider.ts
       diagnosticProvider.ts
       suggestionProvider.ts
    services/
       apiService.ts
       configService.ts
    commands/
       analyzeCommand.ts
       configureCommand.ts
    types/
        index.ts
 package.json
 tsconfig.json
 webpack.config.js
 README.md
```

### 2. Package Configuration

```json
// package.json
{
  "name": "aiguardian",
  "displayName": "AI Guardians",
  "description": "AI-powered code analysis and protection",
  "version": "1.0.0",
  "publisher": "aiguardian",
  "engines": {
    "vscode": "^1.74.0"
  },
  "categories": [
    "Linters",
    "Other",
    "Machine Learning"
  ],
  "keywords": [
    "ai",
    "bias",
    "security",
    "analysis",
    "guard"
  ],
  "activationEvents": [
    "onLanguage:typescript",
    "onLanguage:javascript",
    "onLanguage:python",
    "onLanguage:java",
    "onLanguage:csharp",
    "onCommand:aiguardian.analyze",
    "onCommand:aiguardian.configure"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "aiguardian.analyze",
        "title": "Analyze with AI Guardians",
        "category": "AI Guardians"
      },
      {
        "command": "aiguardian.configure",
        "title": "Configure API Key",
        "category": "AI Guardians"
      },
      {
        "command": "aiguardian.analyzeSelection",
        "title": "Analyze Selection",
        "category": "AI Guardians"
      },
      {
        "command": "aiguardian.analyzeFile",
        "title": "Analyze File",
        "category": "AI Guardians"
      }
    ],
    "configuration": {
      "title": "AI Guardians",
      "properties": {
        "aiguardian.apiKey": {
          "type": "string",
          "default": "",
          "description": "API key for AI Guardians service"
        },
        "aiguardian.apiUrl": {
          "type": "string",
          "default": "https://api.aiguardian.ai",
          "description": "API URL for AI Guardians service"
        },
        "aiguardian.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable AI Guardians analysis"
        },
        "aiguardian.autoAnalyze": {
          "type": "boolean",
          "default": true,
          "description": "Automatically analyze on file changes"
        },
        "aiguardian.services": {
          "type": "array",
          "default": ["tokenguard", "trustguard", "contextguard", "biasguard"],
          "description": "Enabled guard services"
        },
        "aiguardian.confidenceThreshold": {
          "type": "number",
          "default": 0.7,
          "description": "Minimum confidence threshold for suggestions"
        }
      }
    },
    "menus": {
      "editor/context": [
        {
          "command": "aiguardian.analyzeSelection",
          "when": "editorHasSelection",
          "group": "aiguardian"
        }
      ],
      "explorer/context": [
        {
          "command": "aiguardian.analyzeFile",
          "when": "resourceExtname == '.ts' || resourceExtname == '.js' || resourceExtname == '.py'",
          "group": "aiguardian"
        }
      ]
    },
    "keybindings": [
      {
        "command": "aiguardian.analyze",
        "key": "ctrl+shift+a",
        "mac": "cmd+shift+a",
        "when": "editorTextFocus"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run lint",
    "lint": "eslint src --ext ts",
    "test": "node ./out/test/runTest.js"
  },
  "devDependencies": {
    "@types/vscode": "^1.74.0",
    "@types/node": "16.x",
    "@typescript-eslint/eslint-plugin": "^5.45.0",
    "@typescript-eslint/parser": "^5.45.0",
    "eslint": "^8.28.0",
    "typescript": "^4.9.4"
  },
  "dependencies": {
    "axios": "^1.3.4"
  }
}
```

## Core Implementation

### 1. API Service

```typescript
// src/services/apiService.ts
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import * as vscode from 'vscode';
import { GuardRequest, GuardResponse } from '../types';

export class APIService {
  private client: AxiosInstance;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.client = axios.create({
      baseURL: this.getApiUrl(),
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'X-Client-Type': 'vscode',
        'X-Client-Version': context.extension.packageJSON.version
      }
    });

    this.setupInterceptors();
  }

  private getApiUrl(): string {
    const config = vscode.workspace.getConfiguration('aiguardian');
    return config.get<string>('apiUrl') || 'https://api.aiguardian.ai';
  }

  private getApiKey(): string {
    const config = vscode.workspace.getConfiguration('aiguardian');
    return config.get<string>('apiKey') || '';
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const apiKey = this.getApiKey();
        if (apiKey) {
          config.headers['X-API-Key'] = apiKey;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          vscode.window.showErrorMessage('AI Guardians: Invalid API key. Please configure your API key.');
        } else if (error.response?.status === 429) {
          vscode.window.showWarningMessage('AI Guardians: Rate limit exceeded. Please try again later.');
        } else if (error.code === 'ECONNREFUSED') {
          vscode.window.showErrorMessage('AI Guardians: Unable to connect to API. Please check your internet connection.');
        }
        return Promise.reject(error);
      }
    );
  }

  async analyzeText(
    text: string,
    serviceType: GuardRequest['service_type'],
    context?: {
      filePath?: string;
      language?: string;
      selection?: vscode.Range;
    }
  ): Promise<GuardResponse> {
    const request: GuardRequest = {
      service_type: serviceType,
      payload: {
        text,
        context: {
          file_path: context?.filePath,
          language: context?.language,
          selection: context?.selection ? {
            start_line: context.selection.start.line,
            start_character: context.selection.start.character,
            end_line: context.selection.end.line,
            end_character: context.selection.end.character
          } : undefined
        }
      },
      client_type: 'vscode',
      client_version: this.context.extension.packageJSON.version
    };

    const response: AxiosResponse<GuardResponse> = await this.client.post(
      '/api/v1/guards/process',
      request
    );

    return response.data;
  }

  async analyzeMultipleServices(
    text: string,
    services: GuardRequest['service_type'][],
    context?: {
      filePath?: string;
      language?: string;
      selection?: vscode.Range;
    }
  ): Promise<Map<string, GuardResponse>> {
    const results = new Map<string, GuardResponse>();

    const promises = services.map(async (service) => {
      try {
        const response = await this.analyzeText(text, service, context);
        results.set(service, response);
      } catch (error) {
        console.error(`Error analyzing with ${service}:`, error);
        results.set(service, {
          request_id: '',
          service_type: service,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
          processing_time: 0
        });
      }
    });

    await Promise.allSettled(promises);
    return results;
  }

  async getServiceHealth(): Promise<Record<string, any>> {
    try {
      const response = await this.client.get('/api/v1/guards/health');
      return response.data;
    } catch (error) {
      console.error('Error getting service health:', error);
      return {};
    }
  }
}
```

### 2. Diagnostic Provider

```typescript
// src/providers/diagnosticProvider.ts
import * as vscode from 'vscode';
import { APIService } from '../services/apiService';
import { GuardResponse } from '../types';

export class DiagnosticProvider {
  private diagnosticCollection: vscode.DiagnosticCollection;
  private apiService: APIService;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.diagnosticCollection = vscode.languages.createDiagnosticCollection('aiguardian');
    this.apiService = new APIService(context);
    
    context.subscriptions.push(this.diagnosticCollection);
  }

  async analyzeDocument(document: vscode.TextDocument): Promise<void> {
    const config = vscode.workspace.getConfiguration('aiguardian');
    const enabled = config.get<boolean>('enabled', true);
    const services = config.get<string[]>('services', ['tokenguard', 'trustguard', 'contextguard', 'biasguard']);

    if (!enabled || services.length === 0) {
      this.diagnosticCollection.clear();
      return;
    }

    try {
      const text = document.getText();
      if (!text.trim()) {
        this.diagnosticCollection.clear();
        return;
      }

      const results = await this.apiService.analyzeMultipleServices(
        text,
        services as any[],
        {
          filePath: document.fileName,
          language: document.languageId
        }
      );

      const diagnostics = this.convertToDiagnostics(results, document);
      this.diagnosticCollection.set(document.uri, diagnostics);
    } catch (error) {
      console.error('Error analyzing document:', error);
      vscode.window.showErrorMessage(`AI Guardians analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private convertToDiagnostics(
    results: Map<string, GuardResponse>,
    document: vscode.TextDocument
  ): vscode.Diagnostic[] {
    const diagnostics: vscode.Diagnostic[] = [];

    for (const [serviceType, result] of results) {
      if (!result.success || !result.data) {
        continue;
      }

      const issues = result.data.issues || [];
      const warnings = result.data.warnings || [];
      const recommendations = result.data.recommendations || [];

      // Convert issues to diagnostics
      for (const issue of issues) {
        const range = this.createRange(issue, document);
        const diagnostic = new vscode.Diagnostic(
          range,
          issue.message || `AI Guardian ${serviceType} issue`,
          this.getSeverity(issue.severity || 'warning')
        );

        diagnostic.source = `AI Guardian (${serviceType})`;
        diagnostic.code = issue.code;
        diagnostic.tags = issue.tags || [];

        if (issue.suggestions && issue.suggestions.length > 0) {
          diagnostic.relatedInformation = issue.suggestions.map(suggestion => 
            new vscode.DiagnosticRelatedInformation(
              new vscode.Location(document.uri, range),
              suggestion
            )
          );
        }

        diagnostics.push(diagnostic);
      }

      // Convert warnings to diagnostics
      for (const warning of warnings) {
        const diagnostic = new vscode.Diagnostic(
          new vscode.Range(0, 0, 0, 0),
          warning,
          vscode.DiagnosticSeverity.Warning
        );

        diagnostic.source = `AI Guardian (${serviceType})`;
        diagnostics.push(diagnostic);
      }
    }

    return diagnostics;
  }

  private createRange(issue: any, document: vscode.TextDocument): vscode.Range {
    const startLine = issue.start_line || 0;
    const startCharacter = issue.start_character || 0;
    const endLine = issue.end_line || startLine;
    const endCharacter = issue.end_character || startCharacter;

    return new vscode.Range(
      Math.max(0, startLine),
      Math.max(0, startCharacter),
      Math.min(document.lineCount - 1, endLine),
      Math.max(0, endCharacter)
    );
  }

  private getSeverity(severity: string): vscode.DiagnosticSeverity {
    switch (severity.toLowerCase()) {
      case 'error':
        return vscode.DiagnosticSeverity.Error;
      case 'warning':
        return vscode.DiagnosticSeverity.Warning;
      case 'info':
        return vscode.DiagnosticSeverity.Information;
      case 'hint':
        return vscode.DiagnosticSeverity.Hint;
      default:
        return vscode.DiagnosticSeverity.Warning;
    }
  }

  clear(): void {
    this.diagnosticCollection.clear();
  }
}
```

### 3. Suggestion Provider

```typescript
// src/providers/suggestionProvider.ts
import * as vscode from 'vscode';
import { APIService } from '../services/apiService';
import { GuardResponse } from '../types';

export class SuggestionProvider implements vscode.CodeActionProvider {
  private apiService: APIService;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.apiService = new APIService(context);
  }

  async provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range,
    context: vscode.CodeActionContext,
    token: vscode.CancellationToken
  ): Promise<vscode.CodeAction[]> {
    const actions: vscode.CodeAction[] = [];

    // Get diagnostics from AI Guardians
    const diagnostics = context.diagnostics.filter(d => d.source.startsWith('AI Guardian'));

    for (const diagnostic of diagnostics) {
      if (diagnostic.relatedInformation && diagnostic.relatedInformation.length > 0) {
        for (const info of diagnostic.relatedInformation) {
          const action = new vscode.CodeAction(
            `Apply AI Guardian suggestion: ${info.message}`,
            vscode.CodeActionKind.QuickFix
          );

          action.diagnostics = [diagnostic];
          action.edit = new vscode.WorkspaceEdit();
          action.edit.replace(document.uri, range, info.message);

          actions.push(action);
        }
      }
    }

    return actions;
  }
}
```

### 4. Commands

```typescript
// src/commands/analyzeCommand.ts
import * as vscode from 'vscode';
import { APIService } from '../services/apiService';
import { DiagnosticProvider } from '../providers/diagnosticProvider';

export class AnalyzeCommand {
  private apiService: APIService;
  private diagnosticProvider: DiagnosticProvider;

  constructor(context: vscode.ExtensionContext, diagnosticProvider: DiagnosticProvider) {
    this.apiService = new APIService(context);
    this.diagnosticProvider = diagnosticProvider;
  }

  async analyzeDocument(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active editor found');
      return;
    }

    await this.diagnosticProvider.analyzeDocument(editor.document);
    vscode.window.showInformationMessage('AI Guardians analysis completed');
  }

  async analyzeSelection(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active editor found');
      return;
    }

    const selection = editor.selection;
    if (selection.isEmpty) {
      vscode.window.showWarningMessage('No text selected');
      return;
    }

    const text = editor.document.getText(selection);
    const config = vscode.workspace.getConfiguration('aiguardian');
    const services = config.get<string[]>('services', ['tokenguard', 'trustguard', 'contextguard', 'biasguard']);

    try {
      const results = await this.apiService.analyzeMultipleServices(
        text,
        services as any[],
        {
          filePath: editor.document.fileName,
          language: editor.document.languageId,
          selection: selection
        }
      );

      this.showResults(results, selection);
    } catch (error) {
      vscode.window.showErrorMessage(`Analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async analyzeFile(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active editor found');
      return;
    }

    await this.analyzeDocument();
  }

  private showResults(
    results: Map<string, any>,
    selection: vscode.Selection
  ): void {
    const panel = vscode.window.createWebviewPanel(
      'aiguardianResults',
      'AI Guardians Analysis Results',
      vscode.ViewColumn.Beside,
      {
        enableScripts: true,
        retainContextWhenHidden: true
      }
    );

    let html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Guardians Analysis Results</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          .service { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
          .service-title { font-weight: bold; margin-bottom: 10px; }
          .success { border-color: #4CAF50; background-color: #f1f8e9; }
          .error { border-color: #f44336; background-color: #ffebee; }
          .warning { border-color: #ff9800; background-color: #fff3e0; }
          .confidence { font-size: 14px; color: #666; }
          .issues, .warnings, .recommendations { margin-top: 10px; }
          .issue, .warning, .recommendation { margin: 5px 0; padding: 5px; background: #f5f5f5; border-radius: 3px; }
        </style>
      </head>
      <body>
        <h1>AI Guardians Analysis Results</h1>
        <p>Analysis for selection: lines ${selection.start.line + 1}-${selection.end.line + 1}</p>
    `;

    for (const [serviceType, result] of results) {
      const statusClass = result.success ? 'success' : 'error';
      html += `
        <div class="service ${statusClass}">
          <div class="service-title">${serviceType.toUpperCase()}</div>
          <div class="confidence">Confidence: ${(result.confidence_score || 0) * 100}%</div>
          <div class="processing-time">Processing Time: ${result.processing_time || 0}s</div>
      `;

      if (result.success && result.data) {
        if (result.data.issues && result.data.issues.length > 0) {
          html += '<div class="issues"><h4>Issues Found:</h4>';
          for (const issue of result.data.issues) {
            html += `<div class="issue">${issue.message || 'Issue detected'}</div>`;
          }
          html += '</div>';
        }

        if (result.warnings && result.warnings.length > 0) {
          html += '<div class="warnings"><h4>Warnings:</h4>';
          for (const warning of result.warnings) {
            html += `<div class="warning">${warning}</div>`;
          }
          html += '</div>';
        }

        if (result.recommendations && result.recommendations.length > 0) {
          html += '<div class="recommendations"><h4>Recommendations:</h4>';
          for (const rec of result.recommendations) {
            html += `<div class="recommendation">${rec}</div>`;
          }
          html += '</div>';
        }
      } else {
        html += `<div class="error">Error: ${result.error || 'Unknown error'}</div>`;
      }

      html += '</div>';
    }

    html += '</body></html>';
    panel.webview.html = html;
  }
}
```

### 5. Configuration Command

```typescript
// src/commands/configureCommand.ts
import * as vscode from 'vscode';

export class ConfigureCommand {
  async configureApiKey(): Promise<void> {
    const apiKey = await vscode.window.showInputBox({
      prompt: 'Enter your AI Guardians API key',
      placeHolder: 'API key',
      password: true,
      validateInput: (value) => {
        if (!value || value.trim().length === 0) {
          return 'API key is required';
        }
        if (value.length < 10) {
          return 'API key appears to be too short';
        }
        return null;
      }
    });

    if (apiKey) {
      const config = vscode.workspace.getConfiguration('aiguardian');
      await config.update('apiKey', apiKey, vscode.ConfigurationTarget.Global);
      vscode.window.showInformationMessage('API key configured successfully');
    }
  }

  async configureSettings(): Promise<void> {
    await vscode.commands.executeCommand('workbench.action.openSettings', 'aiguardian');
  }
}
```

## Extension Activation

```typescript
// src/extension.ts
import * as vscode from 'vscode';
import { DiagnosticProvider } from './providers/diagnosticProvider';
import { SuggestionProvider } from './providers/suggestionProvider';
import { AnalyzeCommand } from './commands/analyzeCommand';
import { ConfigureCommand } from './commands/configureCommand';

export function activate(context: vscode.ExtensionContext) {
  console.log('AI Guardians extension is now active!');

  // Initialize providers
  const diagnosticProvider = new DiagnosticProvider(context);
  const suggestionProvider = new SuggestionProvider(context);
  const analyzeCommand = new AnalyzeCommand(context, diagnosticProvider);
  const configureCommand = new ConfigureCommand();

  // Register commands
  const analyzeDocumentCommand = vscode.commands.registerCommand(
    'aiguardian.analyze',
    () => analyzeCommand.analyzeDocument()
  );

  const analyzeSelectionCommand = vscode.commands.registerCommand(
    'aiguardian.analyzeSelection',
    () => analyzeCommand.analyzeSelection()
  );

  const analyzeFileCommand = vscode.commands.registerCommand(
    'aiguardian.analyzeFile',
    () => analyzeCommand.analyzeFile()
  );

  const configureApiKeyCommand = vscode.commands.registerCommand(
    'aiguardian.configure',
    () => configureCommand.configureApiKey()
  );

  const configureSettingsCommand = vscode.commands.registerCommand(
    'aiguardian.configureSettings',
    () => configureCommand.configureSettings()
  );

  // Register code action provider
  const codeActionProvider = vscode.languages.registerCodeActionsProvider(
    { scheme: 'file' },
    suggestionProvider
  );

  // Register document change handler
  const documentChangeHandler = vscode.workspace.onDidChangeTextDocument(
    (event) => {
      const config = vscode.workspace.getConfiguration('aiguardian');
      const autoAnalyze = config.get<boolean>('autoAnalyze', true);
      
      if (autoAnalyze) {
        diagnosticProvider.analyzeDocument(event.document);
      }
    }
  );

  // Register document open handler
  const documentOpenHandler = vscode.workspace.onDidOpenTextDocument(
    (document) => {
      const config = vscode.workspace.getConfiguration('aiguardian');
      const autoAnalyze = config.get<boolean>('autoAnalyze', true);
      
      if (autoAnalyze) {
        diagnosticProvider.analyzeDocument(document);
      }
    }
  );

  // Register configuration change handler
  const configChangeHandler = vscode.workspace.onDidChangeConfiguration(
    (event) => {
      if (event.affectsConfiguration('aiguardian')) {
        // Re-analyze all open documents
        vscode.workspace.textDocuments.forEach(document => {
          diagnosticProvider.analyzeDocument(document);
        });
      }
    }
  );

  // Add to subscriptions
  context.subscriptions.push(
    analyzeDocumentCommand,
    analyzeSelectionCommand,
    analyzeFileCommand,
    configureApiKeyCommand,
    configureSettingsCommand,
    codeActionProvider,
    documentChangeHandler,
    documentOpenHandler,
    configChangeHandler
  );

  // Initial analysis of open documents
  vscode.workspace.textDocuments.forEach(document => {
    diagnosticProvider.analyzeDocument(document);
  });
}

export function deactivate() {
  console.log('AI Guardians extension is now deactivated');
}
```

## Testing

### Unit Tests

```typescript
// src/test/apiService.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';
import { APIService } from '../services/apiService';

suite('APIService', () => {
  let apiService: APIService;
  let mockContext: vscode.ExtensionContext;

  setup(() => {
    mockContext = {
      extension: {
        packageJSON: { version: '1.0.0' }
      }
    } as any;

    apiService = new APIService(mockContext);
  });

  test('should create API service', () => {
    assert.ok(apiService);
  });

  test('should analyze text', async () => {
    // Mock axios
    const mockAxios = require('axios');
    mockAxios.create = () => ({
      post: () => Promise.resolve({
        data: {
          success: true,
          data: { confidence: 0.85 }
        }
      })
    });

    const result = await apiService.analyzeText('test text', 'tokenguard');
    assert.strictEqual(result.success, true);
  });
});
```

## Publishing

### 1. Build Extension

```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
npx vsce package
```

### 2. Publish to Marketplace

```bash
# Install vsce
npm install -g vsce

# Login to marketplace
vsce login

# Publish extension
vsce publish
```

## Usage Examples

### 1. Basic Analysis

```typescript
// User selects text and runs command
// Extension analyzes with all enabled services
// Results displayed in diagnostics panel
```

### 2. Configuration

```typescript
// User opens settings
// Configures API key and service preferences
// Extension applies new settings immediately
```

### 3. Quick Fixes

```typescript
// User sees diagnostic with suggestion
// Clicks on lightbulb icon
// Applies AI Guardian suggestion
```

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Check API key in settings
   - Verify API key is valid
   - Check network connectivity

2. **Analysis Not Running**
   - Check if extension is enabled
   - Verify auto-analyze is enabled
   - Check service configuration

3. **Performance Issues**
   - Reduce number of enabled services
   - Increase confidence threshold
   - Check API rate limits

### Debug Mode

```typescript
// Enable debug logging
const config = vscode.workspace.getConfiguration('aiguardian');
await config.update('debug', true, vscode.ConfigurationTarget.Global);
```

## Internal Testing

For development and testing purposes, you can use the internal testing system with JWT tokens instead of API keys.

### Setup Internal Testing

1. **Enable internal testing** in your AWS secrets:
   ```bash
   aws secretsmanager update-secret \
     --secret-id "codeguardians-gateway/internal-testing" \
     --secret-string '{
       "INTERNAL_TESTING_ENABLED": "true",
       "INTERNAL_TESTING_JWT_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
     }'
   ```

2. **Update VS Code extension** to use JWT authentication:

```typescript
// src/services/apiService.ts - Updated for internal testing
export class APIService {
  private jwtToken: string | null = null;
  private apiUrl = 'http://localhost:8000';
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.init();
  }

  async init() {
    // Get JWT token from internal testing endpoint
    try {
      const response = await fetch('http://localhost:8000/api/v1/internal-testing/token');
      const data = await response.json();
      this.jwtToken = data.jwt_token;
      console.log('Internal testing JWT token loaded');
    } catch (error) {
      console.error('Failed to get JWT token:', error);
    }
  }

  async analyzeText(text: string, serviceType: string): Promise<GuardResponse> {
    if (!this.jwtToken) {
      throw new Error('JWT token not available');
    }

    const response = await fetch(`${this.apiUrl}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.jwtToken}`,
        'X-Client-Type': 'vscode'
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'vscode'
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }
}
```

### Benefits of Internal Testing

-  **No API key management** - JWT token is automatically retrieved
-  **Simplified setup** - Just enable internal testing in AWS secrets
-  **Secure** - JWT tokens with proper authentication
-  **Easy to rotate** - Update JWT token in AWS secrets

For more details, see [Internal Testing Setup Guide](./INTERNAL_TESTING_SETUP.md).

## Getting Help

- [VS Code Extension API](https://code.visualstudio.com/api)
- [AI Guardians API Documentation](./API_DOCUMENTATION.md)
- [Internal Testing Setup Guide](./INTERNAL_TESTING_SETUP.md)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

