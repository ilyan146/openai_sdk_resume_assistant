import numpy as np
from agents import function_tool
from loguru import logger
from openai import AzureOpenAI

from openai_sdk_resume_assistant.base_agent import AIAgent
from openai_sdk_resume_assistant.client import AzureAIClient
from openai_sdk_resume_assistant.mcp_params import playwright_params
from openai_sdk_resume_assistant.RAG.vector_db import VectorDB

"""
This file will be used to serve a RAG agent as a tool for the resume agent.

TODO:
- RAG tool --> Use embedding models to create vectorstore and use it to retrieve relevant information [DONE]
- RAG Agent with tool integration [DONE]
- RAG Agent is provided to other agents through MCP servers
"""


class RAGTool:
    """
    RAGTool class for connecting and retrieving from a vectorstore.
    """

    def __init__(self, collection_name: str, azure_ai_client: AzureAIClient | AzureOpenAI, db_name: str = "default_vectorstore"):
        """
        Initialize RAGtool with collection and azure ai client
        connection.
        """
        self.vector_db = VectorDB(vector_db_name=db_name, azure_openai_client=azure_ai_client)
        self.collection_name = collection_name
        self.collection = self._get_chroma_collection()
        self.azure_openai_client = azure_ai_client

    def _get_chroma_collection(self):
        """Get the chroma collection from the vector database."""
        collection = self.vector_db.get_or_create_collection(collection_name=self.collection_name)
        logger.info(f"Using ChromaDB collection: {self.collection_name}")
        return collection

    def _get_embeddings(self, text_input: str) -> np.ndarray:
        """Compute the embeddings for the given text input using an
        OpenAI model."""

        response = self.azure_openai_client.embeddings.create(input=text_input, model="text-embedding-ada-002")
        emb = np.array(response.data[0].embedding).astype("float32")
        return emb

    def _find_similar(self, text_input: str, top_k: int = 5) -> tuple[list[str], list[str]]:
        """Find similar documents in the collection given a text input
        :param text_input: the text we want to search the document for
        :param top_k: the number of results to return that are similar

        :return: a tuple of two lists, the first is the list of document and the other is list of pages
        """
        results = self.collection.query(
            query_embeddings=self._get_embeddings(text_input=text_input).tolist(),
            n_results=top_k,
        )
        logger.debug(f"Retrieved {len(results['documents'][0])} similar documents from the collection.")
        documents = results["documents"][0][:]
        pages = [page["page"] for page in results["metadatas"][0][:]]
        return documents, pages

    # @function_tool
    def create_rag_context(self, text_input: str) -> str:
        """Create more context for the Rag agent based on the input text using similar documents."""
        message = "To provide some context, here are some relevant documents:\n\n"
        # Find similar documents from the vector collection
        documents, pages = self._find_similar(text_input=text_input)
        # Create context from the documents
        for doc, page in zip(documents, pages, strict=False):
            message += f"Potentially related Document: {doc}\nPage number: {page}\n\n"
        logger.info(f"RAG context created successfully. {message}")
        return message


RAG_AGENT_INSTRUCTIONS = """
You are a retrieval assistant focused exclusively on questions about Ilyan.
Always call the tool `create_rag_context` first with the user's full query before drafting an answer.
If the tool returns no documents, state that clearly.
Answer using only retrieved factual context; do not invent details.
"""


# Create the rag agent
async def create_rag_agent(collection_name: str, db_name: str = "resume_vectorstore"):  # -> AIAgent:
    client = AzureAIClient()
    _openai_client = client.set_openai_client_defaults()

    rag_tool = RAGTool(
        collection_name=collection_name,
        azure_ai_client=client,
        db_name=db_name,
    )

    @function_tool
    def create_rag_context(text_input: str) -> str:
        """Retrieve similar resume documents for the given query."""
        return rag_tool.create_rag_context(text_input)

    rag_agent = AIAgent(
        name="RAGAgent",
        instructions=RAG_AGENT_INSTRUCTIONS,
        model="gpt-4o",
        tools=[create_rag_context],
        mcp_params=[playwright_params],
    )

    return rag_agent


if __name__ == "__main__":
    import asyncio

    COLLECTION_NAME = "ilyan_resume"
    # COLLECTION_NAME = "sample_texts"

    rag_agent_instance = asyncio.run(create_rag_agent(collection_name=COLLECTION_NAME))

    async def main(user_input: str):
        """
        Run the RAG agent with the provided user input.
        """
        response = await rag_agent_instance.run_agent_with_mcp(user_input)
        return response

    while True:
        text_input = input("Enter your question for RAG Agent: ")
        if text_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response = asyncio.run(main(text_input))
        print("Response:", response)
