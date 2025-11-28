import Link from 'next/link'
import { getProductById, getAllProducts } from '@/lib/shopify-ready'
import { ProductClient } from './ProductClient'

// Required for static export with dynamic routes
export function generateStaticParams() {
  return getAllProducts().map((product) => ({
    id: product.id,
  }))
}

interface ProductPageProps {
  params: {
    id: string
  }
}

export default function ProductPage({ params }: ProductPageProps) {
  const product = getProductById(params.id)

  if (!product) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-amber-50 to-yellow-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-amber-900 mb-4">Product Not Found</h1>
          <Link href="/shop" className="text-amber-600 hover:text-amber-700">
            ← Back to Shop
          </Link>
        </div>
      </main>
    )
  }

  return <ProductClient product={product} />
}
