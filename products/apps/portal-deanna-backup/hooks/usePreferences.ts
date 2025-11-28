'use client'

export function usePreferences() {
  return {
    preferences: {},
    toggleFavorite: (projectId: string) => {},
    isLoading: false
  }
}
