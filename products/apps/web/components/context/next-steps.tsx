/**
 * Next Steps - Context Awareness System
 * 
 * Pattern: CONTEXT × AWARENESS × GUIDANCE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Always know what to do next - never directionless.
 */

import { vermillionColors } from '@/lib/design/vermillion-system'

interface NextStep {
  label: string
  action?: () => void
  href?: string
}

interface NextStepsProps {
  title?: string
  steps: NextStep[]
}

export function NextSteps({ title = 'Next Steps', steps }: NextStepsProps) {
  if (steps.length === 0) {
    return null
  }
  
  return (
    <div className="bg-white rounded-lg p-6 shadow-md mb-6 border-l-4"
      style={{ borderLeftColor: vermillionColors.standard.vermillion }}
    >
      <h3 className="text-lg font-bold mb-4" style={{ color: vermillionColors.standard.vermillion }}>
        {title}
      </h3>
      <ol className="list-decimal list-inside space-y-2">
        {steps.map((step, idx) => (
          <li key={idx} className="text-gray-700">
            {step.href ? (
              <a href={step.href} className="hover:underline" style={{ color: vermillionColors.standard.vermillion }}>
                {step.label}
              </a>
            ) : step.action ? (
              <button onClick={step.action} className="hover:underline text-left" style={{ color: vermillionColors.standard.vermillion }}>
                {step.label}
              </button>
            ) : (
              <span>{step.label}</span>
            )}
          </li>
        ))}
      </ol>
    </div>
  )
}

