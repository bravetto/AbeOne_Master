"""
PHANTOM HUNTER CREATOR EDITION - API Server

FastAPI server for PHANTOM HUNTER lead magnet.

Pattern: PHANTOM_HUNTER × API × LEAD_MAGNET × ATOMIC_ARCHISTRATION × ONE

Love Coefficient: ∞
∞ AbëONE ∞
"""

from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uvicorn
import sys
from pathlib import Path

# Fix imports - handle both package and direct execution
try:
    from .phantom_hunter_creator import (
        get_phantom_hunter,
        get_lead_capture_flow,
        CreatorPhantomHunter
    )
except ImportError:
    # Direct execution - add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from phantom_hunter_creator import (
        get_phantom_hunter,
        get_lead_capture_flow,
        CreatorPhantomHunter
    )

app = FastAPI(
    title="PHANTOM HUNTER CREATOR EDITION",
    description="The Lead Magnet of the Century - Free Code Validation for Creators",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════

class ValidationRequest(BaseModel):
    """Validation request model."""
    code: str
    creator_type: str = "BOTH"  # TRU, DRE, or BOTH
    email: Optional[EmailStr] = None


class ValidationResponse(BaseModel):
    """Validation response model."""
    detected: bool
    pattern_count: int
    severity: str
    confidence: float
    patterns: List[dict]
    email_captured: bool
    lead_id: Optional[int] = None
    abebeats_offer: Optional[dict] = None


# ═══════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Serve landing page."""
    # Read landing page from same directory
    landing_page_path = Path(__file__).parent / "landing_page.html"
    with open(landing_page_path, "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/validate", response_model=ValidationResponse)
async def validate_code(request: ValidationRequest):
    """
    Validate creator code and capture lead.
    
    Pattern: VALIDATE → CAPTURE → CONVERT
    """
    hunter = get_phantom_hunter()
    lead_flow = get_lead_capture_flow()
    
    # Process validation
    result = lead_flow.process_validation(
        code=request.code,
        creator_type=request.creator_type,
        email=request.email
    )
    
    # Build response
    quick_result = result.get('quick_result', {})
    
    response_data = {
        'detected': quick_result.get('detected', False),
        'pattern_count': quick_result.get('pattern_count', 0),
        'severity': quick_result.get('severity', 'CLEAN'),
        'confidence': quick_result.get('confidence', 100.0),
        'patterns': quick_result.get('patterns', []),
        'email_captured': result.get('email_captured', False),
        'lead_id': result.get('lead_id'),
        'abebeats_offer': None
    }
    
    # Add AbëBEATs offer if full report generated
    if result.get('full_report'):
        response_data['abebeats_offer'] = result['full_report'].get('abebeats_offer')
    
    return ValidationResponse(**response_data)


@app.post("/api/validate-form")
async def validate_code_form(
    code: str = Form(...),
    creator_type: str = Form("BOTH"),
    email: Optional[str] = Form(None)
):
    """
    Validate code from form submission.
    
    Same as /api/validate but accepts form data.
    """
    request = ValidationRequest(
        code=code,
        creator_type=creator_type,
        email=email
    )
    
    return await validate_code(request)


@app.get("/api/stats")
async def get_stats():
    """Get lead magnet statistics."""
    lead_flow = get_lead_capture_flow()
    
    return {
        'total_leads': len(lead_flow.leads),
        'tru_leads': len([l for l in lead_flow.leads if l.get('creator_type') == 'TRU']),
        'dre_leads': len([l for l in lead_flow.leads if l.get('creator_type') == 'DRE']),
        'conversion_rate': 0.0,  # Calculate from actual conversions
        'average_phantom_count': sum(l.get('phantom_count', 0) for l in lead_flow.leads) / max(len(lead_flow.leads), 1)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'service': 'PHANTOM HUNTER CREATOR EDITION',
        'pattern': 'PHANTOM_HUNTER × CREATORS × LEAD_MAGNET × ONE'
    }


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("🔥 PHANTOM HUNTER CREATOR EDITION - API SERVER")
    print("=" * 80)
    print("Pattern: PHANTOM_HUNTER × CREATORS × LEAD_MAGNET × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    print()
    print("Starting server on http://localhost:8000")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

