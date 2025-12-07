"""Database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    consultations = relationship("Consultation", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Consultation(Base):
    """Consultation history model."""
    
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Patient information (anonymized)
    age = Column(Integer)
    gender = Column(String(50))
    
    # Symptom details
    symptoms = Column(Text, nullable=False)
    duration = Column(String(255))
    severity = Column(String(50))
    medical_history = Column(JSON)  # Store as JSON array
    
    # Analysis results
    analysis_result = Column(JSON, nullable=False)  # Full analysis from Groq
    is_emergency = Column(Boolean, default=False)
    severity_level = Column(String(50))  # critical, urgent, moderate, routine
    
    # Possible conditions identified
    possible_conditions = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    session_id = Column(String(255), index=True)  # For tracking sessions
    
    # Relationships
    user = relationship("User", back_populates="consultations")
    
    def __repr__(self):
        return f"<Consultation {self.id} - User {self.user_id}>"


class AuditLog(Base):
    """Audit log for tracking system events."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255))
    details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.id} - {self.action}>"
