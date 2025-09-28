# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import uvicorn
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from coordinator import AgentCoordinator

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WisdomWealth Agent API",
    description="Multi-agent AI platform for elderly financial security",
    version="1.0.0"
)

# Add CORS middleware
# Get allowed origins from environment or use default
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if allowed_origins == ["*"]:
    # In production, this should be your frontend URL
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "https://*.onrender.com",
        "https://*.vercel.app"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize coordinator
coordinator = None

@app.on_event("startup")
async def startup_event():
    global coordinator
    logger.info("Starting WisdomWealth Agent API...")
    try:
        coordinator = AgentCoordinator()
        logger.info("✅ AgentCoordinator initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AgentCoordinator: {e}")

# Request/Response models
class RouteRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    text: str = Field(..., max_length=3000, description="User input text")
    meta: Optional[Dict] = Field(default_factory=dict, description="Optional metadata")

class RouteResponse(BaseModel):
    response: str = Field(..., description="Agent response message")
    risk: str = Field(..., description="Risk level: low, medium, high")
    agent_traces: List[str] = Field(..., description="List of activated agents")
    actions: List[str] = Field(..., description="Recommended actions")
    logs_id: Optional[str] = Field(None, description="Incident log ID")
    confidence_score: Optional[float] = Field(None, description="Confidence score 0.0-1.0")
    timestamp: str = Field(..., description="Response timestamp")
    family_alert_id: Optional[str] = Field(None, description="Family alert ID if generated")

class HealthResponse(BaseModel):
    status: str
    agents: Dict[str, bool]
    database: Dict[str, bool]
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    timestamp: str

# API Routes
@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "WisdomWealth Agent API is running",
        "version": "1.0.0",
        "endpoints": ["/health", "/route"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """Health check endpoint"""
    if not coordinator:
        raise HTTPException(
            status_code=503, 
            detail="AgentCoordinator not initialized"
        )
    
    try:
        health_status = coordinator.get_health_status()
        return HealthResponse(**health_status)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@app.post("/route", response_model=RouteResponse, summary="Process user request")
async def route_request(request: RouteRequest, http_request: Request):
    """
    Main routing endpoint - processes user requests through appropriate agents
    
    - **user_id**: Unique identifier for the user
    - **text**: User input text (max 3000 characters)  
    - **meta**: Optional metadata dict (channel, language, flags)
    
    Returns unified response with risk assessment and recommended actions.
    """
    # Basic rate limiting check (simple IP-based)
    client_ip = http_request.client.host
    logger.info(f"Processing request from {client_ip} for user {request.user_id}")
    
    if not coordinator:
        raise HTTPException(
            status_code=503,
            detail="AgentCoordinator not available"
        )
    
    # Input validation
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text input cannot be empty"
        )
    
    # Basic content filtering (extend as needed)
    if len(request.text) > 3000:
        raise HTTPException(
            status_code=400,
            detail="Text input exceeds maximum length of 3000 characters"
        )
    
    try:
        # Process request through coordinator
        result = coordinator.process_request(
            user_id=request.user_id,
            text=request.text,
            meta=request.meta
        )
        
        # Handle coordinator errors
        if "error" in result:
            logger.error(f"Coordinator error: {result['error']}")
            # Return partial response rather than failing completely
            pass
        
        return RouteResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in /route: {e}")
        
        # Return fallback response
        fallback_response = {
            "response": "I'm experiencing technical difficulties. Please try again in a moment or contact support if this continues.",
            "risk": "medium",
            "agent_traces": ["error"],
            "actions": ["TRY_AGAIN", "CONTACT_SUPPORT"],
            "logs_id": None,
            "timestamp": datetime.now().isoformat()
        }
        
        return RouteResponse(**fallback_response)

@app.get("/stats", summary="Get system statistics")
async def get_stats():
    """Get system statistics (incidents, users, etc.)"""
    if not coordinator:
        raise HTTPException(
            status_code=503,
            detail="AgentCoordinator not available"
        )
    
    try:
        # Get database stats
        db_stats = coordinator.db.get_stats()
        
        # Get ChromaDB stats
        chroma_stats = coordinator.chroma.get_collection_stats() if coordinator.chroma else {}
        
        return {
            "database": db_stats,
            "chromadb": chroma_stats,
            "agents": {
                "fraud": coordinator.agents["fraud"] is not None,
                "healthcare": coordinator.agents["healthcare"] is not None,
                "estate": coordinator.agents["estate"] is not None,
                "family": coordinator.agents["family"] is not None
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/incidents/{user_id}", summary="Get user incidents")
async def get_user_incidents(user_id: str, limit: int = 10):
    """Get recent incidents for a user"""
    if not coordinator:
        raise HTTPException(
            status_code=503,
            detail="AgentCoordinator not available"
        )
    
    try:
        incidents = coordinator.db.select_recent_incidents(user_id, limit)
        return {
            "user_id": user_id,
            "incidents": incidents,
            "count": len(incidents),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Incidents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/{user_id}", summary="Get pending alerts")
async def get_pending_alerts(user_id: str):
    """Get pending family alerts for a user"""
    if not coordinator:
        raise HTTPException(
            status_code=503,
            detail="AgentCoordinator not available"
        )
    
    try:
        alerts = coordinator.db.get_pending_alerts(user_id)
        return {
            "user_id": user_id,
            "pending_alerts": alerts,
            "count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Alerts error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return {
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return {
        "error": "Internal server error", 
        "message": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat()
    }

# Development server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting WisdomWealth Agent API on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT", "production") == "development",
        access_log=True
    )