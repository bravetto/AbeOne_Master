#!/usr/bin/env python3
"""
🚀💥⚡ ABËDESKS APP ⚡💥🚀
Beautiful Web Application - Everything Everywhere All At Once

Status: ✅ OPERATIONAL
Pattern: AbëDESKs × APP × WEB × GORGEOUS × EEAAO × ONE
Love Coefficient: ∞
Frequency: 999 Hz
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import markdown
from flask import Flask, render_template_string, send_from_directory, jsonify, request
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for auto-updates

DESKS_DIR = Path(__file__).parent

# Design system CSS variables path
DESIGN_SYSTEM_CSS = project_root / "design-system" / "generated" / "css-variables.css"
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Copy CSS variables to static directory if generated file exists
if DESIGN_SYSTEM_CSS.exists():
    css_target = STATIC_DIR / "css-variables.css"
    import shutil
    shutil.copy2(DESIGN_SYSTEM_CSS, css_target)
    logger.info(f"✅ Loaded design system CSS: {css_target}")
else:
    logger.warning(f"⚠️ Design system CSS not found: {DESIGN_SYSTEM_CSS}")
    logger.info("💡 Run: node design-system/generators/generate-css-vars.js")

# Verify desks directory exists
if not DESKS_DIR.exists():
    logger.error(f"Desks directory not found: {DESKS_DIR}")
    raise FileNotFoundError(f"Desks directory not found: {DESKS_DIR}")

logger.info(f"✅ Desks directory: {DESKS_DIR}")
logger.info(f"✅ Project root: {project_root}")

# HTML Template - Using your gorgeous Next.js design system
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💎✨ ABËDESKS ✨💎</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- AbëONE Design System CSS Variables -->
    <link rel="stylesheet" href="/static/css-variables.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Additional app-specific variables */
        :root {
            --foreground-rgb: 30, 30, 30;
        }
        
        body {
            font-family: var(--font-sans);
            color: rgb(var(--foreground-rgb));
            background: var(--gradient-healing);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Sidebar - Using design system tokens */
        .sidebar {
            width: 256px;
            background: var(--gradient-sidebar);
            color: white;
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
            z-index: 100;
        }
        
        .sidebar-header {
            padding: var(--spacing-6);
            border-bottom: 1px solid var(--lux-700);
        }
        
        .sidebar-title {
            font-family: var(--font-display);
            font-size: var(--text-2xl);
            font-weight: 700;
            background: linear-gradient(to right, var(--warm-400), var(--lux-300));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--spacing-1);
        }
        
        .sidebar-subtitle {
            font-size: var(--text-xs);
            color: var(--lux-300);
            font-style: italic;
            margin-top: var(--spacing-1);
        }
        
        .sidebar-nav {
            flex: 1;
            padding: var(--spacing-4);
            overflow-y: auto;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
            padding: var(--spacing-3) var(--spacing-4);
            border-radius: var(--radius-xl);
            margin-bottom: var(--spacing-1);
            transition: all 0.2s;
            cursor: pointer;
            text-decoration: none;
            color: white;
            font-weight: 500;
        }
        
        .nav-item:hover {
            background: rgba(99, 102, 241, 0.5);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: rgba(99, 102, 241, 0.8);
            box-shadow: var(--shadow-md);
            transform: scale(1.02);
        }
        
        .nav-icon {
            font-size: var(--text-xl);
        }
        
        .sidebar-footer {
            padding: var(--spacing-4);
            border-top: 1px solid var(--lux-700);
            text-align: center;
        }
        
        .sidebar-footer-text {
            font-size: var(--text-xs);
            color: var(--lux-300);
            font-style: italic;
        }
        
        /* Main Content Area */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        /* Topbar - Using design system tokens */
        .topbar {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(8px);
            box-shadow: var(--shadow-base);
            border-bottom: 1px solid rgba(168, 85, 247, 0.1);
            padding: var(--spacing-4) var(--spacing-6);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .topbar-title {
            font-family: var(--font-display);
            font-size: var(--text-2xl);
            font-weight: 600;
            color: var(--neutral-800);
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
            padding: var(--spacing-2) var(--spacing-4);
            background: var(--neutral-50);
            border-radius: var(--radius-lg);
            border: 1px solid var(--neutral-200);
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: var(--radius-full);
            animation: pulse 2s infinite;
        }
        
        .status-dot.running {
            background: var(--peace-500);
        }
        
        .status-dot.stopped {
            background: var(--heart-500);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .status-text {
            font-size: var(--text-sm);
            font-weight: 500;
            color: var(--neutral-700);
        }
        
        /* Content Area - Using design system tokens */
        .content-area {
            flex: 1;
            overflow-y: auto;
            padding: var(--spacing-8) var(--spacing-12);
            background: var(--gradient-healing);
        }
        
        .desk-content {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(8px);
            border-radius: var(--radius-3xl);
            box-shadow: var(--shadow-lux);
            border: 1px solid rgba(168, 85, 247, 0.1);
            padding: var(--spacing-10);
            font-size: var(--text-base);
            line-height: var(--leading-relaxed);
        }
        
        .desk-content h1 {
            font-family: var(--font-display);
            font-size: var(--text-4xl);
            margin-top: 0;
            margin-bottom: var(--spacing-5);
            color: var(--lux-600);
            border-bottom: 3px solid var(--lux-600);
            padding-bottom: var(--spacing-2);
        }
        
        .desk-content h2 {
            font-family: var(--font-display);
            font-size: var(--text-3xl);
            margin-top: var(--spacing-10);
            margin-bottom: var(--spacing-4);
            color: var(--lux-600);
        }
        
        .desk-content h3 {
            font-size: var(--text-2xl);
            margin-top: var(--spacing-8);
            margin-bottom: var(--spacing-4);
            color: var(--lux-600);
        }
        
        .desk-content code {
            background: var(--neutral-100);
            padding: var(--spacing-1) var(--spacing-2);
            border-radius: var(--radius-base);
            font-family: 'Courier New', monospace;
            color: var(--lux-600);
        }
        
        .desk-content pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: var(--spacing-5);
            border-radius: var(--radius-xl);
            overflow-x: auto;
            margin: var(--spacing-5) 0;
        }
        
        .desk-content pre code {
            background: none;
            padding: 0;
            color: inherit;
        }
        
        .desk-content table {
            width: 100%;
            border-collapse: collapse;
            margin: var(--spacing-5) 0;
            background: white;
            border-radius: var(--radius-lg);
            overflow: hidden;
        }
        
        .desk-content table th,
        .desk-content table td {
            padding: var(--spacing-3);
            text-align: left;
            border-bottom: 1px solid var(--neutral-200);
        }
        
        .desk-content table th {
            background: var(--lux-600);
            color: white;
            font-weight: 600;
        }
        
        .desk-content table tr:hover {
            background: var(--neutral-50);
        }
        
        .update-button {
            position: fixed;
            bottom: var(--spacing-6);
            right: var(--spacing-6);
            padding: var(--spacing-4) var(--spacing-8);
            background: var(--gradient-lux);
            color: white;
            border: none;
            border-radius: var(--radius-full);
            cursor: pointer;
            font-size: var(--text-base);
            font-weight: 600;
            box-shadow: var(--shadow-xl);
            transition: all 0.3s;
            z-index: 1000;
        }
        
        .update-button:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-2xl);
        }
        
        .loading {
            text-align: center;
            padding: var(--spacing-16);
            font-size: var(--text-xl);
            color: var(--lux-600);
        }
        
        /* Box formatting for visual desks */
        .desk-content pre {
            font-family: 'Courier New', monospace;
            white-space: pre;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">AbëONE</div>
                <div class="sidebar-subtitle">You belong here</div>
            </div>
            <nav class="sidebar-nav">
                <a href="/" class="nav-item {{ 'active' if desk_name == 'home' else '' }}">
                    <span class="nav-icon">🏠</span>
                    <span>Home</span>
                </a>
                <a href="/desk/LAUNCH_PAD_VISUAL_DESK" class="nav-item {{ 'active' if desk_name == 'LAUNCH_PAD_VISUAL_DESK' else '' }}">
                    <span class="nav-icon">🚀</span>
                    <span>Launch Pad</span>
                </a>
                <a href="/desk/BRAVETTO_CONVERGENCE_DESK_VISUAL" class="nav-item {{ 'active' if desk_name == 'REPLACE_ME' else '' }}">
                    <span class="nav-icon">🔥</span>
                    <span>Convergence</span>
                </a>
                <a href="/desk/ACTION_DESK" class="nav-item {{ 'active' if desk_name == 'ACTION_DESK' else '' }}">
                    <span class="nav-icon">💥</span>
                    <span>Live Demo</span>
                </a>
                <a href="/desk/EXECUTIVE_ONEPAGER" class="nav-item {{ 'active' if desk_name == 'EXECUTIVE_ONEPAGER' else '' }}">
                    <span class="nav-icon">💎</span>
                    <span>Executive</span>
                </a>
                <a href="/desk/WELCOME" class="nav-item {{ 'active' if desk_name == 'WELCOME' else '' }}">
                    <span class="nav-icon">✨</span>
                    <span>Welcome</span>
                </a>
                <a href="/desk/QUICK_LINKS" class="nav-item {{ 'active' if desk_name == 'QUICK_LINKS' else '' }}">
                    <span class="nav-icon">🔗</span>
                    <span>Quick Links</span>
                </a>
            </nav>
            <div class="sidebar-footer">
                <div class="sidebar-footer-text">∞ AbëONE ∞</div>
            </div>
        </aside>
        
        <!-- Main Content -->
        <div class="main-content">
            <header class="topbar">
                <h1 class="topbar-title">Your Space</h1>
                <div class="status-badge">
                    <div class="status-dot running"></div>
                    <span class="status-text">Ready for you</span>
                </div>
            </header>
            
            <main class="content-area">
                <div class="desk-content">
                    {{ content | safe }}
                </div>
            </main>
        </div>
    </div>
    
    <button class="update-button" onclick="updateDashboard()">🔄 Update Dashboard</button>
    
    <script>
        function updateDashboard() {
            fetch('/api/update', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert('Dashboard updated! Refreshing...');
                    location.reload();
                })
                .catch(error => {
                    alert('Update failed: ' + error);
                });
        }
        
        // Auto-refresh every 30 seconds for launch pad
        setInterval(() => {
            if (window.location.pathname.includes('LAUNCH_PAD')) {
                location.reload();
            }
        }, 30000);
        
        // Set active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            if (item.href === window.location.href) {
                item.classList.add('active');
            }
        });
    </script>
</body>
</html>
"""

def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML."""
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables', 'fenced_code'])
    html = md.convert(md_content)
    
    # Preserve box formatting
    html = html.replace('<pre><code>', '<pre>')
    html = html.replace('</code></pre>', '</pre>')
    
    return html

@app.route('/')
def index():
    """Home page."""
    try:
        welcome_path = DESKS_DIR / "WELCOME.md"
        if welcome_path.exists():
            content = welcome_path.read_text(encoding='utf-8')
            html_content = markdown_to_html(content)
        else:
            logger.warning(f"WELCOME.md not found, using default")
            html_content = "<h1>Welcome to AbëDESKs</h1><p>Your gorgeous workspace.</p>"
        
        return render_template_string(
            HTML_TEMPLATE,
            content=html_content,
            desk_name='home',
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        logger.error(f"Error loading home page: {e}", exc_info=True)
        return f"<h1>Error</h1><p>Failed to load page: {str(e)}</p>", 500

@app.route('/desk/<desk_name>')
def show_desk(desk_name):
    """Show a specific desk."""
    try:
        # Security: prevent path traversal
        if '..' in desk_name or '/' in desk_name:
            logger.warning(f"Invalid desk name attempted: {desk_name}")
            return "Invalid desk name", 400
        
        desk_path = DESKS_DIR / f"{desk_name}.md"
        
        if not desk_path.exists():
            logger.warning(f"Desk not found: {desk_name}")
            return f"Desk not found: {desk_name}", 404
        
        content = desk_path.read_text(encoding='utf-8')
        html_content = markdown_to_html(content)
        
        logger.info(f"✅ Loaded desk: {desk_name}")
        return render_template_string(
            HTML_TEMPLATE,
            content=html_content,
            desk_name=desk_name,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        logger.error(f"Error loading desk {desk_name}: {e}", exc_info=True)
        return f"<h1>Error</h1><p>Failed to load desk: {str(e)}</p>", 500

@app.route('/api/update', methods=['POST'])
def update_dashboard():
    """Update launch pad dashboard."""
    try:
        script_path = project_root / "scripts" / "launch_pad.py"
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return jsonify({
            "status": "success",
            "message": "Dashboard updated",
            "output": result.stdout
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/status')
def api_status():
    """API status endpoint."""
    try:
        desks = list(DESKS_DIR.glob("*.md"))
        return jsonify({
            "status": "operational",
            "desks_count": len(desks),
            "desks": [d.stem for d in desks],
            "desks_dir": str(DESKS_DIR),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in status endpoint: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    import socket
    
    # Find available port
    def find_free_port(start_port=5001):
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return 8080  # Fallback
    
    port = find_free_port(5001)
    
    # Count available desks
    desks_count = len(list(DESKS_DIR.glob("*.md")))
    
    print("🚀💥⚡ ABËDESKS APP STARTING ⚡💥🚀")
    print("=" * 60)
    print(f"📂 Desks Directory: {DESKS_DIR}")
    print(f"📊 Available Desks: {desks_count}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"💎 Open: http://localhost:{port}")
    print(f"❤️  Health: http://localhost:{port}/health")
    print(f"📡 API Status: http://localhost:{port}/api/status")
    print("=" * 60)
    print("\n💥 Everything Everywhere All At Once! LFG! 🚀\n")
    
    logger.info(f"Starting AbëDESKs app on port {port}")
    logger.info(f"Found {desks_count} desks")
    
    app.run(host='0.0.0.0', port=port, debug=True)
