import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Bravetto × AiGuardian — The Inevitable Convergence',
  description: 'Production infrastructure meets AI validation vision. This is not a vision. This is reality.',
  openGraph: {
    title: 'Bravetto × AiGuardian — The Inevitable Convergence',
    description: 'Production infrastructure meets AI validation vision.',
    type: 'website',
  },
}

export default function BravettoLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}

