"""Authentication API routes for JWT token generation."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from core.auth import create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleLoginRequest(BaseModel):
    """Request model for Google OAuth login."""
    email: EmailStr
    name: str
    picture: str | None = None


class TokenResponse(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(request: GoogleLoginRequest):
    """
    Generate JWT token for authenticated user.
    
    This endpoint receives user info from Google OAuth (verified by NextAuth)
    and generates a JWT token for backend API authorization.
    
    Args:
        request: User information from Google OAuth
        
    Returns:
        JWT access token and user information
    """
    try:
        # Prepare user data
        user_data = {
            "email": request.email,
            "name": request.name,
            "picture": request.picture
        }
        
        # Create JWT token with user email as subject
        access_token = create_access_token(
            data={
                "sub": user_data["email"],
                "name": user_data["name"],
                "picture": user_data["picture"]
            }
        )
        
        logger.info(f"JWT token generated for user: {request.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
    except Exception as e:
        logger.error(f"Error generating JWT token: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate authentication token"
        )


@router.post("/verify")
async def verify_token_endpoint(token: str):
    """
    Verify if a JWT token is valid.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Token validity status and decoded payload
    """
    from jose import jwt, JWTError
    from core.auth import SECRET_KEY, ALGORITHM
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "valid": True,
            "payload": payload
        }
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
