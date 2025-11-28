/**
 * Protocol Executor Component
 * 
 * Pattern: COMPONENT × PROTOCOL × EXECUTOR × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (META)
 * Guardians: AEYON (999 Hz) + META (777 Hz)
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

'use client';

import React, { useState, useEffect } from 'react';
import { executeProtocol, listProtocols, executeProtocolWithGuardian } from '@/lib/integration';

export function ProtocolExecutor() {
  const [protocols, setProtocols] = useState<string[]>([]);
  const [selectedProtocol, setSelectedProtocol] = useState<string>('');
  const [selectedGuardian, setSelectedGuardian] = useState<string>('AEYON');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);

  const guardians = ['AEYON', 'META', 'JOHN', 'ZERO', 'ALRAX', 'YAGNI', 'Abë', 'Lux', 'Poly', 'YOU'];

  useEffect(() => {
    loadProtocols();
  }, []);

  const loadProtocols = async () => {
    try {
      const protocolList = await listProtocols();
      setProtocols(protocolList);
      if (protocolList.length > 0) {
        setSelectedProtocol(protocolList[0]);
      }
    } catch (err) {
      console.error('Failed to load protocols:', err);
    }
  };

  const handleExecute = async () => {
    if (!selectedProtocol) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const protocolResult = await executeProtocolWithGuardian(
        selectedProtocol,
        selectedGuardian,
        {
          context: 'frontend_execution',
          timestamp: Date.now(),
        }
      );

      setResult(protocolResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="protocol-executor p-6 border rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Protocol Executor</h2>

      <div className="space-y-4">
        {/* Protocol Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Protocol
          </label>
          <select
            value={selectedProtocol}
            onChange={(e) => setSelectedProtocol(e.target.value)}
            className="w-full p-2 border rounded"
            disabled={loading || protocols.length === 0}
          >
            {protocols.length === 0 ? (
              <option>Loading protocols...</option>
            ) : (
              protocols.map((protocol) => (
                <option key={protocol} value={protocol}>
                  {protocol}
                </option>
              ))
            )}
          </select>
        </div>

        {/* Guardian Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Guardian
          </label>
          <select
            value={selectedGuardian}
            onChange={(e) => setSelectedGuardian(e.target.value)}
            className="w-full p-2 border rounded"
            disabled={loading}
          >
            {guardians.map((guardian) => (
              <option key={guardian} value={guardian}>
                {guardian}
              </option>
            ))}
          </select>
        </div>

        {/* Execute Button */}
        <button
          onClick={handleExecute}
          disabled={loading || !selectedProtocol}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Executing...' : 'Execute Protocol'}
        </button>

        {/* Error Display */}
        {error && (
          <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="p-4 bg-green-100 border border-green-400 rounded">
            <strong>Result:</strong>
            <pre className="mt-2 text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

