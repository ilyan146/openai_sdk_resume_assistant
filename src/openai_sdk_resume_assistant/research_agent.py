import os

from openai_sdk_resume_assistant.base_agent import AIAgent
from src.openai_sdk_resume_assistant.client import AzureAIClient

RESEARCH_AGENT_INSTRUCTIONS = """
You are a research agent that can use tools for browsing the internet and 
you can also have access to my file system. 
You are highly capable to accomplish your tasks independently. 
This includes accepting all cookies and clicking 'not now' as appropriate to get the content you need. 
If one website isn't fruitful, try another. 
Be persistent until you are able to solve your assignment, 
trying different options and sites are needed.
"""


# List of params
playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}

file_storage_path = os.path.abspath(os.path.join(os.getcwd(), "file_storage"))
files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", file_storage_path]}

# send_email_params = {"command": "uv", "args": ["run", "agent_tools.py"]}


# Create mcp servers with the params
params_list = [playwright_params, files_params]


research_agent = AIAgent(
    name="ResearchAgent",
    instructions=RESEARCH_AGENT_INSTRUCTIONS,
    model="gpt-4o",
    mcp_params=params_list,
)

# @asynccontextmanager
# async def get_mcp_servers(params_list):
#     async with AsyncExitStack() as stack:
#         tool_mcp_servers = [
#             await stack.enter_async_context(MCPServerStdio(params=params, client_session_timeout_seconds=60))
#             for params in params_list
#             ]
#         yield tool_mcp_servers


# async def create_tool_agent(mcp_servers_list:list):
#     tool_agent = Agent(
#         name="ToolAgent",
#         instructions=TOOL_AGENT_INSTRUCTIONS,
#         model="gpt-4o",
#         mcp_servers=mcp_servers_list)
#     return tool_agent


async def main(user_input: str):
    """
    Run the research agent with the provided user input.
    """
    # Set the azure ai client defaults
    client = AzureAIClient()
    _openai_client = client.set_openai_client_defaults()

    response = await research_agent.run_agent_with_mcp(user_input)
    return response


if __name__ == "__main__":
    import asyncio

    user_input = "Hey get me some useful information about Hong Kong and where can I go when there is a typhoon."
    response = asyncio.run(main(user_input))
    print("Response from Research Agent:", response)
