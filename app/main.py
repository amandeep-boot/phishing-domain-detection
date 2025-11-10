from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api.routes_enhanced import app_router
import os

# Create FastAPI app
app = FastAPI(
    title="Phishing Domain Detection API",
    description="ML-powered API for detecting phishing domains",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def startup():
    """Initialize database and load ML models"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Load both Random Forest and Deep Learning models
    from app.utils.ml_loader_enhanced import model_loader
    
    print("\n" + "="*60)
    print("🔧 Loading ML Models")
    print("="*60)
    
    # Load Random Forest
    rf_loaded = model_loader.load_random_forest('model_full.pkl')
    
    # Load Deep Learning
    dl_loaded = model_loader.load_deep_learning(
        model_path='models/phishing_model_dl.h5',
        scaler_path='models/scaler_dl.pkl'
    )
    
    if rf_loaded and dl_loaded:
        print("\n✅ Both models loaded successfully!")
        print(f"   Active model: {model_loader.active_model.upper()}")
    elif dl_loaded:
        print("\n✅ Deep Learning model ready!")
        print("   ⚠️  Random Forest not available - train with: python scripts/train_with_dataset.py")
    elif rf_loaded:
        print("\n✅ Random Forest model ready!")
    else:
        print("\n❌ No models loaded")
    
    print("="*60 + "\n")

# Include all routes
app.include_router(app_router)
