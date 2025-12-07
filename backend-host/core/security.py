"""Security utilities for authentication and PII protection."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
import re
import logging

from core.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logger.error(f"JWT decode error: {e}")
        return None


class PIIMasker:
    """Mask personally identifiable information in text."""
    
    # PII patterns
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "name": r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Simple name pattern
    }
    
    REPLACEMENTS = {
        "email": "[EMAIL]",
        "phone": "[PHONE]",
        "ssn": "[SSN]",
        "credit_card": "[CREDIT_CARD]",
        "name": "[NAME]",
    }
    
    @classmethod
    def mask_text(cls, text: str, patterns: Optional[list] = None) -> str:
        """
        Mask PII in text.
        
        Args:
            text: Text to mask
            patterns: List of pattern types to mask (uses all if None)
            
        Returns:
            Masked text
        """
        if not text:
            return text
        
        if patterns is None:
            patterns = list(cls.PATTERNS.keys())
        
        masked_text = text
        
        for pattern_type in patterns:
            if pattern_type in cls.PATTERNS:
                pattern = cls.PATTERNS[pattern_type]
                replacement = cls.REPLACEMENTS[pattern_type]
                masked_text = re.sub(pattern, replacement, masked_text)
        
        return masked_text
    
    @classmethod
    def mask_dict(cls, data: Dict[str, Any], fields: list = None) -> Dict[str, Any]:
        """
        Mask PII in dictionary values.
        
        Args:
            data: Dictionary with potential PII
            fields: List of field names to mask (masks string fields if None)
            
        Returns:
            Dictionary with masked values
        """
        if not data:
            return data
        
        masked_data = data.copy()
        
        for key, value in masked_data.items():
            if isinstance(value, str):
                if fields is None or key in fields:
                    masked_data[key] = cls.mask_text(value)
            elif isinstance(value, dict):
                masked_data[key] = cls.mask_dict(value, fields)
            elif isinstance(value, list):
                masked_data[key] = [
                    cls.mask_text(item) if isinstance(item, str) else item
                    for item in value
                ]
        
        return masked_data


def sanitize_user_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: User input text
        
    Returns:
        Sanitized text
    """
    # Remove potential SQL injection characters
    sanitized = re.sub(r'[;\'"\\]', '', text)
    
    # Limit length
    sanitized = sanitized[:5000]
    
    return sanitized.strip()
