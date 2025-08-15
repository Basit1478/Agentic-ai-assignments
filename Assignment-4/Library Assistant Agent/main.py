import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    function_tool, input_guardrail, GuardrailFunctionOutput,AsyncOpenAI,
    RunContextWrapper, ModelSettings, set_tracing_disabled
)

# ------------------ Setup ------------------

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# ------------------ Book Database ------------------

BOOK_DATABASE = {
    "The Great Technology": {"copies": 3},
    "The 80's Technologies": {"copies": 0},
    "Enter the Agentic Ai World": {"copies": 5}

}

# ------------------ Context Model ------------------


class SingleUser(BaseModel):
    name: str
    member_id: str

class MultiUserContext(BaseModel):
    users: list[SingleUser]
# ------------------ Guardrail Output ------------------

class GuardrailOutput(BaseModel):
    isNot_library_related: bool = Field(
        ..., description="True if the query is NOT related to library services"
    )

# ------------------ Guardrail Agent ------------------

guardrail_agent = Agent(
    name="LibraryGuardrailAgent",
    instructions="""
    Determine if the user's query is related to library services.
    
    Library-related topics include:
    - Searching for a book (even if the book is not in the database)
    - Checking book availability
    - Asking for library timings

    Not related topics include:
    - Weather, banking, cooking, sports, unrelated events

    If the query is about a book (search or availability) or timings,
    return isNot_library_related=False.
    Only return isNot_library_related=True if it is completely unrelated.
    """,
    output_type=GuardrailOutput,
    model=model
)


# ------------------ Input Guardrail ------------------

@input_guardrail
async def check_library_related(ctx: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    runner= Runner()
    result = await runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.isNot_library_related
    )

# ------------------ Member Check Function ------------------

def is_valid_member(ctx: RunContextWrapper[MultiUserContext], agent: Agent) -> bool:
    return any(u.member_id.strip() for u in ctx.context.users)

# ------------------ Function Tools ------------------

@function_tool()
def search_book(ctx: RunContextWrapper[MultiUserContext], title: str) -> str:
    if title in BOOK_DATABASE:
        return f"'{title}' is available in our catalog."
    else:     
        return f"'{title}' is not found in our catalog."

@function_tool(is_enabled=is_valid_member)
def check_availability(ctx: RunContextWrapper[MultiUserContext], title: str) -> str:
    if title not in BOOK_DATABASE:
        return f"'{title}' is not found in our catalog."
    copies = BOOK_DATABASE[title]["copies"]
    if copies > 0:
        return f"'{title}' has {copies} copies available."
    else:
        return f"'{title}' is currently out of stock."

@function_tool()
def library_timings(ctx: RunContextWrapper[MultiUserContext]) -> str:
    return "The library is open from 9 AM to 8 PM, Monday to Saturday."

# ------------------ Dynamic Instructions ------------------

def dynamic_instruction(ctx: RunContextWrapper[MultiUserContext], agent: Agent):
    names = ", ".join([u.name for u in ctx.context.users])
    return f"""
    You are a helpful Library Assistant for the City Library.
    Begin every response with greet **all users together**  by their names: {names}.
    You can search for books, check availability for registered members,
    and give library timings. Ignore non-library queries.
    """

# ------------------ Library Agent ------------------

library_agent = Agent(
    name="LibraryAgent",
    instructions=dynamic_instruction,
    tools=[search_book, check_availability, library_timings],
    input_guardrails=[check_library_related],
    model_settings=ModelSettings(
        temperature=0.2,
        tool_choice="auto",
        max_tokens=800
    ),
    model=model
)
# ------------------ Test ------------------
if __name__ == "__main__":
    user_context = MultiUserContext(
        users=[
            SingleUser(name="Basit ali", member_id="M12346"),
            SingleUser(name="Sir Asharib Ali", member_id="M12347"),
            SingleUser(name="Sir Naeem Hussain", member_id="M12345")
            ]
    )
    queries = [
        "Search for Book : Enter the Agentic Ai World",
        "Check availability for Book: The 80's Technologies",
        "Check Library timings",
        "What's the weather like?"
    ]

from agents.exceptions import InputGuardrailTripwireTriggered

for q in queries:
    print(f"\nUser: {q}")
    try:
        result = Runner.run_sync(library_agent, input=q, context=user_context)
        print("Assistant:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Assistant: Sorry to all users, I can only help with library-related questions.")