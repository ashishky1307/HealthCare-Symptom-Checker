"""Pydantic input schemas."""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime


class SymptomAnalysisRequest(BaseModel):
    """Request schema for symptom analysis."""
    
    symptoms: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed description of symptoms"
    )
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age")
    gender: Optional[str] = Field(None, description="Patient gender")
    medical_history: Optional[List[str]] = Field(
        None,
        description="List of existing medical conditions"
    )
    duration: Optional[str] = Field(None, description="How long symptoms have been present")
    severity: Optional[str] = Field(
        None,
        description="Subjective severity: mild, moderate, or severe"
    )
    
    @validator('severity')
    def validate_severity(cls, v):
        if v and v.lower() not in ['mild', 'moderate', 'severe']:
            raise ValueError('Severity must be mild, moderate, or severe')
        return v.lower() if v else None
    
    class Config:
        json_schema_extra = {
            "example": {
                "symptoms": "I have a severe headache on the right side, sensitivity to light, and nausea",
                "age": 35,
                "gender": "female",
                "medical_history": ["migraine history"],
                "duration": "6 hours",
                "severity": "severe"
            }
        }


class UserRegister(BaseModel):
    """User registration schema."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, description="User full name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "John Doe"
            }
        }


class UserLogin(BaseModel):
    """User login schema."""
    
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class ConsultationFilter(BaseModel):
    """Filter parameters for consultation history."""
    
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_emergency: Optional[bool] = None
    severity_level: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
