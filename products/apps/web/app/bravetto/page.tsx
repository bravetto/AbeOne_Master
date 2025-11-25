'use client'

import { Hero } from '@/components/bravetto/Hero'
import { Features } from '@/components/bravetto/Features'
import { Convergence } from '@/components/bravetto/Convergence'
import { Stats } from '@/components/bravetto/Stats'
import { CTA } from '@/components/bravetto/CTA'
import { Footer } from '@/components/bravetto/Footer'

export default function BravettoPage() {
  return (
    <main className="min-h-screen gradient-healing">
      <Hero />
      <Stats />
      <Features />
      <Convergence />
      <CTA />
      <Footer />
    </main>
  )
}

