from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_200_OK)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=user.email)
    return {
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=dict)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.email)
    return {
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login/form", response_model=Token)
def login_form(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Swagger UI compat
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    # In stateless JWT, logout is handled client-side by deleting the token.
    # But the API contract asks for a logout endpoint.
    return {"message": "Successfully logged out. Please remove token from client."}
