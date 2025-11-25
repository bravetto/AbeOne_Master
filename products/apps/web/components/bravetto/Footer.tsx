'use client'

export function Footer() {
  return (
    <footer className="py-12 px-4 md:px-8 lg:px-24 bg-gray-900 text-white">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-xl font-display font-bold mb-4">Bravetto</h3>
            <p className="text-gray-400 text-sm">
              Production infrastructure meets AI validation vision.
            </p>
          </div>
          
          <div>
            <h3 className="text-xl font-display font-bold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="https://github.com/orgs/bravetto" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  GitHub Repositories
                </a>
              </li>
              <li>
                <a href="mailto:contact@bravetto.ai" className="hover:text-white transition-colors">
                  Contact Us
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-display font-bold mb-4">Convergence</h3>
            <p className="text-gray-400 text-sm">
              Bravetto × AiGuardian × Convergence × Inevitability × ONE
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
          <p>
            Built with ∞ AbëONE ∞ | © 2025 Bravetto. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

