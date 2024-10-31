import sqlite3

#Sets up the database for login, the database contains username as primary key and a passwordhash as value
def setup_login_db():
    # This example uses sqlite3 for demonstration. In a real application, use an encrypted database connection.
    conn = sqlite3.connect('login.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, password_hash TEXT)''')

    # Insert a row of data
    # For real applications, hash the password before storing it
    # Example: password_hash = generate_password_hash('your-password')

    conn.commit()
    conn.close()



def setup_app_db():
    # Define database name
    db_name = 'app.db'

    # Establish a connection to the database.
    # This will create the database file if it does not exist.
    conn = sqlite3.connect(db_name)

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create a new table with 'orgnumber' as the PRIMARY KEY, and both 'companyname' and 'companydata' as TEXT fields
    # Additionally, enforce 'companyname' to be unique
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS company_info
    (orgnumber TEXT PRIMARY KEY,
     companyname TEXT UNIQUE,
     companydata TEXT)
    ''')

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    print(f"Database '{db_name}' and table 'company_info' updated successfully.")



if __name__ == "__main__":
    setup_app_db()




