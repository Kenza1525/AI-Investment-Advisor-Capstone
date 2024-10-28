import sqlite3

DATABASE = 'user_profiles.db'

# Function to initialize the database and create tables if they don't exist
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            education TEXT,
            investment_length TEXT,
            investment_goal TEXT,
            risk_tolerance TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new user profile into the database
def insert_profile(name, age, education, investment_length, investment_goal, risk_tolerance):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO profiles (name, age, education, investment_length, investment_goal, risk_tolerance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, education, investment_length, investment_goal, risk_tolerance))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:  # Handles duplicate profile insertion
        success = False
    conn.close()
    return success

# Function to query profiles (optional, for later use)
def query_profiles():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM profiles')
    rows = c.fetchall()
    conn.close()
    return rows
