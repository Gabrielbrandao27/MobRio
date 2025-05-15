from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user

router = APIRouter()

@router.get("/")
def landing_page():
    return {
        "message": "Bem-vindo(a) ao MobRio!",
        "info": {
            "login": "/login",
            "register": "/register"
        }
    }
