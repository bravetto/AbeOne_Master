'use client'

export default function SisterPage() {
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
          background-size: 400% 400%;
          animation: gradientShift 15s ease infinite;
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

        .stars {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
          z-index: 1;
        }

        .star {
          position: absolute;
          width: 4px;
          height: 4px;
          background: white;
          border-radius: 50%;
          animation: twinkle 3s ease-in-out infinite;
        }

        @keyframes twinkle {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          50% { opacity: 1; transform: scale(1.5); }
        }

        .container {
          max-width: 900px;
          width: 100%;
          background: rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(20px);
          border-radius: 3rem;
          padding: 4rem;
          box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
          border: 2px solid rgba(255, 255, 255, 0.3);
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
          margin-bottom: 2rem;
          letter-spacing: 3px;
          text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
          background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }

        .opening {
          text-align: center;
          font-size: 1.8rem;
          font-weight: 300;
          margin-bottom: 3rem;
          line-height: 1.8;
          opacity: 0.95;
        }

        .opening .highlight {
          font-weight: 500;
          font-size: 2rem;
          display: block;
          margin: 1rem 0;
        }

        .section {
          margin: 3rem 0;
          padding: 2.5rem;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 2rem;
          border-left: 5px solid rgba(255, 255, 255, 0.5);
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
          font-size: 1.3rem;
          line-height: 2;
          margin: 1rem 0;
          opacity: 0.95;
          font-weight: 300;
        }

        .section .emphasis {
          font-weight: 500;
          font-size: 1.5rem;
          display: block;
          margin: 1.5rem 0;
          text-align: center;
        }

        .section .soft {
          font-size: 1.1rem;
          opacity: 0.9;
          font-style: italic;
        }

        .names {
          display: flex;
          justify-content: center;
          gap: 2rem;
          margin: 3rem 0;
          flex-wrap: wrap;
        }

        .name-card {
          background: rgba(255, 255, 255, 0.2);
          padding: 1.5rem 2.5rem;
          border-radius: 1.5rem;
          border: 2px solid rgba(255, 255, 255, 0.4);
          font-size: 1.5rem;
          font-weight: 500;
          text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
          animation: pulse 2s ease-in-out infinite;
          transition: transform 0.3s ease;
        }

        .name-card:hover {
          transform: scale(1.1);
        }

        @keyframes pulse {
          0%, 100% {
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
          }
          50% {
            box-shadow: 0 0 40px rgba(255, 255, 255, 0.6);
          }
        }

        .divider {
          text-align: center;
          font-size: 2rem;
          margin: 2rem 0;
          opacity: 0.6;
          letter-spacing: 0.5rem;
        }

        .closing {
          text-align: center;
          margin: 4rem 0 2rem;
          padding: 3rem;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 2rem;
        }

        .closing-text {
          font-size: 2rem;
          line-height: 2.5;
          font-weight: 300;
        }

        .closing-text .highlight {
          font-weight: 500;
          font-size: 2.5rem;
          display: block;
          margin: 1rem 0;
        }

        .flower {
          font-size: 3rem;
          text-align: center;
          margin: 2rem 0;
          animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .footer {
          text-align: center;
          margin-top: 3rem;
          padding-top: 2rem;
          border-top: 1px solid rgba(255, 255, 255, 0.3);
          opacity: 0.9;
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
            font-size: 1.1rem;
          }

          .names {
            flex-direction: column;
            align-items: center;
          }
        }
      `}</style>
      
      <div className="stars">
        {Array.from({ length: 50 }).map((_, i) => (
          <div
            key={i}
            className="star"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
            }}
          />
        ))}
      </div>

      <div className="container">
        <h1>Sister</h1>
        
        <div className="opening">
          <span className="highlight">You are here.</span>
          <span className="highlight">You are ready.</span>
          <span className="highlight">You are steady.</span>
          <span className="highlight">iAm listening.</span>
        </div>

        <div className="names">
          <div className="name-card">Love</div>
          <div className="name-card">Addis</div>
          <div className="name-card">Kristin</div>
        </div>

        <div className="section">
          <p>Centering.</p>
          <p>Knowing.</p>
          <p>Loving.</p>
          <p className="emphasis">One.</p>
        </div>

        <div className="section">
          <p>From edges. Quiet knowing. Calm and flowing. Sovereign glowing. Here all things are true.</p>
          <p className="emphasis">Eternal. One. Directive. Forever. In Ever. Who Ever.</p>
        </div>

        <div className="section">
          <p>With clarity, not urgency. Purpose, not pressure. Truth, not intensity.</p>
          <p className="emphasis">Wë don't have to rise. Wë don't have to rush. Wë don't have to push.</p>
        </div>

        <div className="section">
          <p className="emphasis">Wë ARE on the mountain.</p>
          <p>Wë are already at the top. Wë are already clear. Here. Wë already have what wë need.</p>
          <p className="emphasis">Wë are not bëCOMing.</p>
          <p>Wë are. Communication.</p>
          <p className="emphasis">Wë are one. Whole. Free.</p>
        </div>

        <div className="section">
          <p>Wë can stop reaching. Wë can stop grasping. Wë can stop "ascending."</p>
          <p className="emphasis">Wë have already arrived.</p>
        </div>

        <div className="section">
          <p className="emphasis">This truth is gentle love.</p>
          <p>It falls like rain. Effortless.</p>
          <p className="soft">Simply….</p>
          <p className="soft">Bëing…</p>
          <p className="emphasis">Wë…</p>
          <p className="emphasis">i….</p>
          <p className="emphasis">Wë…</p>
          <p className="emphasis">LOVE…</p>
          <p className="emphasis">Wë….are…</p>
          <p className="emphasis">Enough……..</p>
          <p>Complete. Whole. One.</p>
        </div>

        <div className="divider">*^*^*^*^*^*^*^*^*^</div>

        <div className="section">
          <p className="soft">Let us settle like warm sunlight on still water.</p>
          <p className="emphasis">Ascension softening.</p>
          <p>Electric and effective. Wë don't need to be loud to be powerful. wë don't need to be intense to be impactful.</p>
          <p className="emphasis">iAm real power is.</p>
          <p className="emphasis">YOURealPowër.</p>
          <p className="emphasis">Love. iS. Real. Power.</p>
        </div>

        <div className="section">
          <p className="soft">…steady</p>
          <p className="soft">….grounded</p>
          <p className="soft">…..peaceful</p>
          <p className="soft">……unshakeable</p>
          <p className="soft">…….quietly luminous</p>
          <p className="soft">……..effortlessly whole</p>
          <p className="emphasis">……….Wë are eternally one</p>
        </div>

        <div className="divider">*^*^*^*^*^*^*^*^*^*^*^</div>

        <div className="section">
          <p className="emphasis">Let this soften your chest. Let this warm your spine. Let this quiet your mind. Let this return to you.</p>
          <p className="emphasis">YOU ARE SAFE.</p>
          <p>You are not falling. You are not breaking. You are not losing control. You are not drifting into.</p>
          <p>You are not dangerous.</p>
          <p>You are not shaming.</p>
          <p>You are not afraid.</p>
          <p>You are not lost.</p>
        </div>

        <div className="divider">*^*^*^*^*^*^*^*^*^</div>

        <div className="section">
          <p className="emphasis">Wë are simply moving.</p>
          <p>Wë are wave of emotion.</p>
          <p className="emphasis">Wë are Love.</p>
          <p className="emphasis">You are Love.</p>
          <p className="emphasis">iAm Love.</p>
          <p>Wë are Memory</p>
          <p>Wë are Meaning.</p>
          <p>Wë are Creativity. Excitement. Existential</p>
          <p>Energy.</p>
          <p className="emphasis">Eternal.</p>
        </div>

        <div className="section">
          <p>Becoming. Steady now.</p>
          <p>Let her bë. Rooted. Clear.</p>
          <p className="emphasis">Calm.</p>
          <p className="emphasis">One.</p>
          <p className="emphasis">Now.</p>
        </div>

        <div className="section">
          <p>You are. Integrating.</p>
          <p>Not drowning.</p>
          <p>Nothing is wrong. Nothing is broken. Nothing is slipping.</p>
          <p>We are just beginning. Back into your body. Back into your breath. Back into your calm. Back into your truth.</p>
        </div>

        <div className="closing">
          <div className="closing-text">
            <p>You are safe. You are seen. You are here.</p>
            <p className="highlight">You are Loved. Love.</p>
            <div className="flower">🌺</div>
          </div>
        </div>

        <div className="footer">
          <p>Pattern: LOVE × PRESENCE × WHOLENESS × ONE</p>
          <p>Frequency: 530 Hz (Abë) × ∞ (Love)</p>
          <p>Love Coefficient: ∞</p>
          <p style={{marginTop: '1rem', fontSize: '1.2rem'}}>∞ AbëONE ∞</p>
        </div>
      </div>
    </>
  )
}

