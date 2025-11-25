/**
 * Configuration management for Bravetto AI Shopify App
 * 
 * READ-ONLY ACCESS: This app only reads Shopify store data
 */

export const config = {
  // Bravetto AI Backend Integration
  bravetto: {
    apiUrl: process.env.BRAVETTO_API_URL || 'https://www.bravetto.ai',
    apiKey: process.env.BRAVETTO_API_KEY || '',
    defaultSystemPromptId: process.env.DEFAULT_SYSTEM_PROMPT_ID || '',
    defaultOrgId: process.env.DEFAULT_ORG_ID || 'shopify_integration',
  },

  // Shopify App Authentication (from Partner Dashboard)
  shopify: {
    apiKey: process.env.SHOPIFY_API_KEY || '',
    apiSecret: process.env.SHOPIFY_API_SECRET || '',
    webhookSecret: process.env.SHOPIFY_WEBHOOK_SECRET || '',
    scopes: process.env.SHOPIFY_SCOPES || 'read_products,read_content', // READ-ONLY access
    appUrl: process.env.SHOPIFY_APP_URL || '',
  },

  // Chat Configuration
  chat: {
    maxMessagesPerConversation: 100,
    responseTimeoutMs: 30000,
    enableStreaming: true,
  },

  // Analytics
  analytics: {
    enabled: process.env.ENABLE_ANALYTICS === 'true',
    trackUserMessages: true,
    trackResponseTimes: true,
  },

  // Development
  dev: {
    logLevel: process.env.LOG_LEVEL || 'info',
    enableDebugLogs: process.env.NODE_ENV === 'development',
  }
};

export const validateConfig = () => {
  const errors: string[] = [];

  if (!config.bravetto.apiUrl) {
    errors.push('BRAVETTO_API_URL is required');
  }

  if (!config.shopify.apiKey) {
    errors.push('SHOPIFY_API_KEY is required');
  }

  if (!config.shopify.apiSecret) {
    errors.push('SHOPIFY_API_SECRET is required');
  }

  if (!config.shopify.webhookSecret && process.env.NODE_ENV === 'production') {
    errors.push('SHOPIFY_WEBHOOK_SECRET is required for production');
  }

  if (errors.length > 0) {
    throw new Error(`Configuration errors: ${errors.join(', ')}`);
  }

  return true;
}; 