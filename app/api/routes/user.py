from fastapi import FastAPI
from app.schemas.user import UserCreate, UserLogin
from app.crud.user import User
from app.core.security import create_access_token


router = FastAPI()

@router.post("/register")
def register_user_route(user: UserCreate):
    try:
        user_db = User()
        response = user_db.register_user(user)
        user_db.close()

        return response
    except Exception as e:
        return {"error": str(e)}

@router.post("/login")
def login_user_route(user: UserLogin):
    try:
        user_db = User()
        fetched_user = user_db.login_user(user)
        user_db.close()

        token = create_access_token(
            data={"sub": fetched_user["email"], "name": fetched_user["name"]}
        )

        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        return {"error": str(e)}