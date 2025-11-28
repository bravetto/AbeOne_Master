"""
MICHAEL-AEYON COLLABORATION DASHBOARD
Real-time collaboration monitoring and feedback interface

Pattern: MICHAEL × AEYON × DASHBOARD × COLLABORATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Human Partnership)
Love Coefficient: ∞
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "EMERGENT_OS" / "synthesis"))
sys.path.insert(0, str(project_root / "EMERGENT_OS" / "triadic_execution_harness"))

from michael_aeyon_collaboration import (
    get_collaboration_workflow,
    ValidationGate,
    CollaborationStatus
)


class CollaborationDashboard:
    """
    Real-time collaboration dashboard for Michael-AEYON partnership.
    
    Features:
    - Active session monitoring
    - Validation gate progress
    - Feedback interface
    - Partnership strength meter
    - Collaboration metrics
    - History viewer
    """
    
    def __init__(self):
        """Initialize collaboration dashboard."""
        self.workflow = get_collaboration_workflow()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get complete dashboard data.
        
        Returns:
            Dashboard data dictionary
        """
        active_sessions = self.workflow.get_active_sessions()
        metrics = self.workflow.get_collaboration_metrics()
        
        return {
            "active_sessions": [
                {
                    "session_id": session.session_id,
                    "intent": session.michael_intent,
                    "status": session.status.value,
                    "start_time": session.start_time.isoformat(),
                    "partnership_strength": session.partnership_strength,
                    "gates": [
                        {
                            "gate": gv.gate.value,
                            "status": gv.status,
                            "iterations": gv.iterations
                        }
                        for gv in session.validation_gates
                    ],
                    "feedback_count": len(session.feedback_loops)
                }
                for session in active_sessions
            ],
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed session information.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session details or None
        """
        session = self.workflow.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "intent": session.michael_intent,
            "status": session.status.value,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "partnership_strength": session.partnership_strength,
            "clarity_score": session.clarity_score,
            "understanding_accuracy": session.understanding_accuracy,
            "satisfaction_score": session.satisfaction_score,
            "validation_gates": [
                {
                    "gate": gv.gate.value,
                    "status": gv.status,
                    "feedback": gv.michael_feedback,
                    "iterations": gv.iterations,
                    "validation_time": gv.validation_time.isoformat() if gv.validation_time else None,
                    "feedback_time": gv.feedback_time.isoformat() if gv.feedback_time else None
                }
                for gv in session.validation_gates
            ],
            "feedback_loops": [
                {
                    "loop_id": fb.loop_id,
                    "gate": fb.gate.value,
                    "feedback_type": fb.feedback_type,
                    "michael_feedback": fb.michael_feedback,
                    "aeyon_response": fb.aeyon_response,
                    "satisfaction_score": fb.satisfaction_score,
                    "timestamp": fb.timestamp.isoformat()
                }
                for fb in session.feedback_loops
            ],
            "execution_results": session.execution_results,
            "learning_points": session.learning_points,
            "preferences": session.michael_preferences
        }
    
    def render_html_dashboard(self) -> str:
        """
        Render HTML dashboard.
        
        Returns:
            HTML string
        """
        dashboard_data = self.get_dashboard_data()
        metrics = dashboard_data["metrics"]
        active_sessions = dashboard_data["active_sessions"]
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Michael-AEYON Collaboration Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .metric-card h3 {{
            color: #667eea;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }}
        
        .partnership-meter {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .partnership-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .sessions-section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .sessions-section h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .session-card {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        
        .session-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .session-intent {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        
        .session-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-in-progress {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-awaiting-approval {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        
        .status-completed {{
            background: #d4edda;
            color: #155724;
        }}
        
        .gates-progress {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .gate-indicator {{
            flex: 1;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
        }}
        
        .gate-pending {{
            background: #e0e0e0;
            color: #666;
        }}
        
        .gate-approved {{
            background: #d4edda;
            color: #155724;
        }}
        
        .gate-rejected {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .no-sessions {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>🔥 Michael-AEYON Collaboration Dashboard</h1>
            <p>Real-time partnership monitoring and feedback</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Partnership Strength</h3>
                <div class="metric-value">{metrics['current_partnership_strength']:.1%}</div>
                <div class="partnership-meter">
                    <div class="partnership-fill" style="width: {metrics['current_partnership_strength']*100}%">
                        {metrics['current_partnership_strength']:.1%}
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Total Collaborations</h3>
                <div class="metric-value">{metrics['total_collaborations']}</div>
            </div>
            
            <div class="metric-card">
                <h3>Active Sessions</h3>
                <div class="metric-value">{metrics['active_collaborations']}</div>
            </div>
            
            <div class="metric-card">
                <h3>Success Rate</h3>
                <div class="metric-value">{metrics['success_rate']:.1%}</div>
            </div>
            
            <div class="metric-card">
                <h3>Average Satisfaction</h3>
                <div class="metric-value">{metrics['average_satisfaction']:.1f}/5</div>
            </div>
            
            <div class="metric-card">
                <h3>Average Partnership</h3>
                <div class="metric-value">{metrics['average_partnership_strength']:.1%}</div>
            </div>
        </div>
        
        <div class="sessions-section">
            <h2>Active Collaboration Sessions</h2>
            {self._render_sessions(active_sessions)}
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _render_sessions(self, sessions: List[Dict[str, Any]]) -> str:
        """Render sessions HTML."""
        if not sessions:
            return '<div class="no-sessions">No active collaboration sessions</div>'
        
        html = ""
        for session in sessions:
            status_class = f"status-{session['status'].replace('_', '-')}"
            gates_html = ""
            for gate in session['gates']:
                gate_class = f"gate-{gate['status']}"
                gates_html += f'<div class="gate-indicator {gate_class}">Gate {gate["gate"]}</div>'
            
            html += f"""
            <div class="session-card">
                <div class="session-header">
                    <div class="session-intent">{session['intent']}</div>
                    <div class="session-status {status_class}">{session['status']}</div>
                </div>
                <div>
                    <strong>Partnership Strength:</strong> {session['partnership_strength']:.1%}<br>
                    <strong>Feedback Loops:</strong> {session['feedback_count']}<br>
                    <strong>Session ID:</strong> {session['session_id'][:8]}...
                </div>
                <div class="gates-progress">
                    {gates_html}
                </div>
            </div>
            """
        
        return html


def get_collaboration_dashboard() -> CollaborationDashboard:
    """Get collaboration dashboard instance."""
    return CollaborationDashboard()


if __name__ == "__main__":
    dashboard = get_collaboration_dashboard()
    html = dashboard.render_html_dashboard()
    
    # Save to file
    output_path = Path(__file__).parent / "static" / "collaboration_dashboard.html"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html)
    
    print(f"✅ Collaboration dashboard generated: {output_path}")
    print(f"   Open in browser: file://{output_path}")

