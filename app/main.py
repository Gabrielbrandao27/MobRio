from fastapi import FastAPI
from app.api.routes import user, main

app = FastAPI()

app.include_router(user.router)
app.include_router(main.router)