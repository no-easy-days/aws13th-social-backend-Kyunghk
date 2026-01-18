import json
import bcrypt
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from models.users import User, UserCreate, UserResponse
from typing import List

router = APIRouter()

def read_users() -> List[dict]:
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_users(users: List[dict]):
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4, default=str)

@router.post("/users/sign-up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user_create: UserCreate):
    users = read_users()

    if any(u["email"] == user_create.email for u in users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    if any(u["nickname"] == user_create.nickname for u in users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nickname already taken",
        )

    hashed_password = bcrypt.hashpw(
        user_create.password.encode("utf-8"), bcrypt.gensalt()
    )

    new_id = max([u["id"] for u in users]) + 1 if users else 1
    
    new_user = User(
        id=new_id,
        email=user_create.email,
        nickname=user_create.nickname,
        hashed_password=hashed_password.decode("utf-8"),
        profileImageUrl=user_create.profileImageUrl,
        createdAt=datetime.utcnow()
    )

    users.append(new_user.dict())
    write_users(users)

    return new_user
