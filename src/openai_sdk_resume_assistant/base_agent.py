# type: ignore
import os
from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from openai.types.responses import ResponseTextDeltaEvent


class AIAgent:
    """
    This is the base agent class that can be used to create agents with tools that are served through MCP servers.
    Args:
        name (str): The name of the agent.
        instructions (str): The instructions for the agent.
        model (str): The model to use for the agent.
        mcp_params (List[Dict[str, Any]] | Dict[str, Any]): MCP server parameters.
        **agent_kwargs: Additional keyword arguments passed to the Agent class.
            See agents.Agent class documentation for all available parameters including:
            - handoff_description: Description used when agent is used as handoff
            - tools: List of tools the agent can use
            - handoffs: List of sub-agents for delegation
            - model_settings: Model-specific tuning parameters
            - input_guardrails: Input validation checks
            - output_guardrails: Output validation checks
            - output_type: Type of the output object
            - hooks: Lifecycle event callbacks
            - tool_use_behavior: How tool use is handled
            And more. Refer to agents.Agent for complete documentation.
    """

    def __init__(
        self, name: str, instructions: str, model: str, mcp_params: list[dict[str, Any]] | dict[str, Any], **agent_kwargs
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.mcp_params_list = self._create_mcp_params_list(mcp_params)
        self.agent_kwargs = agent_kwargs

    # Internal converter for the params
    @staticmethod
    def _create_mcp_params_list(mcp_params) -> list[dict[str, Any]]:
        if isinstance(mcp_params, dict):
            return [mcp_params]
        elif isinstance(mcp_params, list):
            return mcp_params
        else:
            raise ValueError("mcp_params must be a dict or a list of dicts.")

    @asynccontextmanager
    async def _get_mcp_servers(self):  # -> List[MCPServerStdio]:  # type:ignore
        async with AsyncExitStack() as stack:
            tool_mcp_servers = [
                await stack.enter_async_context(
                    MCPServerStdio(params=params, client_session_timeout_seconds=60, env={**os.environ})
                )  # type:ignore
                for params in self.mcp_params_list
            ]
            yield tool_mcp_servers

    async def _create_agent(self, mcp_servers_list: list[MCPServerStdio] | None) -> Agent:
        """
        Create an Agent instance with the provided MCP servers and any other kwargs.
        """
        agent = Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model,
            mcp_servers=mcp_servers_list,
            **self.agent_kwargs,
        )
        return agent

    async def run_agent_with_mcp(self, user_input: str):
        """
        Create agents with MCP servers and run with the provided user input
        """
        async with self._get_mcp_servers() as servers:
            active_agent = await self._create_agent(servers)
            response = await Runner.run(active_agent, input=user_input)

        return response.final_output

    # Add streaming support as per the agents sdk docs
    async def run_agent_with_mcp_stream(self, user_input: str) -> AsyncGenerator[str, None]:
        """
        Stream agent responses as they are generated
        """
        async with self._get_mcp_servers() as servers:
            active_agent = await self._create_agent(servers)
            result = Runner.run_streamed(active_agent, input=user_input)

            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    yield event.data.delta
