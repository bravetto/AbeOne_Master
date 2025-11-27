/**
 * AbëONE Root Layout
 * 
 * BëHUMAN. MakeTHiNGs. Bë Bold.
 * Powered by Bravëtto.
 */

import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AbëONE | The Interface of the Future',
  description: 'The single point of contact between Biological Intelligence and Digital Intelligence. Powered by Bravëtto.',
  keywords: ['AI', 'Voice Interface', 'Neuromorphic', 'Design System', 'Bravëtto'],
  authors: [{ name: 'Bravëtto' }],
  openGraph: {
    title: 'AbëONE | The Interface of the Future',
    description: 'BëHUMAN. MakeTHiNGs. Bë Bold.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[var(--abe-background)]">
        {children}
      </body>
    </html>
  );
}
