from fastapi import FastAPI
from app.schemas.user import UserSchema
from app.crud.user import User

router = FastAPI()

@router.post("/user/")
def create_user_route(user: UserSchema):
    try:
        user_db = User()

        response = user_db.insert_user(user)

        user_db.close()

        return response
    except Exception as e:
        return {"error": str(e)}

@router.get("/user/{user_id}")
def get_user_route(user_id: int):
    try:
        user_db = User()

        response = user_db.fetch_user(user_id)

        user_db.close()

        return response
    except Exception as e:
        return {"error": str(e)}