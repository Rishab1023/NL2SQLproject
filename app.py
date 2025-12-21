import streamlit as st
import pandas as pd
import sqlite3
import os
from functools import wraps
from google import genai
from google.genai import errors

# --- 1. CONFIGURATION ---
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL_ID = "gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="NL2SQL",
                   page_icon="⚡", layout="wide")

# --- 2. ENV: Ensure local DB (for Streamlit deployment) ---



def validate_db():
    db_path = 'mock_data.db'
    # If file doesn't exist OR is size 0 (corrupted), recreate it
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        st.info("Re-initializing database from CSV...")
        df = pd.read_csv('data.csv')
        df = df.fillna(0)
        conn = sqlite3.connect(db_path)
        df.to_sql('health_metrics', conn, index=False, if_exists='replace')
        conn.close()
        st.success("Database ready!")
        return True
    return False


# Validate DB and set flag for UI
db_created = validate_db()

# --- 2. THE AI ENGINE ---


def get_sql_from_ai(user_question):
    # Unified prompt for Gemini 2.5 Flash
    prompt = f"""
    Act as a precise Natural Language to SQL translator.
    Database Schema: Table 'health_metrics' with columns (Duration, Pulse, Maxpulse, Calories).
    
    Task: Convert the user's question into a valid SQLite query.
    Rules:
    - Return ONLY the raw SQL string (no markdown, no ```sql).
    - Use only the provided column names.
    - If the request is not a data query, return 'ERROR: Invalid Request'.
    
    User Question: {user_question}
    """
    try:
        response = client.models.generate_content(
            model=MODEL_ID, contents=prompt)
        return response.text.strip()
    except errors.ClientError as e:
        if "429" in str(e):
            return "ERROR: Rate limit hit. Please wait a few seconds."
        return f"ERROR: {str(e)}"


# --- 3. UI LAYOUT & STYLE ---
st.title("⚡ NL2SQL")
st.markdown("---")

# Sidebar for schema and quick actions
with st.sidebar:
    st.header("📊 Data Reference")
    st.write("**Table:** `health_metrics`")
    st.write("**Columns:** `Duration`, `Pulse`, `Maxpulse`, `Calories`")

    # Small status indicator for DB initialization
    if db_created:
        st.success("✅ `mock_data.db` created from `data.csv`")
    else:
        st.caption("Using existing `mock_data.db`")

    st.divider()
    st.subheader("💡 Suggested Queries")
    if st.button("Top 5 highest calorie sessions"):
        st.session_state.chat_input_val = "Show top 5 sessions by calories"
    if st.button("Average pulse for 60m sessions"):
        st.session_state.chat_input_val = "What is the average pulse for 60 min duration?"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "df" in msg:
            st.dataframe(msg["df"], use_container_width=True)

# --- 4. CHAT INPUT LOGIC ---
if "chat_input_val" in st.session_state:
    user_query = st.chat_input(
        "Ask about your activity data...", key="main_chat", on_submit=None)
    # This logic handles the sidebar button clicks
    user_query = st.session_state.pop("chat_input_val")
else:
    user_query = st.chat_input("Ask about your activity data...")

if user_query:
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Process with AI
    with st.chat_message("assistant"):
        with st.spinner("Gemini is analyzing your data..."):
            sql = get_sql_from_ai(user_query)

        if "ERROR" in sql:
            st.warning(sql)
        else:
            try:
                # Query Database
                conn = sqlite3.connect('mock_data.db')
                df = pd.read_sql_query(sql, conn)
                conn.close()

                if df.empty:
                    st.info("Query successful, but no results found.")
                else:
                    # 5. DASHBOARD ELEMENTS
                    st.toast("Data Retrieved!", icon="✅")

                    # Show quick metrics if numeric data is available
                    m_col1, m_col2, m_col3 = st.columns(3)
                    if 'Calories' in df.columns:
                        m_col1.metric("Max Calories",
                                      f"{df['Calories'].max():.1f}")
                    if 'Pulse' in df.columns:
                        m_col2.metric(
                            "Avg Pulse", f"{df['Pulse'].mean():.0f} BPM")
                    m_col3.metric("Records Found", len(df))

                    # Use Tabs for a clean look
                    t_data, t_chart, t_sql = st.tabs(
                        ["📄 Data Table", "📈 Visualization", "💻 SQL Code"])

                    with t_data:
                        st.dataframe(df, use_container_width=True)

                    with t_chart:
                        if len(df) > 1:
                            st.area_chart(df)
                        else:
                            st.write("Not enough data points for a chart.")

                    with t_sql:
                        st.code(sql, language="sql")

                    # Save to History
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I found the following for: *{user_query}*",
                        "df": df
                    })
            except Exception as e:
                st.error(f"Execution Error: {e}")
