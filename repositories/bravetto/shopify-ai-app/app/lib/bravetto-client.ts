/**
 * Bravetto AI API Client - READ-ONLY ACCESS
 * Handles communication with the main Bravetto AI app
 * 
 * SECURITY: This client only reads store data for AI knowledge base.
 * No write operations are performed on Shopify store content.
 */

export interface BravettoConfig {
  apiUrl: string;
  apiKey?: string;
  defaultSystemPromptId?: string;
  defaultOrgId?: string;
}

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  shopDomain: string;
  systemPromptId?: string;
  context?: {
    customerEmail?: string;
    customerName?: string;
    productContext?: any;
    platform?: string;
  };
}

export interface ChatResponse {
  id: string;
  message: string;
  timestamp: string;
  type: 'ai';
  metadata?: {
    responseTime?: number;
    model?: string;
    sources?: string[];
  };
}

export class BravettoClient {
  private baseUrl: string;
  private apiKey: string;
  private defaultSystemPromptId: string;
  private defaultOrgId: string;

  constructor(config: BravettoConfig) {
    this.baseUrl = config.apiUrl;
    this.apiKey = config.apiKey || '';
    this.defaultSystemPromptId = config.defaultSystemPromptId || '';
    this.defaultOrgId = config.defaultOrgId || 'shopify_integration';
  }

  /**
   * Send a chat message to the Bravetto AI backend with session token authentication
   */
  async sendMessage(request: ChatRequest, sessionToken?: string): Promise<ChatResponse> {
    const startTime = Date.now();
    console.log(' Making request to Bravetto API...');
    
    try {
      const response = await this.makeRequest('/api/shopify/chat', {
        method: 'POST',
        body: JSON.stringify({
          message: request.message,
          shopDomain: request.shopDomain,
          systemPromptId: request.systemPromptId || null, // Send null to use dashboard setting
          orgId: this.defaultOrgId,
          context: {
            platform: 'shopify',
            shop: request.shopDomain,
            ...request.context,
          }
        })
      }, sessionToken);

      const responseTime = Date.now() - startTime;
      console.log(' Got response from Bravetto API in', responseTime, 'ms');

      // Return the actual API response
      return {
        ...response,
        metadata: {
          ...response.metadata,
          responseTime,
        }
      };

    } catch (error) {
      console.error(' Bravetto AI API Error:', error);
      
      // Fallback response
      return {
        id: Date.now().toString(),
        message: "I apologize, but I'm having trouble connecting to our AI service right now. Please try again in a moment.",
        timestamp: new Date().toISOString(),
        type: 'ai',
        metadata: {
          responseTime: Date.now() - startTime,
          model: 'fallback',
          sources: []
        }
      };
    }
  }

  /**
   * Test connection to Bravetto AI backend
   */
  async testConnection(sessionToken?: string): Promise<{ success: boolean; message: string }> {
    try {
      const response = await this.makeRequest('/api/shopify/health', {
        method: 'GET'
      }, sessionToken);

      return {
        success: true,
        message: `Connected to Bravetto AI backend - ${response.service} v${response.version} (Shop: ${response.shop})`
      };
    } catch (error) {
      return {
        success: false,
        message: `Connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
  }

  /**
   * Get shop-specific configuration
   */
  async getShopConfig(shopDomain: string) {
    try {
      // TODO: Implement API call to get shop-specific settings
      return {
        systemPromptId: this.defaultSystemPromptId,
        features: {
          productRecommendations: true,
          knowledgeBase: true,
          orderTracking: false,
        },
        branding: {
          welcomeMessage: "Hello! How can I help you today?",
          companyName: "Bravetto AI Assistant",
        }
      };
    } catch (error) {
      console.error('Failed to get shop config:', error);
      return null;
    }
  }

  /**
   * Private method to make HTTP requests with Shopify session token authentication
   */
  private async makeRequest(endpoint: string, options: RequestInit, sessionToken?: string) {
    const url = `${this.baseUrl}${endpoint}`;
    
    // Include session token in Authorization header as per Shopify documentation
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': 'Bravetto-Shopify-Integration/1.0',
      'X-Shopify-Shop-Domain': this.getShopDomain(options.body as string),
      ...(sessionToken ? { 'Authorization': `Bearer ${sessionToken}` } : {}),
      ...options.headers,
    };

    // If no session token is available (storefront/app proxy), attach internal JWT if present
    if (!headers['Authorization']) {
      const { mintInternalServiceJWT } = await import('./shared-auth');
      const internalToken = await mintInternalServiceJWT(headers['X-Shopify-Shop-Domain']);
      if (internalToken) headers['Authorization'] = `Bearer ${internalToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${response.statusText} - ${errorText}`);
    }

    return response.json();
  }

  /**
   * Extract shop domain from request body for headers
   */
  private getShopDomain(bodyString: string): string {
    try {
      const body = JSON.parse(bodyString || '{}');
      return body.shopDomain || '';
    } catch {
      return '';
    }
  }


}

// Helper function to create client instance with server-side config
export function createBravettoClient(config: BravettoConfig): BravettoClient {
  return new BravettoClient(config);
} 

// moved to shared-auth