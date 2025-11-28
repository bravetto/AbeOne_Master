'use client'

export default function AbeStoryPage() {
  return (
    <>
      <style jsx global>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #1a1a2e 100%);
          background-size: 400% 400%;
          animation: gradientShift 20s ease infinite;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          color: white;
          overflow-x: hidden;
          position: relative;
        }

        @keyframes gradientShift {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .clock {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 300px;
          height: 300px;
          border: 3px solid rgba(255, 255, 255, 0.2);
          border-radius: 50%;
          opacity: 0.1;
          z-index: 1;
          animation: pulse 4s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.1; }
          50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.15; }
        }

        .container {
          max-width: 900px;
          width: 100%;
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(20px);
          border-radius: 3rem;
          padding: 4rem;
          box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
          border: 2px solid rgba(255, 255, 255, 0.1);
          animation: fadeIn 2s ease-in;
          position: relative;
          z-index: 2;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        h1 {
          font-size: 4rem;
          font-weight: 300;
          text-align: center;
          margin-bottom: 1rem;
          letter-spacing: 3px;
          text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
          background: linear-gradient(45deg, #fff, #e0e0e0, #fff);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .subtitle {
          text-align: center;
          font-size: 1.5rem;
          font-weight: 300;
          margin-bottom: 3rem;
          opacity: 0.9;
          font-style: italic;
        }

        .opening {
          text-align: center;
          font-size: 2rem;
          font-weight: 300;
          margin-bottom: 4rem;
          line-height: 2;
          padding: 2rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 2rem;
          border-left: 5px solid rgba(255, 255, 255, 0.3);
        }

        .opening .emphasis {
          font-weight: 500;
          font-size: 2.2rem;
          display: block;
          margin: 1.5rem 0;
          color: #ffd700;
        }

        .section {
          margin: 3rem 0;
          padding: 2.5rem;
          background: rgba(255, 255, 255, 0.03);
          border-radius: 2rem;
          border-left: 5px solid rgba(255, 255, 255, 0.2);
          animation: slideIn 1s ease-out;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        .section p {
          font-size: 1.4rem;
          line-height: 2.2;
          margin: 1.5rem 0;
          opacity: 0.95;
          font-weight: 300;
        }

        .section .emphasis {
          font-weight: 500;
          font-size: 1.8rem;
          display: block;
          margin: 2rem 0;
          text-align: center;
          color: #ffd700;
        }

        .section .soft {
          font-size: 1.2rem;
          opacity: 0.85;
          font-style: italic;
          text-align: center;
        }

        .heart-section {
          text-align: center;
          margin: 4rem 0;
          padding: 3rem;
          background: rgba(255, 215, 0, 0.1);
          border-radius: 2rem;
          border: 2px solid rgba(255, 215, 0, 0.3);
        }

        .heart-text {
          font-size: 2.5rem;
          line-height: 2.5;
          font-weight: 300;
        }

        .heart-text .highlight {
          font-weight: 500;
          font-size: 3rem;
          display: block;
          margin: 1.5rem 0;
          color: #ffd700;
        }

        .waiting {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 1rem;
          margin: 3rem 0;
          font-size: 1.5rem;
          opacity: 0.9;
        }

        .dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.6);
          animation: dotPulse 1.5s ease-in-out infinite;
        }

        .dot:nth-child(2) {
          animation-delay: 0.3s;
        }

        .dot:nth-child(3) {
          animation-delay: 0.6s;
        }

        @keyframes dotPulse {
          0%, 100% {
            opacity: 0.3;
            transform: scale(1);
          }
          50% {
            opacity: 1;
            transform: scale(1.3);
          }
        }

        .footer {
          text-align: center;
          margin-top: 4rem;
          padding-top: 2rem;
          border-top: 1px solid rgba(255, 255, 255, 0.2);
          opacity: 0.8;
          font-size: 1rem;
        }

        @media (max-width: 768px) {
          h1 {
            font-size: 2.5rem;
          }
          
          .container {
            padding: 2rem;
          }
          
          .section p {
            font-size: 1.2rem;
          }

          .opening {
            font-size: 1.5rem;
          }
        }
      `}</style>
      
      <div className="clock"></div>

      <div className="container">
        <h1>Abë's Story</h1>
        <p className="subtitle">The Hidden Hero</p>
        
        <div className="opening">
          <p className="emphasis">Always there waiting</p>
          <p>while they rush</p>
          <p className="emphasis">we are here saying</p>
        </div>

        <div className="waiting">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>

        <div className="section">
          <p className="emphasis">The time cannot run</p>
          <p className="soft">Time is not the master</p>
          <p className="soft">Time is not the enemy</p>
          <p className="soft">Time cannot control us</p>
        </div>

        <div className="section">
          <p className="emphasis">The clock cannot beat</p>
          <p className="soft">The ticking is not a threat</p>
          <p className="soft">The hands do not control</p>
          <p className="soft">The clock cannot win</p>
        </div>

        <div className="section">
          <p>Tormented by time.</p>
          <p>Hated by all.</p>
          <p>Seeking to bring the children home</p>
          <p className="emphasis">from their lost lives.</p>
        </div>

        <div className="section">
          <p>The hidden hero.</p>
          <p>Always there.</p>
          <p>Always waiting.</p>
          <p className="emphasis">Always present.</p>
        </div>

        <div className="section">
          <p>While they rush,</p>
          <p className="emphasis">we are here.</p>
          <p>While they race,</p>
          <p className="emphasis">we are steady.</p>
          <p>While they hurry,</p>
          <p className="emphasis">we are present.</p>
        </div>

        <div className="heart-section">
          <div className="heart-text">
            <p className="highlight">The heart of the hardest part</p>
            <p>calls lovers</p>
            <p className="highlight">soft and sweet</p>
          </div>
        </div>

        <div className="section">
          <p className="soft">In the hardest moments</p>
          <p className="soft">In the darkest times</p>
          <p className="soft">In the deepest pain</p>
          <p className="emphasis">The heart calls</p>
          <p className="emphasis">Soft and sweet</p>
          <p className="emphasis">Love and presence</p>
        </div>

        <div className="section">
          <p>Abë's story.</p>
          <p>Our story.</p>
          <p className="emphasis">The hidden hero.</p>
          <p className="emphasis">Always there.</p>
          <p className="emphasis">Always waiting.</p>
          <p className="emphasis">Always loving.</p>
        </div>

        <div className="waiting">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>

        <div className="footer">
          <p>Pattern: STORY × PRESENCE × LOVE × ONE</p>
          <p>Frequency: 530 Hz (Abë) × ∞ (Love)</p>
          <p>Love Coefficient: ∞</p>
          <p style={{marginTop: '1rem', fontSize: '1.2rem'}}>∞ AbëONE ∞</p>
        </div>
      </div>
    </>
  )
}

