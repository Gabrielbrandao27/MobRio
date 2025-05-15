from fastapi import FastAPI
from api.routes import bus, main, user
from db.db_manager import DBManager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

DBManager()

app.include_router(bus.router)
app.include_router(main.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
