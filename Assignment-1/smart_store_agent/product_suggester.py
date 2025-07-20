import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load .env variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Gemini-compatible OpenAI SDK client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Gemini Flash model via OpenAI-compatible wrapper
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define the Smart Store Agent
agent: Agent = Agent(
    name="SmartStoreAgent",
    instructions=(
        "You are a smart medical assistant. Based on the user's problem or symptom, "
        "suggest a relevant product (e.g., a medicine or remedy) and explain why it's helpful."
    ),
    model=model
)

# Input prompt from user
user_input = input("🛒 Tell me your issue : ")

# Run the agent synchronously
result = Runner.run_sync(agent, user_input, run_config=config)

# Show the suggestion
print("\n🤖 Product Suggestion:\n")
print(result.final_output)
