from fastapi import FastAPI
from app.presentation.api.router import router

app = FastAPI()

app.include_router(router)