import asyncio
import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
# Gemini API key and endpoint setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

async def main():
    agent = Agent(
        name="SupportAgent",
        instructions="You are a helpful technical support assistant. Answer questions clearly and concisely.",
        model=OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=client),
    )

    while True:
        query = input("👤 User: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting Support Agent.")
            break

        result = await Runner.run(agent, query)
        print("🤖 Support Agent:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
