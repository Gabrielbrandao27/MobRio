from fastapi import FastAPI, Depends
from app.dependencies.auth import get_current_user

router = FastAPI()

@router.get("/")
def landing_page():
    return {
        "message": "Bem-vindo(a) ao MobRio!",
        "info": {
            "login": "/login",
            "register": "/register"
        }
    }

@router.get("/home")
def home(current_user: dict = Depends(get_current_user)):
    return {"message": f"Bem-vindo de volta, {current_user['name']}!"}