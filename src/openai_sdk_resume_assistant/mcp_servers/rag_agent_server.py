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

    def __init__(self, collection, azure_ai_client):
        """
        Initialize RAGtool with collection and azure ai client
        connection.
        """
