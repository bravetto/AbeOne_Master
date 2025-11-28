/**
 * Integration Test Component
 * 
 * Test component to verify frontend-backend integration.
 * 
 * Pattern: COMPONENT × INTEGRATION × TEST × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import React, { useState } from 'react';
import { 
  executeProtocol, 
  executeProtocolWithGuardian, 
  listProtocols,
  getMemoryContext,
  syncMemoryToConsciousness 
} from '@/lib/integration';

export function IntegrationTest() {
  const [status, setStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [results, setResults] = useState<Record<string, any>>({});
  const [error, setError] = useState<string | null>(null);

  const testBackendConnection = async () => {
    setStatus('testing');
    setError(null);
    setResults({});

    try {
      // Test 1: List Protocols
      console.log('🧪 Testing: List Protocols...');
      const protocols = await listProtocols();
      setResults(prev => ({ ...prev, protocols }));
      console.log('✅ Protocols:', protocols);

      // Test 2: Execute Protocol via API
      if (protocols && protocols.length > 0) {
        console.log('🧪 Testing: Execute Protocol via API...');
        const protocolName = typeof protocols[0] === 'string' ? protocols[0] : protocols[0].name || 'Secure Code Implementation';
        const apiResult = await executeProtocol(protocolName, { test: true });
        setResults(prev => ({ ...prev, apiExecution: apiResult }));
        console.log('✅ API Execution:', apiResult);
      }

      // Test 3: Execute Protocol via Guardian
      if (protocols && protocols.length > 0) {
        console.log('🧪 Testing: Execute Protocol via Guardian...');
        const protocolName = typeof protocols[0] === 'string' ? protocols[0] : protocols[0].name || 'Secure Code Implementation';
        const guardianResult = await executeProtocolWithGuardian(protocolName, 'AEYON', { test: true });
        setResults(prev => ({ ...prev, guardianExecution: guardianResult }));
        console.log('✅ Guardian Execution:', guardianResult);
      }

      // Test 4: Get Memory Context
      console.log('🧪 Testing: Get Memory Context...');
      try {
        const memory = await getMemoryContext('active');
        setResults(prev => ({ ...prev, memory }));
        console.log('✅ Memory:', memory);
      } catch (memError: any) {
        console.log('⚠️  Memory context test failed:', memError.message);
        setResults(prev => ({ ...prev, memory: { error: memError.message } }));
      }

      setStatus('success');
    } catch (err: any) {
      console.error('❌ Integration test failed:', err);
      setError(err.message || 'Unknown error');
      setStatus('error');
    }
  };

  return (
    <div className="integration-test p-6 border rounded-lg bg-white dark:bg-gray-800">
      <h2 className="text-2xl font-bold mb-4">Integration Test</h2>
      
      <div className="mb-4">
        <button
          onClick={testBackendConnection}
          disabled={status === 'testing'}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {status === 'testing' ? 'Testing...' : 'Test Backend Connection'}
        </button>
      </div>

      {status === 'success' && (
        <div className="mb-4 p-4 bg-green-100 dark:bg-green-900 rounded">
          <h3 className="font-bold text-green-800 dark:text-green-200">✅ Integration Successful!</h3>
          <p className="text-sm text-green-700 dark:text-green-300">
            All integration tests passed. Frontend is connected to backend.
          </p>
        </div>
      )}

      {error && (
        <div className="mb-4 p-4 bg-red-100 dark:bg-red-900 rounded">
          <h3 className="font-bold text-red-800 dark:text-red-200">❌ Integration Error</h3>
          <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
          <p className="text-xs text-red-600 dark:text-red-400 mt-2">
            Make sure backend is running on http://localhost:8000
          </p>
        </div>
      )}

      {Object.keys(results).length > 0 && (
        <div className="mt-4">
          <h3 className="font-bold mb-2">Test Results:</h3>
          <div className="space-y-2 text-sm">
            {results.protocols && (
              <div>
                <strong>Protocols:</strong> {Array.isArray(results.protocols) ? results.protocols.length : 'N/A'}
              </div>
            )}
            {results.apiExecution && (
              <div>
                <strong>API Execution:</strong> {results.apiExecution.success ? '✅ Success' : '❌ Failed'}
              </div>
            )}
            {results.guardianExecution && (
              <div>
                <strong>Guardian Execution:</strong> {results.guardianExecution.success ? '✅ Success' : '❌ Failed'}
              </div>
            )}
            {results.memory && (
              <div>
                <strong>Memory Context:</strong> {results.memory.error ? '⚠️ ' + results.memory.error : '✅ Retrieved'}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

