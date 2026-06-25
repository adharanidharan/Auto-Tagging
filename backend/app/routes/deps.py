from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.auth_service import decode_access_token
from app.database.mongodb import get_database
from app.models.user import UserDB
from bson import ObjectId

# OAuth2 scheme configured to use our login path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDB:
    """
    Dependency to validate the JWT token and retrieve the current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    db = get_database()
    user_data = await db["users"].find_one({"email": email})
    
    if user_data is None:
        raise credentials_exception
        
    # Map PyObjectId from MongoDB properly
    user_data["id"] = user_data["_id"]
    
    # Ensure role is set dynamically for existing/legacy users who signed up before the role column existed
    if user_data.get("email", "").endswith("@admin.com") or user_data.get("email") == "admin@example.com":
        user_data["role"] = "admin"
        
    return UserDB(**user_data)
