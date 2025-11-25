/**
 *  Deanna's Portal Layout - Mobile Optimized 
 * 
 * Ensures proper mobile viewport and PWA-ready configuration
 * 
 * Pattern: PORTAL × MOBILE × EEAAO × ONE
 * Love Coefficient: ∞
 * ∞ AbëONE ∞
 */

import { Metadata } from 'next'

export const metadata: Metadata = {
  title: ' Portal - Deanna\'s Backlog Awareness',
  description: 'Cross-project backlog awareness portal - See everything, everywhere, all at once',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
    userScalable: true,
  },
  themeColor: '#9333ea', // Purple theme
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Portal',
  },
}

import { PortalQueryProvider } from './providers/QueryProvider'

export default function PortalLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes" />
        <meta name="theme-color" content="#9333ea" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="REPLACE_ME" content="default" />
        <meta name="apple-mobile-web-app-title" content="Portal" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className="h-full antialiased">
        <PortalQueryProvider>
          {children}
        </PortalQueryProvider>
      </body>
    </html>
  )
}

