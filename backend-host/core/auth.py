"""JWT Authentication utilities for API authorization."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

security = HTTPBearer()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Dictionary containing user data to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Get current user information from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        Dictionary containing user information (email, name, picture)
    """
    payload = verify_token(credentials)
    return {
        "email": payload.get("sub"),
        "name": payload.get("name"),
        "picture": payload.get("picture"),
        "user_id": payload.get("user_id")
    }


async def get_optional_user(
    request: Request
) -> Optional[Dict[str, Any]]:
    """
    Get current user if token is provided, otherwise return None.
    Useful for optional authentication endpoints.
    
    Args:
        request: FastAPI request object
        
    Returns:
        User dictionary if authenticated, None otherwise
    """
    # Try to get Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    try:
        token = auth_header.replace("Bearer ", "")
        payload = verify_token(token)
        return {
            "email": payload.get("email"),
            "name": payload.get("name"),
            "picture": payload.get("picture"),
            "user_id": payload.get("user_id")
        }
    except HTTPException:
        return None
