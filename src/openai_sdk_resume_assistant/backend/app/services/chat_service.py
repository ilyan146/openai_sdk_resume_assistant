from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from openai_sdk_resume_assistant.backend.app.models.chat_schemas import UploadFilesResponse
from openai_sdk_resume_assistant.client import AzureAIClient
from openai_sdk_resume_assistant.RAG.vector_db import VectorDB  # type: ignore
from openai_sdk_resume_assistant.resume_agent import resume_agent


class ChatService:
    VECTORSTORE = "resume_vectorstore"  # Some defaults
    COLLECTION_NAME = "ilyan_resume"

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

    # Add agent chat response streaming support
    async def get_agent_response_stream(self, question: str, chat_history: list | None = None) -> AsyncGenerator[str, None]:
        """
        Stream the agent response as it's generated.
        Args:
            question: The question to ask the resume agent.

        Yields:
            Text chunks as they are generated.
        """
        # Build context string from chat history
        prompt = self._build_prompt_with_history(question, chat_history)

        # Debug logging
        print("[DEBUG] Final prompt being sent to agent:")
        print(prompt)
        print("-" * 50)

        async for chunk in self.agent.run_agent_with_mcp_stream(prompt):
            yield chunk

    def _build_prompt_with_history(self, question: str, chat_history: list | None = None) -> str:
        """Build a prompt string that includes chat history for context."""
        # No history - just return the question
        if not chat_history or len(chat_history) == 0:
            return question

        # Limit to last 6 messages
        recent_history = chat_history[-6:]

        # Build simple history format
        history_lines = []
        for msg in recent_history:
            role = msg.role if hasattr(msg, "role") else msg.get("role", "user")
            content = msg.content if hasattr(msg, "content") else msg.get("content", "")
            prefix = "User" if role == "user" else "Assistant"
            history_lines.append(f"{prefix}: {content}")

        # Keep prompt simple - don't override agent instructions
        prompt = f"""Conversation history:
        {chr(10).join(history_lines)}

        Current question: {question}"""

        print(f"[DEBUG] Built prompt:\n{prompt}")
        return prompt

    def process_uploaded_files(self, files_directory: Path | str) -> UploadFilesResponse:  # dict:
        """
        Process uploaded files and add them to the vector database.
        Automatically detects PDFs and text files and processes them accordingly.
        Args:
            files_directory: Directory containing the uploaded files
        Returns:
            UploadFilesResponse with processing status and details
        """
        if isinstance(files_directory, str):
            files_directory = Path(files_directory)

        result = UploadFilesResponse(pdf_count=0, text_count=0, errors=[], success=False)

        try:
            # Check for PDF files
            pdf_files = list(files_directory.glob("*.pdf"))
            if pdf_files:
                self.vector_db.add_pdf_to_collection(directory=files_directory, collection_name=self.COLLECTION_NAME)
                result.pdf_count = len(pdf_files)

            # Check for text files
            text_files = list(files_directory.glob("*.txt"))
            if text_files:
                self.vector_db.add_texts_to_collection(directory=files_directory, collection_name=self.COLLECTION_NAME)
                result.text_count = len(text_files)

            result.success = True
            return result

        except Exception as e:
            result.errors.append(str(e))
            return result

    def list_collection_items(self) -> dict[str, Any]:
        return self.vector_db.list_collection_items(collection_name=self.COLLECTION_NAME)
