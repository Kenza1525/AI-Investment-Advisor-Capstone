import sqlite3

def print_db_contents():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    print("Contents of 'auth' table:")
    for row in cursor.execute('SELECT * FROM auth'):
        print(row)
    
    print("Contents of 'user_info' table:")
    for row in cursor.execute('SELECT * FROM user_info'):
        print(row)
    
    conn.close()

print_db_contents()
