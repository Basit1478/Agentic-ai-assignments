🖥 Console-Based Support Agent System (Gemini API + OpenAI Agents SDK)
📌 Overview

This is a CLI-based multi-agent customer support system that uses OpenAI Agents SDK with Gemini API to route customer queries to the correct specialist agent (Billing or Technical Support) and execute relevant tools.

Roman Urdu:
Ye ek CLI-based customer support system hai jo OpenAI Agents SDK aur Gemini API ka use karta hai. Ye user ke issue ko analyze karke sahi agent (Billing ya Technical) ke paas route karta hai aur relevant tools run karta hai.

✨ Features

Triage Agent for routing to correct support type

Billing Agent for handling refund/payment issues

Technical Agent for handling technical issues

Tool Execution (refund processing, service restart)

Guardrails to block unwanted phrases like apologies

Gemini API Integration for AI reasoning

📂 Files & Structure
main.py          # Main script with agents, guardrails, routing, and CLI logic
.env             # Environment variables file (contains GEMINI_API_KEY)
README.md        # Documentation
requirements.txt # Python dependencies

⚙️ Requirements

Python 3.10+

Gemini API Key (from Google AI Studio)

📦 Installation

1️⃣ Clone the repository

git clone https://github.com/yourusername/support-agent-cli.git
cd support-agent-cli


2️⃣ Create and activate virtual environment

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Create .env file

GEMINI_API_KEY=your_gemini_api_key_here

▶️ How to Run
python main.py

🖥 Example CLI Flow
🎓 Welcome to the Console-Based Support Agent System

👤 Your name: Ali Khan
💎 Are you a premium user? (yes/no): yes
📝 Describe your issue: refund for last payment

🤖 TriageAgent is analyzing your issue...
➡️ Routing to BillingAgent...

📡 Streaming tool execution and reasoning steps...

🛠️ Tool Output: ✅ Refund processed for user ID: Ali Khan

🎉 Support session completed. Thank you for using our service!

🔒 Guardrails

Output is checked for the word "sorry" and blocked if found

Tool access depends on user context:

Refund Tool → Premium users only

Restart Service Tool → Technical issues only

🛠 Technologies Used

Python

OpenAI Agents SDK

Gemini API

Pydantic

python-dotenv
