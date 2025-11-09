import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openai_sdk_resume_assistant.backend.app.api.chat import router
from openai_sdk_resume_assistant.backend.app.api.mongodb import DEBUG, lifespan

APP_TITLE = "CV API"
APP_VERSION = "1.0.0"
app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan, debug=DEBUG)

app.include_router(router, prefix="/api")

ALLOWED_ORIGINS = ["http://localhost", "http://localhost:3000", "http://localhost:5173"]  # Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
