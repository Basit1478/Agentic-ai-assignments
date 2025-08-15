🏦 Bank Agent CLI (Gemini API + OpenAI Agents SDK)
📌 Overview

This is a console-based banking agent built with OpenAI Agents SDK and Gemini API.
It allows a user to securely check their account balance using guardrails, authentication, and agent handoff checks.

Roman Urdu:
Ye ek console-based banking agent hai jo OpenAI Agents SDK aur Gemini API ka use karta hai.
Ye user ko secure tarike se apna balance check karne ka option deta hai, guardrails aur authentication ke sath.

✨ Features

Secure Authentication (PIN verification)

Balance Inquiry Tool

Guardrails for safe input/output

Handoff Agents for complex or suspicious requests

Environment-based API Key Loading

📂 Files & Structure
main.py          # Main program with agents, guardrails, and CLI loop
.env             # Environment variables file (stores GEMINI_API_KEY)
README.md        # Documentation
requirements.txt # Python dependencies

⚙️ Requirements

Python 3.10+

Gemini API Key (from Google AI Studio)

📦 Installation

1️⃣ Clone the repository

git clone https://github.com/yourusername/bank-agent-cli.git
cd bank-agent-cli


2️⃣ Create and activate virtual environment

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Set up .env file
Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

▶️ How to Run
python main.py

🖥 Example CLI Flow
Bank Agent CLI
1. Check Balance
2. Exit
Choose an option (1-2): 1
Enter your name: Basit ali
Enter your query: Check my balance
Enter 4-digit PIN: 1234
The balance for Basit ali is $5000.00

🔒 Security Notes

PIN must be 4 digits

Balance is only shown if authentication passes

Suspicious or unsafe queries are flagged

🛠 Technologies Used

Python

OpenAI Agents SDK

Gemini API

Pydantic

python-dotenv
