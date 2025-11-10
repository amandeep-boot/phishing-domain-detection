from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.utils.token import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token (required)"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return user_id

def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> Optional[int]:
    """Get current user ID from JWT token (optional)"""
    if not token:
        return None
    
    payload = decode_access_token(token)
    if not payload:
        return None
    
    return payload.get("user_id")
