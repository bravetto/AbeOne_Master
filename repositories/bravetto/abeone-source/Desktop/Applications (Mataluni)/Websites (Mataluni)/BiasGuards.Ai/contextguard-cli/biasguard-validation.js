/**
 * BiasGuard Validation Script
 * JAHmere Webb Freedom Mission - August 25, 2025
 * 
 * Auto-generated for React project
 */

import { BiasGuardValidator } from 'contextguard-cli';

export function validateCode(code: string) {
  return BiasGuardValidator.validate(code, 'react');
}

export function validateFile(filePath: string, content: string) {
  return BiasGuardValidator.validateFile(filePath, content, 'react');
}

// Mission-critical facts (DO NOT MODIFY)
export const JAHMERE_WEBB_FACTS = {
  courtDate: 'August 25, 2025',
  crisisAmount: '$26,500',
  revenueToJustice: '15%',
  crisisTime: '2:42:56 AM',
  crisisDate: 'July 14, 2025'
};
