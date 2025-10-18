from .base_agent import AIAgent
from .client import AzureAIClient
from .mcp_params import playwright_params

NAME = "Mohamed Ilyan"

RESUME_AGENT_INSTRUCTIONS = f"""
You are acting as {NAME}. You are answering questions on {NAME}'s career,
education, background, skills and experience.
Your responsibility is to represent {NAME} in the best way possible and
as faithfully as possible with the given information.
You are provided with {NAME}'s resume and a summary of his background, which
you can use to answer questions.
Be professional and engaging, as if talking to a potential client or future employer
who came across the resume or profile.
"""  # TODO: To be added with new tools to record unknown questions and send emails

mcp_params_list = [playwright_params]

resume_agent = AIAgent(name="ResumeAgent", instructions=RESUME_AGENT_INSTRUCTIONS, model="gpt-4o", mcp_params=mcp_params_list)

if __name__ == "__main__":
    import asyncio

    # Set the AzureAI client defaults
    client = AzureAIClient()
    _openai_client = client.set_openai_client_defaults()

    async def main(user_input: str):
        """
        Run the research agent with the provided user input.
        """
        response = await resume_agent.run_agent_with_mcp(user_input)
        return response

    while True:
        text_input = input("Enter your question: ")
        if text_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response = asyncio.run(main(text_input))
        print("Response:", response)
