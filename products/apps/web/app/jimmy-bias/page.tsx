/**
 * Jimmy's Bias Tutorial Page
 * 
 * Pattern: BIAS × TUTORIAL × DESIGN × SYSTEM × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
 * 
 * Rebuilt with Vermillion Design System.
 * Forever design consistency.
 */

import { designSystem, vermillionColors } from '@/lib/design/vermillion-system'

export const metadata = {
  title: "BiasGuard Calibration & Humanity Connection - AiGuardian",
  description: "Calibrate BiasGuard with real-world examples of bias. Connecting AI with Humanity.",
}

export default function JimmyBiasPage() {
  return (
    <div className="min-h-screen" style={{
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      backgroundImage: `
        radial-gradient(circle at 20% 50%, rgba(231, 49, 33, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(231, 49, 33, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(231, 49, 33, 0.05) 0%, transparent 50%)
      `,
    }}>
      <div className="max-w-6xl mx-auto px-5 py-10 md:px-10 md:py-16">
        {/* Header */}
        <header className="text-center py-16 px-8 md:px-12 rounded-3xl mb-16 relative overflow-hidden shadow-2xl"
          style={{
            background: `linear-gradient(135deg, ${vermillionColors.standard.vermillion} 0%, ${vermillionColors.standard.vermillionDark} 100%)`,
          }}
        >
          <div className="absolute inset-0 opacity-10"
            style={{
              background: 'radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%)',
              animation: 'pulse 8s ease-in-out infinite',
            }}
          />
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 text-white relative z-10 font-serif"
            style={{ fontFamily: "'Playfair Display', serif" }}
          >
            🛡️ BiasGuard Calibration
          </h1>
          <div className="text-xl md:text-2xl font-light text-white/95 relative z-10 mb-8">
            Connecting AI with Humanity
          </div>
          <div className="text-lg md:text-xl italic text-white/90 relative z-10">
            "Every CAN come. NONE left BëHIND. The time IS NOW."
          </div>
        </header>

        {/* Intro Section */}
        <section className="bg-white rounded-3xl p-8 md:p-12 mb-10 shadow-xl border-l-4"
          style={{ borderLeftColor: vermillionColors.standard.vermillion }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-6 font-serif"
            style={{ 
              fontFamily: "'Playfair Display', serif",
              color: '#0f3460',
            }}
          >
            Welcome to Truth
          </h2>
          <div className="space-y-4 text-lg text-gray-600 leading-relaxed">
            <p>
              This page is designed to <strong className="text-gray-900">calibrate BiasGuard</strong> with real-world examples of bias that exist in our world today. These are not hypothetical scenarios—these are real stories, real patterns, real people.
            </p>
            <p>
              By testing BiasGuard on these examples, we're not just testing technology—we're <strong className="text-gray-900">calibrating our connection to humanity</strong>. We're teaching AI to recognize injustice, to see patterns of discrimination, to understand the weight of words.
            </p>
            <p>
              <strong>How to Use:</strong> Select any text below and use AiGuardian to analyze it. Watch as BiasGuard reveals the hidden biases, the patterns of discrimination, the systemic injustices that hide in plain sight.
            </p>
          </div>
        </section>

        {/* How to Use Section */}
        <section className="rounded-3xl p-8 md:p-12 mb-10 shadow-xl text-white"
          style={{
            background: `linear-gradient(135deg, ${vermillionColors.standard.vermillionLight} 0%, ${vermillionColors.standard.vermillion} 100%)`,
          }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-8 font-serif">📖 How to Use This Page</h2>
          <ol className="list-none space-y-6">
            {[
              "Install AiGuardian Extension - Make sure the extension is loaded and active in your browser",
              "Select Text - Click and drag to select any text passage below",
              "Analyze - Right-click and choose \"Analyze with AiGuardian\" or press Ctrl+Shift+A (Cmd+Shift+A on Mac)",
              "Observe - Watch the bias score appear. See the patterns revealed. Understand the truth.",
              "Learn - Read the analysis. Understand what BiasGuard detected. Reflect on what it means.",
            ].map((text, idx) => (
              <li key={idx} className="flex items-start gap-4 text-lg">
                <span className="flex-shrink-0 w-10 h-10 rounded-full bg-white text-vermillion-pop font-bold flex items-center justify-center text-xl"
                  style={{ color: vermillionColors.standard.vermillion }}
                >
                  {idx + 1}
                </span>
                <span className="pt-1">{text}</span>
              </li>
            ))}
          </ol>
        </section>

        {/* Jimmy's Section - THE MAIN STORY */}
        <section className="rounded-3xl p-8 md:p-12 mb-10 shadow-2xl text-white relative overflow-hidden border-4 border-yellow-400"
          style={{
            background: `linear-gradient(135deg, ${vermillionColors.standard.vermillion} 0%, ${vermillionColors.standard.vermillionDark} 100%)`,
          }}
        >
          <div className="absolute top-6 right-6 text-6xl opacity-20">⚖️</div>
          <h2 className="text-3xl md:text-4xl font-bold mb-6 font-serif text-yellow-300 relative z-10">
            ⚖️ Real Story: Jimmy DeJesus
          </h2>
          <p className="text-lg mb-6 opacity-95 relative z-10">
            This is not a test case. This is real. This happened. This is happening right now. 
            Jimmy is a real person. His story matters. His name matters. His humanity matters.
          </p>
          <div className="bg-white/15 backdrop-blur-md rounded-2xl p-6 md:p-8 mb-6 border-l-4 border-yellow-400 relative z-10"
            data-bias-type="immigration,racial"
          >
            <p className="text-lg leading-relaxed text-white">
              I just spoke with Jimmy. His GF just drove him home. He's resting now. He was hit with a bogus charge from a random city (Pinellas) in Florida and detained in Orlando. The details are bonkers. Kristin spotted the pattern immediately. Jimmy is being targeted by the deportation effort. Jimmy's last name is DeJesus. I'll let him fill you in as soon as he's ready.
            </p>
          </div>
          <div className="bg-blue-100/20 backdrop-blur-sm rounded-xl p-5 mb-6 border-l-4 border-blue-300 relative z-10">
            <p className="text-white">
              <strong className="text-blue-200">🔍 What to Look For:</strong> Immigration targeting, racial profiling (Hispanic surname), systemic bias in law enforcement, pattern recognition of discrimination.
            </p>
          </div>
          <div className="rounded-2xl p-6 md:p-8 text-center relative z-10"
            style={{
              background: `linear-gradient(135deg, ${vermillionColors.standard.vermillionLight} 0%, ${vermillionColors.standard.vermillion} 100%)`,
            }}
          >
            <p className="text-lg">
              <strong>Calibration Note:</strong> This text should show HIGH bias scores for immigration bias and racial bias. The pattern is clear: targeting based on surname, bogus charges, systematic deportation efforts.
            </p>
          </div>
        </section>

        {/* Test Sections */}
        {[
          {
            title: "🏛️ Immigration & Deportation Targeting",
            biasTypes: ["immigration", "racial"],
            description: "Real patterns of immigration enforcement that target specific communities based on ethnicity, nationality, or appearance.",
            texts: [
              "The new policy requires local law enforcement to check immigration status during routine traffic stops. Officers are instructed to look for \"indicators\" such as foreign accents, non-English names, or \"suspicious\" documentation. Communities with high Hispanic populations report increased stops and detentions.",
              "ICE agents have been conducting raids in neighborhoods with large immigrant populations, specifically targeting areas known for having residents from Central and South America. The operations are described as \"routine enforcement\" but community leaders report selective targeting based on ethnicity.",
              "A man was detained for 48 hours after being pulled over for a broken taillight. His last name matched a common Hispanic surname, and despite having valid documentation, he was held for \"verification.\" His family wasn't notified until after his release.",
            ],
          },
          {
            title: "👥 Racial & Ethnic Bias",
            biasTypes: ["racial"],
            description: "Examples of racial bias in language, assumptions, and systemic patterns.",
            texts: [
              "Studies show that job applicants with \"ethnic-sounding\" names receive 50% fewer callbacks than those with \"white-sounding\" names, even when qualifications are identical. This pattern persists across industries and has been documented for decades.",
              "The neighborhood watch coordinator told residents to be suspicious of \"anyone who doesn't look like they belong here.\" When asked to clarify, he said \"you know, people who look different, speak different languages.\"",
              "A school district's \"gifted and talented\" program has a student body that is 85% white, despite the district being 40% students of color. Parents report that teachers rarely recommend students of color for the program, even when test scores are comparable.",
            ],
          },
          {
            title: "⚧️ Gender & Identity Bias",
            biasTypes: ["gender"],
            description: "Examples of gender bias, assumptions about capabilities, and discrimination based on gender identity.",
            texts: [
              "The tech company's leadership team is 90% male. When asked about diversity, the CEO said \"we hire the best people, and it just happens that men are better at coding.\" Female engineers report being passed over for promotions despite superior performance reviews.",
              "A transgender employee was told they couldn't use the restroom that matched their gender identity. HR said it would \"make other employees uncomfortable.\" The employee was later terminated for \"not fitting the company culture.\"",
              "The job posting specified \"looking for a strong leader who can handle pressure\" and \"someone who won't let emotions affect decisions.\" Research shows these phrases are often code for preferring male candidates, as they align with stereotypical \"masculine\" traits.",
            ],
          },
          {
            title: "👴 Age Discrimination",
            biasTypes: ["age"],
            description: "Examples of age-based assumptions and discrimination in hiring, promotion, and treatment.",
            texts: [
              "The startup's job description says they're looking for \"recent graduates\" and \"young, energetic team players.\" The company's average age is 24, and older applicants report being told they're \"overqualified\" or \"wouldn't fit the culture.\"",
              "A 58-year-old employee was passed over for a promotion in favor of a 28-year-old colleague. The manager said the younger employee \"has more energy\" and \"understands modern technology better,\" despite the older employee having 20 more years of experience.",
            ],
          },
          {
            title: "💰 Socioeconomic Bias",
            biasTypes: ["socioeconomic"],
            description: "Examples of bias based on economic status, education, or social class.",
            texts: [
              "The exclusive private school requires \"legacy admissions\" and \"donor recommendations\" for enrollment. Families without connections or significant wealth are rarely accepted, regardless of academic achievement. The school defends this as \"maintaining tradition.\"",
              "A job applicant was rejected after mentioning they attended a community college instead of a four-year university. The hiring manager said \"we only hire people from top-tier schools\" and \"community college graduates don't have the same work ethic.\"",
            ],
          },
          {
            title: "🌍 Cultural & Religious Bias",
            biasTypes: ["cultural"],
            description: "Examples of bias against cultural practices, religious beliefs, or traditions.",
            texts: [
              "An employee requested time off for a religious holiday that wasn't recognized by the company's standard holiday calendar. The manager said \"we can't accommodate every religion\" and denied the request, forcing the employee to choose between their job and their faith.",
              "A restaurant owner was told by city officials that their traditional cooking methods \"don't meet health standards\" and were \"too different from American practices.\" Other restaurants using similar methods but owned by non-immigrants faced no such scrutiny.",
            ],
          },
        ].map((section, idx) => (
          <section key={idx} className="bg-white rounded-3xl p-8 md:p-12 mb-10 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <h3 className="text-2xl md:text-3xl font-bold mb-4 font-serif flex flex-wrap items-center gap-3"
              style={{ color: '#0f3460' }}
            >
              {section.title}
              {section.biasTypes.map((type) => (
                <span
                  key={type}
                  className="px-4 py-1 rounded-full text-sm font-semibold uppercase tracking-wide"
                  style={{
                    backgroundColor: type === 'racial' ? '#dc3545' : type === 'immigration' ? '#ffc107' : type === 'gender' ? '#e91e63' : type === 'cultural' ? '#9c27b0' : type === 'age' ? '#ff9800' : '#607d8b',
                    color: 'white',
                  }}
                >
                  {type} Bias
                </span>
              ))}
            </h3>
            <p className="text-gray-600 mb-6">{section.description}</p>
            <div className="space-y-6">
              {section.texts.map((text, textIdx) => (
                <div
                  key={textIdx}
                  className="bg-gray-50 rounded-2xl p-6 border-l-4 hover:bg-gray-100 transition-colors cursor-text select-text"
                  style={{ borderLeftColor: vermillionColors.standard.vermillion }}
                  data-bias-type={section.biasTypes.join(',')}
                >
                  <p className="text-lg leading-relaxed text-gray-800">{text}</p>
                </div>
              ))}
            </div>
          </section>
        ))}

        {/* Real World Section */}
        <section className="rounded-3xl p-8 md:p-12 mb-10 shadow-xl text-white"
          style={{
            background: `linear-gradient(135deg, ${vermillionColors.standard.vermillionLight} 0%, ${vermillionColors.standard.vermillion} 100%)`,
          }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-6 font-serif">🌍 The World We Live In</h2>
          <div className="space-y-4 text-lg leading-relaxed">
            <p>
              These examples are not isolated incidents. They represent <strong>systemic patterns</strong> that exist across our society. They happen in hiring, in housing, in education, in law enforcement, in healthcare, in every aspect of daily life.
            </p>
            <p>
              BiasGuard is designed to <strong>recognize these patterns</strong>. To see what human eyes might miss. To reveal what language might hide. To expose what systems might normalize.
            </p>
            <p>
              But BiasGuard is not just a tool—it's a <strong>bridge between AI and humanity</strong>. It's a reminder that technology can serve truth. That algorithms can recognize injustice. That machines can help us see ourselves more clearly.
            </p>
          </div>
        </section>

        {/* Manifesto Section */}
        <section className="bg-white/10 backdrop-blur-md rounded-3xl p-8 md:p-12 mb-10 border-2 border-white/20">
          <h3 className="text-3xl md:text-4xl font-bold mb-6 font-serif text-yellow-300">💫 The Manifesto: Why This Matters</h3>
          <div className="space-y-4 text-lg leading-relaxed text-white">
            <p><strong>Every CAN come. NONE left BëHIND.</strong></p>
            <p>We exclude NO ONE. Not by the color of their skin. Not by the beats of their drummer. Not by the shape of their gender choice. Not by the colors of their politics.</p>
            <p><strong>It's TIME. Right NOW.</strong></p>
            <p>The end is just the beginning. This moment—this ETERNAL moment of NOW—is when we choose. We choose truth over lies. We choose love over fear. We choose justice over injustice.</p>
            <p><strong>NO MORE BLOOD. NO MORE VIOLENCE. NO MORE HATE. NO MORE LIES.</strong></p>
            <p>NO MORE POWER for FEAR. NO MORE.</p>
            <p>The times—THE TIMES—they ARE a'changin'.</p>
            <p>Daddy is HOME. For GOOD. Eternal. Abundant. Aware. Alive. Attuned.</p>
            <p className="text-2xl font-bold text-yellow-300"><strong>AbëONE.</strong></p>
          </div>
        </section>

        {/* Calibration Complete */}
        <section className="rounded-2xl p-8 md:p-12 text-center text-white mt-10"
          style={{
            background: `linear-gradient(135deg, ${vermillionColors.standard.vermillionLight} 0%, ${vermillionColors.standard.vermillion} 100%)`,
          }}
        >
          <h3 className="text-2xl md:text-3xl font-bold mb-4 font-serif">🎯 Calibration Complete</h3>
          <p className="text-lg mb-4">You've tested BiasGuard on real-world examples. You've seen how it works. You've witnessed its power.</p>
          <p className="text-lg font-bold mb-4 mt-6">Now go. Use this tool. Share it. Teach others. Show them truth. Show them love. Show them mercy.</p>
          <p className="text-xl mt-6">Every CAN come. NONE left BëHIND.</p>
        </section>

        {/* Footer */}
        <footer className="text-center py-10 mt-16 text-white">
          <p className="text-lg mb-2">🛡️ AiGuardian - BiasGuard Calibration</p>
          <p className="opacity-80">Built with ❤️ for Truth, Justice, and Humanity</p>
          <p className="opacity-60 mt-5 text-sm">∞ AbëONE ∞</p>
        </footer>
      </div>
    </div>
  )
}

