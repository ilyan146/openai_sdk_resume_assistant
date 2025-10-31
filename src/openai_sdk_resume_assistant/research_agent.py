import os

from openai_sdk_resume_assistant.client import AzureAIClient
from openai_sdk_resume_assistant.mcp_params import playwright_params
from src.openai_sdk_resume_assistant.base_agent import AIAgent

RESEARCH_AGENT_INSTRUCTIONS = """
You are a research agent that can use tools for browsing the internet and
you also have access to my file system.
You are highly capable to accomplish your tasks independently.
This includes accepting all cookies and clicking 'not now' as appropriate to get the content you need.
If one website isn't fruitful, try another.
Be persistent until you are able to solve your assignment,
trying different options and sites are needed.
If the amount of information in one site is too large, please summarize it before using it.
"""


# # List of params
# playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}

file_storage_path = os.path.abspath(os.path.join(os.getcwd(), "file_storage"))
files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", file_storage_path]}

# # send_email_params = {"command": "uv", "args": ["run", "agent_tools.py"]}

# memory_params = {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": "file:./memory/ed.db"}}


# Create mcp servers with the params
# params_list = [playwright_params, files_params, memory_params]
params_list = [playwright_params]


research_agent = AIAgent(
    name="ResearchAgent",
    instructions=RESEARCH_AGENT_INSTRUCTIONS,
    model="gpt-4o",
    mcp_params=params_list,
)


async def main(user_input: str):
    """
    Run the research agent with the provided user input.
    """
    # Set the AzureAI client defaults
    client = AzureAIClient()
    _openai_client = client.set_openai_client_defaults()

    response = await research_agent.run_agent_with_mcp(user_input)
    return response


if __name__ == "__main__":
    import asyncio

    user = (
        "Hey get me some useful information about Hong Kong and where can I go when there is a typhoon and please "
        "write the information to a file named 'hong_kong_typhoon_info.md' as a markdown file."
    )

    muthuvapa_input = (
        "Please find all the contact information for the RTO office chennai and write to the file "
        "'rto_chennai_contact_info.md' as a markdown file."
    )

    news_input = (
        "My name is Ilyan and I am a Journalist, please find top news from BBC about Gaza Israel conflict "
        "and write to file gaza_report.md as a markdown file."
    )

    check_input = "Hey what is my name and what are the news that you searched for before ?"

    # result = asyncio.run(main(news_input))
    result = asyncio.run(main(user))
    print("Response from Research Agent:", result)
