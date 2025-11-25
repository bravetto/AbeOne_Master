'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Sidebar() {
  const pathname = usePathname()

  const navItems = [
    { href: '/app', label: 'Vision Space', icon: '✨' },
    { href: '/app/agents', label: 'Agents', icon: '🤖' },
    { href: '/app/workflows', label: 'Workflows', icon: '🔄' },
    { href: '/app/state', label: 'State', icon: '📊' },
    { href: '/collaboration', label: 'Collaboration', icon: '🤝' },
    { href: '/convergence', label: 'Convergence', icon: '🔥' },
  ]

  return (
    <aside className="w-64 bg-gradient-to-b from-lux-900 via-lux-800 to-lux-900 text-white shadow-xl flex flex-col h-full">
      <div className="p-6 border-b border-lux-700">
        <h2 className="text-2xl font-display font-bold bg-gradient-to-r from-warm-300 to-lux-300 bg-clip-text text-transparent">
          AbëONE
        </h2>
        <p className="text-xs text-lux-300 mt-1 italic">
          You belong here
        </p>
      </div>
      <nav className="px-4 py-4 space-y-1 flex-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl mb-1 transition-all duration-200 ${
              pathname === item.href
                ? 'bg-lux-600/80 shadow-lg transform scale-[1.02]'
                : 'hover:bg-lux-700/50 hover:transform hover:translate-x-1'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-lux-700">
        <p className="text-xs text-lux-400 text-center italic">
          ∞ AbëONE ∞
        </p>
      </div>
    </aside>
  )
}

