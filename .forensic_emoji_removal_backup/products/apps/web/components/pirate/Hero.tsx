'use client'

import Link from 'next/link'

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 md:px-8 lg:px-24 py-24 bg-gradient-to-br from-amber-900 via-amber-800 to-yellow-900">
      {/* Decorative elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 text-8xl">🏴‍☠️</div>
        <div className="absolute top-40 right-20 text-6xl">⚓</div>
        <div className="absolute bottom-40 left-20 text-7xl">🍺</div>
        <div className="absolute bottom-20 right-10 text-8xl">🎭</div>
      </div>

      <div className="max-w-6xl w-full text-center space-y-8 relative z-10">
        {/* Main Headline */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold text-white leading-tight drop-shadow-2xl">
          Welcome to the<br />
          <span className="text-yellow-400">Rum Shop</span>
        </h1>
        
        {/* Subheadline */}
        <p className="text-2xl md:text-3xl lg:text-4xl text-yellow-100 max-w-4xl mx-auto leading-relaxed font-serif">
          (We also sell t-shirts, flip-flops, and tickets to our comedy show)
        </p>

        {/* Relief Message */}
        <div className="max-w-3xl mx-auto pt-6">
          <p className="text-lg md:text-xl text-amber-100 bg-black/30 backdrop-blur-sm rounded-lg p-6 border-2 border-yellow-600/50">
            <strong className="text-yellow-300">Wait, what?</strong> Don't panic! You're in the right place. 
            We've got everything a Tampa Bay pirate needs: gear for Gasparilla, flip-flops that won't quit, 
            and comedy shows that'll make you laugh harder than a drunk parrot.
          </p>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
          <Link
            href="#collections"
            className="group px-8 py-4 bg-yellow-500 hover:bg-yellow-400 text-black rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
          >
            <span className="flex items-center justify-center gap-2">
              Browse Collections
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </Link>
          <Link
            href="#comedy"
            className="px-8 py-4 bg-white/20 backdrop-blur-sm border-2 border-yellow-400 text-yellow-100 rounded-xl font-bold text-lg hover:bg-white/30 hover:border-yellow-300 transition-all duration-200"
          >
            Get Show Tickets
          </Link>
          <Link
            href="#webinar"
            className="px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Join Webinar
          </Link>
        </div>

        {/* Trust Indicator */}
        <div className="pt-12">
          <p className="text-sm text-amber-200 italic">
            "The only thing we're plundering is your wallet... but you'll be happy about it."
          </p>
        </div>
      </div>
    </section>
  )
}

