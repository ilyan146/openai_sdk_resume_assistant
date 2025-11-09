import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from openai_sdk_resume_assistant.backend.app.services.data_access_layer import MongoDAL

COLLECTION_NAME = "chat_memories"
MONGODB_URI = os.environ["MONGODB_URI"]
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_default_database()  # Connect to default database from URI

    # Ensure database connection available
    pong = await database.command("ping")
    if int(pong.get("ok", 0)) != 1:
        raise Exception("Cluster connection is not okay!")

    chat_mem_collection = database.get_collection(COLLECTION_NAME)
    app.mongo_dal = MongoDAL(chat_mem_collection)  # type: ignore

    yield

    client.close()
