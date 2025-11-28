'use client'

import Link from 'next/link'
import { Collection } from '@/lib/shopify-ready'

interface CollectionClientProps {
  collection: Collection
}

export function CollectionClient({ collection }: CollectionClientProps) {
  return (
    <main className="min-h-screen bg-gradient-to-b from-amber-50 to-yellow-50">
      {/* Header */}
      <header className="bg-white border-b-2 border-amber-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 md:px-8 lg:px-24 py-4">
          <Link href="/shop" className="text-amber-900 hover:text-amber-700 font-bold">
            ← Back to Shop
          </Link>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 md:px-8 lg:px-24 py-12">
        <div className="mb-12">
          <h1 className="text-4xl md:text-6xl font-display font-bold text-amber-900 mb-4">
            {collection.title}
          </h1>
          <p className="text-xl text-amber-800 max-w-3xl">
            {collection.description}
          </p>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {collection.products.map((product) => (
            <Link
              key={product.id}
              href={`/products/${product.id}`}
              className="bg-white rounded-xl shadow-md hover:shadow-xl overflow-hidden transform hover:scale-105 transition-all duration-300 border border-amber-200 group"
            >
              {/* Product Image Placeholder */}
              <div className="h-64 bg-gradient-to-br from-amber-300 to-yellow-500 flex items-center justify-center text-6xl">
                {product.tags.includes('flip-flops') ? '👟' : '👕'}
              </div>
              
              <div className="p-6">
                <h2 className="text-xl font-bold text-amber-900 mb-2 group-hover:text-amber-700">
                  {product.title}
                </h2>
                <p className="text-amber-700 mb-4 line-clamp-3">
                  {product.description}
                </p>
                <div className="flex items-center justify-between">
                  <div>
                    {product.compareAtPrice && (
                      <span className="text-sm text-gray-500 line-through mr-2">
                        ${product.compareAtPrice}
                      </span>
                    )}
                    <span className="text-2xl font-bold text-amber-900">
                      ${product.price}
                    </span>
                  </div>
                  <span className="text-amber-600 group-hover:translate-x-1 transition-transform">
                    View →
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  )
}

