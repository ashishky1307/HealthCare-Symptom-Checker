"""API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional, Dict, Any
import uuid
import logging

from core.auth import get_current_user, get_optional_user
from db.session import get_db
from db.models import User
from schemas.input import (
    SymptomAnalysisRequest,
    UserRegister,
    UserLogin,
    ConsultationFilter
)
from schemas.output import (
    SymptomAnalysisResponse,
    UserResponse,
    TokenResponse,
    ConsultationResponse,
    ConsultationDetail,
    PaginatedConsultations,
    ErrorResponse
)
from services.history_service import HistoryService
from services.symptom_analyzer import SymptomAnalyzer
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    sanitize_user_input
)
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
symptom_analyzer = SymptomAnalyzer()
history_service = HistoryService()


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.email}")
    
    return new_user


@router.post("/auth/login", response_model=TokenResponse)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


# ============================================================================
# SYMPTOM ANALYSIS ROUTES
# ============================================================================

@router.post("/analyze", response_model=SymptomAnalysisResponse)
async def analyze_symptoms(
    request: SymptomAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_user)
):
    """
    Analyze symptoms and provide recommendations.
    
    This endpoint performs comprehensive symptom analysis using Groq LLM directly:
    1. Sanitizes and validates input
    2. Analyzes with Groq (Llama 3.1)
    3. Stores consultation history (if authenticated)
    4. Returns structured recommendations
    """
    try:
        # Sanitize input
        sanitized_symptoms = sanitize_user_input(request.symptoms)
        
        # Analyze symptoms directly with Groq
        analysis_result = await symptom_analyzer.analyze(
            symptoms=sanitized_symptoms,
            age=request.age,
            gender=request.gender,
            medical_history=request.medical_history,
            duration=request.duration,
            severity=request.severity
        )
        
        # Save to history if user is authenticated
        consultation_id = None
        if current_user:
            session_id = str(uuid.uuid4())
            consultation = history_service.create_consultation(
                db=db,
                user_id=current_user.id,
                symptoms=sanitized_symptoms,
                age=request.age,
                gender=request.gender,
                medical_history=request.medical_history,
                duration=request.duration,
                severity=request.severity,
                analysis_result=analysis_result,
                session_id=session_id
            )
            consultation_id = consultation.id
        
        # Add consultation ID to response
        analysis_result["consultation_id"] = consultation_id
        
        logger.info(f"Symptom analysis completed. Emergency: {analysis_result.get('status')}")
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in symptom analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/emergency-check")
async def quick_emergency_check(
    request: SymptomAnalysisRequest
):
    """Quick emergency assessment without full analysis."""
    try:
        sanitized_symptoms = sanitize_user_input(request.symptoms)
        
        # Quick emergency keyword check
        symptoms_lower = sanitized_symptoms.lower()
        
        critical_keywords = [
            "chest pain", "difficulty breathing", "can't breathe", "severe bleeding",
            "unconscious", "seizure", "stroke", "heart attack", "suicide",
            "severe injury", "compound fracture", "heavy bleeding"
        ]
        
        urgent_keywords = [
            "high fever", "severe pain", "blood in stool", "blood in urine",
            "severe headache", "confusion", "severe dizziness", "fainting"
        ]
        
        matched_critical = [kw for kw in critical_keywords if kw in symptoms_lower]
        matched_urgent = [kw for kw in urgent_keywords if kw in symptoms_lower]
        
        if matched_critical:
            return {
                "is_emergency": True,
                "severity_level": "critical",
                "matched_keywords": matched_critical,
                "message": "⚠️ SEEK IMMEDIATE EMERGENCY CARE - Call 911 or go to the nearest ER"
            }
        elif matched_urgent:
            return {
                "is_emergency": False,
                "severity_level": "urgent",
                "matched_keywords": matched_urgent,
                "message": "⚠️ Urgent care recommended within 24 hours"
            }
        else:
            return {
                "is_emergency": False,
                "severity_level": "routine",
                "matched_keywords": [],
                "message": "Schedule an appointment with your healthcare provider"
            }
        
    except Exception as e:
        logger.error(f"Error in emergency check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Emergency check failed: {str(e)}"
        )


# ============================================================================
# CONSULTATION HISTORY ROUTES
# ============================================================================

@router.get("/history", response_model=PaginatedConsultations)
async def get_consultation_history(
    start_date: str = None,
    end_date: str = None,
    is_emergency: bool = None,
    severity_level: str = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get consultation history for the current user."""
    try:
        filters = ConsultationFilter(
            start_date=start_date,
            end_date=end_date,
            is_emergency=is_emergency,
            severity_level=severity_level,
            limit=limit,
            offset=offset
        )
        
        consultations, total = history_service.get_user_consultations(
            db=db,
            user_id=current_user.id,
            filters=filters
        )
        
        return {
            "total": total,
            "items": consultations,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Error getting consultation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve history"
        )


@router.get("/history/{consultation_id}", response_model=ConsultationDetail)
async def get_consultation_detail(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific consultation."""
    consultation = history_service.get_consultation_by_id(
        db=db,
        consultation_id=consultation_id,
        user_id=current_user.id
    )
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    return consultation


@router.get("/history/stats")
async def get_consultation_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics about user's consultations."""
    try:
        stats = history_service.get_statistics(db=db, user_id=current_user.id)
        return stats
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve statistics"
        )


# ============================================================================
# KNOWLEDGE BASE ROUTES (Disabled - Direct Groq LLM Only)
# ============================================================================

@router.get("/knowledge/search")
async def search_knowledge_base(
    query: str,
    n_results: int = 5
):
    """Knowledge base search disabled (using direct Groq LLM instead)."""
    return {
        "message": "Knowledge base search not available. Using direct Groq LLM for symptom analysis.",
        "query": query,
        "suggestion": "Use /analyze endpoint for symptom analysis"
    }
