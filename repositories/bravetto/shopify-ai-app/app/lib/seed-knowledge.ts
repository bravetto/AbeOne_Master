/**
 * Utility to seed Shopify store data to Bravetto AI knowledge base
 * 
 * MULTI-INDEX ARCHITECTURE: Uses separate Shopify Pinecone index for optimal performance
 * and data isolation from organization data.
 * 
 * READ-ONLY OPERATIONS: This utility only reads store data.
 * No modifications are made to your Shopify store content.
 */

import type { BravettoConfig } from "./bravetto-client";

export interface SeedKnowledgeConfig {
  shopDomain: string;
  accessToken: string;
  resourceTypes?: Array<'products' | 'collections' | 'pages' | 'blogs' | 'articles' | 'policies'>;
  includeWebCrawl?: boolean;
  webCrawlUrl?: string;
  maxPages?: number;
  chunkSize?: number;
  chunkOverlap?: number;
  namespace?: string;
}

export interface SeedKnowledgeResult {
  success: boolean;
  message?: string;
  documentsProcessed?: number;
  error?: string;
  summary?: {
    sources: Record<string, number>;
    types: Record<string, number>;
  };
}

export class KnowledgeSeeder {
  private apiUrl: string;
  private apiKey?: string;

  constructor(config: BravettoConfig) {
    this.apiUrl = config.apiUrl;
    this.apiKey = config.apiKey;
  }

  /**
   * Seed Shopify store data to the knowledge base (READ-ONLY operation)
   * Uses the fully implemented crawler pipeline in the main Bravetto AI app.
   * 
   * SECURITY: Only reads Shopify data - never modifies store content.
   */
  async seedShopifyData(config: SeedKnowledgeConfig): Promise<SeedKnowledgeResult> {
    try {
      // Build sources array
      const sources = [
        {
          type: 'shopify'
        }
      ];

      // Add web source if requested
      if (config.includeWebCrawl && config.webCrawlUrl) {
        sources.push({
          type: 'web'
        });
      }

      // Build request body
      const requestBody = {
        // Top-level auth fields required by API
        shopDomain: config.shopDomain,
        accessToken: config.accessToken,
        
        // Top-level configuration fields expected by API
        resourceTypes: config.resourceTypes || ['products', 'collections', 'pages'],
        includeWebCrawl: !!config.webCrawlUrl,
        webCrawlUrl: config.webCrawlUrl,
        maxPages: config.maxPages || 10,
        chunkSize: config.chunkSize || 1000,
        chunkOverlap: config.chunkOverlap || 200,
        namespace: config.namespace || config.shopDomain.replace('.myshopify.com', ''),
        
        // Keep nested structure for pipeline compatibility
        sources,
        crawlConfig: {
          // Shopify specific
          shopDomain: config.shopDomain,
          accessToken: config.accessToken,
          resourceTypes: config.resourceTypes || ['products', 'collections', 'pages'],
          
          // Web crawl specific
          startUrl: config.webCrawlUrl,
          maxPages: config.maxPages || 10,
          maxDepth: 2
        },
        processingConfig: {
          splittingMethod: 'recursive',
          chunkSize: config.chunkSize || 1000,
          chunkOverlap: config.chunkOverlap || 200
        },
        seedConfig: {
          indexName: process.env.PINECONE_SHOPIFY_INDEX || 'shopify-knowledge',
          namespace: config.namespace || config.shopDomain.replace('.myshopify.com', ''),
          batchSize: 10
        }
      };

      // Make API request to Shopify-specific endpoint with session token auth
      const response = await fetch(`${this.apiUrl}/api/shopify/seed-knowledge`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Bravetto-Shopify-Integration/1.0',
          'X-Shopify-Shop-Domain': config.shopDomain,
          ...(this.apiKey && { 'X-API-Key': this.apiKey })
        },
        body: JSON.stringify(requestBody)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return {
        success: data.success,
        message: data.message,
        documentsProcessed: data.result?.documentsProcessed,
        summary: data.result?.summary
      };
    } catch (error) {
      console.error('Failed to seed knowledge:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  /**
   * Check seeding progress (if implemented with webhooks/polling)
   */
  async checkProgress(jobId: string): Promise<any> {
    // TODO: Implement progress checking if needed
    // This would require the API to return a job ID and support status checking
    throw new Error('Progress checking not yet implemented');
  }
}

// Example usage:
/*
const seeder = new KnowledgeSeeder({
  apiUrl: process.env.BRAVETTO_API_URL || 'https://www.bravetto.ai',
  apiKey: process.env.BRAVETTO_API_KEY
});

const result = await seeder.seedShopifyData({
  shopDomain: 'myshop.myshopify.com',
  accessToken: 'shpat_xxx',
  resourceTypes: ['products', 'collections'],
  includeWebCrawl: true,
  webCrawlUrl: 'https://myshop.com',
  namespace: 'myshop'
});

console.log(result);
*/ 