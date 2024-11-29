import sqlite3
from werkzeug.security import check_password_hash

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create auth table
    c.execute('''
        CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create user info table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            user_id INTEGER,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            career_status TEXT,
            FOREIGN KEY(user_id) REFERENCES auth(id)
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, password, fname, lname, email, career_status):
    create_db()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        # Insert into the auth table
        c.execute("INSERT INTO auth (username, password) VALUES (?, ?)", (username, password))
        user_id = c.lastrowid  # Fetch the last inserted id to use in user_info
        
        # Insert into the user_info table
        c.execute("INSERT INTO user_info (user_id, first_name, last_name, email, career_status) VALUES (?, ?, ?, ?, ?)",
                  (user_id, fname, lname, email, career_status))
        conn.commit()
    except sqlite3.IntegrityError:  # This will occur if the username is not unique
        return False
    finally:
        conn.close()
    return True

def get_user(username):
    """Retrieve user details by username"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM auth WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    """Verify user credentials"""
    user = get_user(username)
    if user is not None:
        user_id, stored_password = user
        if check_password_hash(stored_password, password):
            return True, user_id
    return False, None