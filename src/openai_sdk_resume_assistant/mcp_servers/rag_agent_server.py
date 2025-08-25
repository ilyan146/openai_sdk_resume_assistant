from typing import List, Tuple

import numpy as np
from openai import AzureOpenAI

from src.openai_sdk_resume_assistant.client import AzureAIClient

"""
This file will be used to serve a RAG agent as a tool for the resume agent.

TODO:
- RAG tool --> Use embedding models to create vectorstore and use it to retrieve relevant information
- RAG Agent with tool integration
- RAG Agent is provided to other agents through MCP servers
"""


class RAGTool:
    """
    RAGTool class for connecting and retrieving from a vectorstore.
    """

    def __init__(self, collection, azure_ai_client: AzureAIClient | AzureOpenAI):
        """
        Initialize RAGtool with collection and azure ai client
        connection.
        """
        self.collection = collection
        self.azure_openai_client = azure_ai_client

    def _get_embeddings(self, text_input: str) -> np.ndarray:
        """Compute the embeddings for the given text input using an
        OpenAI model."""

        response = self.azure_openai_client.embeddings.create(input=text_input, model="text-embedding-ada-002")
        emb = np.array(response.data[0].embedding).astype("float32")
        return emb

    def _find_similar(self, text_input: str, top_k: int = 5) -> Tuple[List[str], List[str]]:
        """Find similar documents in the collection given a text input
        :param text_input: the text we want to search the document for
        :param top_k: the number of results to return that are similar

        :return: a tuple of two lists, the first is the list of document and the other is list of pages
        """
        results = self.collection.query(
            query_embeddings=self._get_embeddings(text_input=text_input).tolist(),
            n_results=top_k,
        )
        documents = results["documents"][0][:]
        pages = [page["page"] for page in results["metadatas"][0][:]]
        return documents, pages

    def create_rag_context(self, text_input: str) -> str:
        """Create more context for the Rag agent based on the input text using similar documents."""
        message = "To provide some context, here are some relevant documents:\n\n"
        # Find similar documents from the vector collection
        documents, pages = self._find_similar(text_input=text_input)
        # Create context from the documents
        for doc, page in zip(documents, pages, strict=False):
            message += f"Potentially related Document: {doc}\nPage number: {page}\n\n"
        return message
