'use client'

const stats = [
  { label: 'Codebase Size', value: '3.9GB', description: 'Production-ready codebase' },
  { label: 'Agent Swarm', value: '149', description: 'Scalable backend agents' },
  { label: 'Guard Services', value: '6', description: 'Running on AWS EKS' },
  { label: 'Guardians', value: '8', description: 'All operational in production' },
  { label: 'Test Coverage', value: '100%', description: '277+ tests' },
  { label: 'Production Ready', value: '100%', description: 'Live infrastructure' },
]

export function Stats() {
  return (
    <section className="py-24 px-4 md:px-8 lg:px-24 bg-white/50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-display font-bold text-center mb-16 text-gray-800">
          The Numbers
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-xl border border-lux-200 hover:shadow-lg transition-shadow"
            >
              <div className="text-3xl md:text-4xl font-display font-bold text-gradient-healing mb-2">
                {stat.value}
              </div>
              <div className="text-sm md:text-base font-semibold text-gray-700 mb-1">
                {stat.label}
              </div>
              <div className="text-xs text-gray-500">
                {stat.description}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

