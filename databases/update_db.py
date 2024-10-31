import sqlite3
import json
from cryptography.fernet import Fernet


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


def format_company_identifier(companyid): #companyid is either companyname or orgnumber
    cid = companyid.replace(" ", "")
    cid = cid.lower()
    return cid


def add_new_company_data(orgnumber, companyname, companydata):
    # Serialize company_data if it's not a string (e.g., if it's a Python dict)
    if not isinstance(companydata, str):
        companydata = json.dumps(companydata)

    if len(orgnumber) > 50 or len(companyname) > 50 or len(companydata) > 250:
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




if __name__ == "__main__":
    with open('databases/Innlogging_data.csv', 'r') as filref:
        teller = 0
        for linje in filref:
            if teller == 0:
                teller = 1
                continue

            try:
                komponenter = linje.split(",")
                navn = format_company_identifier(komponenter[0])
                orgnr = format_company_identifier(komponenter[1])
                brukernavn = komponenter[2]
                passord = komponenter[3]

                if len(orgnr) == 9 and int(orgnr) != 0:
                    data = [f"Forskningsrådet;{brukernavn};{passord}"]
                    add_new_company_data(orgnr, navn, data)
                    print(f"{teller}. Successfully added: {navn}")
                    teller += 1
            except:
                print(f"COULD NOT ADD COMPANY TO DATABASE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
