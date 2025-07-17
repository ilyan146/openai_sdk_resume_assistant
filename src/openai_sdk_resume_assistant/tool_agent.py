import os

from agents import Agent
from agents.mcp import MCPServerStdio

TOOL_AGENT_INSTRUCTIONS = """
You are a tool agent that can use tools for browsing the internet and 
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
tools_params = {"command": "uv", "args": ["run", "src/openai_sdk_resume_assistant/agent_tools.py"]}


# Create mcp servers with the params
params_list = [playwright_params, files_params]
tool_mcp_servers = [MCPServerStdio(params, client_session_timeout_seconds=30) for params in params_list]


# Connect to the servers
async def connect_to_servers(mcp_servers):
    for server in mcp_servers:
        await server.connect()


tool_agent = Agent(name="ToolAgent", instructions=TOOL_AGENT_INSTRUCTIONS, model="gpt-4o", mcp_servers=tool_mcp_servers)
