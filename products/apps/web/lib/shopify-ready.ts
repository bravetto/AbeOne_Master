// Shopify-ready data structure
// When ready to connect Shopify, just swap this with API calls

export interface Product {
  id: string
  title: string
  description: string
  price: number
  compareAtPrice?: number
  images: string[]
  variants: ProductVariant[]
  tags: string[]
  collection: string
  inStock: boolean
}

export interface ProductVariant {
  id: string
  title: string
  price: number
  available: boolean
  option1?: string // Size, Color, etc.
  option2?: string
}

export interface Collection {
  id: string
  title: string
  description: string
  handle: string
  image?: string
  products: Product[]
}

// Mock data - replace with Shopify API when ready
export const collections: Collection[] = [
  {
    id: 'gasparilla-essentials',
    title: 'Gasparilla Essentials',
    description: 'Everything you need to not look like a landlubber at Gasparilla',
    handle: 'gasparilla-essentials',
    products: [
      {
        id: 'pirate-tshirt-1',
        title: 'Arrr You Ready? T-Shirt',
        description: 'The perfect shirt for when you\'re ready to plunder... or at least look like you are. Made for Tampa Bay pirates who know Gasparilla is serious business.',
        price: 29.99,
        compareAtPrice: 39.99,
        images: ['/products/pirate-tshirt-1.jpg'],
        variants: [
          { id: 'v1', title: 'Small', price: 29.99, available: true, option1: 'S' },
          { id: 'v2', title: 'Medium', price: 29.99, available: true, option1: 'M' },
          { id: 'v3', title: 'Large', price: 29.99, available: true, option1: 'L' },
          { id: 'v4', title: 'XL', price: 29.99, available: true, option1: 'XL' },
        ],
        tags: ['t-shirt', 'gasparilla', 'pirate'],
        collection: 'gasparilla-essentials',
        inStock: true,
      },
      {
        id: 'flipflop-multi',
        title: 'Multi-Use Flip-Flops',
        description: 'These aren\'t just flip-flops. They\'re flip-flops that can handle sand, water, rum spills, and questionable life choices. Perfect for Gasparilla, the beach, or when you need to make a quick escape.',
        price: 24.99,
        compareAtPrice: 34.99,
        images: ['/products/flipflop-multi.jpg'],
        variants: [
          { id: 'v5', title: 'Size 8', price: 24.99, available: true, option1: '8' },
          { id: 'v6', title: 'Size 9', price: 24.99, available: true, option1: '9' },
          { id: 'v7', title: 'Size 10', price: 24.99, available: true, option1: '10' },
          { id: 'v8', title: 'Size 11', price: 24.99, available: true, option1: '11' },
        ],
        tags: ['flip-flops', 'multi-use', 'gasparilla', 'beach'],
        collection: 'gasparilla-essentials',
        inStock: true,
      },
    ],
  },
  {
    id: 'comedy-merch',
    title: 'Comedy Show Merch',
    description: 'Wear our gear to the show, get a free drink. (Just kidding, but we\'ll think you\'re cool)',
    handle: 'comedy-merch',
    products: [
      {
        id: 'comedy-tshirt-1',
        title: 'Two Drink Minimum T-Shirt',
        description: 'Because we need to pay rent. Also, it\'s funny. Wear this to our show and we\'ll definitely notice you.',
        price: 27.99,
        images: ['/products/comedy-tshirt-1.jpg'],
        variants: [
          { id: 'v9', title: 'Small', price: 27.99, available: true, option1: 'S' },
          { id: 'v10', title: 'Medium', price: 27.99, available: true, option1: 'M' },
          { id: 'v11', title: 'Large', price: 27.99, available: true, option1: 'L' },
        ],
        tags: ['t-shirt', 'comedy', 'stand-up'],
        collection: 'comedy-merch',
        inStock: true,
      },
    ],
  },
]

// Helper function to get collection by handle
export function getCollectionByHandle(handle: string): Collection | undefined {
  return collections.find(c => c.handle === handle)
}

// Helper function to get all products
export function getAllProducts(): Product[] {
  return collections.flatMap(c => c.products)
}

// Helper function to get product by ID
export function getProductById(id: string): Product | undefined {
  return getAllProducts().find(p => p.id === id)
}

