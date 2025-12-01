import json
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import StreamingResponse

from openai_sdk_resume_assistant.backend.app.models.chat_schemas import ChatMemory, ChatNameResponse, QuestionRequest
from openai_sdk_resume_assistant.backend.app.mongodb import User
from openai_sdk_resume_assistant.backend.app.services.chat_service import ChatService
from openai_sdk_resume_assistant.backend.app.users import current_active_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
async def ask_resume_question(request: QuestionRequest, service: ChatService = Depends(ChatService)):
    response = await service.get_agent_response(request.question)
    return {"response": response}


@router.post("/ask_stream")
async def ask_question_stream(
    request: QuestionRequest,
    fastapi_request: Request,
    user: User = Depends(current_active_user),
    service: ChatService = Depends(ChatService),
):
    """Stream responses and store in chat history"""
    # Verify chat exists
    if not request.chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")

    # chat = await fastapi_request.app.mongo_dal.get_chat_memory(request.chat_id)
    # Verify chat belongs to user
    chat = await fastapi_request.app.mongo_dal.get_chat_memory_for_user(chat_id=request.chat_id, user_id=str(user.id))
    if not chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")

    # Debug log
    print(f"[DEBUG] Received chat_history: {len(request.chat_history)} messages")
    for msg in request.chat_history:
        print(f"  - {msg.role}: {msg.content[:50]}...")

    await fastapi_request.app.mongo_dal.add_message_to_chat(request.chat_id, role="user", content=request.question)

    async def event_generator():
        full_response = ""
        try:
            async for chunk in service.get_agent_response_stream(
                request.question,
                chat_history=request.chat_history,
            ):
                full_response += chunk
                # Send as JSON for easier parsing on frontend
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            await fastapi_request.app.mongo_dal.add_message_to_chat(request.chat_id, role="assistant", content=full_response)

            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/upload_files")
async def upload_resume_files(
    files: list[UploadFile] = File(...), _user: User = Depends(current_active_user), service: ChatService = Depends(ChatService)
):
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
def list_collection_items(_user: User = Depends(current_active_user), service: ChatService = Depends(ChatService)):
    """List all items in the resume collection"""
    try:
        items = service.list_collection_items()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# MongoDB chat memory endpoints
@router.post("/create_chat_memory", status_code=status.HTTP_201_CREATED)
async def create_chat_memory(
    chat_name: str,
    request: Request,
    user: User = Depends(current_active_user),
) -> ChatNameResponse:
    """Create a new chat memory in MongoDB for current user"""
    chat_id = await request.app.mongo_dal.create_chat_memory(
        chat_name=chat_name,
        user_id=str(user.id),  # Pass user_id
    )
    return ChatNameResponse(id=chat_id, chat_name=chat_name, user_id=str(user.id))


@router.get("/chat_memory/{chat_id}")
async def get_chat_memory(
    chat_id: str,
    request: Request,
    user: User = Depends(current_active_user),
) -> ChatMemory:
    """Get a specific chat memory if it belongs to the current user"""
    chat = await request.app.mongo_dal.get_chat_memory_for_user(chat_id=chat_id, user_id=str(user.id))
    if not chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")
    return chat


@router.delete("/chat_memory/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat_memory(
    chat_id: str,
    request: Request,
    user: User = Depends(current_active_user),
) -> dict:
    """Delete a chat memory by ID"""
    deleted = await request.app.mongo_dal.delete_chat_memory(chat_id, user_id=str(user.id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat memory not found")
    return {"message": "Chat deleted successfully", "chat_id": chat_id}


@router.get("/all_chats")
async def get_all_chats(
    request: Request,
    limit: int = 50,
    user: User = Depends(current_active_user),
) -> list[ChatMemory]:
    """Get all chat memories"""
    return await request.app.mongo_dal.get_all_chats(user_id=str(user.id), limit=limit)


@router.post("/chat_memory/{chat_id}/message")
async def add_message(
    chat_id: str, role: str, content: str, request: Request, user: User = Depends(current_active_user)
) -> ChatMemory:
    """Add a message to an existing chat"""
    # First verify the chat belongs to user
    chat = await request.app.mongo_dal.get_chat_memory_for_user(chat_id=chat_id, user_id=str(user.id))
    if not chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")

    updated_chat = await request.app.mongo_dal.add_message_to_chat(chat_id, role, content)
    if not updated_chat:
        raise HTTPException(status_code=404, detail="Chat memory not found")
    return updated_chat
