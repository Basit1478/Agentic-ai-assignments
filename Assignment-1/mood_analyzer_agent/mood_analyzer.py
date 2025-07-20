from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import os
from dotenv import load_dotenv
# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in your .env file")
# Gemini setup
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# ------------------------ Agent 1: Mood Analyzer ------------------------
mood_agent = Agent(
    name="MoodAnalyzer",
    instructions=(
        "You are a mood detection expert. Analyze the user's message and return only the mood. "
        "Examples: happy, sad, stressed, anxious, excited, relaxed, angry, etc. Respond with only one word."
    ),
    model=model
)

# ------------------------ Agent 2: Support Agent ------------------------
support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "You are a caring assistant. If the user's mood is 'sad' or 'stressed', suggest a helpful activity or advice. "
        "Give a short, supportive response. If the mood is something else, just say: 'No support needed.'"
    ),
    model=model
)
# ------------------------ Run Program ------------------------
user_input = input("🧠 How are you feeling today? Describe in a sentence: ")
# Step 1: Detect Mood
mood_result = Runner.run_sync(mood_agent, user_input, run_config=config)
mood = mood_result.final_output.lower().strip()

print(f"\n🔎 Detected Mood: {mood}")
# Step 2: Provide Support if necessary
if "sad" in mood or "stressed" in mood:
    support_result = Runner.run_sync(support_agent, mood, run_config=config)
    print("\n🤖 Support Suggestion:\n")
    print(support_result.final_output)
else:
    print("\n✅ You seem to be doing well! Keep it up 💪")
