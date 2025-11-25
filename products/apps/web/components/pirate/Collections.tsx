'use client'

import Link from 'next/link'
import { collections } from '@/lib/shopify-ready'

export function Collections() {
  return (
    <section id="collections" className="py-24 px-4 md:px-8 lg:px-24 bg-gradient-to-b from-amber-50 to-yellow-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-display font-bold text-amber-900 mb-4">
            Our Collections
          </h2>
          <p className="text-xl text-amber-800 max-w-2xl mx-auto">
            Everything you need to look like a proper pirate (or at least not embarrass yourself at Gasparilla)
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {collections.map((collection) => (
            <Link
              key={collection.id}
              href={`/collections/${collection.handle}`}
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl overflow-hidden transform hover:scale-105 transition-all duration-300 border-2 border-amber-200 hover:border-amber-400"
            >
              {/* Collection Image Placeholder */}
              <div className="h-64 bg-gradient-to-br from-amber-400 to-yellow-600 flex items-center justify-center text-6xl">
                {collection.handle === 'gasparilla-essentials' ? '‍' : ''}
              </div>
              
              <div className="p-6">
                <h3 className="text-2xl font-display font-bold text-amber-900 mb-2 group-hover:text-amber-700">
                  {collection.title}
                </h3>
                <p className="text-amber-700 mb-4">
                  {collection.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-amber-600">
                    {collection.products.length} {collection.products.length === 1 ? 'item' : 'items'}
                  </span>
                  <span className="text-amber-900 font-bold group-hover:translate-x-2 transition-transform">
                    Shop Now →
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Featured Products Preview */}
        <div className="mt-16">
          <h3 className="text-3xl font-display font-bold text-amber-900 mb-8 text-center">
            Popular Right Now
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {collections[0].products.slice(0, 3).map((product) => (
              <Link
                key={product.id}
                href={`/products/${product.id}`}
                className="bg-white rounded-xl shadow-md hover:shadow-xl overflow-hidden transform hover:scale-105 transition-all duration-300 border border-amber-200"
              >
                <div className="h-48 bg-gradient-to-br from-amber-300 to-yellow-500 flex items-center justify-center text-5xl">
                  {product.tags.includes('flip-flops') ? '' : ''}
                </div>
                <div className="p-4">
                  <h4 className="font-bold text-amber-900 mb-1">{product.title}</h4>
                  <p className="text-sm text-amber-700 mb-2 line-clamp-2">{product.description}</p>
                  <div className="flex items-center justify-between">
                    {product.compareAtPrice && (
                      <span className="text-sm text-gray-500 line-through">
                        ${product.compareAtPrice}
                      </span>
                    )}
                    <span className="text-lg font-bold text-amber-900">
                      ${product.price}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

