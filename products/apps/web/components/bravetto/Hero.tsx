'use client'

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 md:px-8 lg:px-24 py-24">
      <div className="max-w-6xl w-full text-center space-y-8 animate-fade-in">
        {/* Main Headline */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold text-gradient-healing leading-tight">
          Bravetto × AiGuardian
        </h1>
        <h2 className="text-3xl md:text-5xl lg:text-6xl font-display font-semibold text-gray-800">
          The Inevitable Convergence
        </h2>
        
        {/* Subheadline */}
        <p className="text-xl md:text-2xl lg:text-3xl text-gray-700 max-w-4xl mx-auto leading-relaxed text-balance pt-4">
          Production infrastructure meets AI validation vision.
          <br />
          <span className="text-lg md:text-xl text-gray-600 font-normal">
            This is not a vision. This is reality.
          </span>
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
          <a
            href="#convergence"
            className="group px-8 py-4 bg-gradient-to-r from-lux-600 to-warm-500 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            <span className="flex items-center justify-center gap-2">
              See the Convergence
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </a>
          <a
            href="https://github.com/orgs/bravetto"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 bg-white/80 backdrop-blur-sm border-2 border-lux-300 text-lux-700 rounded-xl font-semibold text-lg hover:bg-white hover:border-lux-400 transition-all duration-200"
          >
            View GitHub Repositories
          </a>
        </div>

        {/* Trust Indicator */}
        <div className="pt-12">
          <p className="text-sm text-gray-500 italic">
            "We've built what they're promising. They have the vision we've implemented."
          </p>
        </div>
      </div>
    </section>
  )
}

