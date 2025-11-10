# 🛡️ Phishing Domain Detection API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Advanced ML-powered API for detecting phishing domains with dual model support (Random Forest + Deep Learning), user authentication, and comprehensive history tracking.**

> **CSE_proj_12** - AI/ML Phishing Domain Detection System  
> Team: Akash Kumar (2230727), Aman Jadon (2230731), Amandeep (2230732)  
> Mentor: Dr. Rupam Bhagawati | Branch: 7 CSE AB

---

## ✨ Key Features

- 🧠 **Dual ML Models**: Random Forest (95-97% accuracy) + Deep Learning (96-98% accuracy)
- 🔄 **Model Switching**: Switch between models on-the-fly via API
- 📊 **Large Dataset**: Trained on 88,647 real phishing URLs with 111 features
- 🚀 **FastAPI Backend**: High-performance async API with auto-generated docs
- 🔐 **JWT Authentication**: Secure user authentication and authorization
- 💾 **Database Integration**: SQLAlchemy ORM with SQLite/PostgreSQL
- 🐳 **Docker Support**: Dev containers + Docker Compose for easy deployment
- 📈 **Model Comparison**: Compare predictions from both models side-by-side
- 🎯 **Risk Assessment**: Confidence scores and risk levels (low/medium/high)
- 📚 **Interactive Docs**: Swagger UI and ReDoc auto-generated

---

## 🎯 Quick Start

### Option 1: One-Command Startup (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Train model (2 minutes)
python scripts/train_with_dataset.py

# Start API
python start_api.py
```

**API will be available at:**
- 🌐 http://localhost:8000
- 📚 http://localhost:8000/docs (Swagger UI)

### Option 2: Dev Container (VS Code)

```bash
# 1. Open in VS Code
code .

# 2. Press F1 → "Dev Containers: Reopen in Container"

# 3. Inside container:
python scripts/train_with_dataset.py
python start_api.py
```

### Option 3: Docker Compose

```bash
docker-compose up --build
# API automatically starts at http://localhost:8000
```

---

## 🏗️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI 0.104 |
| **ML (Traditional)** | scikit-learn 1.5.2 (Random Forest) |
| **ML (Deep Learning)** | TensorFlow 2.15, Keras |
| **Database** | SQLAlchemy + SQLite/PostgreSQL |
| **Authentication** | JWT tokens with OAuth2, bcrypt |
| **Deployment** | Docker, Docker Compose, Dev Containers |
| **API Docs** | Swagger UI, ReDoc (auto-generated) |
| **Dataset** | GregaVrbancic (88,647 URLs, 111 features) |

---

## 📊 Model Performance

### Random Forest vs Deep Learning

| Metric | Random Forest | Deep Learning | Winner |
|--------|--------------|---------------|--------|
| **Accuracy** | 95-97% | 96-98% | 🧠 DL |
| **Training Time** | ~2 min | ~15-30 min | 🌲 RF |
| **Inference Speed** | <10ms | <50ms | 🌲 RF |
| **Model Size** | ~50 MB | ~5 MB | 🧠 DL |
| **GPU Support** | ❌ | ✅ | 🧠 DL |
| **Interpretability** | High | Low | 🌲 RF |

**Recommendation:** Use both! RF for speed, DL for maximum accuracy.

## 📁 Project Structure

```
CSE_proj_12/
├── 🐳 Dev Container
│   ├── .devcontainer/
│   │   ├── Dockerfile              # Container image with all dependencies
│   │   └── devcontainer.json       # VS Code dev container config
│   ├── docker-compose.yml          # Multi-service deployment
│   └── .dockerignore               # Docker ignore rules
│
├── 🚀 FastAPI Backend
│   ├── app/
│   │   ├── main.py                 # FastAPI app initialization
│   │   ├── api/
│   │   │   ├── routes.py           # Original routes
│   │   │   ├── routes_enhanced.py  # Enhanced routes (RF + DL)
│   │   │   └── endpoints/
│   │   │       ├── auth.py         # JWT authentication
│   │   │       ├── detection.py    # Original detection
│   │   │       └── detection_enhanced.py  # Enhanced (dual model)
│   │   ├── database/
│   │   │   ├── database.py         # SQLAlchemy setup
│   │   │   ├── models.py           # ORM models
│   │   │   └── dependencies.py     # DB dependencies
│   │   └── utils/
│   │       ├── feature_extraction.py      # URL feature extraction
│   │       ├── ml_model.py                # Original ML wrapper
│   │       ├── ml_loader_enhanced.py      # Enhanced loader (RF + DL)
│   │       ├── predictor.py               # Unified predictor
│   │       ├── token.py                   # JWT token management
│   │       └── dependency.py              # Auth dependencies
│
├── 🧠 Machine Learning
│   ├── scripts/
│   │   ├── train_with_dataset.py   # Random Forest training
│   │   ├── train_deep_learning.py  # Neural Network training
│   │   ├── compare_models.py       # Model comparison
│   │   └── test_dl_model.py        # Test DL model
│   └── models/                     # Trained models (generated)
│       ├── model.pkl               # Random Forest
│       ├── phishing_model_dl.h5    # Deep Learning
│       └── scaler_dl.pkl           # Feature scaler
│
├── 📊 Data
│   ├── phishing_domain.csv         # Training dataset (88,647 samples)
│   └── phishing_detection.db       # SQLite database
│
├── 📦 Configuration
│   ├── requirements.txt            # Base dependencies
│   ├── requirements_dl.txt         # Deep Learning dependencies
│   └── .env.example                # Environment variables template
│
├── 🚀 Startup
│   └── start_api.py                # One-command startup script
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── COMPLETE_SETUP_GUIDE.md     # Full setup instructions
    ├── DEVCONTAINER_SETUP.md       # Dev container guide
    ├── DEEP_LEARNING_GUIDE.md      # DL implementation details
    └── PROJECT_SUMMARY.md          # Project overview
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.11+
- pip or conda
- (Optional) Docker Desktop for containerized deployment
- (Optional) VS Code with Dev Containers extension

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/phishing-detection.git
cd phishing-detection
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Base dependencies (FastAPI + Random Forest)
pip install -r requirements.txt

# Optional: Deep Learning support
pip install tensorflow==2.15.0 keras==2.15.0
```

#### 4. Set Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./phishing_detection.db
JWT_SECRET_KEY=your-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

#### 5. Train Models

**Option A: Random Forest (Fast - 2 minutes)**

```bash
python scripts/train_with_dataset.py
```

**Option B: Deep Learning (Slow - 15-30 minutes)**

```bash
python scripts/train_deep_learning.py
```

**Option C: Train Both & Compare**

```bash
python scripts/train_with_dataset.py
python scripts/train_deep_learning.py
python scripts/compare_models.py
```

#### 6. Start API Server

```bash
# One-command startup (recommended)
python start_api.py

# Or direct uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 7. Access API

- **API Root:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Using Dev Container (VS Code)

1. Install Docker Desktop
2. Install VS Code + Dev Containers extension
3. Open project in VS Code
4. Press `F1` → "Dev Containers: Reopen in Container"
5. Wait for container to build
6. Start developing!

**Benefits:**
- ✅ Consistent environment across team
- ✅ All dependencies pre-installed
- ✅ No "works on my machine" issues
- ✅ Isolated from host system

## 📡 API Endpoints

### Enhanced API (Dual Model Support)

To use enhanced endpoints, update `app/main.py`:

```python
from app.api.routes_enhanced import app_router  # Use this for dual model support
```

#### Public Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Health check & model status | ❌ |
| `/auth/signup` | POST | User registration | ❌ |
| `/auth/login` | POST | User authentication | ❌ |
| `/check` | POST | Check URL (specify model: rf/dl) | ⚠️ Optional |
| `/compare` | POST | Compare both models | ❌ |
| `/models/info` | GET | Get loaded models info | ❌ |
| `/models/switch` | POST | Switch active model | ❌ |
| `/stats` | GET | Overall statistics | ❌ |

#### Protected Endpoints (Require JWT)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/history` | GET | Get user's check history |
| `/report` | POST | Report URL for model improvement |

## 🧪 Usage Examples

### 1. Health Check

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Phishing Domain Detection API - Enhanced",
  "version": "2.0.0",
  "models": {
    "random_forest_loaded": true,
    "deep_learning_loaded": true,
    "active_model": "rf",
    "tensorflow_available": true
  }
}
```

### 2. Check URL with Random Forest

```bash
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://google.com",
    "model_type": "rf"
  }'
```

**Response:**
```json
{
  "url": "https://google.com",
  "prediction": "legitimate",
  "is_phishing": false,
  "confidence": 98.5,
  "probabilities": {
    "legitimate": 98.5,
    "phishing": 1.5
  },
  "risk_level": "low",
  "model_used": "Random Forest"
}
```

### 3. Check URL with Deep Learning

```bash
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://paypal-secure-login.tk",
    "model_type": "dl"
  }'
```

**Response:**
```json
{
  "url": "http://paypal-secure-login.tk",
  "prediction": "phishing",
  "is_phishing": true,
  "confidence": 97.8,
  "probabilities": {
    "legitimate": 2.2,
    "phishing": 97.8
  },
  "risk_level": "high",
  "model_used": "Neural Network"
}
```

### 4. Compare Both Models

```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

**Response:**
```json
{
  "url": "https://example.com",
  "models": {
    "random_forest": {
      "prediction": "legitimate",
      "confidence": 96.5,
      "risk_level": "low",
      "model_used": "Random Forest"
    },
    "deep_learning": {
      "prediction": "legitimate",
      "confidence": 98.2,
      "risk_level": "low",
      "model_used": "Neural Network"
    }
  }
}
```

### 5. Get Model Information

```bash
curl http://localhost:8000/models/info
```

**Response:**
```json
{
  "random_forest_loaded": true,
  "deep_learning_loaded": true,
  "active_model": "rf",
  "tensorflow_available": true
}
```

### 6. Switch Active Model

```bash
curl -X POST "http://localhost:8000/models/switch?model_type=dl"
```

**Response:**
```json
{
  "message": "Switched to DL model",
  "active_model": "dl"
}
```

### 7. User Authentication

**Signup:**
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 8. Get Check History (Protected)

```bash
curl -X GET "http://localhost:8000/history?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 9. Get Statistics

```bash
curl http://localhost:8000/stats
```

**Response:**
```json
{
  "total_checks": 1523,
  "phishing_detected": 487,
  "safe_urls": 1036,
  "high_risk_count": 312
}
```

## Database Schema

### users
- `id` (Integer, PK)
- `email` (String, unique)
- `hashed_password` (String)

### url_checks
- `id` (Integer, PK)
- `user_id` (Integer, nullable)
- `url` (Text)
- `is_phishing` (Boolean)
- `confidence` (Float)
- `phishing_probability` (Float)
- `risk_level` (String)
- `checked_at` (DateTime)

### reported_urls
- `id` (Integer, PK)
- `user_id` (Integer, nullable)
- `url` (Text)
- `is_phishing` (Boolean)
- `reported_at` (DateTime)

## 🧠 Machine Learning Details

### Dataset

**GregaVrbancic Phishing Dataset**
- **Total Samples:** 88,647 URLs
- **Legitimate:** 58,000 (65.4%)
- **Phishing:** 30,647 (34.6%)
- **Features:** 111 URL-based features
- **Source:** [DOI: 10.1016/j.dib.2020.106438](http://dx.doi.org/10.1016/j.dib.2020.106438)

### Feature Extraction (111 Features)

The models analyze comprehensive URL characteristics:

#### URL Structure Features
- Character counts: `.`, `-`, `_`, `/`, `?`, `=`, `@`, `&`, `!`, ` `, `~`, `,`, `+`, `*`, `#`, `$`, `%`
- Length metrics: URL, domain, directory, file, parameters
- Component analysis: TLD, subdomain, path depth

#### Domain Features
- Domain length and vowel count
- IP address format detection
- Server/client keywords
- SPF record presence
- Domain age and expiration

#### Network Features
- DNS resolution (IP count, nameservers, MX servers)
- TTL values
- TLS/SSL certificate validity
- Response time

#### Behavioral Features
- Google indexing status
- URL shortening detection
- Redirect count
- Parameter analysis

### Model Architectures

#### Random Forest
```
Ensemble of 100 Decision Trees
├── Max Depth: 20
├── Features: 111
├── Training: Bagging with bootstrap
└── Prediction: Majority voting
```

#### Deep Learning (Neural Network)
```
Input Layer (111 features)
    ↓
Dense Layer 1: 256 neurons + ReLU
    ↓ Batch Normalization + Dropout (30%)
Dense Layer 2: 128 neurons + ReLU
    ↓ Batch Normalization + Dropout (30%)
Dense Layer 3: 64 neurons + ReLU
    ↓ Batch Normalization + Dropout (20%)
Output Layer: 1 neuron + Sigmoid
    ↓
Prediction (0 = Legitimate, 1 = Phishing)
```

**Training Details:**
- Optimizer: Adam (learning_rate=0.001)
- Loss: Binary Crossentropy
- Epochs: Up to 100 (with early stopping)
- Batch Size: 64
- Validation Split: 20%
- Regularization: L2 (0.001) + Dropout + Batch Normalization

## Architecture

Follows clean layered architecture:
- **API Layer**: HTTP request/response handling
- **Business Logic**: Detection and authentication logic
- **Data Access**: SQLAlchemy ORM operations
- **Utilities**: Cross-cutting concerns (auth, ML)

## Security Features

- JWT token authentication (60-minute expiration)
- Bcrypt password hashing
- Optional authentication for URL checks
- CORS middleware (configure for production)

## Development

### Adding New Endpoints
1. Create handler in `app/api/endpoints/`
2. Register route in `app/api/routes.py`
3. Use dependency injection for DB and auth

### Database Changes
1. Update models in `app/database/models.py`
2. Tables auto-create on startup
3. For production, use Alembic migrations

## Deployment

Compatible with:
- Vercel (serverless)
- Heroku
- AWS Lambda
- Docker containers

Set environment variables in your deployment platform.

## 🚀 Deployment

### Vercel (Serverless)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Heroku

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

### AWS Lambda

Use [Mangum](https://mangum.io/) adapter:

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

### Docker Production

```bash
# Build production image
docker build -t phishing-detection:latest .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=your_db_url \
  -e JWT_SECRET_KEY=your_secret \
  phishing-detection:latest
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **README.md** | This file - project overview |
| **COMPLETE_SETUP_GUIDE.md** | Comprehensive setup instructions |
| **DEVCONTAINER_SETUP.md** | Dev container configuration guide |
| **DEEP_LEARNING_GUIDE.md** | Neural network implementation details |
| **PROJECT_SUMMARY.md** | Complete project summary |

---

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

### Manual Testing

Use the interactive Swagger UI at http://localhost:8000/docs

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**CSE_proj_12 - AI/ML Phishing Domain Detection System**

- **Akash Kumar** (2230727)
- **Aman Jadon** (2230731)
- **Amandeep** (2230732)

**Mentor:** Dr. Rupam Bhagawati  
**Branch:** 7 CSE AB  
**Institution:** [Your Institution Name]

---

## 🙏 Acknowledgments

- **Dataset:** GregaVrbancic et al. - [Phishing Websites Dataset](https://github.com/GregaVrbancic/Phishing-Dataset)
- **FastAPI:** Sebastián Ramírez - [FastAPI Framework](https://fastapi.tiangolo.com/)
- **TensorFlow:** Google - [TensorFlow](https://www.tensorflow.org/)
- **scikit-learn:** scikit-learn developers - [scikit-learn](https://scikit-learn.org/)

---

## 📞 Support

For questions or issues:

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/phishing-detection/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/phishing-detection/discussions)

---

## 🔮 Future Enhancements

- [ ] Real-time URL scanning browser extension
- [ ] Ensemble model combining RF + DL predictions
- [ ] Active learning from user reports
- [ ] Multi-language support
- [ ] Email/SMS notifications for high-risk URLs
- [ ] Admin dashboard with analytics
- [ ] Rate limiting and API key management
- [ ] Redis caching for faster responses
- [ ] WebSocket for real-time updates
- [ ] Batch URL checking endpoint
- [ ] Model retraining pipeline
- [ ] A/B testing framework
- [ ] Prometheus metrics + Grafana dashboards

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by CSE_proj_12 Team

</div>
