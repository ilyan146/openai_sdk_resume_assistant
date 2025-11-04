from pathlib import Path

from openai_sdk_resume_assistant.client import AzureAIClient
from openai_sdk_resume_assistant.RAG.vector_db import VectorDB
from openai_sdk_resume_assistant.resume_agent import resume_agent


class ChatService:
    VECTORSTORE = "upload_vectorstore"
    COLLECTION_NAME = "upload_collection"

    def __init__(self):
        # Set the AzureAI client defaults
        client = AzureAIClient()
        self._openai_client = client.set_openai_client_defaults()
        self.agent = resume_agent

        # Initialize the vector database
        self.vector_db = VectorDB(self.VECTORSTORE)

    async def get_agent_response(self, question: str) -> str:
        """
        Get a response from the resume agent for the given question.
        Args:
            question: The question to ask the resume agent.

        Returns:
            The response from the resume agent.
        """
        return await self.agent.run_agent_with_mcp(question)

    def process_uploaded_files(self, files_directory: Path | str) -> dict:
        """
        Process uploaded files and add them to the vector database.
        Automatically detects PDFs and text files and processes them accordingly.
        Args:
            files_directory: Directory containing the uploaded files
        Returns:
            Dictionary with processing status and details
        """
        if isinstance(files_directory, str):
            files_directory = Path(files_directory)

        result = {"pdf_count": 0, "text_count": 0, "errors": [], "success": False}

        try:
            # Check for PDF files
            pdf_files = list(files_directory.glob("*.pdf"))
            if pdf_files:
                self.vector_db.add_pdf_to_collection(directory=files_directory, collection_name=self.COLLECTION_NAME)
                result["pdf_count"] = len(pdf_files)

            # Check for text files
            text_files = list(files_directory.glob("*.txt"))
            if text_files:
                self.vector_db.add_texts_to_collection(directory=files_directory, collection_name=self.COLLECTION_NAME)
                result["text_count"] = len(text_files)

            result["success"] = True
            return result

        except Exception as e:
            result["errors"].append(str(e))
            return result
