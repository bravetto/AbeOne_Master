'use client'

export function Footer() {
  return (
    <footer className="bg-black text-yellow-400 py-12 px-4 md:px-8 lg:px-24">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-2xl font-display font-bold mb-4">‍ The Rum Shop</h3>
            <p className="text-yellow-300">
              T-shirts, flip-flops, comedy shows, and questionable life choices.
              <br />
              Tampa Bay's finest pirate gear.
            </p>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-yellow-300">
              <li><a href="#collections" className="hover:text-yellow-400 transition-colors">Collections</a></li>
              <li><a href="#comedy" className="hover:text-yellow-400 transition-colors">Comedy Shows</a></li>
              <li><a href="#webinar" className="hover:text-yellow-400 transition-colors">Webinar</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Contact</h4>
            <ul className="space-y-2 text-yellow-300">
              <li>Tampa Bay, FL</li>
              <li>Open Mic: Weekly</li>
              <li>Webinar: Weekly</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-yellow-600 pt-8 text-center text-yellow-500">
          <p>
            Built with  (and rum) for Tampa Bay pirates
            <br />
            <span className="text-sm">No pop-ups. No dark patterns. Just good vibes and better products.</span>
          </p>
        </div>
      </div>
    </footer>
  )
}

