"""The RAG agent module will be served here"""

import asyncio

from fastmcp import FastMCP

from openai_sdk_resume_assistant.RAG.rag_agent import create_rag_agent

# Create a mcp server
rag_mcp = FastMCP(name="rag_agent_server")

# Create the rag agent first
COLLECTION_NAME = "ilyan_resume"
rag_agent = asyncio.run(create_rag_agent(collection_name=COLLECTION_NAME))


@rag_mcp.tool(name="RAG_tool", description="RAG tool for retrieving relevant documents from the vector database")
async def rag_agent_tool(query: str) -> str:
    """RAG Agent TOOL to use a rag agent as tool to retrieve relevant information about Ilyan and his resume."""
    rag_agent_response = await rag_agent.run_agent_with_mcp(query)
    return rag_agent_response


if __name__ == "__main__":
    rag_mcp.run(transport="stdio")
