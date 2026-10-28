from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify backend service and database connectivity."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        raise HTTPException(status_code=503, detail={"status": "degraded", "database": db_status})

    return {
        "status": "healthy",
        "database": db_status,
        "service": "Terminal Quiz Master API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
