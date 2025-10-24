import os

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled
from azure.identity import InteractiveBrowserCredential, get_bearer_token_provider
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncAzureOpenAI, AzureOpenAI

load_dotenv(override=True)

"""
If using Azure DefaultAzureCredential,
Set up Azure CLI (add to system path)
-> az login to set up a onetime authentication
"""


class AzureAIClient(AzureOpenAI):
    """A Client setup class for AzureOpenAI API"""

    API_VERSION = "2024-10-21"

    def __init__(self, azure_endpoint=None, api_version=None, credential=None):
        self.api_version = api_version or self.API_VERSION
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        if not self.azure_endpoint:
            raise ValueError("Azure OpenAI endpoint is not set. Please set the AZURE_OPENAI_ENDPOINT environment variable.")

        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not self.api_key:
            self.credential = credential or InteractiveBrowserCredential()
            self.token_provider = self._get_token_provider

            super().__init__(
                azure_endpoint=self.azure_endpoint,
                azure_ad_token_provider=self.token_provider,
                api_version=self.api_version,
            )
        else:
            super().__init__(
                azure_endpoint=self.azure_endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )

    @property
    def _get_token_provider(self):
        try:
            # Test token retrieval
            self.credential.get_token("https://cognitiveservices.azure.com/.default")
            token_provider = get_bearer_token_provider(self.credential, "https://cognitiveservices.azure.com/.default")
            logger.success("Successfully initialized Azure Credentials!!")
            return token_provider
        except Exception as e:
            raise RuntimeError(f" Failed to initialize Azure Credential: {e}") from e

    # Set credential for openai client and defaults
    def set_openai_client_defaults(self):
        # make available the LLM
        load_dotenv(override=True)

        if self.api_key:
            openai_client = AsyncAzureOpenAI(
                azure_endpoint=self.azure_endpoint, api_version=self.api_version, api_key=self.api_key
            )
        else:
            openai_client = AsyncAzureOpenAI(
                azure_endpoint=self.azure_endpoint, api_version=self.api_version, azure_ad_token_provider=self.token_provider
            )
        # Set default client and configs
        set_default_openai_client(openai_client)
        set_default_openai_api("chat_completions")
        set_tracing_disabled(True)

        return openai_client


class AzureAIChatModel(AzureAIClient):
    def __init__(self, model: str, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Instantiate the parent class
        self.model = model

    def invoke(self, messages, **kwargs):
        """Invoke the model with messages to get the response message content"""

        chat_response = self.chat.completions.create(model=self.model, messages=messages, **kwargs)
        # return chat_response.choices[0].message.content
        return chat_response


if __name__ == "__main__":
    openai_llm = AzureAIChatModel(model="gpt-4o-mini")
    while True:
        user_input = input("Your Question: ")
        if user_input.lower() in ["exit", "quit"]:
            logger.info("Exiting chat.")
            break

        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
        response_message = openai_llm.invoke(messages=message)

        logger.success(f"Sample response:, {response_message.choices[0].message.content}")
