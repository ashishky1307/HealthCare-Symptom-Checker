# 🏥 HealthAI Assistant - AI-Powered Medical Symptom Analysis System

## 📋 Overview

HealthAI Assistant is a comprehensive full-stack healthcare application that provides intelligent symptom analysis using advanced AI technology. The system combines a modern Next.js frontend with a robust FastAPI backend, enhanced with Retrieval-Augmented Generation (RAG) for accurate medical information retrieval.

**🎯 Key Capabilities:**
- 🤖 AI-powered symptom analysis using Groq LLM (Llama 3.3 70B)
- 📚 RAG-enhanced medical knowledge base with 5,345+ indexed medical document chunks
- 🚨 Real-time emergency detection and safety assessment
- 🔒 Secure user authentication and consultation history tracking
- 💻 Professional medical-themed UI with responsive design

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│  Next.js 14 + TypeScript + Tailwind CSS + Clerk Auth            │
│                    (Port: 3000)                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────────────┐
│                        Backend Layer                            │
│              FastAPI + Python 3.11                              │
│                    (Port: 8000)                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │  Auth Service  │  │ Symptom Analyzer│ │  History Service │   │
│  └────────────────┘  └────────────────┘  └──────────────────┘   │
│           │                   │                    │            │
│           └───────────────────┴────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      AI & Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐     │
│  │  Groq API    │  │  ChromaDB    │  │  Medical Knowledge │     │
│  │  (LLM)       │  │ (Vector DB)  │  │  Base (PDF)        │     │
│  └──────────────┘  └──────────────┘  └────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Database & Cache Layer                       │
│  ┌──────────────────────┐         ┌─────────────────────────┐   │
│  │  PostgreSQL (Aiven)  │         │   Redis (Cloud)         │   │
│  │  User & History Data │         │   Session Cache         │   │
│  └──────────────────────┘         └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### 💻 Frontend Technologies
- **Framework:** Next.js 14 (React 18)
- **Language:** TypeScript
- **Styling:** Tailwind CSS with custom design system
- **Authentication:** Clerk (OAuth + JWT)
- **Forms:** React Hook Form
- **HTTP Client:** Axios
- **Icons:** Lucide React
- **Notifications:** Sonner (Toast notifications)
- **State Management:** React Hooks

### ⚙️ Backend Technologies
- **Framework:** FastAPI 0.109+
- **Language:** Python 3.11+
- **ORM:** SQLAlchemy 2.0
- **Authentication:** JWT (python-jose)
- **Security:** Bcrypt password hashing
- **Validation:** Pydantic v2
- **CORS:** FastAPI CORS middleware

### 🤖 AI & Machine Learning
- **LLM Provider:** Groq Cloud
- **Model:** Llama 3.3 70B Versatile
- **Vector Database:** ChromaDB 0.4.22+
- **Embeddings:** SentenceTransformer (all-MiniLM-L6-v2)
- **RAG Framework:** LangChain
- **Document Processing:** PyPDF 3.17+
- **Token Management:** Tiktoken

### 💾 Databases & Caching
- **Primary Database:** PostgreSQL (Aiven Cloud)
- **Caching Layer:** Redis (Redis Labs Cloud)
- **Vector Storage:** ChromaDB (Local/Persistent)

### Additional Libraries
- **PDF Processing:** pypdf 6.4.0
- **ML Backend:** TensorFlow Keras 2.15+
- **GPU Monitoring:** nvidia-ml-py 11.495+
- **Environment:** python-dotenv
- **HTTP Requests:** httpx

---

## 📁 Project Structure

```
Health_Care/
│
├── backend-host/                    # FastAPI Backend Application
│   ├── api/                         # API Layer
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication endpoints
│   │   ├── deps.py                  # Dependency injection
│   │   └── routes.py                # Main API routes
│   │
│   ├── core/                        # Core Configuration
│   │   ├── __init__.py
│   │   ├── auth.py                  # JWT token handling
│   │   ├── config.py                # App settings & RAG config
│   │   └── security.py              # Password hashing
│   │
│   ├── db/                          # Database Layer
│   │   ├── __init__.py
│   │   ├── models.py                # SQLAlchemy models
│   │   └── session.py               # Database session management
│   │
│   ├── schemas/                     # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── input.py                 # Request schemas
│   │   └── output.py                # Response schemas
│   │
│   ├── services/                    # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── history_service.py       # Consultation history management
│   │   ├── rag_service.py           # RAG implementation
│   │   └── symptom_analyzer.py      # AI symptom analysis
│   │
│   ├── data/                        # Medical Knowledge Base
│   │   └── medical_knowledge/
│   │       ├── common_symptoms.txt
│   │       ├── emergency_conditions.txt
│   │       ├── chronic_conditions.txt
│   │       └── guideline-170-en.pdf # 409-page medical guideline
│   │
│   ├── scripts/                     # Utility Scripts
│   │   └── reindex_knowledge_base.py
│   │
│   ├── main.py                      # Application entry point
│   ├── load_env.py                  # Environment loader
│   └── requirements.txt             # Python dependencies
│
├── frontend/                        # Next.js Frontend Application
│   ├── src/
│   │   ├── app/                     # App Router (Next.js 14)
│   │   │   ├── layout.tsx           # Root layout with Clerk
│   │   │   ├── page.tsx             # Home page
│   │   │   ├── globals.css          # Global styles + animations
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx         # Sign-in page
│   │   │   └── sign-up/
│   │   │       └── page.tsx         # Sign-up page
│   │   │
│   │   ├── components/              # React Components
│   │   │   ├── SymptomForm.tsx      # Symptom input form
│   │   │   └── ResultCard.tsx       # Analysis results display
│   │   │
│   │   └── lib/                     # Utilities
│   │       ├── api.ts               # API client functions
│   │       └── utils.ts             # Helper functions
│   │
│   ├── middleware.ts                # Clerk auth middleware
│   ├── next.config.js               # Next.js configuration
│   ├── tailwind.config.js           # Tailwind CSS config
│   ├── tsconfig.json                # TypeScript config
│   └── package.json                 # Node dependencies
│


---

## 🔧 Core Components

### 🔌 Backend Components

#### 1. API Layer (`backend-host/api/`)
**Purpose:** Handles HTTP requests and routes

- **auth.py** - User registration, login, and authentication endpoints
- **routes.py** - Symptom analysis, emergency check, and history endpoints  
- **deps.py** - Dependency injection for database sessions and authentication

**Key Endpoints:**
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user information
- `POST /api/analyze` - Analyze symptoms with AI
- `POST /api/emergency-check` - Quick emergency keyword check
- `GET /api/history` - Retrieve consultation history
- `GET /api/health` - Backend health check

#### 2. Core Layer (`backend-host/core/`)
**Purpose:** Application configuration and security

- **config.py** - Environment settings, RAG configuration, database URLs
- **auth.py** - JWT token creation and verification
- **security.py** - Password hashing with bcrypt

#### 3. Database Layer (`backend-host/db/`)
**Purpose:** Data persistence and models

- **models.py** - SQLAlchemy ORM models
  - `User` - User accounts with authentication
  - `ConsultationHistory` - Symptom analysis records
- **session.py** - Database session factory and connection management

#### 4. Services Layer (`backend-host/services/`)
**Purpose:** Business logic and AI integration

- **symptom_analyzer.py** - Groq LLM integration with RAG enhancement
  - Analyzes symptoms using AI
  - Integrates RAG context from medical knowledge base
  - Emergency detection and safety checks
  - Structured medical response generation

- **rag_service.py** - Retrieval-Augmented Generation implementation
  - ChromaDB vector database management
  - SentenceTransformer embeddings
  - PDF and text document processing
  - Semantic search with configurable retrieval

- **history_service.py** - Consultation history management
  - Save analysis results
  - Retrieve user history
  - Query filtering and pagination

#### 5. Medical Knowledge Base (`backend-host/data/medical_knowledge/`)
**Purpose:** Source documents for RAG

- **common_symptoms.txt** - Common medical symptoms reference
- **emergency_conditions.txt** - Life-threatening conditions guide
- **chronic_conditions.txt** - Chronic disease information
- **guideline-170-en.pdf** - 409-page comprehensive medical guideline

**Vector Database Stats:**
- Total chunks indexed: 5,345
- Embedding model: all-MiniLM-L6-v2 (384 dimensions)
- Chunk size: ~500 tokens with 50 token overlap

### 🎨 Frontend Components

#### 1. Pages (`frontend/src/app/`)

- **page.tsx** - Main landing page
  - Hero section with feature cards
  - Symptom form integration
  - Results display
  - How it works section
  - Medical disclaimer

- **layout.tsx** - Root layout
  - Clerk authentication provider
  - Global styling
  - Navigation structure

- **sign-in/page.tsx** - User sign-in interface
- **sign-up/page.tsx** - User registration interface

#### 2. Components (`frontend/src/components/`)

- **SymptomForm.tsx** - Symptom input form
  - Symptoms description (required)
  - Age and gender selection
  - Duration and severity inputs
  - Medical history entry
  - Form validation with react-hook-form
  - Loading states and error handling

- **ResultCard.tsx** - Analysis results display
  - Safety check with severity-based styling
  - Emergency alerts with 112 call-to-action
  - Possible conditions list
  - Severity assessment
  - Recommended actions
  - Self-care tips
  - Red flags warning
  - Confidence level display

#### 3. Utilities (`frontend/src/lib/`)

- **api.ts** - API client functions
  - `analyzeSymptoms()` - Send symptoms for AI analysis
  - Error handling and response parsing

- **utils.ts** - Helper functions
  - `cn()` - Tailwind CSS class merging utility

---

## 🧠 RAG (Retrieval-Augmented Generation) System

### 📊 Architecture

The RAG system enhances AI responses by retrieving relevant medical information from a knowledge base before generating responses.

**Flow:**
1. User submits symptoms
2. RAG service embeds the query using SentenceTransformer
3. ChromaDB performs semantic search for relevant medical chunks
4. Top-K relevant chunks are retrieved (default: 5)
5. Retrieved context is injected into the LLM prompt
6. Groq LLM generates informed response based on symptoms + context
7. Response is structured and returned to user

### Components

**Vector Database:** ChromaDB
- Persistent storage in `backend-host/chroma_db/`
- Collection name: `medical_knowledge`
- Distance metric: Cosine similarity

**Embedding Model:** all-MiniLM-L6-v2
- Lightweight and fast (384 dimensions)
- Optimized for semantic similarity
- ~120MB model size

**Document Processing:**
- Text files: Direct chunking with overlap
- PDF files: PyPDF extraction with metadata preservation
- Chunk size: ~500 tokens
- Overlap: 50 tokens for context continuity

**Configuration** (`core/config.py`):
```python
RAG_ENABLED = True
RAG_TOP_K = 5  # Number of chunks to retrieve
RAG_CHUNK_SIZE = 500  # Tokens per chunk
RAG_CHUNK_OVERLAP = 50  # Token overlap
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

### Knowledge Base Content

**Total Documents:** 4 files
- 3 text files (common symptoms, emergency conditions, chronic conditions)
- 1 PDF (409 pages, 706,491 characters)

**Indexed Chunks:** 5,345 searchable segments

**Re-indexing:**
```bash
cd backend-host
python scripts/reindex_knowledge_base.py
```

---

## 📡 API Reference

### 🔐 Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}

Response 201:
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

### 🩺 Symptom Analysis Endpoints

#### Analyze Symptoms
```http
POST /api/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "symptoms": "severe headache and fever for 3 days",
  "age": 30,
  "gender": "male",
  "medical_history": ["diabetes", "hypertension"],
  "duration": "3 days",
  "severity": "moderate"
}

Response 200:
{
  "status": "success",
  "safety_check": {
    "is_emergency": false,
    "severity": "moderate",
    "recommendation": "Monitor symptoms and consult doctor if worsens",
    "matched_keywords": []
  },
  "analysis": {
    "possible_conditions": [
      "Viral infection (flu or common cold)",
      "Sinusitis",
      "Tension headache"
    ],
    "severity_assessment": "Moderate condition requiring medical attention",
    "recommended_actions": [
      "Schedule appointment with primary care physician",
      "Monitor temperature regularly",
      "Stay hydrated"
    ],
    "self_care_tips": [
      "Rest in a dark, quiet room",
      "Take over-the-counter pain relievers",
      "Apply cold compress to forehead"
    ],
    "red_flags": [
      "Sudden severe headache (thunderclap)",
      "Fever above 103°F (39.4°C)",
      "Stiff neck with confusion"
    ],
    "when_to_seek_care": "Seek immediate care if symptoms worsen or new concerning symptoms develop",
    "confidence_level": "High"
  },
  "recommendations": [
    "Consult with healthcare provider within 24-48 hours",
    "Continue monitoring symptoms",
    "Maintain adequate fluid intake"
  ]
}
```

#### Emergency Check
```http
POST /api/emergency-check
Content-Type: application/json

{
  "symptoms": "chest pain and difficulty breathing"
}

Response 200:
{
  "is_emergency": true,
  "severity": "critical",
  "recommendation": "CALL 112 IMMEDIATELY - Possible cardiac or respiratory emergency",
  "matched_keywords": ["chest pain", "difficulty breathing"]
}
```

#### Get Consultation History
```http
GET /api/history?skip=0&limit=10
Authorization: Bearer <token>

Response 200:
[
  {
    "id": 1,
    "symptoms": "headache and fever",
    "analysis_result": {...},
    "created_at": "2025-12-07T10:30:00Z",
    "user_id": 1
  }
]
```

---

## 🚀 Installation & Setup

### ✅ Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager
- PostgreSQL database (cloud or local)
- Redis instance (cloud or local)
- Groq API key (free tier available)

### ⚙️ Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend-host
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create `.env` file in project root:
```env
# Groq AI API
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://default:password@host:port

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
SECRET_KEY=your_secret_key_minimum_32_characters

# RAG Configuration
RAG_ENABLED=true
RAG_TOP_K=5
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=50
```

5. **Initialize RAG knowledge base:**
```bash
python scripts/reindex_knowledge_base.py
```

6. **Start backend server:**
```bash
python main.py
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 💻 Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment variables:**

Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
```

4. **Start development server:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Quick Start (Windows)

**Double-click batch files:**
1. `START_BACKEND.bat` - Starts FastAPI backend
2. `START_FRONTEND.bat` - Starts Next.js frontend

---

## 🔒 Security Features

### 🔐 Authentication
- JWT token-based authentication
- Token expiration: 30 minutes
- Secure token storage in httpOnly cookies (recommended)
- Password hashing with bcrypt (cost factor: 12)

### Data Protection
- SQL injection prevention via SQLAlchemy ORM
- CORS middleware with allowed origins
- Environment variable encryption
- Sensitive data never logged

### API Security
- Rate limiting on authentication endpoints
- Request validation with Pydantic
- Error messages without sensitive information
- HTTPS recommended for production

### Recommendations for Production
- Change default `SECRET_KEY`
- Enable HTTPS/TLS
- Implement rate limiting
- Use secure session storage
- Regular dependency updates
- Database connection encryption
- API key rotation policy

---

