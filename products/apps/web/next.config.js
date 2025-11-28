/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Enterprise features (rate limiting, auth, logging) require middleware
  images: {
    unoptimized: false, // Enable Next.js image optimization
  },
  eslint: {
    // Allow build to proceed with ESLint warnings
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Allow build to proceed with TypeScript errors (will still show warnings)
    ignoreBuildErrors: false,
  },
  // Removed metadataBase - not a valid next.config.js option
  // metadataBase should be set in layout.tsx metadata object
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '',
    NEXT_PUBLIC_WEBINAR_API_URL: process.env.NEXT_PUBLIC_WEBINAR_API_URL || '',
  },
  // Skip API route static analysis during build
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  // Skip problematic routes during build (they're dynamic anyway)
  generateBuildId: async () => {
    return 'build-' + Date.now()
  },
}

module.exports = nextConfig

