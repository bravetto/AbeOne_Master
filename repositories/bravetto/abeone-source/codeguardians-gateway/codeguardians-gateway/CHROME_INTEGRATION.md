# Chrome Extension Integration Guide

## Overview

This guide covers integrating the AI Guardians platform with Chrome extensions, providing real-time content analysis, bias detection, and AI-powered suggestions for web content.

## Architecture

```
        
   Web Page             Chrome Ext           AI Guardians  
   Content          (JavaScript)     API Gateway   
        
                              
                              
                    
                       Guard Services
                      (TokenGuard,   
                       TrustGuard,   
                       ContextGuard, 
                       BiasGuard)    
                    
```

## Extension Setup

### 1. Project Structure

```
chrome-extension/
 manifest.json
 background.js
 content.js
 popup.html
 popup.js
 options.html
 options.js
 content.css
 popup.css
 options.css
 icons/
    icon16.png
    icon48.png
    icon128.png
 README.md
```

### 2. Manifest Configuration

```json
// manifest.json
{
  "manifest_version": 3,
  "name": "AI Guardians",
  "version": "1.0.0",
  "description": "AI-powered content analysis and protection for web pages",
  "permissions": [
    "activeTab",
    "storage",
    "scripting",
    "tabs"
  ],
  "host_permissions": [
    "https://api.aiguardian.ai/*",
    "<all_urls>"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["content.css"],
      "run_at": "document_end"
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_title": "AI Guardians",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "options_page": "options.html",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "web_accessible_resources": [
    {
      "resources": ["content.css"],
      "matches": ["<all_urls>"]
    }
  ]
}
```

## Core Implementation

### 1. Background Script

```javascript
// background.js
class AIGuardianBackground {
  constructor() {
    this.apiKey = null;
    this.apiUrl = 'https://api.aiguardian.ai';
    this.enabledServices = ['tokenguard', 'trustguard', 'contextguard', 'biasguard'];
    this.confidenceThreshold = 0.7;
    this.init();
  }

  async init() {
    // Load configuration from storage
    const config = await chrome.storage.sync.get([
      'apiKey',
      'apiUrl',
      'enabledServices',
      'confidenceThreshold',
      'enabled'
    ]);

    this.apiKey = config.apiKey || null;
    this.apiUrl = config.apiUrl || 'https://api.aiguardian.ai';
    this.enabledServices = config.enabledServices || ['tokenguard', 'trustguard', 'contextguard', 'biasguard'];
    this.confidenceThreshold = config.confidenceThreshold || 0.7;

    // Set up message listeners
    this.setupMessageListeners();
  }

  setupMessageListeners() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.handleMessage(request, sender, sendResponse);
      return true; // Keep message channel open for async response
    });
  }

  async handleMessage(request, sender, sendResponse) {
    try {
      switch (request.action) {
        case 'analyze':
          const result = await this.analyzeText(request.text, request.serviceType);
          sendResponse({ success: true, data: result });
          break;

        case 'analyzeMultiple':
          const results = await this.analyzeMultipleServices(request.text);
          sendResponse({ success: true, data: results });
          break;

        case 'getConfig':
          const config = await this.getConfig();
          sendResponse({ success: true, data: config });
          break;

        case 'updateConfig':
          await this.updateConfig(request.config);
          sendResponse({ success: true });
          break;

        case 'getServiceHealth':
          const health = await this.getServiceHealth();
          sendResponse({ success: true, data: health });
          break;

        default:
          sendResponse({ success: false, error: 'Unknown action' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ success: false, error: error.message });
    }
  }

  async analyzeText(text, serviceType = 'biasguard') {
    if (!this.apiKey) {
      throw new Error('API key not configured');
    }

    const response = await fetch(`${this.apiUrl}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'X-Client-Type': 'chrome'
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'chrome',
        client_version: chrome.runtime.getManifest().version
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }

  async analyzeMultipleServices(text) {
    const results = {};

    for (const service of this.enabledServices) {
      try {
        const result = await this.analyzeText(text, service);
        results[service] = result;
      } catch (error) {
        console.error(`Error analyzing with ${service}:`, error);
        results[service] = {
          success: false,
          error: error.message
        };
      }
    }

    return results;
  }

  async getConfig() {
    return await chrome.storage.sync.get([
      'apiKey',
      'apiUrl',
      'enabledServices',
      'confidenceThreshold',
      'enabled'
    ]);
  }

  async updateConfig(config) {
    await chrome.storage.sync.set(config);
    
    // Update local state
    this.apiKey = config.apiKey || this.apiKey;
    this.apiUrl = config.apiUrl || this.apiUrl;
    this.enabledServices = config.enabledServices || this.enabledServices;
    this.confidenceThreshold = config.confidenceThreshold || this.confidenceThreshold;
  }

  async getServiceHealth() {
    try {
      const response = await fetch(`${this.apiUrl}/api/v1/guards/health`);
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      return { error: error.message };
    }
  }
}

// Initialize background script
const aiGuardian = new AIGuardianBackground();
```

### 2. Content Script

```javascript
// content.js
class AIGuardianContent {
  constructor() {
    this.highlights = [];
    this.overlay = null;
    this.config = null;
    this.init();
  }

  async init() {
    // Load configuration
    this.config = await this.sendMessage({ action: 'getConfig' });
    
    if (!this.config.data.enabled) {
      return;
    }

    // Wait for page to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.analyzePage());
    } else {
      this.analyzePage();
    }

    // Set up mutation observer for dynamic content
    this.setupMutationObserver();
  }

  setupMutationObserver() {
    const observer = new MutationObserver((mutations) => {
      let shouldAnalyze = false;
      
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          shouldAnalyze = true;
        }
      });

      if (shouldAnalyze) {
        this.analyzePage();
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  async analyzePage() {
    const text = this.extractText();
    if (!text.trim() || text.length < 50) {
      return;
    }

    try {
      const results = await this.sendMessage({
        action: 'analyzeMultiple',
        text: text
      });

      if (results.success) {
        this.displayResults(results.data);
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
      'p',
      'div[role="article"]',
      '.story',
      '.entry'
    ];

    let text = '';
    const processedElements = new Set();

    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      for (const element of elements) {
        if (processedElements.has(element)) {
          continue;
        }

        const elementText = element.textContent.trim();
        if (elementText.length > 20) {
          text += elementText + ' ';
          processedElements.add(element);
        }
      }
    }

    return text.trim();
  }

  async sendMessage(message) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(message, resolve);
    });
  }

  displayResults(results) {
    // Clear previous highlights
    this.clearHighlights();

    // Create badge
    this.createBadge(results);

    // Process results for each service
    for (const [serviceType, result] of Object.entries(results)) {
      if (result.success && result.data) {
        this.processServiceResult(serviceType, result.data);
      }
    }
  }

  createBadge(results) {
    // Remove existing badge
    const existingBadge = document.querySelector('.ai-guardian-badge');
    if (existingBadge) {
      existingBadge.remove();
    }

    // Calculate overall status
    let totalIssues = 0;
    let hasErrors = false;

    for (const [serviceType, result] of Object.entries(results)) {
      if (result.success && result.data) {
        totalIssues += result.data.issues_count || 0;
      } else {
        hasErrors = true;
      }
    }

    const badge = document.createElement('div');
    badge.className = 'ai-guardian-badge';
    badge.innerHTML = `
      <div class="badge-content">
        <span class="badge-icon">${hasErrors ? '' : (totalIssues > 0 ? '' : '')}</span>
        <span class="badge-text">${totalIssues > 0 ? totalIssues : 'OK'}</span>
      </div>
    `;

    badge.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${hasErrors ? '#ff4444' : (totalIssues > 0 ? '#ff9800' : '#4caf50')};
      color: white;
      padding: 8px 12px;
      border-radius: 20px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      z-index: 10000;
      cursor: pointer;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
      transition: all 0.3s ease;
    `;

    badge.addEventListener('click', () => {
      this.showDetails(results);
    });

    badge.addEventListener('mouseenter', () => {
      badge.style.transform = 'scale(1.05)';
    });

    badge.addEventListener('mouseleave', () => {
      badge.style.transform = 'scale(1)';
    });

    document.body.appendChild(badge);
  }

  processServiceResult(serviceType, data) {
    // Process issues
    if (data.issues && data.issues.length > 0) {
      this.highlightIssues(serviceType, data.issues);
    }

    // Process warnings
    if (data.warnings && data.warnings.length > 0) {
      this.showWarnings(serviceType, data.warnings);
    }
  }

  highlightIssues(serviceType, issues) {
    for (const issue of issues) {
      if (issue.text && issue.start && issue.end) {
        this.highlightText(issue.text, issue.start, issue.end, serviceType, issue.severity);
      }
    }
  }

  highlightText(text, start, end, serviceType, severity) {
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    let node;
    while (node = walker.nextNode()) {
      const nodeText = node.textContent;
      const index = nodeText.indexOf(text);
      
      if (index !== -1) {
        const range = document.createRange();
        range.setStart(node, index);
        range.setEnd(node, index + text.length);

        const highlight = document.createElement('span');
        highlight.className = `ai-guardian-highlight ai-guardian-${serviceType} ai-guardian-${severity || 'warning'}`;
        highlight.setAttribute('data-service', serviceType);
        highlight.setAttribute('data-severity', severity || 'warning');
        highlight.title = `AI Guardian ${serviceType}: ${text}`;

        try {
          range.surroundContents(highlight);
          this.highlights.push(highlight);
        } catch (e) {
          console.warn('Could not highlight text:', e);
        }
        break;
      }
    }
  }

  showWarnings(serviceType, warnings) {
    // Create warning overlay
    const overlay = document.createElement('div');
    overlay.className = `ai-guardian-warning-overlay ai-guardian-${serviceType}`;
    overlay.innerHTML = `
      <div class="warning-content">
        <h4>AI Guardian ${serviceType} Warnings</h4>
        <ul>
          ${warnings.map(warning => `<li>${warning}</li>`).join('')}
        </ul>
      </div>
    `;

    overlay.style.cssText = `
      position: fixed;
      top: 60px;
      right: 20px;
      background: #fff3cd;
      border: 1px solid #ffeaa7;
      border-radius: 5px;
      padding: 15px;
      max-width: 300px;
      z-index: 9999;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;

    document.body.appendChild(overlay);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }, 5000);
  }

  showDetails(results) {
    // Remove existing modal
    const existingModal = document.querySelector('.ai-guardian-modal');
    if (existingModal) {
      existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.className = 'ai-guardian-modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h2>AI Guardians Analysis Results</h2>
          <button class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          ${this.generateResultsHTML(results)}
        </div>
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

    // Close modal handlers
    modal.querySelector('.close-btn').addEventListener('click', () => {
      modal.remove();
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });

    document.body.appendChild(modal);
  }

  generateResultsHTML(results) {
    let html = '';

    for (const [serviceType, result] of Object.entries(results)) {
      const statusClass = result.success ? 'success' : 'error';
      html += `
        <div class="service-result ${statusClass}">
          <h3>${serviceType.toUpperCase()}</h3>
          <div class="confidence">
            Confidence: ${(result.confidence_score || 0) * 100}%
          </div>
          <div class="processing-time">
            Processing Time: ${result.processing_time || 0}s
          </div>
      `;

      if (result.success && result.data) {
        if (result.data.issues && result.data.issues.length > 0) {
          html += '<div class="issues"><h4>Issues Found:</h4><ul>';
          for (const issue of result.data.issues) {
            html += `<li>${issue.message || 'Issue detected'}</li>`;
          }
          html += '</ul></div>';
        }

        if (result.warnings && result.warnings.length > 0) {
          html += '<div class="warnings"><h4>Warnings:</h4><ul>';
          for (const warning of result.warnings) {
            html += `<li>${warning}</li>`;
          }
          html += '</ul></div>';
        }

        if (result.recommendations && result.recommendations.length > 0) {
          html += '<div class="recommendations"><h4>Recommendations:</h4><ul>';
          for (const rec of result.recommendations) {
            html += `<li>${rec}</li>`;
          }
          html += '</ul></div>';
        }
      } else {
        html += `<div class="error">Error: ${result.error || 'Unknown error'}</div>`;
      }

      html += '</div>';
    }

    return html;
  }

  clearHighlights() {
    this.highlights.forEach(highlight => {
      if (highlight.parentNode) {
        highlight.parentNode.replaceChild(
          document.createTextNode(highlight.textContent),
          highlight
        );
      }
    });
    this.highlights = [];
  }
}

// Initialize content script
new AIGuardianContent();
```

### 3. Popup Interface

```html
<!-- popup.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Guardians</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="popup-container">
    <div class="header">
      <h1>AI Guardians</h1>
      <div class="status-indicator" id="statusIndicator"></div>
    </div>
    
    <div class="content">
      <div class="service-status" id="serviceStatus">
        <h3>Service Status</h3>
        <div class="status-list" id="statusList">
          Loading...
        </div>
      </div>
      
      <div class="quick-actions">
        <button id="analyzeBtn" class="btn btn-primary">Analyze Page</button>
        <button id="settingsBtn" class="btn btn-secondary">Settings</button>
      </div>
      
      <div class="results" id="results" style="display: none;">
        <h3>Analysis Results</h3>
        <div class="results-content" id="resultsContent"></div>
      </div>
    </div>
  </div>
  
  <script src="popup.js"></script>
</body>
</html>
```

```css
/* popup.css */
.popup-container {
  width: 350px;
  min-height: 400px;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.header h1 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ccc;
}

.status-indicator.connected {
  background: #4caf50;
}

.status-indicator.error {
  background: #f44336;
}

.service-status {
  margin-bottom: 20px;
}

.service-status h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.status-list {
  font-size: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-item:last-child {
  border-bottom: none;
}

.service-name {
  font-weight: bold;
}

.service-status-badge {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  text-transform: uppercase;
}

.service-status-badge.healthy {
  background: #e8f5e8;
  color: #2e7d32;
}

.service-status-badge.unhealthy {
  background: #ffebee;
  color: #c62828;
}

.quick-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
}

.btn-primary {
  background: #2196f3;
  color: white;
}

.btn-primary:hover {
  background: #1976d2;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.results {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.results h3 {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #666;
}

.results-content {
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  font-size: 12px;
}

.result-item.success {
  background: #e8f5e8;
  border-left: 3px solid #4caf50;
}

.result-item.warning {
  background: #fff3e0;
  border-left: 3px solid #ff9800;
}

.result-item.error {
  background: #ffebee;
  border-left: 3px solid #f44336;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.result-service {
  font-weight: bold;
  text-transform: uppercase;
}

.result-confidence {
  color: #666;
}

.result-issues {
  margin-top: 5px;
}

.result-issues ul {
  margin: 5px 0 0 0;
  padding-left: 15px;
}

.result-issues li {
  margin: 2px 0;
}
```

```javascript
// popup.js
class AIGuardianPopup {
  constructor() {
    this.init();
  }

  async init() {
    await this.loadServiceStatus();
    this.setupEventListeners();
  }

  async loadServiceStatus() {
    try {
      const response = await this.sendMessage({ action: 'getServiceHealth' });
      
      if (response.success) {
        this.displayServiceStatus(response.data);
        this.updateStatusIndicator('connected');
      } else {
        this.updateStatusIndicator('error');
      }
    } catch (error) {
      console.error('Error loading service status:', error);
      this.updateStatusIndicator('error');
    }
  }

  displayServiceStatus(healthData) {
    const statusList = document.getElementById('statusList');
    
    if (Object.keys(healthData).length === 0) {
      statusList.innerHTML = '<div class="status-item">No services available</div>';
      return;
    }

    let html = '';
    for (const [serviceName, status] of Object.entries(healthData)) {
      const statusClass = status.status === 'healthy' ? 'healthy' : 'unhealthy';
      html += `
        <div class="status-item">
          <span class="service-name">${serviceName}</span>
          <span class="service-status-badge ${statusClass}">${status.status}</span>
        </div>
      `;
    }
    
    statusList.innerHTML = html;
  }

  updateStatusIndicator(status) {
    const indicator = document.getElementById('statusIndicator');
    indicator.className = `status-indicator ${status}`;
  }

  setupEventListeners() {
    document.getElementById('analyzeBtn').addEventListener('click', () => {
      this.analyzeCurrentPage();
    });

    document.getElementById('settingsBtn').addEventListener('click', () => {
      chrome.runtime.openOptionsPage();
    });
  }

  async analyzeCurrentPage() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const results = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');

    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;

    try {
      // Get current tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send message to content script
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'analyze' });
      
      if (response.success) {
        this.displayResults(response.data);
        results.style.display = 'block';
      } else {
        throw new Error(response.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      resultsContent.innerHTML = `<div class="result-item error">Error: ${error.message}</div>`;
      results.style.display = 'block';
    } finally {
      analyzeBtn.textContent = 'Analyze Page';
      analyzeBtn.disabled = false;
    }
  }

  displayResults(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '';
    for (const [serviceType, result] of Object.entries(results)) {
      const statusClass = result.success ? 'success' : 'error';
      html += `
        <div class="result-item ${statusClass}">
          <div class="result-header">
            <span class="result-service">${serviceType}</span>
            <span class="result-confidence">${(result.confidence_score || 0) * 100}%</span>
          </div>
          ${result.success && result.data ? this.generateResultContent(result.data) : `<div>Error: ${result.error}</div>`}
        </div>
      `;
    }
    
    resultsContent.innerHTML = html;
  }

  generateResultContent(data) {
    let html = '';
    
    if (data.issues && data.issues.length > 0) {
      html += '<div class="result-issues"><strong>Issues:</strong><ul>';
      for (const issue of data.issues) {
        html += `<li>${issue.message || 'Issue detected'}</li>`;
      }
      html += '</ul></div>';
    }

    if (data.warnings && data.warnings.length > 0) {
      html += '<div class="result-issues"><strong>Warnings:</strong><ul>';
      for (const warning of data.warnings) {
        html += `<li>${warning}</li>`;
      }
      html += '</ul></div>';
    }

    if (data.recommendations && data.recommendations.length > 0) {
      html += '<div class="result-issues"><strong>Recommendations:</strong><ul>';
      for (const rec of data.recommendations) {
        html += `<li>${rec}</li>`;
      }
      html += '</ul></div>';
    }

    return html || '<div>No issues found</div>';
  }

  async sendMessage(message) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(message, resolve);
    });
  }
}

// Initialize popup
new AIGuardianPopup();
```

### 4. Options Page

```html
<!-- options.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Guardians Settings</title>
  <link rel="stylesheet" href="options.css">
</head>
<body>
  <div class="options-container">
    <h1>AI Guardians Settings</h1>
    
    <form id="settingsForm">
      <div class="form-group">
        <label for="apiKey">API Key</label>
        <input type="password" id="apiKey" placeholder="Enter your API key">
        <small>Get your API key from <a href="https://app.aiguardian.ai" target="_blank">app.aiguardian.ai</a></small>
      </div>
      
      <div class="form-group">
        <label for="apiUrl">API URL</label>
        <input type="url" id="apiUrl" placeholder="https://api.aiguardian.ai">
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" id="enabled" checked>
          Enable AI Guardians
        </label>
      </div>
      
      <div class="form-group">
        <label>Enabled Services</label>
        <div class="checkbox-group">
          <label><input type="checkbox" name="services" value="tokenguard" checked> Token Guard</label>
          <label><input type="checkbox" name="services" value="trustguard" checked> Trust Guard</label>
          <label><input type="checkbox" name="services" value="contextguard" checked> Context Guard</label>
          <label><input type="checkbox" name="services" value="biasguard" checked> Bias Guard</label>
        </div>
      </div>
      
      <div class="form-group">
        <label for="confidenceThreshold">Confidence Threshold</label>
        <input type="range" id="confidenceThreshold" min="0" max="1" step="0.1" value="0.7">
        <span id="confidenceValue">70%</span>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">Save Settings</button>
        <button type="button" id="testConnection" class="btn btn-secondary">Test Connection</button>
      </div>
    </form>
    
    <div id="statusMessage" class="status-message"></div>
  </div>
  
  <script src="options.js"></script>
</body>
</html>
```

```css
/* options.css */
.options-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="password"],
.form-group input[type="url"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group input[type="checkbox"] {
  margin-right: 8px;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  margin-bottom: 0;
}

.form-group input[type="range"] {
  width: 100%;
  margin-right: 10px;
}

#confidenceValue {
  font-weight: bold;
  color: #2196f3;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.btn-primary {
  background: #2196f3;
  color: white;
}

.btn-primary:hover {
  background: #1976d2;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.status-message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  display: none;
}

.status-message.success {
  background: #e8f5e8;
  color: #2e7d32;
  border: 1px solid #4caf50;
}

.status-message.error {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #f44336;
}

small {
  color: #666;
  font-size: 12px;
}

a {
  color: #2196f3;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

```javascript
// options.js
class AIGuardianOptions {
  constructor() {
    this.init();
  }

  async init() {
    await this.loadSettings();
    this.setupEventListeners();
  }

  async loadSettings() {
    try {
      const response = await this.sendMessage({ action: 'getConfig' });
      
      if (response.success) {
        const config = response.data;
        
        document.getElementById('apiKey').value = config.apiKey || '';
        document.getElementById('apiUrl').value = config.apiUrl || 'https://api.aiguardian.ai';
        document.getElementById('enabled').checked = config.enabled !== false;
        document.getElementById('confidenceThreshold').value = config.confidenceThreshold || 0.7;
        
        // Update confidence value display
        this.updateConfidenceValue();
        
        // Set service checkboxes
        const serviceCheckboxes = document.querySelectorAll('input[name="services"]');
        serviceCheckboxes.forEach(checkbox => {
          checkbox.checked = (config.enabledServices || []).includes(checkbox.value);
        });
      }
    } catch (error) {
      console.error('Error loading settings:', error);
      this.showStatus('Error loading settings', 'error');
    }
  }

  setupEventListeners() {
    document.getElementById('settingsForm').addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveSettings();
    });

    document.getElementById('testConnection').addEventListener('click', () => {
      this.testConnection();
    });

    document.getElementById('confidenceThreshold').addEventListener('input', () => {
      this.updateConfidenceValue();
    });
  }

  updateConfidenceValue() {
    const threshold = document.getElementById('confidenceThreshold').value;
    document.getElementById('confidenceValue').textContent = Math.round(threshold * 100) + '%';
  }

  async saveSettings() {
    const formData = new FormData(document.getElementById('settingsForm'));
    const config = {
      apiKey: document.getElementById('apiKey').value,
      apiUrl: document.getElementById('apiUrl').value,
      enabled: document.getElementById('enabled').checked,
      confidenceThreshold: parseFloat(document.getElementById('confidenceThreshold').value),
      enabledServices: Array.from(document.querySelectorAll('input[name="services"]:checked')).map(cb => cb.value)
    };

    try {
      await this.sendMessage({ action: 'updateConfig', config });
      this.showStatus('Settings saved successfully', 'success');
    } catch (error) {
      console.error('Error saving settings:', error);
      this.showStatus('Error saving settings', 'error');
    }
  }

  async testConnection() {
    const testBtn = document.getElementById('testConnection');
    const originalText = testBtn.textContent;
    
    testBtn.textContent = 'Testing...';
    testBtn.disabled = true;

    try {
      const response = await this.sendMessage({ action: 'getServiceHealth' });
      
      if (response.success && Object.keys(response.data).length > 0) {
        this.showStatus('Connection successful', 'success');
      } else {
        this.showStatus('Connection failed', 'error');
      }
    } catch (error) {
      console.error('Connection test error:', error);
      this.showStatus('Connection test failed', 'error');
    } finally {
      testBtn.textContent = originalText;
      testBtn.disabled = false;
    }
  }

  showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    
    setTimeout(() => {
      statusMessage.style.display = 'none';
    }, 3000);
  }

  async sendMessage(message) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(message, resolve);
    });
  }
}

// Initialize options page
new AIGuardianOptions();
```

## Content Styling

```css
/* content.css */
.ai-guardian-highlight {
  position: relative;
  background: rgba(255, 193, 7, 0.3);
  border-bottom: 2px solid #ffc107;
  cursor: pointer;
}

.ai-guardian-highlight:hover {
  background: rgba(255, 193, 7, 0.5);
}

.ai-guardian-highlight.ai-guardian-error {
  background: rgba(244, 67, 54, 0.3);
  border-bottom-color: #f44336;
}

.ai-guardian-highlight.ai-guardian-warning {
  background: rgba(255, 152, 0, 0.3);
  border-bottom-color: #ff9800;
}

.ai-guardian-highlight.ai-guardian-info {
  background: rgba(33, 150, 243, 0.3);
  border-bottom-color: #2196f3;
}

.ai-guardian-tooltip {
  position: absolute;
  background: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 10000;
  pointer-events: none;
  white-space: nowrap;
  max-width: 300px;
  word-wrap: break-word;
}

.ai-guardian-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #333 transparent transparent transparent;
}

.ai-guardian-badge {
  font-family: Arial, sans-serif;
  user-select: none;
}

.ai-guardian-badge .badge-content {
  display: flex;
  align-items: center;
  gap: 5px;
}

.ai-guardian-badge .badge-icon {
  font-size: 16px;
}

.ai-guardian-badge .badge-text {
  font-weight: bold;
}

.ai-guardian-modal {
  font-family: Arial, sans-serif;
}

.ai-guardian-modal .modal-content {
  background: white;
  border-radius: 8px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.ai-guardian-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.ai-guardian-modal .modal-header h2 {
  margin: 0;
  color: #333;
}

.ai-guardian-modal .close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.ai-guardian-modal .close-btn:hover {
  color: #333;
}

.ai-guardian-modal .modal-body {
  padding: 20px;
}

.service-result {
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 5px;
  border-left: 4px solid #ddd;
}

.service-result.success {
  background: #f1f8e9;
  border-left-color: #4caf50;
}

.service-result.error {
  background: #ffebee;
  border-left-color: #f44336;
}

.service-result h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.service-result .confidence,
.service-result .processing-time {
  font-size: 12px;
  color: #666;
  margin: 5px 0;
}

.service-result .issues,
.service-result .warnings,
.service-result .recommendations {
  margin-top: 10px;
}

.service-result .issues h4,
.service-result .warnings h4,
.service-result .recommendations h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #555;
}

.service-result ul {
  margin: 0;
  padding-left: 20px;
}

.service-result li {
  margin: 5px 0;
  font-size: 13px;
  line-height: 1.4;
}
```

## Testing

### 1. Unit Tests

```javascript
// test/background.test.js
describe('AIGuardianBackground', () => {
  let background;

  beforeEach(() => {
    background = new AIGuardianBackground();
  });

  test('should initialize with default config', () => {
    expect(background.apiUrl).toBe('https://api.aiguardian.ai');
    expect(background.enabledServices).toEqual(['tokenguard', 'trustguard', 'contextguard', 'biasguard']);
  });

  test('should analyze text', async () => {
    // Mock fetch
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        success: true,
        data: { confidence: 0.85 }
      })
    });

    const result = await background.analyzeText('test text', 'tokenguard');
    expect(result.success).toBe(true);
    expect(result.data.confidence).toBe(0.85);
  });
});
```

### 2. Integration Tests

```javascript
// test/integration.test.js
describe('Extension Integration', () => {
  test('should communicate between content and background', async () => {
    // Test message passing
    const message = { action: 'analyze', text: 'test' };
    const response = await new Promise(resolve => {
      chrome.runtime.sendMessage(message, resolve);
    });
    
    expect(response.success).toBe(true);
  });
});
```

## Publishing

### 1. Build Extension

```bash
# Install dependencies
npm install

# Build extension
npm run build

# Package extension
npm run package
```

### 2. Chrome Web Store

```bash
# Create zip file
zip -r aiguardian-extension.zip . -x "*.git*" "node_modules/*" "test/*"

# Upload to Chrome Web Store
# Go to https://chrome.google.com/webstore/devconsole
# Upload the zip file
```

## Usage Examples

### 1. Basic Analysis

```javascript
// User visits a webpage
// Extension automatically analyzes content
// Results displayed in badge and highlights
```

### 2. Manual Analysis

```javascript
// User clicks extension icon
// Clicks "Analyze Page" button
// Results displayed in popup
```

### 3. Configuration

```javascript
// User opens options page
// Configures API key and settings
// Extension applies new configuration
```

## Troubleshooting

### Common Issues

1. **Extension Not Working**
   - Check if extension is enabled
   - Verify API key is configured
   - Check browser console for errors

2. **API Errors**
   - Verify API key is valid
   - Check network connectivity
   - Verify API URL is correct

3. **Content Not Highlighted**
   - Check if content script is loaded
   - Verify page is not restricted
   - Check for JavaScript errors

### Debug Mode

```javascript
// Enable debug logging
chrome.storage.sync.set({ debug: true });

// Check logs in background script
console.log('Debug mode enabled');
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

2. **Update Chrome extension** to use JWT authentication:

```javascript
// background.js - Updated for internal testing
class AIGuardianBackground {
  constructor() {
    this.jwtToken = null;
    this.apiUrl = 'http://localhost:8000';
    this.enabledServices = ['tokenguard', 'trustguard', 'contextguard', 'biasguard'];
    this.confidenceThreshold = 0.7;
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

    // Set up message listeners
    this.setupMessageListeners();
  }

  async analyzeText(text, serviceType = 'biasguard') {
    if (!this.jwtToken) {
      throw new Error('JWT token not available');
    }

    const response = await fetch(`${this.apiUrl}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.jwtToken}`,
        'X-Client-Type': 'chrome'
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'chrome',
        client_version: chrome.runtime.getManifest().version
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
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

- [Chrome Extension API](https://developer.chrome.com/docs/extensions/)
- [AI Guardians API Documentation](./API_DOCUMENTATION.md)
- [Internal Testing Setup Guide](./INTERNAL_TESTING_SETUP.md)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

