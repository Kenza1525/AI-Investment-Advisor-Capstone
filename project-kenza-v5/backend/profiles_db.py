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
                    fullName TEXT UNIQUE,
                    age INTEGER,
                    job TEXT,
                    phoneNumber TEXT,
                    email TEXT,
                    amount INTEGER,
                    time_horizon INTEGER,
                    current_portfolio TEXT,
                    profile TEXT
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
                        fullName, age, job, phoneNumber, email, amount, time_horizon, current_portfolio, profile
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile_data.get("fullName"),
                    profile_data.get("age"),
                    profile_data.get("job"),
                    profile_data.get("phoneNumber"),
                    profile_data.get("email"),
                    profile_data.get("amount"),
                    profile_data.get("time_horizon"),
                    profile_data.get("profile"),
                    json.dumps(profile_data.get("current_portfolio"))
                    
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
            c.execute('SELECT * FROM profiles WHERE fullName = ?', (name,))
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
                WHERE fullName = ?
            ''', values)
            conn.commit()
            return c.rowcount  # Returns the number of rows updated
        
    def update_portfolio(self, username, **allocation_data):
        """
        Update the profile information for a specific user in the database.

        :param username: The unique username of the user whose profile is being updated.
        :param allocation_data: The data to update as keyword arguments.
        """
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()

            # Ensure "profile" exists in allocation_data
            if "profile" in allocation_data:
                # Serialize the profile if necessary
                if isinstance(allocation_data["profile"], dict):
                    allocation_data["profile"] = json.dumps(allocation_data["profile"])
            else:
                raise ValueError("Profile information is required to update.")

            # Prepare the SQL fields and values
            fields = "profile = ?"
            values = [allocation_data["profile"], username]

            # Update the database record
            c.execute(f'''
                UPDATE profiles
                SET {fields}
                WHERE fullName = ?
            ''', values)

            # Commit the changes
            conn.commit()

            # Return the number of rows updated
            return c.rowcount
        

    def delete_profile(self, name):
        """Delete a user profile by name."""
        with sqlite3.connect(self.DATABASE) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM profiles WHERE fullName = ?', (name,))
            conn.commit()
            return c.rowcount  # Returns the number of rows deleted

    def _deserialize_profile(self, profile):
        """Convert serialized fields back to their original types."""
        if profile:
            profile = list(profile)
            profile[8] = json.loads(profile[8]) if profile[8] else None  # Deserialize current_portfolio
        return tuple(profile) if profile else None


# Testing the class
# if __name__ == "__main__":
#     db = UserProfileDatabase()

#     # Create a profile
#     print("Creating profile...")
#     profile_data = {
#         "name": "John Doe",
#         "age": 30,
#         "job": "Engineer",
#         "phone": "123-456-7890",
#         "email": "johndoe@example.com",
#         "investment_amount": 5000,
#         "time_horizon": 10,
#         "current_portfolio": {"stocks": 70, "bonds": 30},
#         "risk_tolerance": "Moderate"
#     }
#     db.create_profile(profile_data)

#     # Output after insertion
#     print("\nAll profiles:")
#     profiles = db.read_profiles()
#     print(profiles)

#     # Read single profile
#     print("\nReading profile by name:")
#     profile = db.read_profile_by_name("John Doe")
#     print(profile)

#     # Update profile
#     print("\nUpdating profile...")
#     db.update_profile("John Doe", age=31, investment_amount=5500, current_portfolio={"stocks": 75, "bonds": 25})

#     # Verify update
#     print("\nProfile after update:")
#     profile = db.read_profile_by_name("John Doe")
#     print(profile)

#     # Delete profile
#     print("\nDeleting profile...")
#     db.delete_profile("John Doe")

#     # Verify deletion
#     print("\nAll profiles after deletion:")
#     profiles = db.read_profiles()
#     print(profiles)
