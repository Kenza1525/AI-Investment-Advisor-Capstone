import sqlite3
import json


class UserProfileDatabase:
    DATABASE = 'user_info.db'

    def __init__(self):
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the database and create the profiles table if it doesn't exist."""
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    age INTEGER,
                    job TEXT,
                    phone TEXT,
                    email TEXT,
                    investment_amount INTEGER,
                    time_horizon INTEGER,
                    current_portfolio TEXT,
                    risk_tolerance TEXT
                )
            ''')
            conn.commit()

    def create_profile(self, profile_data):
        """
        Insert a new user profile into the database.
        :param profile_data: Dictionary containing the profile fields and values.
        """
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            try:
                # Extract values from the dictionary
                c.execute('''
                    INSERT INTO profiles (
                        name, age, job, phone, email, investment_amount, time_horizon, current_portfolio, risk_tolerance
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile_data.get("name"),
                    profile_data.get("age"),
                    profile_data.get("job"),
                    profile_data.get("phone"),
                    profile_data.get("email"),
                    profile_data.get("investment_amount"),
                    profile_data.get("time_horizon"),
                    json.dumps(profile_data.get("current_portfolio")),
                    profile_data.get("risk_tolerance")
                ))
                conn.commit()
                return c.lastrowid  # Return the ID of the newly created profile
            except sqlite3.IntegrityError:
                return None  # Indicates a failure to create due to a duplicate name

    def read_profiles(self):
        """Retrieve all user profiles."""
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM profiles')
            profiles = c.fetchall()
            return [self._deserialize_profile(profile) for profile in profiles]

    def read_profile_by_name(self, name):
        """Retrieve a user profile by name."""
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM profiles WHERE name = ?', (name,))
            profile = c.fetchone()
            return self._deserialize_profile(profile) if profile else None

    def update_profile(self, name, **updates):
        """
        Update an existing user profile.
        :param name: The unique name of the profile to update.
        :param updates: The fields to update as keyword arguments.
        """
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            if "current_portfolio" in updates:
                updates["current_portfolio"] = json.dumps(updates["current_portfolio"])
            fields = ', '.join(f"{key} = ?" for key in updates.keys())
            values = list(updates.values()) + [name]
            c.execute(f'''
                UPDATE profiles
                SET {fields}
                WHERE name = ?
            ''', values)
            conn.commit()
            return c.rowcount  # Returns the number of rows updated

    def delete_profile(self, name):
        """Delete a user profile by name."""
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM profiles WHERE name = ?', (name,))
            conn.commit()
            return c.rowcount  # Returns the number of rows deleted

    def _deserialize_profile(self, profile):
        """Convert serialized fields back to their original types."""
        if profile:
            profile = list(profile)
            profile[8] = json.loads(profile[8]) if profile[8] else None  # Deserialize current_portfolio
        return tuple(profile) if profile else None


# Standalone functions
def init_db():
    """Initialize the database."""
    db = UserProfileDatabase()
    return db


def insert_profile(profile_data):
    """Insert a new user profile."""
    db = UserProfileDatabase()
    return db.create_profile(profile_data)


# Testing the class
if __name__ == "__main__":
    db = UserProfileDatabase()

    # Create a profile
    print("Creating profile...")
    profile_data = {
        "name": "John Doe",
        "age": 30,
        "job": "Engineer",
        "phone": "123-456-7890",
        "email": "johndoe@example.com",
        "investment_amount": 5000,
        "time_horizon": 10,
        "current_portfolio": {"stocks": 70, "bonds": 30},
        "risk_tolerance": "Moderate"
    }
    db.create_profile(profile_data)

    # Output after insertion
    print("\nAll profiles:")
    profiles = db.read_profiles()
    print(profiles)

    # Read single profile
    print("\nReading profile by name:")
    profile = db.read_profile_by_name("John Doe")
    print(profile)

    # Update profile
    print("\nUpdating profile...")
    db.update_profile("John Doe", age=31, investment_amount=5500, current_portfolio={"stocks": 75, "bonds": 25})

    # Verify update
    print("\nProfile after update:")
    profile = db.read_profile_by_name("John Doe")
    print(profile)

    # Delete profile
    print("\nDeleting profile...")
    db.delete_profile("John Doe")

    # Verify deletion
    print("\nAll profiles after deletion:")
    profiles = db.read_profiles()
    print(profiles)
