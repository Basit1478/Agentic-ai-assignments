🛒 Smart Store Agent — Powered by Gemini
A medical assistant AI agent built using the OpenAI Agents SDK with Gemini API support. This intelligent assistant helps users by analyzing symptoms or health-related issues and suggesting relevant medicines or remedies.

✨ Features
🤖 AI-Powered Suggestions using Gemini 2.0 Flash model

🩺 Health symptom input and relevant product recommendation

⚡ OpenAI-Compatible Gemini Integration

🧠 Custom instructions to ensure domain-specific reasoning

📁 Project Structure
bash
Copy
Edit
smart-store-agent/
│
├── smart_store_agent.py     # Main agent logic
├── .env                     # Environment variables (API key)
├── requirements.txt         # Dependencies (optional if using uv)
└── README.md                # You're here!
⚙️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/Basit1478/Agentic-ai-assignments/Assignment-1/smart_store_agent.git
cd smart-store-agent
2. Set up environment
Create a .env file and add your Gemini API Key:

ini
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
🔐 You can get a Gemini API key from: https://aistudio.google.com/app/apikey

3. Install dependencies (via uv or pip)
Option A: Using uv
bash
Copy
Edit
uv venv
uv pip install -r requirements.txt
uv run smart_store_agent.py
Option B: Using regular venv
bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python smart_store_agent.py
📌 How to Use
Run the script and enter your health concern:

bash
Copy
Edit
$ uv run smart_store_agent.py
🛒 Tell me your issue : I have a headache and mild fever

🤖 Product Suggestion:
You can take Paracetamol, which is effective for both pain relief and fever reduction...
📦 Requirements
You can create a requirements.txt like this (for pip fallback):

txt
Copy
Edit
python-dotenv
openai-agents
🧪 Agent Prompt
“You are a smart medical assistant. Based on the user's problem or symptom, suggest a relevant product (e.g., a medicine or remedy) and explain why it's helpful.”
