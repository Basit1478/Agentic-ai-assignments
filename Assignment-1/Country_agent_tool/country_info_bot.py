import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.run import RunConfig
from agents import function_tool
# 🔐 Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ----- 🛠️ TOOLS -----
@function_tool
def get_country_name(country: str) -> str:
    """Returns the official name of the given country."""
    try:
        res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
        data = res.json()[0]
        name = data.get("name", {}).get("official", "N/A")
        return f"The official name of {country} is {name}."
    except Exception as e:
        return f"Error fetching country name: {e}"

@function_tool
def get_country_population(country: str) -> str:
    """Returns the population of the given country."""
    try:
        res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
        data = res.json()[0]
        pop = data.get("population", "N/A")
        return f"{country} has a population of {pop:,} people."
    except Exception as e:
        return f"Error fetching population: {e}"

@function_tool
def get_country_capital(country: str) -> str:
    """Returns the capital of the given country."""
    try:
        res = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
        data = res.json()[0]
        capital = data.get("capital", ["N/A"])[0]
        return f"The capital of {country} is {capital}."
    except Exception as e:
        return f"Error fetching capital: {e}"
# ----- ⚙️ GEMINI CLIENT -----
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)
# ----- 🧠 AGENT SETUP -----
agent = Agent(
    name="CountryBot",
    instructions=(
        "You're a helpful assistant that answers country-related questions using tools like:\n"
        "- get_country_name\n"
        "- get_country_population\n"
        "- get_country_capital\n"
        "Always use tools when relevant to get accurate and fresh data."
    ),
    model=model,
    tools=[get_country_name, get_country_population, get_country_capital],
)
# ----- 🔁 CONFIG -----
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)
# ----- 🚀 MAIN QUERY -----
if __name__ == "__main__":
    query = input("🌍 Ask about a country: ")
    result = Runner.run_sync(agent, query, run_config=config)
    print("\n🧠 Agent Output:")
    print(result.final_output)
