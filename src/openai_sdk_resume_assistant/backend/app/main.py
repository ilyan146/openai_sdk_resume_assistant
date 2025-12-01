import os
import sys

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openai_sdk_resume_assistant.backend.app.api.chat import router
from openai_sdk_resume_assistant.backend.app.models.user_schemas import UserCreate, UserRead, UserUpdate
from openai_sdk_resume_assistant.backend.app.mongodb import DEBUG, User, lifespan
from openai_sdk_resume_assistant.backend.app.users import auth_backend, current_active_user, fastapi_users

APP_TITLE = "CV API"
APP_VERSION = "1.0.0"
app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan, debug=DEBUG)

# FRONTEND_URL from env or hardcoded for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://openai-sdk-resume-assistant.vercel.app")


ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    FRONTEND_URL,
    "https://openai-sdk-resume-assistant-lxrh-ilyan146s-projects.vercel.app",
]  # vercel hosted frontend end point
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


# New user auth routers
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello, {user.email}. You are authenticated."}


@app.get("/", tags=["health"])
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "app": APP_TITLE, "version": APP_VERSION}


def main(_argv=sys.argv[1:]):
    try:
        uvicorn.run("openai_sdk_resume_assistant.app.main:app", host="127.0.0.1", port=8000, reload=DEBUG)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
