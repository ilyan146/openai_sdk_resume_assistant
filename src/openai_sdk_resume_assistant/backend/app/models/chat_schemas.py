from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class UploadFilesResponse(BaseModel):
    pdf_count: int
    text_count: int
    errors: list[str]
    success: bool
