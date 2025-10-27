from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

APP_TITLE = "CV API"
APP_VERSION = "1.0.0"
app = FastAPI(title=APP_TITLE, version=APP_VERSION)

ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
