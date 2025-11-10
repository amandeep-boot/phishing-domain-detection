# 🐳 Dev Container Setup Guide
## CSE_proj_12 - Phishing Detection with FastAPI + Deep Learning

**Complete development environment with Docker support**

---

## 🚀 Quick Start

### Option 1: VS Code Dev Container (Recommended)

1. **Prerequisites:**
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Install [VS Code](https://code.visualstudio.com/)
   - Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Dev Container:**
   ```bash
   # Open VS Code
   code .
   
   # Press F1 or Ctrl+Shift+P
   # Type: "Dev Containers: Reopen in Container"
   # Select it and wait for container to build
   ```

3. **Container will automatically:**
   - Install Python 3.11
   - Install all dependencies (FastAPI, scikit-learn, TensorFlow)
   - Forward port 8000 (API) and 3000 (frontend)
   - Set up development environment

### Option 2: Docker Compose

```bash
# Build and start services
docker-compose up --build

# API will be available at:
# http://localhost:8000
# http://localhost:8000/docs (Swagger UI)
```

### Option 3: Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install Deep Learning support
pip install tensorflow==2.15.0 keras==2.15.0

# Run API
uvicorn app.main:app --reload
```

---

## 📁 Project Structure

```
.
├── .devcontainer/
│   ├── Dockerfile              # Dev container image
│   └── devcontainer.json       # VS Code dev container config
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── detection.py    # Original detection
│   │   │   └── detection_enhanced.py  # Enhanced (RF + DL)
│   │   ├── routes.py           # Original routes
│   │   └── routes_enhanced.py  # Enhanced routes
│   ├── database/
│   │   ├── database.py         # Database setup
│   │   ├── models.py           # SQLAlchemy models
│   │   └── dependencies.py     # DB dependencies
│   ├── utils/
│   │   ├── feature_extraction.py      # URL feature extraction
│   │   ├── ml_model.py                # Original ML model
│   │   ├── ml_loader.py               # Original loader
│   │   ├── ml_loader_enhanced.py      # Enhanced loader (RF + DL)
│   │   ├── predictor.py               # Unified predictor
│   │   ├── token.py                   # JWT tokens
│   │   └── dependency.py              # Auth dependencies
│   └── main.py                 # FastAPI app
├── scripts/
│   ├── train_model.py          # Sample training
│   ├── train_with_dataset.py   # Random Forest training
│   ├── train_deep_learning.py  # Deep Learning training
│   ├── test_dl_model.py        # Test DL model
│   └── compare_models.py       # Compare RF vs DL
├── models/                     # Trained models (generated)
│   ├── model.pkl              # Random Forest
│   ├── phishing_model_dl.h5   # Deep Learning
│   └── scaler_dl.pkl          # Feature scaler
├── phishing_domain.csv         # Training dataset
├── requirements.txt            # Base dependencies
├── requirements_dl.txt         # Deep Learning dependencies
├── docker-compose.yml          # Docker Compose config
└── DEVCONTAINER_SETUP.md       # This file
```

---

## 🔧 Dev Container Features

### Installed Tools:
- ✅ Python 3.11
- ✅ FastAPI + Uvicorn
- ✅ scikit-learn (Random Forest)
- ✅ TensorFlow + Keras (Deep Learning)
- ✅ SQLAlchemy (Database)
- ✅ Git
- ✅ curl

### VS Code Extensions:
- Python
- Pylance (IntelliSense)
- Jupyter (for notebooks)

### Port Forwarding:
- **8000** - FastAPI Backend
- **3000** - Frontend (if added)

---

## 🎯 Training Models in Dev Container

### 1. Train Random Forest (Fast - 2 minutes)

```bash
# Inside dev container terminal
python scripts/train_with_dataset.py
```

**Output:**
```
✓ Dataset loaded: (88647, 112)
✓ Training samples: 70,917
✓ Testing samples: 17,730
✓ Accuracy: 96.23%
✓ Model saved to model.pkl
```

### 2. Train Deep Learning (15-30 minutes)

```bash
# Inside dev container terminal
python scripts/train_deep_learning.py
```

**Output:**
```
Epoch 1/100
732/732 [======] - 5s - loss: 0.2145 - accuracy: 0.9234
...
Epoch 50/100
732/732 [======] - 4s - loss: 0.0456 - accuracy: 0.9823
✓ Accuracy: 97.23%
✓ Model saved to models/phishing_model_dl.h5
```

### 3. Compare Both Models

```bash
python scripts/compare_models.py
```

---

## 🌐 Running the API

### Start API Server:

```bash
# Inside dev container
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API:

- **API Root:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📡 API Endpoints

### Enhanced Endpoints (Support both RF and DL):

#### 1. Check URL
```bash
POST /check
{
  "url": "https://example.com",
  "model_type": "rf"  # or "dl" or null (use active)
}
```

#### 2. Compare Models
```bash
POST /compare
{
  "url": "https://example.com"
}
```

#### 3. Get Model Info
```bash
GET /models/info
```

Response:
```json
{
  "random_forest_loaded": true,
  "deep_learning_loaded": true,
  "active_model": "rf",
  "tensorflow_available": true
}
```

#### 4. Switch Active Model
```bash
POST /models/switch?model_type=dl
```

### Original Endpoints:

- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /report` - Report URL
- `GET /history` - Check history
- `GET /stats` - Statistics

---

## 🔄 Switching Between Enhanced and Original API

### Use Enhanced API (Recommended):

Edit `app/main.py`:
```python
# Change this line:
from app.api.routes import app_router

# To this:
from app.api.routes_enhanced import app_router
```

### Use Original API:

Keep the default import in `app/main.py`.

---

## 🐛 Troubleshooting

### Issue: Container build fails

**Solution:**
```bash
# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Issue: TensorFlow not working

**Solution:**
```bash
# Inside container
pip install tensorflow==2.15.0
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Issue: Models not loading

**Solution:**
```bash
# Train models first
python scripts/train_with_dataset.py
python scripts/train_deep_learning.py
```

---

## 🧪 Testing

### Test API Endpoints:

```bash
# Health check
curl http://localhost:8000/

# Check URL (Random Forest)
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com", "model_type": "rf"}'

# Check URL (Deep Learning)
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com", "model_type": "dl"}'

# Compare both models
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

---

## 📊 Performance Comparison

| Aspect | Random Forest | Deep Learning |
|--------|--------------|---------------|
| Training Time | ~2 min | ~15-30 min |
| Accuracy | 95-97% | 96-98% |
| Inference | <10ms | <50ms |
| Model Size | ~50 MB | ~5 MB |
| GPU Support | ❌ | ✅ |

---

## 🎓 For Your Project

### Presentation Points:

1. **Full-Stack Implementation:**
   - ✅ FastAPI backend
   - ✅ SQLAlchemy database
   - ✅ JWT authentication
   - ✅ Docker containerization

2. **Dual ML Approach:**
   - ✅ Random Forest (traditional ML)
   - ✅ Neural Network (deep learning)
   - ✅ Model comparison API

3. **Production-Ready:**
   - ✅ Dev container setup
   - ✅ Docker Compose
   - ✅ API documentation (Swagger)
   - ✅ Database persistence

4. **Dataset:**
   - ✅ 88,647 real phishing URLs
   - ✅ 111 features per URL
   - ✅ GregaVrbancic dataset

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **TensorFlow Docs:** https://www.tensorflow.org/
- **Docker Docs:** https://docs.docker.com/
- **Dev Containers:** https://code.visualstudio.com/docs/devcontainers/containers

---

## ✅ Checklist

- [ ] Install Docker Desktop
- [ ] Install VS Code + Dev Containers extension
- [ ] Open project in dev container
- [ ] Train Random Forest model
- [ ] (Optional) Train Deep Learning model
- [ ] Start FastAPI server
- [ ] Test API endpoints
- [ ] Review Swagger docs at /docs

---

**Status:** ✅ Ready for Development  
**Last Updated:** November 10, 2025  
**Team:** CSE_proj_12
