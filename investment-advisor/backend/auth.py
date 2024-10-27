import sqlite3
from sqlite3 import Error
import os
import hashlib

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

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to sign up a new user
def signup_user(username, password, first_name, surname):
    conn = create_connection()
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, first_name, surname) VALUES (?, ?, ?, ?)", 
                       (username, hashed_password, first_name, surname))
        conn.commit()
        cursor.close()
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists. Please choose another.")
    except Error as e:
        raise Exception(f"Error signing up user: {e}")
    finally:
        if conn:
            conn.close()

# Function to authenticate an existing user
def authenticate_user(username, password):
    conn = create_connection()
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
    except Error as e:
        raise Exception(f"Error authenticating user: {e}")
    finally:
        if conn:
            conn.close()
