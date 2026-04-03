"""
FastAPI REST API for the Copyright Detection System.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from main import CopyrightDetectionSystem


# Initialize FastAPI app
app = FastAPI(
    title="AI Copyright Detection API",
    description="Detect and attribute copyrighted content in AI-generated text",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system instance
system: Optional[CopyrightDetectionSystem] = None


# Request/Response models
class DetectionRequest(BaseModel):
    """Request model for copyright detection."""
    text: str = Field(..., min_length=1, description="Text to check for copyright issues")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of matches to return")
    use_purpose: Optional[str] = Field("general", description="Intended use purpose")
    citation_style: Optional[str] = Field("APA", description="Citation format style")


class BatchDetectionRequest(BaseModel):
    """Request model for batch detection."""
    texts: List[str] = Field(..., min_items=1, max_items=50, description="List of texts to check")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Matches per text")


class QuickCheckRequest(BaseModel):
    """Request for quick copyright check."""
    text: str = Field(..., min_length=1, description="Text to check")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    vector_count: int
    model_loaded: bool


class DetectionResponse(BaseModel):
    """Detection result response."""
    success: bool
    risk_level: str
    highest_similarity: float
    matches_found: int
    verbatim_detected: bool
    compliance_status: str
    requires_license: bool
    overall_recommendation: str
    report: dict


class QuickCheckResponse(BaseModel):
    """Quick check response."""
    has_issues: bool
    risk_level: str
    similarity: float


@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup."""
    global system
    print("Initializing Copyright Detection System...")
    system = CopyrightDetectionSystem()
    system.initialize()
    print("System initialized and ready.")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": "AI Copyright Detection API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check system health."""
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    stats = system.vector_store.get_stats()
    return HealthResponse(
        status="healthy",
        vector_count=stats["total_vectors"],
        model_loaded=system.embedding_engine is not None
    )


@app.post("/detect", response_model=DetectionResponse, tags=["Detection"])
async def detect_copyright(request: DetectionRequest):
    """
    Detect potential copyright issues in text.
    
    Returns detailed analysis with attribution and compliance recommendations.
    """
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        report = system.analyze(
            text=request.text,
            top_k=request.top_k,
            use_purpose=request.use_purpose,
            citation_style=request.citation_style
        )
        
        return DetectionResponse(
            success=True,
            risk_level=report.detection_summary["risk_level"],
            highest_similarity=report.detection_summary["highest_similarity"],
            matches_found=report.detection_summary["matches_found"],
            verbatim_detected=report.detection_summary["verbatim_detected"],
            compliance_status=report.compliance_assessment["status"],
            requires_license=report.compliance_assessment["requires_license"],
            overall_recommendation=report.overall_recommendation,
            report={
                "report_id": report.report_id,
                "timestamp": report.timestamp,
                "detection_summary": report.detection_summary,
                "attributions": report.attributions,
                "compliance_assessment": report.compliance_assessment
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/quick-check", response_model=QuickCheckResponse, tags=["Detection"])
async def quick_check(request: QuickCheckRequest):
    """
    Perform a quick copyright check.
    
    Returns simple pass/fail result with risk level.
    """
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        has_issues, risk_level, similarity = system.detector.quick_check(request.text)
        return QuickCheckResponse(
            has_issues=has_issues,
            risk_level=risk_level,
            similarity=similarity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-detect", tags=["Detection"])
async def batch_detect(request: BatchDetectionRequest):
    """
    Detect copyright issues in multiple texts.
    
    Returns summary results for each text.
    """
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        results = []
        for text in request.texts:
            has_issues, risk_level, similarity = system.detector.quick_check(text)
            results.append({
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "has_issues": has_issues,
                "risk_level": risk_level,
                "similarity": similarity
            })
        
        return {
            "success": True,
            "total_checked": len(results),
            "issues_found": sum(1 for r in results if r["has_issues"]),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", tags=["System"])
async def get_stats():
    """Get system statistics."""
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    stats = system.vector_store.get_stats()
    return {
        "vector_store": stats,
        "embedding_model": system.embedding_engine.model_name,
        "embedding_dimension": system.embedding_engine.get_embedding_dimension()
    }


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api()
    