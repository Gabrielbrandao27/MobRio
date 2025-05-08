from fastapi import FastAPI
from app.api.routes import bus, main, user
from app.db.db_manager import DBManager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

DBManager()

app.include_router(bus.router)
app.include_router(main.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
