import streamlit as st
import pandas as pd
import sqlite3
from google import genai

# Configuration
API_KEY = "AIzaSyAAhxl95yKVx1ARYm1urtNTz0fdPi3YftE"
client = genai.Client(api_key=API_KEY)

st.title("🏃‍♂️ Health Data Chatbot")

def get_sql_from_ai(user_question):
    # Updated with your specific CSV schema
    prompt = f"""
    Act as a precise Natural Language to SQL translator. Table: `health_metrics` 
    Columns: `Duration`, `Pulse`, `Maxpulse`, `Calories`. 
    Convert this question to SQL: {user_question}
    Return ONLY the raw SQL string.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash', # or 'gemini-3-flash-preview'
        contents=prompt
    )
    return response.text.strip()

user_input = st.text_input("Ask about your activity (e.g., 'What is the average pulse for 60 min sessions?')")

if user_input:
    sql = get_sql_from_ai(user_input)
    
    if "ERROR" in sql:
        st.error(sql)
    else:
        st.code(sql, language="sql")
        try:
            # Connecting to the DB created from your CSV
            conn = sqlite3.connect('mock_data.db')
            df = pd.read_sql_query(sql, conn)
            conn.close()
            
            st.dataframe(df)
            
            # Automated visualization
            if not df.empty and 'Calories' in df.columns:
                st.line_chart(df['Calories'])
        except Exception as e:
            st.error(f"SQL Error: {e}")
