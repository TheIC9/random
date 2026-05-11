"""
StackHeal AI — FastAPI Backend
Wraps the multi-agent pipeline and exposes a single REST endpoint.
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent dir so agent modules are importable when running from /backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import run_stackheal_pipeline

app = FastAPI(title="StackHeal AI", version="2.1.0")

# ── CORS (allow the React dev server on 5173/3000 and any origin in dev) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response schemas ───────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    code: str                          # raw source code or error log pasted by user
    language: Optional[str] = "auto"  # hint (Python / JavaScript / …); not required by agents


class PipelineResponse(BaseModel):
    # From error_detection agent
    type: str
    message: str
    # From error_line agent
    line: int
    snippet: str
    # From error_classify agent
    severity: str
    language: str
    # From root_cause agent
    root_cause: str
    # From fix agent
    description: str
    correctedCode: str
    # From explain agent
    simple: str
    detailed: str
    # From confidence agent
    confidence: float


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "StackHeal AI"}


@app.post("/analyze", response_model=PipelineResponse)
def analyze(body: AnalyzeRequest):
    """
    Run the full 7-agent StackHeal pipeline on the submitted code / log text.
    Returns a structured JSON result with detection, classification, root cause,
    fix suggestion, explanation, and confidence score.
    """
    if not body.code.strip():
        raise HTTPException(status_code=400, detail="code field must not be empty")

    try:
        result = run_stackheal_pipeline(body.code)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(exc)}")

    # Normalise keys that might be missing (agents always return defaults, but be safe)
    return PipelineResponse(
        type=result.get("type", "UnknownError"),
        message=result.get("message", ""),
        line=result.get("line", -1),
        snippet=result.get("snippet", ""),
        severity=result.get("severity", "Medium"),
        language=result.get("language", body.language or "Unknown"),
        root_cause=result.get("root_cause", ""),
        description=result.get("description", ""),
        correctedCode=result.get("correctedCode", ""),
        simple=result.get("simple", ""),
        detailed=result.get("detailed", ""),
        confidence=result.get("confidence", 0.5),
    )