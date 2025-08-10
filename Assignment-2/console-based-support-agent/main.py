import os
import re
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    function_tool,
    GuardrailFunctionOutput,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    output_guardrail,
    ItemHelpers
   
)
from dotenv import load_dotenv

# 📦 Load Gemini API key from .env
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY must be set in the .env file.")

# 🌐 Gemini client and model setup
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🧠 User context
class UserContext(BaseModel):
    name: str
    is_premium_user: bool
    issue_type: str

# 🧰 Tools
@function_tool
def refund(user_id: str) -> str:
    return f"✅ Refund processed for user ID: {user_id}"

@function_tool
def restart_service(service_name: str) -> str:
    return f"🔄 Service '{service_name}' restarted successfully."

# 🔐 Tool conditions
def refund_tool_is_enabled(context: UserContext) -> bool:
    return context.is_premium_user

def restart_tool_is_enabled(context: UserContext) -> bool:
    return context.issue_type.lower() == "technical"

@output_guardrail
def no_apologies(context, agent, output: str) -> GuardrailFunctionOutput:
    if re.search(r"\bsorry\b", output, re.IGNORECASE):
        return GuardrailFunctionOutput(
            output_info=output,
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered=False)

# 🤖 Agent factories
def get_billing_agent(context: UserContext) -> Agent:
    return Agent(
        name="BillingAgent",
        instructions="You are a billing agent. Handle only billing-related questions like refunds.",
        tools=[refund] if refund_tool_is_enabled(context) else [],
        output_guardrails=[no_apologies],
    )

def get_technical_agent(context: UserContext) -> Agent:
    return Agent(
        name="TechnicalAgent",
        instructions="You are a technical support agent. Handle only technical issues like restarting services.",
        tools=[restart_service] if restart_tool_is_enabled(context) else [],
        output_guardrails=[no_apologies],
    )

def get_triage_agent() -> Agent:
    return Agent(
        name="TriageAgent",
        instructions="Route the user to either billing or technical support based on their issue."
    )

# 🧭 Routing logic
def route_to_specialist(context: UserContext) -> str:
    issue = context.issue_type.lower().strip()
    if any(word in issue for word in ["refund", "payment", "invoice"]):
        return "billing"
    elif any(word in issue for word in ["restart", "not working", "crash", "error"]):
        return "technical"
    return "general"


# 🧪 Main CLI
async def main():
    print("🎓 Welcome to the Console-Based Support Agent System\n")

    name = input("👤 Your name: ")
    premium_input = input("💎 Are you a premium user? (yes/no): ").strip().lower()
    issue = input("📝 Describe your issue: ")

    context = UserContext(
        name=name,
        is_premium_user=(premium_input == "yes"),
        issue_type=issue
    )

    print("\n🤖 TriageAgent is analyzing your issue...")
    specialist_type = route_to_specialist(context)

    if specialist_type == "billing":
        agent = get_billing_agent(context)
    elif specialist_type == "technical":
        agent = get_technical_agent(context)
    else:
        print("⚠️ Unable to determine the correct support agent. Try describing your issue more clearly.")
        return

    print(f"➡️ Routing to {agent.name}...\n")

    # Start the run and stream events
    result =  Runner.run_streamed(
        starting_agent=agent,
        input=issue,
        context=context.model_dump(),
        run_config=config,
    )

    print("\n📡 Streaming tool execution and reasoning steps...\n")
    output_message=""
    async for event in result.stream_events():
        # Some events might not have .item, so guard against it
        if hasattr(event, "item"):
            if getattr(event.item, "type", None) == "tool_call_output_item":
                print(f"🛠️ Tool Output: {event.item.output}")
            elif getattr(event.item, "type", None) == "message_output_item":
                print(f"🧠 Agent Thought: {ItemHelpers.text_message_output(event.item)}")
        else:
            # You can optionally print or log unhandled events
            pass

    
    print("\n🎉 Support session completed. Thank you for using our service!")
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    



