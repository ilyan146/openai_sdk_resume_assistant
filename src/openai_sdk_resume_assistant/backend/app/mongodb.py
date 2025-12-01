import os
from contextlib import asynccontextmanager

from beanie import Document, init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_users.db import BeanieBaseUser
from fastapi_users_db_beanie import BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from openai_sdk_resume_assistant.backend.app.services.data_access_layer import MongoDAL

load_dotenv()

COLLECTION_NAME = "chat_memories"
# MONGODB_URI = os.environ["MONGODB_URI"]
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI environment variable not set. Set it to your MongoDB connection string.")

DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}

DATABASE_NAME = os.environ.get("DATABASE_NAME", "resume_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI, uuidRepresentation="standard")
    # database = client.get_default_database()  # Connect to default database from URI
    database = client[DATABASE_NAME]

    # Ensure database connection available
    pong = await database.command("ping")
    if int(pong.get("ok", 0)) != 1:
        raise Exception("Cluster connection is not okay!")

    await init_beanie(
        database=database,  # type:ignore
        document_models=[User],
    )

    chat_mem_collection = database.get_collection(COLLECTION_NAME)
    app.mongo_dal = MongoDAL(chat_mem_collection)  # type: ignore

    yield

    client.close()


# Adding User objects
class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)  # type: ignore
