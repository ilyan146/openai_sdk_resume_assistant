import json
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import StreamingResponse

from openai_sdk_resume_assistant.backend.app.models.chat_schemas import ChatMemory, ChatNameResponse, QuestionRequest
from openai_sdk_resume_assistant.backend.app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
async def ask_resume_question(request: QuestionRequest, service: ChatService = Depends(ChatService)):
    response = await service.get_agent_response(request.question)
    return {"response": response}


@router.post("/ask_stream")
async def ask_question_stream(request: QuestionRequest, service: ChatService = Depends(ChatService)):
    async def event_generator():
        try:
            async for chunk in service.get_agent_response_stream(request.question):
                # Send as JSON for easier parsing on frontend
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/upload_files")
async def upload_resume_files(files: list[UploadFile] = File(...), service: ChatService = Depends(ChatService)):
    """Upload files route for uploading PDFs and Text Files to the vector database"""

    # Create a temporary directory for uploaded files
    temp_dir = Path(tempfile.mkdtemp())

    try:
        # Save uploaded files to temp directory
        for file in files:
            file_path = temp_dir / file.filename  # type: ignore
            with open(file_path, "wb") as buffer:  # type: ignore
                shutil.copyfileobj(file.file, buffer)

        # Process files through the service
        result = service.process_uploaded_files(temp_dir)

        if not result.success:
            raise HTTPException(status_code=500, detail="Error processing uploaded files.")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)


# Endpoint for listing collection items
@router.get("/list_collection_items")
def list_collection_items(service: ChatService = Depends(ChatService)):
    """List all items in the resume collection"""
    try:
        items = service.list_collection_items()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# MongoDB chat memory endpoints
@router.post("/create_chat_memory", status_code=status.HTTP_201_CREATED)
async def create_chat_memory(chat_name: str, request: Request) -> ChatNameResponse:
    """Create a new chat memory in MongoDB"""
    return ChatNameResponse(id=await request.app.mongo_dal.create_chat_memory(chat_name=chat_name), chat_name=chat_name)


@router.get("/chat_memory/{chat_id}")
async def get_chat_memory(chat_id: str, request: Request) -> ChatMemory:
    """Get a specific chat memory by ID"""
    chat = await request.app.mongo_dal.get_chat_memory(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")
    return chat


@router.get("/all_chats")
async def get_all_chats(request: Request, limit: int = 50) -> list[ChatMemory]:
    """Get all chat memories"""
    return await request.app.mongo_dal.get_all_chats(limit=limit)


@router.post("/chat_memory/{chat_id}/message")
async def add_message(chat_id: str, role: str, content: str, request: Request) -> ChatMemory:
    """Add a message to an existing chat"""
    chat = await request.app.mongo_dal.add_message_to_chat(chat_id, role, content)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")
    return chat
