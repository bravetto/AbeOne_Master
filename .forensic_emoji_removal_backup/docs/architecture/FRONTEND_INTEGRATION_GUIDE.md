# AIGuardian Frontend Integration Guide

**Complete Frontend Integration • SDK Usage • Authentication Flow**

---

## 🎯 **Frontend Integration Overview**

This guide provides comprehensive instructions for integrating AIGuardian with frontend applications, including authentication, API usage, and real-time features.

---

## 🚀 **Quick Start**

### **1. Install AIGuardian SDK**
```bash
# NPM
npm install @aiguardian/sdk

# Yarn
yarn add @aiguardian/sdk

# CDN
<script src="https://cdn.aiguardian.ai/sdk/latest/aiguardian.min.js"></script>
```

### **2. Initialize SDK**
```javascript
import { AIGuardian } from '@aiguardian/sdk';

const aiguardian = new AIGuardian({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.aiguardian.ai', // or http://localhost:8000 for dev
  environment: 'production' // or 'development'
});
```

### **3. Basic Usage**
```javascript
// Process content through guard services
const result = await aiguardian.process({
  serviceType: 'tokenguard',
  payload: {
    content: 'Your content to analyze',
    contentType: 'text',
    scanLevel: 'standard'
  },
  userId: 'user-123',
  sessionId: 'session-456'
});

console.log(result);
```

---

## 🔐 **Authentication Integration**

### **Clerk Authentication Setup**

#### **1. Install Clerk**
```bash
npm install @clerk/nextjs
# or
npm install @clerk/react
```

#### **2. Configure Clerk**
```javascript
// Next.js - app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
    >
      {children}
    </ClerkProvider>
  );
}
```

#### **3. Use Authentication in Components**
```javascript
// React component
import { useUser, useAuth } from '@clerk/nextjs';
import { AIGuardian } from '@aiguardian/sdk';

function GuardComponent() {
  const { user, isLoaded } = useUser();
  const { getToken } = useAuth();
  
  const aiguardian = new AIGuardian({
    apiKey: process.env.NEXT_PUBLIC_AIGUARDIAN_API_KEY,
    baseUrl: process.env.NEXT_PUBLIC_AIGUARDIAN_API_URL,
    getAuthToken: async () => {
      return await getToken();
    }
  });

  const handleProcess = async (content) => {
    if (!user) return;
    
    try {
      const result = await aiguardian.process({
        serviceType: 'tokenguard',
        payload: { content },
        userId: user.id,
        sessionId: user.sessionId
      });
      
      console.log('Processed:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!isLoaded) return <div>Loading...</div>;
  if (!user) return <div>Please sign in</div>;

  return (
    <div>
      <h1>Welcome, {user.firstName}!</h1>
      <button onClick={() => handleProcess('Test content')}>
        Process Content
      </button>
    </div>
  );
}
```

---

## 🛡️ **Guard Service Integration**

### **TokenGuard - Token Optimization**
```javascript
// Optimize content for token usage
const optimizeContent = async (content) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'tokenguard',
      payload: {
        content: content,
        contentType: 'text',
        scanLevel: 'standard',
        context: 'user-generated-content'
      },
      userId: user.id
    });

    return {
      optimizedContent: result.data.optimized_content,
      tokenCount: result.data.optimized_tokens,
      costSavings: result.data.cost_savings,
      confidence: result.data.confidence_score
    };
  } catch (error) {
    console.error('TokenGuard error:', error);
    throw error;
  }
};
```

### **TrustGuard - Trust Validation**
```javascript
// Validate content trustworthiness
const validateTrust = async (content) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'trustguard',
      payload: {
        validationType: 'general',
        content: content,
        validationLevel: 'standard',
        context: 'user-input'
      },
      userId: user.id
    });

    return {
      trustScore: result.data.trust_score,
      reliability: result.data.reliability_indicators,
      riskFactors: result.data.risk_factors,
      confidence: result.data.confidence_level
    };
  } catch (error) {
    console.error('TrustGuard error:', error);
    throw error;
  }
};
```

### **ContextGuard - Context Analysis**
```javascript
// Analyze context drift
const analyzeContext = async (context, conversationHistory) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'contextguard',
      payload: {
        operation: 'set',
        data: {
          context: context,
          conversationHistory: conversationHistory
        },
        consciousnessContext: 'user-session'
      },
      userId: user.id
    });

    return {
      driftDetected: result.data.context_drift_detected,
      memoryUsage: result.data.memory_usage,
      stability: result.data.context_stability,
      recommendations: result.data.recommendations
    };
  } catch (error) {
    console.error('ContextGuard error:', error);
    throw error;
  }
};
```

### **BiasGuard - Bias Detection**
```javascript
// Detect bias in content
const detectBias = async (content) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'biasguard',
      payload: {
        operation: 'detect_bias',
        data: { text: content },
        context: 'user-generated'
      },
      userId: user.id
    });

    return {
      biasDetected: result.data.bias_detected,
      biasScore: result.data.bias_score,
      biasTypes: result.data.bias_types,
      mitigationSuggestions: result.data.mitigation_suggestions
    };
  } catch (error) {
    console.error('BiasGuard error:', error);
    throw error;
  }
};
```

### **SecurityGuard - Security Scanning**
```javascript
// Scan content for security issues
const scanSecurity = async (content) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'securityguard',
      payload: {
        content: content,
        contentType: 'text',
        scanLevel: 'standard',
        context: 'user-input'
      },
      userId: user.id
    });

    return {
      threatsDetected: result.data.threats_detected,
      securityScore: result.data.security_score,
      vulnerabilities: result.data.vulnerabilities,
      recommendations: result.data.recommendations
    };
  } catch (error) {
    console.error('SecurityGuard error:', error);
    throw error;
  }
};
```

---

## 🔄 **Real-time Features**

### **WebSocket Connection**
```javascript
// Real-time monitoring
const connectWebSocket = () => {
  const ws = new WebSocket('wss://api.aiguardian.ai/ws');
  
  ws.onopen = () => {
    console.log('Connected to AIGuardian WebSocket');
  };
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch (data.type) {
      case 'health_update':
        updateServiceHealth(data.service, data.status);
        break;
      case 'request_processed':
        updateRequestStatus(data.requestId, data.result);
        break;
      case 'alert':
        showAlert(data.message, data.level);
        break;
    }
  };
  
  ws.onclose = () => {
    console.log('WebSocket disconnected');
    // Implement reconnection logic
  };
  
  return ws;
};
```

### **Event Streaming**
```javascript
// Server-sent events
const connectEventStream = () => {
  const eventSource = new EventSource('https://api.aiguardian.ai/api/v1/events/stream');
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleRealtimeUpdate(data);
  };
  
  eventSource.onerror = (error) => {
    console.error('Event stream error:', error);
  };
  
  return eventSource;
};
```

---

## 💳 **Payment Integration**

### **Stripe Integration**
```javascript
// Stripe payment setup
import { loadStripe } from '@stripe/stripe-js';

const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

// Create checkout session
const createCheckoutSession = async (planId) => {
  try {
    const response = await fetch('/api/v1/subscriptions/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await getToken()}`
      },
      body: JSON.stringify({
        plan: planId,
        billingPeriod: 'monthly'
      })
    });

    const { sessionId } = await response.json();
    
    const { error } = await stripe.redirectToCheckout({
      sessionId: sessionId
    });

    if (error) {
      console.error('Stripe error:', error);
    }
  } catch (error) {
    console.error('Checkout error:', error);
  }
};
```

### **Subscription Management**
```javascript
// Get subscription status
const getSubscription = async () => {
  try {
    const response = await fetch('/api/v1/subscriptions', {
      headers: {
        'Authorization': `Bearer ${await getToken()}`
      }
    });

    const subscription = await response.json();
    return subscription;
  } catch (error) {
    console.error('Subscription error:', error);
  }
};

// Get usage statistics
const getUsage = async (startDate, endDate) => {
  try {
    const response = await fetch(
      `/api/v1/subscriptions/usage?start_date=${startDate}&end_date=${endDate}`,
      {
        headers: {
          'Authorization': `Bearer ${await getToken()}`
        }
      }
    );

    const usage = await response.json();
    return usage;
  } catch (error) {
    console.error('Usage error:', error);
  }
};
```

---

## 📊 **Monitoring & Analytics**

### **Health Monitoring**
```javascript
// Monitor service health
const monitorHealth = async () => {
  try {
    const response = await fetch('https://api.aiguardian.ai/health/comprehensive');
    const health = await response.json();
    
    return {
      status: health.status,
      services: health.services,
      system: health.system
    };
  } catch (error) {
    console.error('Health check error:', error);
    return { status: 'error', error: error.message };
  }
};

// Get guard services health
const getGuardHealth = async () => {
  try {
    const response = await fetch('https://api.aiguardian.ai/api/v1/guards/health');
    const health = await response.json();
    
    return health;
  } catch (error) {
    console.error('Guard health error:', error);
  }
};
```

### **Usage Analytics**
```javascript
// Track usage metrics
const trackUsage = (serviceType, processingTime, success) => {
  // Send to analytics service
  analytics.track('guard_service_used', {
    serviceType,
    processingTime,
    success,
    userId: user.id,
    timestamp: new Date().toISOString()
  });
};

// Get usage statistics
const getUsageStats = async () => {
  try {
    const response = await fetch('/api/v1/analytics/usage', {
      headers: {
        'Authorization': `Bearer ${await getToken()}`
      }
    });

    const stats = await response.json();
    return stats;
  } catch (error) {
    console.error('Usage stats error:', error);
  }
};
```

---

## 🎨 **UI Components**

### **React Components**
```javascript
// GuardServiceButton component
import React, { useState } from 'react';
import { AIGuardian } from '@aiguardian/sdk';

const GuardServiceButton = ({ serviceType, content, onResult }) => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleProcess = async () => {
    setLoading(true);
    
    try {
      const aiguardian = new AIGuardian({
        apiKey: process.env.NEXT_PUBLIC_AIGUARDIAN_API_KEY,
        baseUrl: process.env.NEXT_PUBLIC_AIGUARDIAN_API_URL
      });

      const response = await aiguardian.process({
        serviceType,
        payload: { content },
        userId: user.id
      });

      setResult(response);
      onResult?.(response);
    } catch (error) {
      console.error('Processing error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="guard-service-button">
      <button 
        onClick={handleProcess} 
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {loading ? 'Processing...' : `Process with ${serviceType}`}
      </button>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3>Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default GuardServiceButton;
```

### **Vue.js Components**
```vue
<!-- GuardServiceComponent.vue -->
<template>
  <div class="guard-service">
    <button 
      @click="processContent" 
      :disabled="loading"
      class="bg-blue-500 text-white px-4 py-2 rounded"
    >
      {{ loading ? 'Processing...' : `Process with ${serviceType}` }}
    </button>
    
    <div v-if="result" class="mt-4 p-4 bg-gray-100 rounded">
      <h3>Result:</h3>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
import { AIGuardian } from '@aiguardian/sdk';

export default {
  name: 'GuardServiceComponent',
  props: {
    serviceType: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      result: null,
      aiguardian: null
    };
  },
  mounted() {
    this.aiguardian = new AIGuardian({
      apiKey: process.env.VUE_APP_AIGUARDIAN_API_KEY,
      baseUrl: process.env.VUE_APP_AIGUARDIAN_API_URL
    });
  },
  methods: {
    async processContent() {
      this.loading = true;
      
      try {
        const response = await this.aiguardian.process({
          serviceType: this.serviceType,
          payload: { content: this.content },
          userId: this.$store.state.user.id
        });

        this.result = response;
        this.$emit('result', response);
      } catch (error) {
        console.error('Processing error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
# .env.local
NEXT_PUBLIC_AIGUARDIAN_API_KEY=your-api-key
NEXT_PUBLIC_AIGUARDIAN_API_URL=https://api.aiguardian.ai
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

### **SDK Configuration**
```javascript
// AIGuardian SDK configuration
const aiguardian = new AIGuardian({
  apiKey: process.env.NEXT_PUBLIC_AIGUARDIAN_API_KEY,
  baseUrl: process.env.NEXT_PUBLIC_AIGUARDIAN_API_URL,
  environment: process.env.NODE_ENV,
  timeout: 30000,
  retries: 3,
  getAuthToken: async () => {
    // Return JWT token for authentication
    return await getToken();
  },
  onError: (error) => {
    // Handle errors globally
    console.error('AIGuardian error:', error);
  },
  onSuccess: (result) => {
    // Handle successful requests
    console.log('AIGuardian success:', result);
  }
});
```

---

## 🧪 **Testing**

### **Unit Tests**
```javascript
// Jest test example
import { AIGuardian } from '@aiguardian/sdk';

describe('AIGuardian SDK', () => {
  let aiguardian;

  beforeEach(() => {
    aiguardian = new AIGuardian({
      apiKey: 'test-api-key',
      baseUrl: 'http://localhost:8000',
      environment: 'test'
    });
  });

  it('should process content with TokenGuard', async () => {
    const result = await aiguardian.process({
      serviceType: 'tokenguard',
      payload: { content: 'Test content' }
    });

    expect(result.success).toBe(true);
    expect(result.serviceType).toBe('tokenguard');
  });
});
```

### **Integration Tests**
```javascript
// Cypress test example
describe('AIGuardian Integration', () => {
  it('should process content and display results', () => {
    cy.visit('/');
    cy.get('[data-testid="content-input"]').type('Test content');
    cy.get('[data-testid="process-button"]').click();
    cy.get('[data-testid="result"]').should('be.visible');
  });
});
```

---

## 🚀 **Deployment**

### **Vercel Deployment**
```bash
# Deploy to Vercel
vercel --prod

# Environment variables
vercel env add NEXT_PUBLIC_AIGUARDIAN_API_KEY
vercel env add NEXT_PUBLIC_AIGUARDIAN_API_URL
vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
```

### **Docker Deployment**
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📱 **Mobile Integration**

### **React Native**
```javascript
// React Native integration
import { AIGuardian } from '@aiguardian/sdk';

const aiguardian = new AIGuardian({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.aiguardian.ai',
  environment: 'production'
});

// Process content in React Native
const processContent = async (content) => {
  try {
    const result = await aiguardian.process({
      serviceType: 'tokenguard',
      payload: { content },
      userId: user.id
    });

    return result;
  } catch (error) {
    console.error('Processing error:', error);
  }
};
```

### **Flutter**
```dart
// Flutter integration
import 'package:aiguardian_sdk/aiguardian_sdk.dart';

class AIGuardianService {
  late AIGuardian _aiguardian;

  AIGuardianService() {
    _aiguardian = AIGuardian(
      apiKey: 'your-api-key',
      baseUrl: 'https://api.aiguardian.ai',
      environment: 'production',
    );
  }

  Future<Map<String, dynamic>> processContent(String content) async {
    try {
      final result = await _aiguardian.process(
        serviceType: 'tokenguard',
        payload: {'content': content},
        userId: user.id,
      );

      return result;
    } catch (error) {
      print('Processing error: $error');
      rethrow;
    }
  }
}
```

---

## 🔒 **Security Best Practices**

### **API Key Management**
```javascript
// Secure API key handling
const getApiKey = () => {
  // Never expose API keys in client-side code
  // Use environment variables or secure storage
  return process.env.NEXT_PUBLIC_AIGUARDIAN_API_KEY;
};

// Use JWT tokens for authentication
const getAuthToken = async () => {
  return await getToken(); // From Clerk or your auth provider
};
```

### **Content Sanitization**
```javascript
// Sanitize user input before processing
const sanitizeContent = (content) => {
  // Remove potentially harmful content
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/javascript:/gi, '')
    .trim();
};

// Process sanitized content
const processContent = async (content) => {
  const sanitized = sanitizeContent(content);
  
  return await aiguardian.process({
    serviceType: 'securityguard',
    payload: { content: sanitized }
  });
};
```

---

## 📈 **Performance Optimization**

### **Caching**
```javascript
// Cache results for better performance
const cache = new Map();

const processWithCache = async (content, serviceType) => {
  const cacheKey = `${serviceType}-${content}`;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  const result = await aiguardian.process({
    serviceType,
    payload: { content }
  });

  cache.set(cacheKey, result);
  return result;
};
```

### **Batch Processing**
```javascript
// Process multiple items in batch
const processBatch = async (items, serviceType) => {
  const promises = items.map(item => 
    aiguardian.process({
      serviceType,
      payload: { content: item.content }
    })
  );

  return await Promise.all(promises);
};
```

---

This frontend integration guide provides comprehensive instructions for integrating AIGuardian with any frontend application. The SDK supports multiple frameworks and provides real-time features, authentication, and payment integration.

**Last Updated**: 2025-10-23  
**Version**: 0.1.0  
**Status**: Production Ready
