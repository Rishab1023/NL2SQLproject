# PulseAI: Interactive Health Insights

PulseAI is a smart data assistant built with Streamlit that allows you to have a conversation with your health and activity data. Ask questions in plain English, and the app will translate your query into SQL, fetch the data, and display it in tables and charts.

This application leverages the Gemini 2.5 Flash model from Google AI to understand natural language and generate SQL queries on the fly.

## Features

-   **Natural Language Queries**: Ask questions like "What was my average pulse?" or "Show top 5 sessions by calories burned".
-   **Interactive Data Visualization**: View your data in sortable tables and dynamic charts.
-   **AI-Powered SQL Generation**: Converts your questions into SQLite queries.
-   **Chat History**: Keeps track of your conversation with the data.
-   **Data Schema Reference**: A handy reference in the sidebar shows the table and column names.

## How to Run

### 1. Prerequisites

-   Python 3.7+
-   An API key for the Google AI API.

### 2. Installation

Clone the repository and install the required Python packages.

```bash
git clone https://github.com/your-username/SQLproject.git
cd SQLproject
pip install streamlit pandas google-generativeai
```

### 3. Set Up Your API Key

Open the `app.py` file and replace the placeholder API key with your own.

```python
# In app.py
API_KEY = "YOUR_GOOGLE_AI_API_KEY" 
```

### 4. Initialize the Database

Run the setup script to create the SQLite database (`mock_data.db`) from the provided `data.csv`.

```bash
python setup_db.py
```

### 5. Launch the App

Run the Streamlit application.

```bash
streamlit run app.py
```

The application will open in your web browser.

## Data Schema

The application queries a single table named `health_metrics` in the `mock_data.db` database. The schema for this table is as follows:

| Column     | Type    | Description                               |
|------------|---------|-------------------------------------------|
| `Duration` | INTEGER | The duration of the activity in minutes.  |
| `Pulse`    | INTEGER | The average pulse rate during the activity. |
| `Maxpulse` | INTEGER | The maximum pulse rate during the activity.|
| `Calories` | REAL    | The number of calories burned.            |

Now you can start asking questions about your data!