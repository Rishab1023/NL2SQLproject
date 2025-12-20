import pandas as pd
import sqlite3

def init_db():
    # Load your specific CSV
    df = pd.read_csv('data.csv')
    
    # Clean data (fill missing Calories)
    df = df.fillna(0)
    
    # Create the SQLite database
    conn = sqlite3.connect('mock_data.db')
    df.to_sql('health_metrics', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Successfully created 'mock_data.db' with your health data!")

if __name__ == "__main__":
    init_db()
