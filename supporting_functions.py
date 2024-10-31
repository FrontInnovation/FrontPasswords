from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
from cryptography.fernet import Fernet
from difflib import get_close_matches



# Generate a key for encryption and decryption
# You should store this key securely - if you lose it, you will not be able to decrypt your data
key = b'yhp8Fq5A3kx7y_uUNYJ6o5C8ezaL4fU2yJQGyhCKvhI='
cipher_suite = Fernet(key)


def encrypt_data(data):
    """Encrypt the data."""
    if isinstance(data, str):
        data = data.encode()  # Convert to bytes
    encrypted_data = cipher_suite.encrypt(data)
    return encrypted_data.decode('utf-8')


def decrypt_data(encrypted_data):
    """Decrypt the data."""
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()  # Convert back to string


def convert_reqest_to_datalist(request): #takes in a flask request and returns companyname and datalist
    companyname = request.form['companyname']
    data = []

    datastring = f""
    counter = -1
    for key in request.form:
        if counter > -1:
            if counter % 3 == 0:
                datastring = ""
                datastring += f"{request.form[key]};"
            elif counter % 3 == 1:
                datastring += f"{request.form[key]};"
            elif counter % 3 == 2:
                datastring += f"{request.form[key]}"
                data.append(datastring)
                datastring = ""
            else:
                pass
                
        counter += 1
    
    return companyname, data


def format_company_identifier(companyid): #companyid is either companyname or orgnumber
    cid = companyid.replace(" ", "")
    cid = cid.lower()
    return cid
    


#Validation function for login, takes in username and password and checks if it matches with the database
def validate_credentials(username, password):
    conn = sqlite3.connect('databases/login.db')
    c = conn.cursor()
    
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[0], password):
        session['username'] = username  # Log in the user by setting the session
        session.permanent = True  # Make the session permanent so it respects the session lifetime set in the config
        return True
    else:
        return False
    

#Selfexplanatory function name and input, no output
def add_or_update_user_to_login_db(username, plain_password):
    # Hash the plain password
    if len(username) > 50 or len(plain_password) > 50:
        print("Details to insert into the database are too long string!")
        return
    
    hashed_password = generate_password_hash(plain_password)
    
    try:
        # Connect to the database
        conn = sqlite3.connect('databases/login.db')
        c = conn.cursor()
        
        # Using the ON CONFLICT clause to update the password_hash for an existing username
        c.execute("""
        INSERT INTO users (username, password_hash) 
        VALUES (?, ?) 
        ON CONFLICT(username) 
        DO UPDATE SET password_hash=excluded.password_hash;
        """, (username, hashed_password))
        
        # Commit the changes and close the connection
        conn.commit()
        print("User added or updated successfully.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()


def remove_user_from_login_db(username):
    try:
        # Connect to the database
        conn = sqlite3.connect('databases/login.db')
        c = conn.cursor()
        
        # Execute SQL to delete the user by username
        c.execute("DELETE FROM users WHERE username=?", (username,))
        
        # Check if any rows were affected
        if c.rowcount > 0:
            print("User removed successfully.")
        else:
            print("User with username '{}' not found.".format(username))
        
        # Commit the changes and close the connection
        conn.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()


# Gets companyname based on similar input companyname from app.db
def get_company_name_by_similar_name(companyname):
    """
    Retrieves company name based on similar input company name from the app.db database.

    :param companyname: The name of the company to retrieve data for.
    :return: A string containing the company name found in the database, or None if the company is not found.
    """
    try:
        companyname = format_company_identifier(companyname)
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        c = conn.cursor()
        # Execute a SELECT query to find the accounts data for the specified company
        c.execute("SELECT companyname FROM company_info")
        rows = c.fetchall()
        
        # Extract company names from fetched rows
        company_names = [row[0] for row in rows]

        # Check if the exact company name is present in the database
        if companyname in company_names:
            return companyname
        else:
            # Find the most similar company name
            similar_names = get_close_matches(companyname, company_names, n=1, cutoff=0.75)
            if similar_names:
                return similar_names[0]  # Return the first (most similar) name from the list
            else:
                print("Company not found.")
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_new_company_data(orgnumber, companyname, companydata):
    # Serialize company_data if it's not a string (e.g., if it's a Python dict)
    orgnumber = format_company_identifier(orgnumber)
    companyname = format_company_identifier(companyname)
    namecheck = get_company_name_by_similar_name(companyname)
    print("NAMECHECK: ", namecheck)
    if namecheck != None:
        companyname = get_company_name_by_similar_name(companyname)

    if not isinstance(companydata, str):
        companydata = json.dumps(companydata)

    if len(orgnumber) != 9 or len(companyname) > 50 or len(companydata) > 250:
        print("Details to insert into the database are too long!")
        return

    encrypted_companydata = encrypt_data(companydata)
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        cursor = conn.cursor()
        
        # Insert the new company data
        cursor.execute("INSERT INTO company_info (orgnumber, companyname, companydata) VALUES (?, ?, ?)", 
                       (orgnumber, companyname, encrypted_companydata))
        
        # Commit the changes and close the connection
        conn.commit()
        print(f"Data added successfully for company: {companyname}")
    except sqlite3.IntegrityError as e:
        print(f"An error occurred: {e}. Company with this orgnumber already exists.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()



def update_company_data(companyname, companydata):
    # Serialize company_data if it's not a string (e.g., if it's a Python dict)

    companyname = format_company_identifier(companyname)
    companyname = get_company_name_by_similar_name(companyname)

    if not isinstance(companydata, str):
        companydata = json.dumps(companydata)

    if len(companyname) > 50 or len(companydata) > 250:
        print("Details to insert into the database are too long!")
        return

    encrypted_companydata = encrypt_data(companydata)
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        cursor = conn.cursor()
        
        # Update the company data for a given company name
        cursor.execute("UPDATE company_info SET companydata = ? WHERE companyname = ?", 
                       (encrypted_companydata, companyname))
        
        # Commit the changes and close the connection
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No data updated; company '{companyname}' not found.")
        else:
            print(f"Data updated successfully for company: {companyname}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


def delete_company_by_orgnumber(orgnumber):
    """
    Deletes a company entry from the app.db database based on its organizational number.

    :param orgnumber: The organizational number of the company to be deleted.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        cursor = conn.cursor()
        
        # Execute a DELETE query to remove the company based on the orgnumber
        cursor.execute("DELETE FROM company_info WHERE orgnumber = ?", (orgnumber,))
        
        # Commit the changes
        conn.commit()

        # Check if the deletion was successful
        if cursor.rowcount > 0:
            print(f"Company with orgnumber {orgnumber} deleted successfully.")
        else:
            print("No company found with that orgnumber.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


#Gets companydata based on companyname from app.db
def get_company_data(companyname):
    """
    Retrieves accounts data for a specified company name from the company_accounts.db database.
    
    :param companyname: The name of the company to retrieve data for.
    :return: A dictionary containing the accounts data for the company, or None if the company is not found.
    """
    try:
        companyname = format_company_identifier(companyname)
        companyname = get_company_name_by_similar_name(companyname)
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        c = conn.cursor()
        # Execute a SELECT query to find the accounts data for the specified company
        c.execute("SELECT companydata FROM company_info WHERE companyname = ?", (companyname,))
        data = c.fetchone()
        print(data)
        
        # Check if any data was found
        if data:
            decrypted_accountdata = json.loads(decrypt_data(data[0]))
            return decrypted_accountdata
        else:
            print("Company not found.")
            return "" #If cant find the companyname in the db
    except Exception as e:
        print(f"An error occurred 1111: {e}")
        return "" #If cant find the companyname in the db
    finally:
        if conn:
            conn.close()


# # Gets companydata based on companyname from app.db
# def get_company_data(companyname):
#     """
#     Retrieves accounts data for a specified company name from the company_accounts.db database.

#     :param companyname: The name of the company to retrieve data for.
#     :return: A dictionary containing the accounts data for the company, or None if the company is not found.
#     """
#     try:
#         companyname = format_company_identifier(companyname)
#         # Connect to the SQLite database
#         conn = sqlite3.connect('databases/app.db')
#         c = conn.cursor()
#         # Execute a SELECT query to find the accounts data for the specified company
#         c.execute("SELECT companyname, companydata FROM company_info")
#         rows = c.fetchall()
        
#         # Extract company names from fetched rows
#         company_names = [row[0] for row in rows]

#         # Check if the exact company name is present in the database
#         if companyname in company_names:
#             for row in rows:
#                 if row[0] == companyname:
#                     decrypted_accountdata = json.loads(decrypt_data(row[1]))
#                     return decrypted_accountdata
#         else:
#             # Find the most similar company name
#             similar_names = get_close_matches(companyname, company_names, n=1, cutoff=0.8)
#             if similar_names:
#                 for row in rows:
#                     if row[0] == similar_names[0]:
#                         decrypted_accountdata = json.loads(decrypt_data(row[1]))
#                         return decrypted_accountdata
#             else:
#                 print("Company not found.")
#                 return None

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#     finally:
#         if conn:
#             conn.close()


def get_company_data_by_orgnumber(orgnumber):
    """
    Retrieves company name and data for a specified orgnumber from the app.db database.

    :param orgnumber: The organizational number of the company to retrieve data for.
    :return: A dictionary containing the company name and data for the company, or None if the company is not found.
    """
    try:
        orgnumber = format_company_identifier(orgnumber)
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        cursor = conn.cursor()
        
        # Execute a SELECT query to find the company name and data for the specified orgnumber
        cursor.execute("SELECT companyname, companydata FROM company_info WHERE orgnumber = ?", (orgnumber,))
        data = cursor.fetchone()
        
        # Check if any data was found
        if data:
            companyname, encrypted_companydata = data
            decrypted_companydata = json.loads(decrypt_data(encrypted_companydata))
            return companyname, decrypted_companydata
        else:
            print("Company not found.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()



#writes the inputstring into the log
def write_to_log(string):
    with open('databases/log.txt', 'a') as log:
        log.write(string) 


if __name__ == "__main__":
    ############################## Adds or updates a user with hashed password to the login.db database
    # add_or_update_user_to_login_db("FilipSH", "Front")
    # add_or_update_user_to_login_db("Front", "Filiperkul")
    # add_or_update_user_to_login_db("Erlend", "Front123")
    # add_or_update_user_to_login_db("Filip", "Front")

    ########################## Remove user from login.db by username (primarykey)
    #remove_user_from_login_db('Front')

    ####################### Adds company and their information to the app.db database, the Orgnumber is the primary key, the companyname is unique and the information is encrypted
    #add_new_company_data('913777948', 'Front Innovation', ['Forskningsrådet;FrontInnovation Brukernavn;Front1234'])
    #add_new_company_data('930099996', 'Scalemem', ['Forskningsrådet;Scalemem24;Passord1234', 'NOX;ZZZ24;Passord1234', 'Test;TTTTTTTTTT;Testing12345678'])
    #add_new_company_data('813672782', 'Uniscale', ['Forskningsrådet;Uniscale2024;Passord1234'])

    ####################### Get companydata by companyname or by orgnumber, two examples of the two different functions
    #print("BY COMPANYNAME:", get_company_data('Scalemem'))
    #print("BY ORGNUMBER:", get_company_data_by_orgnumber('12345678'))

    ###################### Deleting row (company) by orgnumber
    #delete_company_by_orgnumber('913777948')

    pass