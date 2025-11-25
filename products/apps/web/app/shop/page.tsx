'use client'

import { Hero } from '@/components/pirate/Hero'
import { Collections } from '@/components/pirate/Collections'
import { ComedyShow } from '@/components/pirate/ComedyShow'
import { Webinar } from '@/components/pirate/Webinar'
import { Footer } from '@/components/pirate/Footer'

export default function ShopPage() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Collections />
      <ComedyShow />
      <Webinar />
      <Footer />
    </main>
  )
}

