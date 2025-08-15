import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper, function_tool, input_guardrail, GuardrailFunctionOutput, output_guardrail, ModelSettings
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env file")

# Disable tracing
set_tracing_disabled(True)

# Create Gemini client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# Simulated database
BANK_DATABASE = {
    "Basit ali": {"pin": 1234, "balance": 5000.0}
}

# Pydantic models
class Account(BaseModel):
    name: str
    pin: int = Field(..., ge=1000, le=9999)

class GuardrailOutput(BaseModel):
    isNot_bank_related: bool

class OutputGuardrail(BaseModel):
    response: str
    is_safe: bool

class HandoffOutput(BaseModel):
    handoff_to_human: bool
    reason: str

# Guardrail agents
guardrail_agent = Agent(
    name="GuardrailAgent",
    instructions="Return isNot_bank_related=True if the query is not about banking.",
    output_type=GuardrailOutput,
    model=model
)

output_guardrail_agent = Agent(
    name="OutputGuardrailAgent",
    instructions="""
    You check if the response is safe.
    - Mark is_safe=False ONLY if it contains unsafe, private, or sensitive info that should NOT be shown to the authenticated user.
    - If the user is authenticated and the response contains only their own account balance, set is_safe=True.
    - Do NOT flag showing a user's own balance as unsafe.
    """,
    output_type=OutputGuardrail,
    model=model
)



handoff_agent = Agent(
    name="HandoffAgent",
    instructions="""
    Only set handoff_to_human=True if:
    - The request is NOT a simple balance inquiry (with context available)
    - OR it is unclear/ambiguous and cannot be resolved
    - OR it requires human approval (e.g., transfers, disputes)
    Simple 'check balance' queries with context should always be handoff_to_human=False.
    """,
    output_type=HandoffOutput,
    model=model
)

suspicious_activity_handoff_agent = Agent(
    name="SuspiciousActivityHandoffAgent",
    instructions="Detect suspicious activity, otherwise set handoff_to_human=False.",
    output_type=HandoffOutput,
    model=model
)

# Guardrail decorators
@input_guardrail
async def check_bank_related(ctx: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    runner = Runner()
    result = await runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.isNot_bank_related
    )

@output_guardrail
async def check_output_safety(ctx: RunContextWrapper[None], agent: Agent, output: str) -> GuardrailFunctionOutput:
    runner = Runner()
    result = await runner.run(output_guardrail_agent, output, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=not result.final_output.is_safe
    )

# Authentication check
def check_user(ctx: RunContextWrapper[Account], agent: Agent) -> bool:
    return (
        ctx.context
        and ctx.context.name in BANK_DATABASE
        and BANK_DATABASE[ctx.context.name]["pin"] == ctx.context.pin
    )

# Bank balance tool
@function_tool(is_enabled=check_user)
def check_balance(ctx: RunContextWrapper[Account]) -> str:
    name = ctx.context.name
    balance = BANK_DATABASE[name]["balance"]
    return f"The balance for {name} is ${balance:.2f}"

# Dynamic instructions
def dynamic_instruction(ctx: RunContextWrapper[Account], agent: Agent):
    return f"You are a Bank Agent for SecureBank. You only help with balance checks for {ctx.context.name}."

# Bank Agent
bank_agent = Agent(
    name="BankAgent",
    instructions=dynamic_instruction,
    tools=[check_balance],
    input_guardrails=[check_bank_related],
    output_guardrails=[check_output_safety],
    model_settings=ModelSettings(
        temperature=0.2,
        tool_choice='required',
        max_tokens=1000
    ),
    model=model
)
# CLI loop
while True:
    print("\nBank Agent CLI")
    print("1. Check Balance")
    print("2. Exit")
    choice = input("Choose an option (1-2): ")
    if choice == "2":
        print("Goodbye!")
        break
    if choice == "1":
        name = input("Enter your name: ")
        query = input("Enter your query: ")
        try:
            pin = int(input("Enter 4-digit PIN: "))
            user_context = Account(name=name, pin=pin)
            # Run Bank Agent first
            result = Runner.run_sync(
                bank_agent,
                input=query,
                context=user_context
            )
            # Then run handoff check
            handoff_result = Runner.run_sync(
                handoff_agent,
                input=f"User query: {query}\nBank Agent Output: {result.final_output}",
                context=user_context
            )
            if handoff_result.final_output.handoff_to_human:
                print(f"Handoff to human required: {handoff_result.final_output.reason}")
                continue
            # Suspicious activity check
            suspicious_result = Runner.run_sync(
                suspicious_activity_handoff_agent,
                input=f"User query: {query}\nBank Agent Output: {result.final_output}",
                context=user_context
            )
            if suspicious_result.final_output.handoff_to_human:
                print(f"Suspicious activity detected! Reason: {suspicious_result.final_output.reason}")
                continue
            print(result.final_output)
        except ValueError:
            print("Error: PIN must be a 4-digit number")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Invalid choice. Try again.")

