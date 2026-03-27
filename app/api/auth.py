from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token
from app.core.fake_users import fake_users_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(username: str, password: str):
    user = fake_users_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {
        "user_id": user["id"],
        "role": user["role"]
    }

    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

