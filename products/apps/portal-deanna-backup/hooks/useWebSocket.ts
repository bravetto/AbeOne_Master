'use client'

export function useWebSocket(url: string, options?: any) {
  return {
    isConnected: false,
    send: () => {},
    close: () => {}
  }
}
