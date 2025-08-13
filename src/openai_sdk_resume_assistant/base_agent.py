from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, Dict, List

from agents import Agent, Runner
from agents.mcp import MCPServerStdio


class AIAgent:
    """
    This is the base agent class that can be used to create agents with tools that are served through MCP servers.
    """

    def __init__(self, name: str, instructions: str, model: str, mcp_params: List[Dict[str, Any]] | Dict[str, Any]):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.mcp_params_list = self._create_mcp_params_list(mcp_params)

    # Internal converter for the params
    def _create_mcp_params_list(self, mcp_params) -> List[Dict[str, Any]]:
        if isinstance(mcp_params, dict):
            return [mcp_params]
        elif isinstance(mcp_params, list):
            return mcp_params
        else:
            raise ValueError("mcp_params must be a dict or a list of dicts.")

    @asynccontextmanager
    async def _get_mcp_servers(self) -> List[MCPServerStdio]:  # type:ignore
        async with AsyncExitStack() as stack:
            tool_mcp_servers = [
                await stack.enter_async_context(MCPServerStdio(params=params, client_session_timeout_seconds=60))
                for params in self.mcp_params_list
            ]
            yield tool_mcp_servers

    async def _create_agent(self, mcp_servers_list: List[MCPServerStdio] | None) -> Agent:
        """
        Create an Agent instance with the provided MCP servers.
        """
        agent = Agent(name=self.name, instructions=self.instructions, model=self.model, mcp_servers=mcp_servers_list)
        return agent

    async def run_agent_with_mcp(self, user_input: str):
        """
        Create agents with MCP servers and run with the provided user input
        """
        async with self._get_mcp_servers() as servers:
            active_agent = await self._create_agent(servers)
            response = await Runner.run(active_agent, input=user_input)

        return response.final_output
