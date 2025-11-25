'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Product } from '@/lib/shopify-ready'

interface ProductClientProps {
  product: Product
}

export function ProductClient({ product }: ProductClientProps) {
  const [selectedVariant, setSelectedVariant] = useState(product.variants[0])
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    setSelectedVariant(product.variants[0])
  }, [product])

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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {/* Product Image */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="h-96 bg-gradient-to-br from-amber-300 to-yellow-500 flex items-center justify-center text-8xl">
              {product.tags.includes('flip-flops') ? '👟' : '👕'}
            </div>
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-4xl md:text-5xl font-display font-bold text-amber-900 mb-4">
              {product.title}
            </h1>
            <p className="text-xl text-amber-800 mb-6">
              {product.description}
            </p>

            {/* Price */}
            <div className="mb-6">
              {product.compareAtPrice && (
                <span className="text-2xl text-gray-500 line-through mr-3">
                  ${product.compareAtPrice}
                </span>
              )}
              <span className="text-4xl font-bold text-amber-900">
                ${selectedVariant?.price || product.price}
              </span>
            </div>

            {/* Variants */}
            {product.variants.length > 1 && (
              <div className="mb-6">
                <label className="block text-amber-900 font-bold mb-2">
                  Select Variant:
                </label>
                <select
                  value={selectedVariant?.id}
                  onChange={(e) => {
                    const variant = product.variants.find(v => v.id === e.target.value)
                    if (variant) setSelectedVariant(variant)
                  }}
                  className="w-full p-3 border-2 border-amber-200 rounded-lg focus:border-amber-400 focus:outline-none"
                >
                  {product.variants.map((variant) => (
                    <option key={variant.id} value={variant.id}>
                      {variant.title} - ${variant.price}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Quantity */}
            <div className="mb-6">
              <label className="block text-amber-900 font-bold mb-2">
                Quantity:
              </label>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-4 py-2 bg-amber-200 hover:bg-amber-300 rounded-lg font-bold"
                >
                  -
                </button>
                <span className="text-xl font-bold text-amber-900 w-12 text-center">
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="px-4 py-2 bg-amber-200 hover:bg-amber-300 rounded-lg font-bold"
                >
                  +
                </button>
              </div>
            </div>

            {/* Add to Cart Button */}
            <button
              className="w-full bg-amber-600 hover:bg-amber-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
            >
              Add to Cart
            </button>

            {/* Stock Status */}
            {selectedVariant && !selectedVariant.available && (
              <p className="mt-4 text-red-600 font-bold">
                This variant is currently out of stock
              </p>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}

