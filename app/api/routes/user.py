import os
from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserLogin, UserBusRelation
from crud.user import User
from core.security import create_access_token
from dependencies.auth import admin_required, get_current_user


router = APIRouter()

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

        if "error" in fetched_user:
            return {"error": "Usuário ou senha inválidos"}

        if fetched_user["email"] == os.getenv("ADMIN_EMAIL"):
            fetched_user["role"] = "admin"
        else:
            fetched_user["role"] = "user"

        token = create_access_token(
            data={"id": fetched_user["id"], "sub": fetched_user["email"], "name": fetched_user["name"], "role": fetched_user["role"]},
            expires_delta=None
        )

        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/user_bus_relation")
def create_user_bus_relation_route(user_bus_relation: UserBusRelation, user: dict = Depends(get_current_user)):
    try:
        user_db = User()
        response = user_db.create_user_bus_relation(user["id"], user_bus_relation)
        user_db.close()

        return response
    except Exception as e:
        return {"error": str(e)}

@router.delete("/drop_table/{table_name}")
def drop_table_route(table_name: str, _: dict = Depends(admin_required)):
    try:
        user_db = User()
        response = user_db.drop_table(table_name)
        user_db.close()

        return response
    except Exception as e:
        return {"error": str(e)}