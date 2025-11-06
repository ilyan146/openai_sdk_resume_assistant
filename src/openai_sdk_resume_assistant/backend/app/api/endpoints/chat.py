import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from openai_sdk_resume_assistant.backend.app.models.chat_schemas import QuestionRequest
from openai_sdk_resume_assistant.backend.app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
async def ask_resume_question(request: QuestionRequest, service: ChatService = Depends(ChatService)):
    response = await service.get_agent_response(request.question)
    return {"response": response}


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
