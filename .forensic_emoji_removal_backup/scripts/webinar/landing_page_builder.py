#!/usr/bin/env python3
"""
Webinar Landing Page Builder
Programmatically generates optimized landing pages from webinar content.
"""

import json
import sys
from pathlib import Path
from typing import Dict

class LandingPageBuilder:
    """Builds optimized landing pages from webinar content."""
    
    def __init__(self):
        self.output_dir = Path("apps/web/app/webinar/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def build(self, webinar_data: Dict) -> str:
        """Build landing page from webinar data."""
        
        topic = webinar_data.get("topic", "Webinar")
        headlines = webinar_data.get("headlines", [topic])
        slides = webinar_data.get("slides", [])
        lead_magnets = webinar_data.get("lead_magnets", [])
        scheduled_time = webinar_data.get("scheduled_time", "TBD")
        zoom_link = webinar_data.get("zoom_join_url", "#")
        
        # Generate page content
        page_content = self._generate_page_content(
            topic=topic,
            headline=headlines[0] if headlines else topic,
            slides=slides,
            lead_magnets=lead_magnets,
            scheduled_time=scheduled_time,
            zoom_link=zoom_link
        )
        
        # Save to Next.js page
        page_filename = topic.lower().replace(" ", "-").replace("/", "-")
        page_path = self.output_dir / f"{page_filename}/page.tsx"
        page_path.parent.mkdir(exist_ok=True)
        page_path.write_text(page_content)
        
        print(f"✅ Landing page generated: {page_path}")
        return str(page_path)
    
    def _generate_page_content(self, topic: str, headline: str, slides: list,
                              lead_magnets: list, scheduled_time: str, zoom_link: str) -> str:
        """Generate Next.js page component."""
        
        # Calculate total value
        total_value = sum(m.get("value", 0) for m in lead_magnets)
        
        # Escape topic for use in template
        topic_escaped = topic.replace("'", "\\'")
        topic_id = topic.lower().replace(" ", "_").replace("/", "-")
        headline_escaped = headline.replace("'", "\\'")
        
        # Generate benefits and lead magnets HTML
        benefits_html = self._generate_benefits_html(slides)
        magnets_html = self._generate_lead_magnets_html(lead_magnets)
        
        # Use .format() instead of f-string to avoid nested brace issues
        template = """'use client'

import {{ useState }} from 'react'

export default function WebinarLandingPage() {{
  const [formData, setFormData] = useState({{
    firstName: '',
    email: ''
  }})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  
  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault()
    setIsSubmitting(true)
    
    try {{
      const response = await fetch('/api/webinar/register', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          ...formData,
          webinar_topic: '{topic_escaped}',
          webinar_id: '{topic_id}'
        }})
      }})
      
      if (response.ok) {{
        setShowSuccess(true)
        setFormData({{ firstName: '', email: '' }})
      }}
    }} catch (error) {{
      console.error('Registration error:', error)
    }} finally {{
      setIsSubmitting(false)
    }}
  }}
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-lux-600 to-warm-500">
      <section className="py-24 px-4 text-center text-white">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-display font-bold mb-6">
            {headline_escaped}
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white/90">
            Join 1,000+ developers learning {topic_escaped}
          </p>
          
          {{!showSuccess ? (
            <form onSubmit={{handleSubmit}} className="max-w-md mx-auto space-y-4">
              <input
                type="text"
                placeholder="First Name"
                value={{formData.firstName}}
                onChange={(e) => setFormData({{...formData, firstName: e.target.value}})}
                required
                className="w-full px-4 py-4 rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70"
              />
              <input
                type="email"
                placeholder="your@email.com"
                value={{formData.email}}
                onChange={(e) => setFormData({{...formData, email: e.target.value}})}
                required
                className="w-full px-4 py-4 rounded-xl border-2 border-white/20 bg-white/10 text-white placeholder-white/70"
              />
              <button
                type="submit"
                disabled={{isSubmitting}}
                className="w-full py-4 bg-white text-lux-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all disabled:opacity-50"
              >
                {{isSubmitting ? 'Registering...' : 'Reserve My Spot - It\\'s Free →'}}
              </button>
            </form>
          ) : (
            <div className="max-w-md mx-auto bg-white/10 rounded-xl p-8">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-3xl font-bold mb-2">You\\'re In!</h2>
              <p>Check your email for webinar details.</p>
            </div>
          )}}
          
          <div className="mt-8 flex flex-wrap justify-center gap-4 text-sm">
            <span>🔒 Your info is safe</span>
            <span>✓ No credit card required</span>
            <span>📧 Unsubscribe anytime</span>
          </div>
        </div>
      </section>
      
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            In This Free 60-Minute Masterclass, You\\'ll Discover:
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {benefits_html}
          </div>
        </div>
      </section>
      
      <section className="py-16 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Register Today & Get The Complete Toolkit:
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            (Valued at ${total_value}, Yours FREE)
          </p>
          <div className="space-y-4 text-left max-w-2xl mx-auto">
            {magnets_html}
          </div>
        </div>
      </section>
      
      <section className="py-16 bg-lux-600 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your {topic_escaped}?</h2>
          <p className="text-xl mb-8">Join 1,000+ developers who\\'ve already registered.</p>
          <a
            href="#register"
            className="inline-block py-4 px-8 bg-white text-lux-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
          >
            Reserve My Spot - Get ${total_value} Toolkit Free
          </a>
        </div>
      </section>
    </div>
  )
}}"""
        
        return template.format(
            topic_escaped=topic_escaped,
            topic_id=topic_id,
            headline_escaped=headline_escaped,
            total_value=total_value,
            benefits_html=benefits_html,
            magnets_html=magnets_html
        )
    
    def _generate_benefits_html(self, slides: list) -> str:
        """Generate benefits HTML from slides."""
        
        if not slides:
            return '<div>Benefits coming soon...</div>'
        
        benefits_html = []
        for slide in slides[:6]:  # First 6 slides as benefits
            title = slide.get("title", "Benefit")
            key_point = slide.get("key_points", [""])[0] if slide.get("key_points") else ""
            
            benefits_html.append(f'''
            <div className="bg-gray-50 rounded-xl p-6">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="font-bold text-lg mb-2">{title}</h3>
              <p className="text-gray-600">{key_point}</p>
            </div>
            ''')
        
        return "\n".join(benefits_html)
    
    def _generate_lead_magnets_html(self, lead_magnets: list) -> str:
        """Generate lead magnets HTML."""
        
        magnets_html = []
        for magnet in lead_magnets:
            magnets_html.append(f'''
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="flex items-start gap-4">
                <span className="text-3xl">🎁</span>
                <div>
                  <h3 className="font-bold text-lg">{magnet.get("title", "Bonus")}</h3>
                  <p className="text-gray-600">{magnet.get("description", "")}</p>
                  <span className="text-sm text-gray-500">(${magnet.get("value", 0)} value)</span>
                </div>
              </div>
            </div>
            ''')
        
        return "\n".join(magnets_html)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build landing page from webinar")
    parser.add_argument("--webinar-file", type=str, required=True, help="Webinar JSON file")
    
    args = parser.parse_args()
    
    builder = LandingPageBuilder()
    
    webinar_data = json.loads(Path(args.webinar_file).read_text())
    page_path = builder.build(webinar_data)
    
    print(f"\n✅ Landing page built: {page_path}")
    print(f"📁 View at: /webinar/generated/{Path(page_path).parent.name}")

