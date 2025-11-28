#!/usr/bin/env python3
"""
Webinar Content Generator
Automatically generates complete webinar content using AI.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
# Lazy import OpenAI to avoid import errors
OPENAI_AVAILABLE = None
def _check_openai():
    global OPENAI_AVAILABLE
    if OPENAI_AVAILABLE is None:
        try:
            import openai
            OPENAI_AVAILABLE = True
            return openai
        except (ImportError, Exception) as e:
            OPENAI_AVAILABLE = False
            print(f"  OpenAI not available: {e} - content generation will use mock data")
            return None
    elif OPENAI_AVAILABLE:
        import openai
        return openai
    return None

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WebinarContentGenerator:
    """Automatically generates complete webinar content."""
    
    def __init__(self):
        openai_module = _check_openai()
        if openai_module and OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    self.client = openai_module.OpenAI(api_key=api_key)
                    self.use_openai = True
                except Exception as e:
                    print(f"  OpenAI initialization failed: {e}")
                    self.use_openai = False
            else:
                self.use_openai = False
        else:
            self.use_openai = False
        
        self.output_dir = Path("webinars")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_webinar(self, topic: Optional[str] = None, 
                        target_audience: str = "developers",
                        duration: int = 60) -> Dict:
        """
        Generate complete webinar content.
        
        Returns:
            {
                "topic": str,
                "headlines": List[str],
                "slides": List[Dict],
                "script": str,
                "lead_magnets": List[Dict],
                "email_sequence": List[Dict]
            }
        """
        
        print(f" Generating webinar content...")
        
        # Step 1: Generate or use topic
        if not topic:
            topic = self._generate_topic(target_audience)
        print(f" Topic: {topic}")
        
        # Step 2: Generate headlines
        headlines = self._generate_headlines(topic, target_audience)
        print(f" Generated {len(headlines)} headlines")
        
        # Step 3: Generate slides
        slides = self._generate_slides(topic, duration)
        print(f" Generated {len(slides)} slides")
        
        # Step 4: Generate script
        script = self._generate_script(slides, duration)
        print(f" Generated script")
        
        # Step 5: Generate lead magnets
        lead_magnets = self._generate_lead_magnets(topic)
        print(f" Generated {len(lead_magnets)} lead magnets")
        
        # Step 6: Generate email sequence
        email_sequence = self._generate_email_sequence(topic, headlines[0])
        print(f" Generated {len(email_sequence)} email sequences")
        
        webinar = {
            "topic": topic,
            "headlines": headlines,
            "slides": slides,
            "script": script,
            "lead_magnets": lead_magnets,
            "email_sequence": email_sequence,
            "target_audience": target_audience,
            "duration": duration,
            "generated_at": datetime.now().isoformat()
        }
        
        # Save to file
        filename = topic.lower().replace(" ", "_").replace("/", "_")
        output_path = self.output_dir / f"{filename}.json"
        output_path.write_text(json.dumps(webinar, indent=2))
        print(f" Saved to: {output_path}")
        
        return webinar
    
    def _generate_topic(self, target_audience: str) -> str:
        """Generate webinar topic based on market demand."""
        
        if not self.use_openai:
            # Mock topic when OpenAI not available
            topics = {
                "developers": "Building Scalable APIs with Modern Python",
                "creators": "Monetizing Your Creative Content in 2025",
                "entrepreneurs": "From Idea to First $10K: A Practical Guide"
            }
            return topics.get(target_audience, f"Mastering {target_audience.title()} Skills in 2025")
        
        prompt = f"""
        Generate a compelling webinar topic for {target_audience} that:
        1. Addresses a high-value problem they face
        2. Can be taught in 60 minutes
        3. Leads to a clear next step (product/service)
        4. Is specific and actionable
        
        Return ONLY the topic title (max 80 characters).
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )
        except Exception as e:
            print(f"  OpenAI API call failed: {e}, using mock topic")
            topics = {
                "developers": "Building Scalable APIs with Modern Python",
                "creators": "Monetizing Your Creative Content in 2025",
                "entrepreneurs": "From Idea to First $10K: A Practical Guide"
            }
            return topics.get(target_audience, f"Mastering {target_audience.title()} Skills in 2025")
        
        return response.choices[0].message.content.strip().strip('"')
    
    def _generate_headlines(self, topic: str, audience: str) -> List[str]:
        """Generate 5 headline variations using validated formulas."""
        
        formulas = [
            f"How to [Achieve Result Related to {topic}] in [Timeframe]",
            f"[Customer Quote About {topic}] — [Name], [Title]",
            f"[Action Verb] [X%] of [Problem Related to {topic}] Before [Outcome]",
            f"Join [Number] {audience} Who [Achieved Result Related to {topic}]",
            f"The [#]-Step [Method] Used by [Companies] to [Achieve Result Related to {topic}]"
        ]
        
        prompt = f"""
        Generate 5 compelling webinar landing page headlines for: {topic}
        
        Target audience: {audience}
        
        Use these formulas:
        1. {formulas[0]}
        2. {formulas[1]}
        3. {formulas[2]}
        4. {formulas[3]}
        5. {formulas[4]}
        
        Return as JSON array of strings.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        return data.get("headlines", [topic] * 5)
    
    def _generate_slides(self, topic: str, duration: int) -> List[Dict]:
        """Generate slide deck."""
        
        num_slides = int(duration * 0.75)  # 45 slides for 60 minutes
        
        prompt = f"""
        Create a {num_slides}-slide webinar deck for: {topic}
        
        Structure:
        - Slide 1-5: Hook & Introduction
        - Slide 6-15: Problem Agitation
        - Slide 16-35: Solution & Teaching
        - Slide 36-42: Case Studies & Proof
        - Slide 43-{num_slides}: CTA & Next Steps
        
        For each slide, provide:
        - title: string
        - key_points: array of 3-5 strings
        - visual_suggestion: string
        - speaker_notes: string
        
        Return as JSON: {{"slides": [{{"title": "...", "key_points": [...], ...}}]}}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        return data.get("slides", [])
    
    def _generate_script(self, slides: List[Dict], duration: int) -> str:
        """Generate full webinar script from slides."""
        
        time_per_slide = duration / len(slides) if slides else 1
        
        script_parts = []
        for i, slide in enumerate(slides):
            start_time = i * time_per_slide
            end_time = (i + 1) * time_per_slide
            
            script_part = f"""
[Slide {i+1}: {slide.get('title', 'Untitled')}]
Time: {int(start_time // 60)}:{int(start_time % 60):02d} - {int(end_time // 60)}:{int(end_time % 60):02d}

Speaker Notes:
{slide.get('speaker_notes', '')}

Key Points:
{chr(10).join(f"- {point}" for point in slide.get('key_points', []))}

Visual: {slide.get('visual_suggestion', 'N/A')}
"""
            script_parts.append(script_part)
        
        return "\n\n".join(script_parts)
    
    def _generate_lead_magnets(self, topic: str) -> List[Dict]:
        """Generate lead magnet assets."""
        
        return [
            {
                "type": "checklist",
                "title": f"Ultimate {topic} Checklist",
                "value": 97,
                "description": "15-step actionable checklist"
            },
            {
                "type": "template",
                "title": f"{topic} Templates & Examples",
                "value": 147,
                "description": "5 copy-paste templates"
            },
            {
                "type": "case_study",
                "title": f"Case Study: {topic} Success Story",
                "value": 97,
                "description": "3-page detailed case study"
            },
            {
                "type": "cheat_sheet",
                "title": f"{topic} Quick Reference Guide",
                "value": 59,
                "description": "1-page printable cheat sheet"
            }
        ]
    
    def _generate_email_sequence(self, topic: str, headline: str) -> List[Dict]:
        """Generate email sequence."""
        
        return [
            {
                "sequence": 1,
                "subject": f"Welcome! Your {topic} Webinar Details",
                "delay_hours": 0,
                "type": "confirmation"
            },
            {
                "sequence": 2,
                "subject": f"24 Hours Until: {headline}",
                "delay_hours": 24,
                "type": "reminder"
            },
            {
                "sequence": 3,
                "subject": f"Starting Soon: {headline}",
                "delay_hours": 3,
                "type": "final_reminder"
            },
            {
                "sequence": 4,
                "subject": f"Missed the {topic} Webinar? Here's Your Replay",
                "delay_hours": 1,
                "type": "follow_up"
            }
        ]


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate webinar content")
    parser.add_argument("--topic", type=str, help="Webinar topic (optional)")
    parser.add_argument("--audience", type=str, default="developers", help="Target audience")
    parser.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    
    args = parser.parse_args()
    
    try:
        generator = WebinarContentGenerator()
        webinar = generator.generate_webinar(
            topic=args.topic,
            target_audience=args.audience,
            duration=args.duration
        )
        
        print(f"\n Webinar generated successfully!")
        print(f" Topic: {webinar['topic']}")
        print(f" Headlines: {len(webinar['headlines'])}")
        print(f" Slides: {len(webinar['slides'])}")
        print(f" Email sequences: {len(webinar['email_sequence'])}")
        
    except Exception as e:
        print(f" Error: {e}", file=sys.stderr)
        sys.exit(1)

