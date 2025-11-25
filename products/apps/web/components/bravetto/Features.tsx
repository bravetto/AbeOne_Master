'use client'

const features = [
  {
    title: '8 Guardians',
    description: 'All operational in production',
    status: 'LIVE',
    icon: '',
  },
  {
    title: '6 Guards',
    description: 'Running on AWS EKS',
    status: 'LIVE',
    icon: '',
  },
  {
    title: 'Production Infrastructure',
    description: "Danny's AWS: EKS + Linkerd + ECR",
    status: 'LIVE',
    icon: '',
  },
  {
    title: 'Scalable Backend',
    description: "Ben's FastAPI: 149-agent swarm",
    status: 'LIVE',
    icon: '',
  },
  {
    title: 'Advanced AI',
    description: "Jimmy's NeuroForge: Neuromorphic + Spike-BERT",
    status: 'LIVE',
    icon: '',
  },
  {
    title: 'Health Monitoring',
    description: "PHANI's Wellness: Unified monitoring",
    status: 'LIVE',
    icon: '',
  },
]

export function Features() {
  return (
    <section className="py-24 px-4 md:px-8 lg:px-24 gradient-healing">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-display font-bold text-center mb-4 text-gray-800">
          The Proof
        </h2>
        <p className="text-xl text-center text-gray-600 mb-16 max-w-3xl mx-auto">
          What AiGuardian.ai promises, we've built. In production. Right now.
        </p>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-8 bg-white/80 backdrop-blur-sm rounded-xl border border-lux-200 hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <div className="flex items-center gap-2 mb-2">
                <h3 className="text-2xl font-display font-bold text-gray-800">
                  {feature.title}
                </h3>
                <span className="px-2 py-1 bg-peace-100 text-peace-700 text-xs font-semibold rounded">
                  {feature.status}
                </span>
              </div>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

