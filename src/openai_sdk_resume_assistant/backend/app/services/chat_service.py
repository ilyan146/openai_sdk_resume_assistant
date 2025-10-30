from openai_sdk_resume_assistant.client import AzureAIClient
from openai_sdk_resume_assistant.resume_agent import resume_agent


class ChatService:
    def __init__(self):
        # Set the AzureAI client defaults
        client = AzureAIClient()
        self._openai_client = client.set_openai_client_defaults()
        self.agent = resume_agent

    async def get_agent_response(self, question: str) -> str:
        """
        Get a response from the resume agent for the given question.
        Args:
            question: The question to ask the resume agent.

        Returns:
            The response from the resume agent.
        """
        return await self.agent.run_agent_with_mcp(question)
