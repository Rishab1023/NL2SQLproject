import pandas as pd
import sqlite3

def init_db():
    # 1. Load your uploaded CSV
    df = pd.read_csv('data.csv')
    
    # 2. Data Cleaning: Fill missing Calories with 0 or a mean
    df = df.fillna(0)
    
    # 3. Connect to SQLite and create the table
    conn = sqlite3.connect('mock_data.db')
    df.to_sql('health_metrics', conn, if_exists='replace', index=False)
    
    print("Database 'mock_data.db' created successfully with table 'health_metrics'!")
    print(f"Columns: {list(df.columns)}")
    conn.close()

if __name__ == "__main__":
    init_db()
