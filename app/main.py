from fastapi import FastAPI
from app.api.routes import user, main
from app.db.db_manager import DBManager

app = FastAPI()

DBManager()

app.include_router(user.router)
app.include_router(main.router)