'use client'

const convergencePoints = [
  {
    need: 'Production Infrastructure',
    solution: "Danny's AWS (EKS + Linkerd + ECR)",
    status: '✅',
  },
  {
    need: 'Scalable Backend',
    solution: "Ben's FastAPI (149-agent swarm + unified gateway)",
    status: '✅',
  },
  {
    need: 'Advanced AI',
    solution: "Jimmy's NeuroForge (Neuromorphic + Spike-BERT)",
    status: '✅',
  },
  {
    need: 'Health Monitoring',
    solution: "PHANI's Wellness (Unified monitoring + Prometheus)",
    status: '✅',
  },
]

export function Convergence() {
  return (
    <section id="convergence" className="py-24 px-4 md:px-8 lg:px-24 bg-white/50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-display font-bold text-center mb-4 text-gray-800">
          The Convergence
        </h2>
        <p className="text-xl text-center text-gray-600 mb-16 max-w-3xl mx-auto">
          What AiGuardian.ai needs to scale, Bravetto provides. This convergence is not optional—it's inevitable.
        </p>

        <div className="space-y-6">
          {convergencePoints.map((point, index) => (
            <div
              key={index}
              className="p-6 bg-white/80 backdrop-blur-sm rounded-xl border-l-4 border-lux-500 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="text-2xl">{point.status}</div>
                <div className="flex-1">
                  <h3 className="text-xl font-display font-bold text-gray-800 mb-2">
                    {point.need}
                  </h3>
                  <p className="text-gray-600">
                    → {point.solution}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 p-8 bg-gradient-to-r from-lux-100 to-warm-100 rounded-xl border-2 border-lux-300">
          <p className="text-lg text-center text-gray-800 font-semibold">
            We have everything they need. They have the vision. This convergence is not optional—it's inevitable.
          </p>
        </div>
      </div>
    </section>
  )
}

