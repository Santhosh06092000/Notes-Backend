from database import SessionDep
from jwt_auth import create_access_token, hash_password, verify_password
from models.user_model import User
from sqlmodel import select
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query


router = APIRouter()

# Register a new user


@router.post("/register/")
async def register_user(user: User, session: SessionDep):
    # Check if the email already exists
    existing_user = session.exec(select(User).where(
        User.user_email == user.user_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "User created successfully"}


# Login to get JWT token
@router.post("/login/")
async def login(user_email: str, password: str, session: SessionDep):
    user = session.exec(select(User).where(
        User.user_email == user_email)).first()
    print("user,...", user)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.user_email})
    return {"access_token": token, "user": user}


@router.get("/users/")
async def read_users(session: SessionDep,
                     offset: int = 0,
                     limit: Annotated[int, Query(le=100)] = 100,) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
