NL2SQL is an AI-powered data assistant that allows users to chat with their database in plain English. Built for the people who are not into tech, it converts natural language questions into complex SQL queries to provide instant insights from activity data.

🚀 Features
Natural Language to SQL: Powered by Gemini 2.5 Flash to translate human questions into precise SQLite queries.

Interactive Chat UI: A clean, conversational interface built with Streamlit.

Instant Dashboarding: Automatically generates metric cards (Avg Pulse, Calories) and interactive area charts based on query results.

Schema Awareness: Deep understanding of health metrics including Duration, Pulse, Maxpulse, and Calories.

Secure & Robust: Implements Streamlit Secrets for API security and robust error handling for rate limits.

🛠️ Tech Stack
LLM: Google Gemini 2.5 Flash

Framework: Streamlit

Database: SQLite (Self-initializing from CSV)

Language: Python 3.11+

Libraries: google-genai, pandas, sqlite3

📋 Database Schema
The assistant queries a table named health_metrics with the following structure: | Column | Type | Description | | :--- | :--- | :--- | | Duration | INT | Length of the workout in minutes | | Pulse | INT | Average heart rate during the session | | Maxpulse | INT | Peak heart rate recorded | | Calories | FLOAT | Total energy expenditure in kcal |

⚙️ Installation & Local Setup
Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:

Bash

pip install -r requirements.txt
Set up your environment variables: Create a .streamlit/secrets.toml file and add your API key:

Ini, TOML

GEMINI_API_KEY = "your_api_key_here"
Run the application:

Bash

streamlit run app.py
🌟 Example Queries to Try
"What is the average pulse for sessions longer than 45 minutes?"

"Show me the top 10 workouts where I burned the most calories."

"Compare Pulse and Maxpulse for my 60-minute sessions."

"Total calories burned across all recorded activities."
