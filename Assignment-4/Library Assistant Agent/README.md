📚 Multi-User Library Assistant (OpenAI Agents SDK + Gemini API)
📌 Overview

This project implements a multi-user, context-aware Library Assistant using OpenAI Agents SDK with Gemini API.
It can:

Search for books in a local catalog

Check availability (for registered members only)

Provide library timings

Ignore non-library-related queries

Roman Urdu:
Ye project ek multi-user, context-aware Library Assistant hai jo OpenAI Agents SDK aur Gemini API ka use karta hai. Ye books search kar sakta hai, registered members ke liye availability check karta hai, library timings deta hai, aur non-library queries ignore karta hai.

✨ Features

Multi-user context support (list of users with names & member IDs)

Dynamic greetings addressing all users together

Input Guardrail to reject non-library-related queries

Member-only tool access for book availability

Search book in local database

Check availability with copy count

Library timings information

📂 Files & Structure
main.py          # Main script with agents, guardrails, tools, and test queries
.env             # Environment variables file (contains GEMINI_API_KEY)
README.md        # Documentation
requirements.txt # Python dependencies

⚙️ Requirements

Python 3.10+

Gemini API Key from Google AI Studio

📦 Installation

1️⃣ Clone the repository

git clone https://github.com/yourusername/library-assistant.git
cd library-assistant


2️⃣ Create and activate a virtual environment

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Create .env file

GEMINI_API_KEY=your_gemini_api_key_here

▶️ How to Run
python main.py

🖥 Example Output
User: Search for Book : Enter the Agentic Ai World
Assistant: Hello Basit ali, Sir Asharib Ali, Sir Naeem Hussain. 'Enter the Agentic Ai World' is available in our catalog.

User: Check availability for Book: The 80's Technologies
Assistant: Hello Basit ali, Sir Asharib Ali, Sir Naeem Hussain. 'The 80's Technologies' is currently out of stock.

User: Check Library timings
Assistant: Hello Basit ali, Sir Asharib Ali, Sir Naeem Hussain. The library is open from 9 AM to 8 PM, Monday to Saturday.

User: What's the weather like?
Assistant: Sorry to all users, I can only help with library-related questions.

🔒 Guardrails

Input Guardrail: Blocks non-library queries (e.g., weather, sports)

Member Validation: Only registered members can check availability

Dynamic Instructions: Greetings include all user names in the session

🛠 Technologies Used

Python

OpenAI Agents SDK

Gemini API

Pydantic

python-dotenv
