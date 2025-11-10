"""
Enhanced API Routes
Supports both Random Forest and Deep Learning models
"""

from fastapi import APIRouter
from app.api.endpoints import auth
from app.api.endpoints import detection_enhanced as detection

# Create main router
app_router = APIRouter()

# ========== Authentication Routes ==========
app_router.post("/auth/signup", tags=["Authentication"])(auth.signup)
app_router.post("/auth/login", tags=["Authentication"])(auth.login)

# ========== Detection Routes (Enhanced) ==========
app_router.get("/", tags=["Health"])(detection.root)

# URL checking with model selection
app_router.post(
    "/check",
    tags=["Detection"],
    summary="Check URL for phishing",
    description="Check if a URL is phishing using RF or DL model"
)(detection.check_url)

# Compare both models
app_router.post(
    "/compare",
    tags=["Detection"],
    summary="Compare both models",
    description="Get predictions from both Random Forest and Deep Learning"
)(detection.compare_models)

# Model management
app_router.get(
    "/models/info",
    tags=["Models"],
    summary="Get model information",
    description="Check which models are loaded"
)(detection.get_model_info)

app_router.post(
    "/models/switch",
    tags=["Models"],
    summary="Switch active model",
    description="Switch between RF and DL models"
)(detection.switch_model)

# Reporting and history
app_router.post("/report", tags=["Reporting"])(detection.report_url)
app_router.get("/history", tags=["History"])(detection.get_history)
app_router.get("/stats", tags=["Statistics"])(detection.get_stats)
