# NL2SQL — Natural Language to SQL (Streamlit)

NL2SQL is an AI-powered data assistant that lets anyone query a dataset in plain English. It translates natural language questions into SQLite queries (using Google Gemini) and displays results in a clean Streamlit chat UI with instant metrics and charts.

---

## 🚀 Key Features

- **Natural Language → SQL**: Gemini 2.5 (via google-genai) converts user questions into precise SQLite queries.
- **Interactive Chat UI**: Conversational interface built with Streamlit.
- **Instant Dashboarding**: Metric cards, data table, and area charts generated from query results.
- **Simple Local DB**: Uses `mock_data.db` (auto-created from `data.csv` on first run).
- **Secure**: API key stored in Streamlit secrets (`.streamlit/secrets.toml`) and basic error handling for rate limits.

---

## 🧭 Quick Demo / How it works
1. On startup, the app checks for `mock_data.db`. If missing, it reads `data.csv` and creates a `health_metrics` table.
2. You ask questions in natural language (e.g., "Top 5 highest calorie sessions").
3. The app sends the question to Gemini, receives a SQL query, executes it against `mock_data.db`, and shows results.

> A small status appears in the sidebar telling you whether the DB was created during startup.

---

## 📦 Tech Stack

- Python 3.11+
- Streamlit
- google-genai (Gemini)
- pandas
- SQLite (sqlite3)

---

## 📋 Database Schema

Table: `health_metrics`

| Column   | Type  | Description                                 |
|----------|-------|---------------------------------------------|
| Duration | INT   | Length of the workout in minutes            |
| Pulse    | INT   | Average heart rate during the session       |
| Maxpulse | INT   | Peak heart rate recorded                    |
| Calories | FLOAT | Total energy expenditure in kcal            |

---

## ⚙️ Installation & Local Setup (Windows)

Recommended: use a virtual environment.

1. Clone the repo:

```bash
git clone https://github.com/Rishab1023/NL2SQLproject.git
cd NL2SQLproject
```

2. Create & activate a venv (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your Gemini API key:

Create `.streamlit/secrets.toml` (or set `STREAMLIT_SECRETS` in your deployment platform) with:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

5. Run the app:

```bash
streamlit run app.py
```

On first run the app will create `mock_data.db` from `data.csv`. A small message in the sidebar will indicate whether the DB was created.

---

## 🧪 Example Queries
- "What is the average pulse for sessions longer than 45 minutes?"
- "Show top 10 workouts by calories burned"
- "Compare Pulse and Maxpulse for 60-minute sessions"
- "Total calories burned across all activities"

---

## ⚠️ Notes & Troubleshooting

- If queries return no results, the query may be syntactically correct but not match your data; try a simpler question first.
- To force re-create the DB for testing, stop the app and delete `mock_data.db` — the app will rebuild it at next start from `data.csv`.
- If you hit API rate limits, wait a few seconds and try again; the app surfaces rate-limit errors as warnings.

---

## Contributing

Contributions are welcome — please open an issue or submit a pull request.

Suggestions:
- Add more sample queries and test cases.
- Add unit tests for SQL generation and query execution.

---

## License

This project is provided under the MIT License. See `LICENSE` (if present) for details.

---


