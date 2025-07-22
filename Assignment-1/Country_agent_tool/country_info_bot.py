import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.run import RunConfig
from agents import function_tool

# 🔐 Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🌍 Tool 1: Official Name
@function_tool
def get_country_official_name(country: str) -> str:
    """Returns the official name of the given country."""
    res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
    data = res.json()[0]
    official_name = data.get("name", {}).get("official", "N/A")
    return f"The official name of {country} is '{official_name}'."

# 🏙️ Tool 2: Capital
@function_tool
def get_country_capital(country: str) -> str:
    """Returns the capital city of the given country."""
    res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
    data = res.json()[0]
    capital = data.get("capital", ["N/A"])[0]
    return f"The capital of {country} is {capital}."

# 👥 Tool 3: Population
@function_tool
def get_country_population(country: str) -> str:
    """Returns the population of the given country."""
    res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
    data = res.json()[0]
    population = data.get("population", "N/A")
    return f"The population of {country} is {population:,}."

# 🗣️ Tool 4: Languages
@function_tool
def get_country_languages(country: str) -> str:
    """Returns the official languages of the given country."""
    res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
    data = res.json()[0]
    languages = data.get("languages", {})
    lang_list = ", ".join(languages.values())
    return f"The official languages of {country} are: {lang_list}."

# 🔧 Gemini Client Setup
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# 🤖 Define Agent
agent = Agent(
    name="CountryInfoAgent",
    instructions="You are an expert on countries. Answer the user's questions using tools to provide the official name, capital, population, and languages.",
    model=model,
    tools=[
        get_country_official_name,
        get_country_capital,
        get_country_population,
        get_country_languages
    ],
)

# 🛠️ Run Config (Tracing Disabled)
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# 🚀 Entry Point
if __name__ == "__main__":
    user_input = input("🌍 Enter country name or ask a question: ")
    result = Runner.run_sync(agent, user_input, run_config=config)
    print("\n📘 Response:")
    print(result.final_output)
