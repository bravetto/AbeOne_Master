'use client'

export function CTA() {
  return (
    <section className="py-24 px-4 md:px-8 lg:px-24 gradient-lux">
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <h2 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold text-white">
          Ready to See the Future?
        </h2>
        <p className="text-xl md:text-2xl text-white/90 max-w-2xl mx-auto">
          The future of AI validation is here. We built it.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
          <a
            href="mailto:contact@bravetto.ai"
            className="px-8 py-4 bg-white text-lux-700 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Schedule Demo
          </a>
          <a
            href="https://github.com/orgs/bravetto"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 bg-white/20 backdrop-blur-sm border-2 border-white text-white rounded-xl font-semibold text-lg hover:bg-white/30 transition-all duration-200"
          >
            View GitHub Repositories
          </a>
        </div>

        <div className="pt-8">
          <p className="text-sm text-white/80 italic">
            "We've built what they're promising. They have the vision we've implemented."
          </p>
        </div>
      </div>
    </section>
  )
}

