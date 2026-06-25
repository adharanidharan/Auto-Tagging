from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserDB, UserResponse, Token
from app.database.mongodb import get_database
from app.auth.auth_service import get_password_hash, verify_password, create_access_token
from app.routes.deps import get_current_user

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Registers a new user, hashes their password, and saves them to MongoDB.
    Validates that the password length is between 6 and 72 characters.
    """
    db = get_database()
    
    # Validate password constraints
    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain minimum 6 characters"
        )
    if len(user.password) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot exceed 72 characters"
        )
    
    # Check if user already exists
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and prepare user document
    hashed_password = get_password_hash(user.password)
    
    # Set role based on email pattern
    role = "admin" if user.email.endswith("@admin.com") or user.email == "admin@example.com" else "user"
    
    # Construct DB user model (using pythonic fields)
    new_user = UserDB(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=role
    )
    
    # Save user with model aliases (saves as passwordHash and createdAt)
    await db["users"].insert_one(new_user.model_dump(by_alias=True))
    
    # Return success response exactly as requested
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT token.
    """
    db = get_database()
    
    user = await db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Verify password against hashed password in DB
    db_password_hash = user.get("passwordHash") or user.get("password_hash")
    if not db_password_hash or not verify_password(form_data.password, db_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Create and return access token
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserDB = Depends(get_current_user)):
    """
    Returns the current authenticated user details.
    """
    return {
        "_id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "createdAt": current_user.created_at
    }
