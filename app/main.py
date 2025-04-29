from fastapi import FastAPI
from app.api.routes import bus, main, user
from app.db.db_manager import DBManager

app = FastAPI()

DBManager()

app.include_router(bus.router)
app.include_router(main.router)
app.include_router(user.router)
