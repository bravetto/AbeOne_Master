import Link from 'next/link'
import { getCollectionByHandle, collections } from '@/lib/shopify-ready'
import { CollectionClient } from './CollectionClient'

// Required for static export with dynamic routes
export function generateStaticParams() {
  return collections.map((collection) => ({
    handle: collection.handle,
  }))
}

interface CollectionPageProps {
  params: {
    handle: string
  }
}

export default function CollectionPage({ params }: CollectionPageProps) {
  const collection = getCollectionByHandle(params.handle)
  
  if (!collection) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-amber-50 to-yellow-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-amber-900 mb-4">Collection Not Found</h1>
          <Link href="/shop" className="text-amber-600 hover:text-amber-700">
            ← Back to Shop
          </Link>
        </div>
      </main>
    )
  }

  return <CollectionClient collection={collection} />
}

