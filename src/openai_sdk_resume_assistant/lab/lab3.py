import asyncio

from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

from openai_sdk_resume_assistant.base_agent import AIAgent
from openai_sdk_resume_assistant.client import AzureAIClient

load_dotenv(override=True)


async def main():
    params = {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": "file:./memory/ed.db"}}

    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        mcp_tools = await server.list_tools()
        # print(mcp_tools)

    return mcp_tools


async def agent_main(request: str):
    agent_params = {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": "file:./memory/ilyan.db"}}
    instructions = "You use your entity tools as a persistent memory to store and recall information about your conversations."

    memory_agent = AIAgent(
        name="MemoryAgent",
        instructions=instructions,
        model="gpt-4o",
        mcp_params=agent_params,
    )

    # Set the AzureAI client defaults
    client = AzureAIClient()
    _openai_client = client.set_openai_client_defaults()

    response = await memory_agent.run_agent_with_mcp(request)

    return response


if __name__ == "__main__":
    tools = asyncio.run(main())
    print("Tools available from the MCP server: ")
    for tool in tools:
        print(tool)

    # request= (
    #     "My name's Ilyan. I'm an AI engineer. I'm teaching a course about AI Agents, including the incredible "
    #     "MCP protocol. MCP is a protocol for connecting agents with tools, "
    #     "resources and prompt templates, and makes it easy to integrate AI agents with capabilities."
    # )

    # request = "My name's Ilyan. What do you know about me?"

    request = "Who is an AI engineer that you know of ?"

    response = asyncio.run(agent_main(request))

    print("Final response from agent:", response)
