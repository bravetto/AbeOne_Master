/**
 * AbëONE API Configuration Atom
 * 
 * Configuration for API endpoints and settings.
 * 
 * Pattern: CONFIG × API × ATOM × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
 * Guardians: AEYON (999 Hz) + ZERO (530 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

/**
 * API Configuration
 */
export interface ApiConfig {
  /** Base URL for API endpoints */
  baseUrl: string;
  /** API timeout in milliseconds */
  timeout: number;
  /** Default headers */
  headers: Record<string, string>;
}

/**
 * Default API configuration
 */
export const defaultApiConfig: ApiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
};

/**
 * Get API configuration (allows override)
 */
export function getApiConfig(overrides?: Partial<ApiConfig>): ApiConfig {
  return {
    ...defaultApiConfig,
    ...overrides,
    headers: {
      ...defaultApiConfig.headers,
      ...overrides?.headers,
    },
  };
}

