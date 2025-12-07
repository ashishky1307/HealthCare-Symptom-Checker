"""Pydantic output schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SafetyCheck(BaseModel):
    """Safety check result schema."""
    
    is_emergency: bool
    severity: str
    matched_keywords: List[str] = []
    recommendation: str
    warning_message: Optional[str] = None
    should_call_911: bool = False
    should_seek_immediate_care: bool = False


class RetrievedSource(BaseModel):
    """Retrieved source document schema."""
    
    content: str
    source: str


class AnalysisResult(BaseModel):
    """Analysis result schema."""
    
    possible_conditions: List[str]
    severity_assessment: str
    recommended_actions: List[str]
    when_to_seek_care: str
    self_care_tips: List[str]
    red_flags: List[str]
    confidence_level: str
    note: Optional[str] = None


class SymptomAnalysisResponse(BaseModel):
    """Response schema for symptom analysis."""
    
    status: str
    safety_check: SafetyCheck
    analysis: Optional[AnalysisResult] = None
    pediatric_check: Optional[Dict[str, Any]] = None
    retrieved_sources: List[RetrievedSource] = []
    recommendations: List[str]
    disclaimer: str
    consultation_id: Optional[int] = None


class UserResponse(BaseModel):
    """User response schema."""
    
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ConsultationResponse(BaseModel):
    """Consultation response schema."""
    
    id: int
    age: Optional[int]
    gender: Optional[str]
    symptoms: str
    duration: Optional[str]
    severity: Optional[str]
    medical_history: Optional[List[str]]
    is_emergency: bool
    severity_level: str
    possible_conditions: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConsultationDetail(ConsultationResponse):
    """Detailed consultation response including full analysis."""
    
    analysis_result: Dict[str, Any]


class PaginatedConsultations(BaseModel):
    """Paginated consultation list."""
    
    total: int
    items: List[ConsultationResponse]
    limit: int
    offset: int


class HealthCheck(BaseModel):
    """Health check response."""
    
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
