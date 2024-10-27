import sqlite3
from sqlite3 import Error
import os

# Database location
DB_FILE = os.path.join(os.path.dirname(__file__), "investment_advisor.db")

# Create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Create tables for users, user profiles, allocations, risk profiles, and investment strategies
def create_tables():
    conn = create_connection()
    try:
        cursor = conn.cursor()

        # Create users table for authentication details
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)

        # Create user_profiles table to store personal user data like name, surname, etc.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                surname TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        # Create allocations table to store asset allocation details for each user
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS allocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                risk_profile TEXT NOT NULL,
                investment_amount REAL NOT NULL,
                source_of_funds TEXT,
                local_equity REAL,
                local_bond REAL,
                local_cash REAL,
                global_assets REAL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        # Create risk_profiles table to store user scores and risk profile classification
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER,
                profile TEXT,  -- Conservative, Cautious, Moderate, Aggressive
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        # Create investment_strategies table to store each user's multiple strategies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investment_strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                profile_name TEXT NOT NULL,
                local_equity REAL,
                local_bond REAL,
                local_cash REAL,
                global_assets REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        conn.commit()
        cursor.close()
        print("Database and all tables created successfully.")

    except Error as e:
        print(f"Error creating tables: {e}")

    finally:
        if conn:
            conn.close()

# Initialize the database tables
if __name__ == "__main__":
    create_tables()
