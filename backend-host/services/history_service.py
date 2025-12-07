"""Service for managing consultation history."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from db.models import Consultation, User
from schemas.input import ConsultationFilter

logger = logging.getLogger(__name__)


class HistoryService:
    """Service for consultation history operations."""
    
    @staticmethod
    def create_consultation(
        db: Session,
        user_id: int,
        symptoms: str,
        analysis_result: dict,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        medical_history: Optional[List[str]] = None,
        duration: Optional[str] = None,
        severity: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Consultation:
        """
        Create a new consultation record.
        
        Args:
            db: Database session
            user_id: User ID
            symptoms: Symptom description
            analysis_result: Full analysis from Groq
            age: Patient age
            gender: Patient gender
            medical_history: Medical history
            duration: Symptom duration
            severity: Symptom severity
            session_id: Session ID
            
        Returns:
            Created consultation object
        """
        # Extract key information from analysis
        is_emergency = analysis_result.get("safety_check", {}).get("is_emergency", False)
        severity_level = analysis_result.get("safety_check", {}).get("severity", "routine")
        
        # Extract possible conditions
        possible_conditions = None
        if analysis_result.get("analysis"):
            possible_conditions = analysis_result["analysis"].get("possible_conditions", [])
        
        consultation = Consultation(
            user_id=user_id,
            symptoms=symptoms,
            age=age,
            gender=gender,
            medical_history=medical_history,
            duration=duration,
            severity=severity,
            analysis_result=analysis_result,
            is_emergency=is_emergency,
            severity_level=severity_level,
            possible_conditions=possible_conditions,
            session_id=session_id
        )
        
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        
        logger.info(f"Created consultation {consultation.id} for user {user_id}")
        
        return consultation
    
    @staticmethod
    def get_user_consultations(
        db: Session,
        user_id: int,
        filters: Optional[ConsultationFilter] = None
    ) -> tuple[List[Consultation], int]:
        """
        Get consultations for a user with filters.
        
        Args:
            db: Database session
            user_id: User ID
            filters: Filter parameters
            
        Returns:
            Tuple of (consultations list, total count)
        """
        query = db.query(Consultation).filter(Consultation.user_id == user_id)
        
        # Apply filters
        if filters:
            if filters.start_date:
                query = query.filter(Consultation.created_at >= filters.start_date)
            if filters.end_date:
                query = query.filter(Consultation.created_at <= filters.end_date)
            if filters.is_emergency is not None:
                query = query.filter(Consultation.is_emergency == filters.is_emergency)
            if filters.severity_level:
                query = query.filter(Consultation.severity_level == filters.severity_level)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        if filters:
            query = query.offset(filters.offset).limit(filters.limit)
        
        # Order by most recent first
        consultations = query.order_by(Consultation.created_at.desc()).all()
        
        return consultations, total
    
    @staticmethod
    def get_consultation_by_id(
        db: Session,
        consultation_id: int,
        user_id: int
    ) -> Optional[Consultation]:
        """
        Get a specific consultation by ID.
        
        Args:
            db: Database session
            consultation_id: Consultation ID
            user_id: User ID (for authorization)
            
        Returns:
            Consultation object or None
        """
        consultation = db.query(Consultation).filter(
            Consultation.id == consultation_id,
            Consultation.user_id == user_id
        ).first()
        
        return consultation
    
    @staticmethod
    def get_recent_emergencies(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> List[Consultation]:
        """
        Get recent emergency consultations for a user.
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            List of emergency consultations
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        consultations = db.query(Consultation).filter(
            Consultation.user_id == user_id,
            Consultation.is_emergency == True,
            Consultation.created_at >= cutoff_date
        ).order_by(Consultation.created_at.desc()).all()
        
        return consultations
    
    @staticmethod
    def get_statistics(db: Session, user_id: int) -> dict:
        """
        Get statistics for a user's consultations.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with statistics
        """
        total = db.query(Consultation).filter(
            Consultation.user_id == user_id
        ).count()
        
        emergencies = db.query(Consultation).filter(
            Consultation.user_id == user_id,
            Consultation.is_emergency == True
        ).count()
        
        # Most recent consultation
        recent = db.query(Consultation).filter(
            Consultation.user_id == user_id
        ).order_by(Consultation.created_at.desc()).first()
        
        return {
            "total_consultations": total,
            "emergency_consultations": emergencies,
            "last_consultation": recent.created_at if recent else None
        }


from datetime import timedelta
