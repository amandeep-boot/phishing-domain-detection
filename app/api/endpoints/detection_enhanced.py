"""
Enhanced Detection Endpoint
Supports both Random Forest and Deep Learning models
"""

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime
from app.database.dependencies import get_db
from app.database.models import URLCheck, ReportedURL
from app.utils.dependency import get_current_user_optional
from app.utils.predictor import predictor
from app.utils.feature_extraction_full import full_feature_extractor
from app.utils.ml_loader_enhanced import model_loader

class URLCheckRequest(BaseModel):
    url: str
    model_type: Optional[Literal['rf', 'dl']] = None  # None = use active model

class URLCheckResponse(BaseModel):
    url: str
    prediction: str
    is_phishing: bool
    confidence: float
    probabilities: dict
    risk_level: str
    model_used: str

class CompareModelsRequest(BaseModel):
    url: str

class ModelInfoResponse(BaseModel):
    random_forest_loaded: bool
    deep_learning_loaded: bool
    active_model: Optional[str]
    tensorflow_available: bool

class ReportRequest(BaseModel):
    url: str
    is_phishing: bool

class HistoryResponse(BaseModel):
    id: int
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str
    checked_at: datetime

class StatsResponse(BaseModel):
    total_checks: int
    phishing_detected: int
    safe_urls: int
    high_risk_count: int

async def root():
    """Health check endpoint"""
    model_info = model_loader.get_model_info()
    return {
        "status": "healthy",
        "service": "Phishing Domain Detection API - Enhanced",
        "version": "2.0.0",
        "models": model_info
    }

async def check_url(
    request: URLCheckRequest,
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_current_user_optional)
):
    """
    Check if a URL is phishing
    
    - **url**: URL to check
    - **model_type**: 'rf' (Random Forest), 'dl' (Deep Learning), or None (use active)
    """
    if not model_loader.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="No model loaded. Train a model first."
        )
    
    try:
        # Predict using specified or active model
        result = predictor.predict(request.url, model_type=request.model_type)
        
        # Store in database
        url_check = URLCheck(
            user_id=user_id,
            url=request.url,
            is_phishing=result['is_phishing'],
            confidence=result['confidence'],
            phishing_probability=result['probabilities']['phishing'],
            risk_level=result['risk_level']
        )
        db.add(url_check)
        db.commit()
        
        return URLCheckResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def compare_models(
    request: CompareModelsRequest,
    db: Session = Depends(get_db)
):
    """
    Compare predictions from both Random Forest and Deep Learning models
    """
    try:
        results = predictor.compare_models(request.url)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_model_info():
    """Get information about loaded models"""
    return ModelInfoResponse(**model_loader.get_model_info())

async def switch_model(
    model_type: Literal['rf', 'dl'] = Query(..., description="Model to activate")
):
    """Switch active model"""
    success = model_loader.set_active_model(model_type)
    
    if success:
        return {
            "message": f"Switched to {model_type.upper()} model",
            "active_model": model_loader.active_model
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{model_type.upper()} model not loaded"
        )

async def report_url(
    request: ReportRequest,
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_current_user_optional)
):
    """Report a URL for model improvement"""
    reported = ReportedURL(
        user_id=user_id,
        url=request.url,
        is_phishing=request.is_phishing
    )
    db.add(reported)
    db.commit()
    
    return {"message": "URL reported successfully", "url": request.url}

async def get_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_optional)
):
    """Get user's URL check history"""
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    checks = db.query(URLCheck)\
        .filter(URLCheck.user_id == user_id)\
        .order_by(URLCheck.checked_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        HistoryResponse(
            id=check.id,
            url=check.url,
            is_phishing=check.is_phishing,
            confidence=check.confidence,
            risk_level=check.risk_level,
            checked_at=check.checked_at
        )
        for check in checks
    ]

async def get_stats(db: Session = Depends(get_db)):
    """Get overall statistics"""
    total = db.query(func.count(URLCheck.id)).scalar()
    phishing = db.query(func.count(URLCheck.id))\
        .filter(URLCheck.is_phishing == True).scalar()
    high_risk = db.query(func.count(URLCheck.id))\
        .filter(URLCheck.risk_level == "high").scalar()
    
    return StatsResponse(
        total_checks=total or 0,
        phishing_detected=phishing or 0,
        safe_urls=(total or 0) - (phishing or 0),
        high_risk_count=high_risk or 0
    )
